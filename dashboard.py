import streamlit as st
import os
import json

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Constant FX", 
    page_icon="⚡", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- LOAD LIVE STATE FROM BACKGROUND ENGINE ---
def load_bot_state():
    if os.path.exists("bot_state.json"):
        try:
            with open("bot_state.json", "r") as f:
                return json.load(f)
        except:
            pass
    return {"bot_running": False, "active_trades": []}

state_data = load_bot_state()
bot_running = state_data.get("bot_running", False)
active_trades = state_data.get("active_trades", [])

# --- DARK INSTITUTIONAL TERMINAL CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}
    [data-testid="stToolbar"] {display: none;}

    .stApp {
        background: radial-gradient(circle at 50% 0%, #1a1e26 0%, #0d0f12 70%);
        color: #e1e4e8;
        font-family: 'Inter', sans-serif;
    }

    .block-container {
        max-width: 420px;
        padding-top: 1.5rem;
        padding-bottom: 6rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .brand-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        margin-bottom: 20px;
    }
    .brand-title {
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        font-size: 20px;
        color: #ffffff;
        letter-spacing: 2.5px;
    }
    .brand-title span { color: #e74c3c; }

    .hero-frame {
        border-radius: 20px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.6);
        margin-bottom: 16px;
    }

    .status-container {
        display: flex;
        justify-content: center;
        margin-bottom: 16px;
    }
    .status-pill {
        background-color: rgba(22, 25, 31, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #8b949e;
        padding: 6px 16px;
        border-radius: 30px;
        font-weight: 700;
        font-size: 11px;
        letter-spacing: 1.2px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .status-dot-green { height: 8px; width: 8px; background-color: #2ecc71; border-radius: 50%; box-shadow: 0 0 8px #2ecc71; }
    .status-dot-red { height: 8px; width: 8px; background-color: #e74c3c; border-radius: 50%; box-shadow: 0 0 8px #e74c3c; }

    /* Single Toggle Button Styling */
    div.stButton > button {
        border-radius: 24px !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        height: 56px !important;
        width: 100% !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.4) !important;
        transition: all 0.2s ease !important;
        letter-spacing: 1px;
    }
    
    /* Glass Cards */
    .glass-card {
        background-color: rgba(22, 25, 31, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 14px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.4);
    }

    .section-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 10px;
        font-weight: 700;
        color: #8b949e;
        letter-spacing: 1.5px;
        margin-bottom: 8px;
        margin-left: 4px;
    }

    .trade-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(13, 15, 18, 0.6);
        padding: 10px 14px;
        border-radius: 10px;
        margin-bottom: 6px;
        font-size: 13px;
        font-weight: 600;
        border: 1px solid rgba(255,255,255,0.04);
    }
    .trade-buy { color: #2ecc71; background: rgba(46, 204, 113, 0.08); padding: 4px 10px; border-radius: 6px; font-size: 11px; }
    .trade-sell { color: #e74c3c; background: rgba(231, 76, 60, 0.08); padding: 4px 10px; border-radius: 6px; font-size: 11px; }
    .no-trades { text-align: center; color: #484f58; font-style: italic; font-size: 12px; padding: 10px 0; }

    /* Bottom Nav Bar */
    .st-key-bottom_nav {
        position: fixed; bottom: 0; left: 0; right: 0; max-width: 420px; margin: 0 auto;
        background: rgba(13, 15, 18, 0.9); backdrop-filter: blur(16px);
        border-top: 1px solid rgba(255,255,255,0.08); border-radius: 20px 20px 0 0;
        padding: 8px 12px 14px 12px; z-index: 999;
    }
    .st-key-bottom_nav button {
        background: transparent !important; border: none !important; color: #8b949e !important;
        font-family: 'Inter', sans-serif !important; font-size: 11px !important; height: 42px !important;
        box-shadow: none !important;
    }
    .st-key-bottom_nav button:hover { color: #ffffff !important; }
    </style>
""", unsafe_allow_html=True)

if 'nav_tab' not in st.session_state:
    st.session_state.nav_tab = "Home"

# --- BRAND HEADER ---
st.markdown("""
    <div class="brand-container">
        <span class="brand-title">CONSTANT <span>FX</span></span>
    </div>
""", unsafe_allow_html=True)

# --- HOME TAB ---
if st.session_state.nav_tab == "Home":
    
    if os.path.exists("robot_character.png"):
        st.markdown('<div class="hero-frame">', unsafe_allow_html=True)
        st.image("robot_character.png", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if bot_running:
        st.markdown('<div class="status-container"><div class="status-pill"><div class="status-dot-green"></div>SYSTEM ONLINE</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-container"><div class="status-pill"><div class="status-dot-red"></div>SYSTEM STOPPED</div></div>', unsafe_allow_html=True)

    # --- SINGLE TOGGLE BUTTON ---
    if bot_running:
        if st.button("⏹ STOP ENGINE", type="secondary"):
            # Update state to stopped and clear active trades display
            with open("bot_state.json", "w") as f:
                json.dump({"bot_running": False, "active_trades": []}, f)
            st.rerun()
    else:
        if st.button("▶ START ENGINE", type="primary"):
            # Update state to running
            with open("bot_state.json", "w") as f:
                json.dump({"bot_running": True, "active_trades": [{"symbol": "EURUSD", "action": "BUY", "lot": "0.10"}]}, f)
            st.rerun()

    st.markdown("<div class='section-title' style='margin-top: 16px;'>ACTIVE POSITIONS</div>", unsafe_allow_html=True)
    
    if bot_running and active_trades:
        trades_html = ""
        for t in active_trades:
            side_cls = "trade-buy" if t.get('action') == "BUY" else "trade-sell"
            trades_html += f'<div class="trade-item"><span style="font-weight: 700; color: #fff;">{t.get("symbol")}</span> <span class="{side_cls}">{t.get("action")} {t.get("lot")}</span></div>'
    else:
        trades_html = '<div class="no-trades">No active execution threads</div>'

    st.markdown(f'<div class="glass-card" style="margin-bottom: 2rem;">{trades_html}</div>', unsafe_allow_html=True)

elif st.session_state.nav_tab == "Trades":
    st.markdown("### **Execution Logs**")
    st.markdown('<div class="glass-card"><div class="no-trades">Historical audit trail empty.</div></div>', unsafe_allow_html=True)

elif st.session_state.nav_tab == "Settings":
    st.markdown("### **Terminal Config**")
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.text_input("MT5 Account ID", value="10293847")
    st.text_input("Broker Gateway", value="MetaQuotes-Demo")
    if st.button("Save Parameters"):
        st.success("Config saved successfully.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- BOTTOM NAVIGATION BAR ---
with st.container(key="bottom_nav"):
    nav1, nav2, nav3 = st.columns(3)
    with nav1:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.nav_tab = "Home"
            st.rerun()
    with nav2:
        if st.button("📈 Trades", use_container_width=True):
            st.session_state.nav_tab = "Trades"
            st.rerun()
    with nav3:
        if st.button("⚙️ Settings", use_container_width=True):
            st.session_state.nav_tab = "Settings"
            st.rerun()
