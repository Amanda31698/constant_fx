import MetaTrader5 as mt5
import time
import os
from dotenv import load_dotenv

load_dotenv()  # reads a local .env file — never commit this file to GitHub

# --- 1. CONNECT TO MT5 ---
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Credentials belong in a .env file, never hardcoded here:
# MT5_ACCOUNT=10293847
# MT5_PASSWORD=your_real_password
# MT5_SERVER=MetaQuotes-Demo
ACCOUNT = os.getenv("MT5_ACCOUNT")
PASSWORD = os.getenv("MT5_PASSWORD")
SERVER = os.getenv("MT5_SERVER")

# Only attempt explicit login if credentials are actually provided.
# If you're already logged into the desktop terminal, you can skip this entirely.
if ACCOUNT and PASSWORD and SERVER:
    authorized = mt5.login(int(ACCOUNT), password=PASSWORD, server=SERVER)
    if not authorized:
        print("Failed to connect to account, error code =", mt5.last_error())
        mt5.shutdown()
        quit()

print("Connected to MT5 successfully! Ready to trade.")


# --- 2. RISK-BASED POSITION SIZING ---
def calculate_lot_size(symbol, stop_loss_pips, risk_percent=1.0):
    """
    Sizes the position so a loss at the stop-loss level costs roughly
    `risk_percent` of current account equity, instead of using a flat lot size.
    """
    account_info = mt5.account_info()
    symbol_info = mt5.symbol_info(symbol)

    if account_info is None or symbol_info is None:
        print(f"⚠️ Could not fetch account/symbol info for {symbol}. Falling back to minimum lot.")
        return symbol_info.volume_min if symbol_info else 0.01

    equity = account_info.equity
    risk_amount = equity * (risk_percent / 100)

    # Value of one point move, per 1.0 lot, in account currency
    point_value = symbol_info.trade_tick_value / symbol_info.trade_tick_size * symbol_info.point
    sl_value_per_lot = stop_loss_pips * point_value

    if sl_value_per_lot <= 0:
        return symbol_info.volume_min

    lot = risk_amount / sl_value_per_lot
    lot = max(symbol_info.volume_min, min(lot, symbol_info.volume_max))
    # Round to the broker's allowed lot step
    lot = round(lot / symbol_info.volume_step) * symbol_info.volume_step
    return round(lot, 2)


# --- 3. TRADE EXECUTION FUNCTION (with SL/TP) ---
def execute_demo_trade(symbol, action, stop_loss_pips=50, take_profit_pips=100, risk_percent=1.0):
    """
    Executes a market order with a mandatory stop-loss and take-profit.
    Position size is calculated from account risk, not hardcoded.
    """
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(f"❌ Symbol {symbol} not found or not enabled in Market Watch.")
        return None

    if not symbol_info.visible:
        mt5.symbol_select(symbol, True)

    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        print(f"❌ Could not get tick data for {symbol}.")
        return None

    point = symbol_info.point
    price = tick.ask if action == "BUY" else tick.bid
    order_type = mt5.ORDER_TYPE_BUY if action == "BUY" else mt5.ORDER_TYPE_SELL

    # SL/TP calculated in price terms from pip distances
    if action == "BUY":
        sl = price - stop_loss_pips * point
        tp = price + take_profit_pips * point
    else:
        sl = price + stop_loss_pips * point
        tp = price - take_profit_pips * point

    lot_size = calculate_lot_size(symbol, stop_loss_pips, risk_percent)

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot_size,
        "type": order_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": 20,
        "magic": 234000,
        "comment": "Constant FX Bot",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    if result is None:
        print(f"❌ order_send returned None for {symbol}, last_error={mt5.last_error()}")
        return None

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"❌ Order failed for {symbol}, retcode={result.retcode}, comment={result.comment}")
    else:
        print(f"✅ Successfully executed {action} {lot_size} lots on {symbol} | SL={sl:.5f} TP={tp:.5f}")

    return result


# --- 4. MAIN RUNTIME LOOP ---
# NOTE: this loop is currently standalone. The next step is connecting it to
# fetch_data.py so that a signal generated there (and approved via Telegram)
# actually calls execute_demo_trade() here, instead of running in isolation.
if __name__ == "__main__":
    try:
        while True:
            print("Bot is monitoring markets... Press Ctrl+C to stop.")
            # Example manual test (uncomment to test on a demo account):
            # execute_demo_trade("EURUSD", "BUY", stop_loss_pips=50, take_profit_pips=100, risk_percent=1.0)
            time.sleep(10)
    except KeyboardInterrupt:
        print("Shutting down MT5 connection...")
        mt5.shutdown() 
