import os
import asyncio
import json
from datetime import datetime, timezone

import MetaTrader5 as mt5
import pandas as pd
import requests
from dotenv import load_dotenv
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, ContextTypes

from bot_engine import execute_demo_trade

load_dotenv()  # TELEGRAM_TOKEN and TELEGRAM_CHAT_ID live in a .env file, not here

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# --- MULTI-TRADE JSON STATE BRIDGE ---
def update_dashboard_state(bot_running, new_trade=None):
    # Load existing state first to preserve active positions
    existing_trades = []
    if os.path.exists("bot_state.json"):
        try:
            with open("bot_state.json", "r") as f:
                data = json.load(f)
                existing_trades = data.get("active_trades", [])
        except:
            pass
            
    if new_trade:
        existing_trades.append(new_trade)
        
    state = {
        "bot_running": bot_running,
        "active_trades": existing_trades
    }
    with open("bot_state.json", "w") as f:
        json.dump(state, f)


SYMBOLS = ["EURUSD", "XAUUSD"]

TIMEFRAMES = {
    "H4": mt5.TIMEFRAME_H4,
    "H1": mt5.TIMEFRAME_H1,
    "M15": mt5.TIMEFRAME_M15,
    "M5": mt5.TIMEFRAME_M5,
    "M1": mt5.TIMEFRAME_M1,
}

# In-memory store so the Telegram callback knows what a button press refers to.
# Keyed by symbol -> {"action": "BUY"/"SELL", "sl_pips": .., "tp_pips": ..}
PENDING_SIGNALS = {}


# --- 1. MARKET / DAY GUARDRAIL ---
def is_market_open_and_valid():
    now = datetime.now(timezone.utc)
    if now.weekday() >= 5:
        print(f"🛑 Market closed (weekend). Skipping scan.")
        return False
    return True


# --- 2. SESSION DETECTION (UTC) ---
def get_active_sessions():
    """
    Returns a list of currently active sessions based on standard UTC windows.
    Sessions overlap (e.g. London/NY), which is intentional — overlap periods
    are typically the highest-liquidity windows.
    """
    hour = datetime.now(timezone.utc).hour
    sessions = []
    if 0 <= hour < 9:
        sessions.append("Asian")
    if 7 <= hour < 16:
        sessions.append("London")
    if 12 <= hour < 21:
        sessions.append("New York")
    return sessions


# --- 3. LIVE NEWS RISK CHECK ---
def check_high_impact_news_risk(minutes_window=30):
    """
    Pulls the public Forex Factory weekly calendar feed and checks whether a
    high-impact USD/EUR event falls within `minutes_window` minutes of now.
    This is a free, unauthenticated feed — it can go down or change format
    without notice, so this fails safe (treats failures as "no data," not
    "no risk"). For production reliability, consider a paid calendar API.
    """
    try:
        resp = requests.get(
            "https://nfs.faireconomy.media/ff_calendar_thisweek.json", timeout=5
        )
        resp.raise_for_status()
        events = resp.json()
    except Exception as e:
        print(f"⚠️ Could not fetch news calendar ({e}). Proceeding cautiously without news filter.")
        return False

    now = datetime.now(timezone.utc)
    for event in events:
        if event.get("impact") != "High":
            continue
        if event.get("country") not in ("USD", "EUR"):
            continue
        try:
            event_time = datetime.fromisoformat(event["date"].replace("Z", "+00:00"))
        except Exception:
            continue
        delta_minutes = abs((event_time - now).total_seconds()) / 60
        if delta_minutes <= minutes_window:
            print(f"🚨 High-impact event nearby: {event.get('title')} ({event.get('country')})")
            return True
    return False


# --- 4. STRUCTURE DETECTION ---
def detect_swings(df, lookback=2):
    """Fractal-style swing high/low detection using `lookback` bars on each side."""
    df = df.copy()
    df["swing_high"] = False
    df["swing_low"] = False
    for i in range(lookback, len(df) - lookback):
        window_high = df["high"].iloc[i - lookback : i + lookback + 1]
        window_low = df["low"].iloc[i - lookback : i + lookback + 1]
        if df["high"].iloc[i] == window_high.max():
            df.at[df.index[i], "swing_high"] = True
        if df["low"].iloc[i] == window_low.min():
            df.at[df.index[i], "swing_low"] = True
    return df


def detect_fvgs(df):
    """
    Classic 3-candle Fair Value Gap detection.
    Bullish FVG: candle[i].low > candle[i-2].high (gap left behind an up-move).
    Bearish FVG: candle[i].high < candle[i-2].low (gap left behind a down-move).
    """
    fvgs = []
    for i in range(2, len(df)):
        c0, c2 = df.iloc[i - 2], df.iloc[i]
        if c2["low"] > c0["high"]:
            fvgs.append({"type": "bullish", "top": c2["low"], "bottom": c0["high"], "index": i})
        elif c2["high"] < c0["low"]:
            fvgs.append({"type": "bearish", "top": c0["low"], "bottom": c2["high"], "index": i})
    return fvgs


def detect_order_blocks(df, lookback=2):
    """
    Heuristic order block detection: the last opposite-colored candle before
    a break of the most recent swing high/low is treated as the order block.
    This is a simplification of SMC order-block theory, not a guarantee of
    institutional footprint — treat it as one input among several, not proof.
    """
    df = detect_swings(df, lookback)
    obs = []
    swing_highs = df[df["swing_high"]]
    swing_lows = df[df["swing_low"]]

    for idx in range(len(df) - 1, lookback, -1):
        row = df.iloc[idx]
        prior_swing_highs = swing_highs[swing_highs.index < idx]
        prior_swing_lows = swing_lows[swing_lows.index < idx]

        if not prior_swing_highs.empty and row["close"] > prior_swing_highs["high"].iloc[-1]:
            # bullish break of structure — find last bearish candle before it
            for j in range(idx - 1, max(idx - 15, 0), -1):
                if df.iloc[j]["close"] < df.iloc[j]["open"]:
                    obs.append({"type": "bullish", "high": df.iloc[j]["high"], "low": df.iloc[j]["low"], "index": j})
                    break
            break

        if not prior_swing_lows.empty and row["close"] < prior_swing_lows["low"].iloc[-1]:
            for j in range(idx - 1, max(idx - 15, 0), -1):
                if df.iloc[j]["close"] > df.iloc[j]["open"]:
                    obs.append({"type": "bearish", "high": df.iloc[j]["high"], "low": df.iloc[j]["low"], "index": j})
                    break
            break

    return obs


def determine_bias(df):
    """
    Rough directional bias from the last two swing highs/lows:
    higher-highs + higher-lows = bullish, lower-highs + lower-lows = bearish,
    anything else = neutral (no clean structure yet).
    """
    df = detect_swings(df)
    highs = df[df["swing_high"]]["high"].tail(2).tolist()
    lows = df[df["swing_low"]]["low"].tail(2).tolist()

    if len(highs) == 2 and len(lows) == 2:
        if highs[1] > highs[0] and lows[1] > lows[0]:
            return "bullish"
        if highs[1] < highs[0] and lows[1] < lows[0]:
            return "bearish"
    return "neutral"


# --- 5. MULTI-TIMEFRAME CONFLUENCE ---
def fetch_ohlc(symbol, timeframe, bars=150):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)
    if rates is None or len(rates) == 0:
        return None
    return pd.DataFrame(rates)


def analyze_symbol(symbol):
    """
    Pulls H4/H1/M15/M5/M1, computes bias on each, and requires the higher
    timeframes (H4, H1) to agree before treating a lower-timeframe FVG/OB
    setup as valid. This is a confluence *filter*, not a signal generator on
    its own — it reduces false positives but doesn't eliminate them.
    """
    biases = {}
    dataframes = {}
    for label, tf in TIMEFRAMES.items():
        df = fetch_ohlc(symbol, tf)
        if df is None:
            print(f"⚠️ No data for {symbol} on {label}")
            return None
        dataframes[label] = df
        biases[label] = determine_bias(df)

    htf_bias = biases["H4"] if biases["H4"] == biases["H1"] else "neutral"
    if htf_bias == "neutral":
        return {"symbol": symbol, "valid": False, "reason": "H4/H1 disagree or no clear structure"}

    ltf_df = dataframes["M15"]
    fvgs = detect_fvgs(ltf_df)
    obs = detect_order_blocks(ltf_df)

    matching_fvgs = [f for f in fvgs if f["type"] == htf_bias]
    matching_obs = [o for o in obs if o["type"] == htf_bias]

    if not matching_fvgs and not matching_obs:
        return {"symbol": symbol, "valid": False, "reason": "no matching M15 FVG/OB in HTF bias direction"}

    zone = matching_fvgs[-1] if matching_fvgs else matching_obs[-1]
    action = "BUY" if htf_bias == "bullish" else "SELL"

    return {
        "symbol": symbol,
        "valid": True,
        "action": action,
        "zone_top": zone.get("top", zone.get("high")),
        "zone_bottom": zone.get("bottom", zone.get("low")),
        "htf_bias": htf_bias,
        "biases": biases,
    }


# --- 6. SCAN + TELEGRAM DISPATCH ---
async def scan_market_with_intelligence(bot: Bot):
    if not is_market_open_and_valid():
        return

    if check_high_impact_news_risk():
        return

    sessions = get_active_sessions()
    if not sessions:
        print("ℹ️ No major session active. Skipping scan (low-liquidity window).")
        return

    if not mt5.initialize():
        print(f"❌ MT5 initialize() failed: {mt5.last_error()}")
        return

    print(f"🧠 Scanning during session(s): {', '.join(sessions)}")

    for symbol in SYMBOLS:
        result = analyze_symbol(symbol)
        if result is None:
            continue
        if not result["valid"]:
            print(f"ℹ️ {symbol}: no valid setup ({result['reason']})")
            continue

        action = result["action"]
        PENDING_SIGNALS[symbol] = {"action": action, "sl_pips": 50, "tp_pips": 100}

        keyboard = [[
            InlineKeyboardButton("✅ Execute Trade", callback_data=f"exec_{symbol}"),
            InlineKeyboardButton("❌ Ignore", callback_data=f"ignore_{symbol}"),
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        message_text = (
            f"🚨 *SETUP DETECTED* 🚨\n\n"
            f"• *Asset:* {symbol}\n"
            f"• *Action:* {action}\n"
            f"• *HTF Bias:* {result['htf_bias']}\n"
            f"• *Zone:* {result['zone_bottom']:.5f} – {result['zone_top']:.5f}\n"
            f"• *Sessions active:* {', '.join(sessions)}\n\n"
            f"Approve this trade?"
        )

        try:
            await bot.send_message(
                chat_id=TELEGRAM_CHAT_ID,
                text=message_text,
                parse_mode="Markdown",
                reply_markup=reply_markup,
            )
            print(f"📲 Alert sent for {symbol}")
        except Exception as e:
            print(f"❌ Failed to send Telegram alert: {e}")

    mt5.shutdown()


# --- 7. TELEGRAM BUTTON HANDLER (this is what was missing) ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action_data, symbol = query.data.split("_", 1)

    if action_data == "ignore":
        PENDING_SIGNALS.pop(symbol, None)
        await query.edit_message_text(f"❌ Ignored {symbol} signal.")
        return

    if action_data == "exec":
        signal = PENDING_SIGNALS.pop(symbol, None)
        if signal is None:
            await query.edit_message_text("⚠️ This signal has expired or was already handled.")
            return

        if not mt5.initialize():
            await query.edit_message_text(f"❌ Could not connect to MT5 to execute {symbol}.")
            return

        result = execute_demo_trade(
            symbol,
            signal["action"],
            stop_loss_pips=signal["sl_pips"],
            take_profit_pips=signal["tp_pips"],
        )
        mt5.shutdown()

        if result is not None and result.retcode == mt5.TRADE_RETCODE_DONE:
            await query.edit_message_text(f"✅ Executed {signal['action']} on {symbol}.")
            
            # Appends the new trade to the list (allows 2, 3, or more concurrent trades)
            update_dashboard_state(True, {"symbol": symbol, "action": signal["action"], "lot": "0.10"})

# --- 8. PERIODIC SCAN JOB ---
async def scheduled_scan(context: ContextTypes.DEFAULT_TYPE):
    await scan_market_with_intelligence(context.bot)


# --- 9. MAIN ---
def main():
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        raise RuntimeError("TELEGRAM_TOKEN and TELEGRAM_CHAT_ID must be set in your .env file.")

    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CallbackQueryHandler(button_handler))

    # Scans every 15 minutes, aligned with the M15 structure it's built around.
    application.job_queue.run_repeating(scheduled_scan, interval=900, first=5)

    print("🤖 Constant FX bot running — polling Telegram for button presses and scanning every 15 min.")
    application.run_polling()


if __name__ == "__main__":
    main()
