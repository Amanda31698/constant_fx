import streamlit as st
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Constant FX",
    page_icon="◈",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}
    [data-testid="stToolbar"] {display: none;}

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: radial-gradient(120% 100% at 50% 0%, #f6e6ea 0%, #eccdd6 55%, #e3b9c6 100%);
        color: #2b1622;
    }

    .block-container {
        max-width: 430px;
        padding-top: 1.6rem;
        padding-bottom: 7rem;
        padding-left: 1.1rem;
        padding-right: 1.1rem;
    }

    /* ---------- BRAND ---------- */
    .brand-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        margin-bottom: 18px;
    }
    .brand-mark {
        width: 26px;
        height: 26px;
        border-radius: 50%;
        border: 2.5px solid #2b1622;
        position: relative;
        flex-shrink: 0;
    }
    .brand-mark::after {
        content: "";
        position: absolute;
        top: 50%;
        left: 50%;
        width: 2.5px;
        height: 14px;
        background: #2b1622;
        transform: translate(-50%, -50%) rotate(35deg);
    }
    .brand-title {
        font-family: 'Poppins', sans-serif;
        font-weight: 800;
        font-size: 21px;
        color: #2b1622;
        letter-spacing: 1.5px;
    }
    .brand-title span {
        font-weight: 600;
        color: #a8455e;
    }

    /* ---------- HERO IMAGE ---------- */
    .hero-frame {
        border-radius: 26px;
        overflow: hidden;
        box-shadow: 0 18px 40px -12px rgba(120, 40, 65, 0.35);
        margin-bottom: 16px;
        border: 1px solid rgba(255,255,255,0.6);
    }

    /* ---------- STATUS PILL ---------- */
    .status-container {
        display: flex;
        justify-content: center;
        margin-bottom: 18px;
    }
    .status-pill {
        background-color: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255,255,255,0.9);
        color: #2b1622;
        padding: 8px 20px;
        border-radius: 30px;
        font-weight: 700;
        font-size: 12px;
        letter-spacing: 0.6px;
        box-shadow: 0 6px 16px rgba(120, 40, 65, 0.08);
        display: flex;
        align-items: center;
        gap: 9px;
    }
    .status-dot-green {
        height: 8px; width: 8px; background-color: #2ecc71; border-radius: 50%;
        box-shadow: 0 0 8px #2ecc71;
    }
    .status-dot-red {
        height: 8px; width: 8px; background-color: #e74c3c; border-radius: 50%;
        box-shadow: 0 0 8px #e74c3c;
    }

    /* ---------- ACTION BUTTONS ---------- */
    div[data-testid="stHorizontalBlock"]:has(button[kind="secondary"]),
    div[data-testid="stHorizontalBlock"]:has(button[kind="primary"]) {
        gap: 12px !important;
        margin-bottom: 18px !important;
    }

    div.stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, #d16a5f 0%, #b8483f 100%) !important;
        color: #ffffff !important;
        border-radius: 22px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        letter-spacing: 0.3px;
        line-height: 1.35 !important;
        white-space: pre-line !important;
        height: 58px !important;
        width: 100% !important;
        border: none !important;
        box-shadow: 0 8px 18px -6px rgba(184, 72, 63, 0.55) !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 20px -6px rgba(184, 72, 63, 0.6) !important;
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #d9557f 0%, #b8305d 100%) !important;
        color: #ffffff !important;
        border-radius: 22px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        letter-spacing: 0.3px;
        line-height: 1.35 !important;
        white-space: pre-line !important;
        height: 58px !important;
        width: 100% !important;
        border: none !important;
        box-shadow: 0 8px 18px -6px rgba(184, 48, 93, 0.55) !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 20px -6px rgba(184, 48, 93, 0.6) !important;
    }

    /* ---------- GLASS CARDS ---------- */
    .glass-card {
        background-color: rgba(255, 255, 255, 0.72);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 18px 18px;
        margin-bottom: 14px;
        box-shadow: 0 10px 26px -12px rgba(120, 40, 65, 0.18);
    }

    .metrics-row {
        display: flex;
        justify-content: space-between;
        text-align: center;
    }
    .metric-item {
        flex: 1;
    }
    .metric-item label {
        font-size: 10px;
        font-weight: 700;
        color: #97788a;
        letter-spacing: 0.8px;
        display: block;
        margin-bottom: 4px;
    }
    .metric-item .value {
        font-family: 'Poppins', sans-serif;
        font-size: 18px;
        font-weight: 800;
        color: #2b1622;
    }
    .metric-divider {
        width: 1px;
        background: rgba(43, 22, 34, 0.1);
        margin: 2px 6px;
    }

    /* ---------- ACTIVE TRADES ---------- */
    .section-title {
        font-size: 11px;
        font-weight: 700;
        color: #97788a;
        letter-spacing: 0.8px;
        margin: 4px 0 8px 4px;
    }
    .trade-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 4px;
        font-size: 13.5px;
        font-weight: 600;
        color: #2b1622;
        border-bottom: 1px solid rgba(43, 22, 34, 0.07);
    }
    .trade-item:last-child { border-bottom: none; }
    .trade-side {
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 11.5px;
        letter-spacing: 0.3px;
    }
    .trade-sell { color: #b8483f; background: rgba(184, 72, 63, 0.1); }
    .trade-buy { color: #27ae60; background: rgba(39, 174, 96, 0.1); }
    .no-trades {
        text-align: center;
        color: #a98da0;
        font-style: italic;
        font-size: 13px;
        padding: 10px 0;
    }

    /* ---------- BOTTOM NAV ---------- */
    .nav-spacer { height: 8px; }
    .st-key-bottom_nav {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        max-width: 430px;
        margin: 0 auto;
        background: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(14px);
        border-top: 1px solid rgba(43,22,34,0.06);
        border-radius: 22px 22px 0 0;
        padding: 10px 14px 16px 14px;
        box-shadow: 0 -8px 24px rgba(120, 40, 65, 0.08);
        z-index: 999;
    }
    .st-key-bottom_nav div[data-testid="stHorizontalBlock"] {
        gap: 6px !important;
    }
    .st-key-bottom_nav button {
        background: transparent !important;
        border: none !important;
        color: #a98da0 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 11.5px !important;
        line-height: 1.3 !important;
        white-space: pre-line !important;
        box-shadow: none !important;
        height: 48px !important;
    }
    .st-key-bottom_nav button:hover {
        color: #b8305d !important;
    }

    h3 { font-family: 'Poppins', sans-serif; color: #2b1622; }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'bot_running' not in st.session_state:
    st.session_state.bot_running = False
if 'nav_tab' not in st.session_state:
    st.session_state.nav_tab = "Home"

# --- BRAND HEADER ---
st.markdown("""
    <div class="brand-container">
        <div class="brand-mark"></div>
        <span class="brand-title">CONSTANT <span>FX</span></span>
    </div>
""", unsafe_allow_html=True)

# --- CONTENT ROUTING ---
if st.session_state.nav_tab == "Home":

    st.markdown('<div class="hero-frame">', unsafe_allow_html=True)
    if os.path.exists("robot_character.png"):
        st.image("robot_character.png", use_container_width=True)
    else:
        st.warning("Place 'robot_character.png' in the repository root.")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.bot_running:
        st.markdown("""
            <div class="status-container">
                <div class="status-pill"><div class="status-dot-green"></div>STATUS: CONNECTED</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="status-container">
                <div class="status-pill"><div class="status-dot-red"></div>STATUS: STOPPED</div>
            </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("■\nSTOP TRADING", key="stop_btn", type="secondary"):
            st.session_state.bot_running = False
            st.rerun()
    with col2:
        if st.button("▶\nEXECUTE TRADES", key="exec_btn", type="primary"):
            st.session_state.bot_running = True
            st.rerun()

    p_val = "+14.2%" if st.session_state.bot_running else "0.0%"
    t_val = "38" if st.session_state.bot_running else "0"
    w_val = "76.3%" if st.session_state.bot_running else "0.0%"

    st.markdown(f"""
        <div class="glass-card">
            <div class="metrics-row">
                <div class="metric-item">
                    <label>PROFIT</label>
                    <div class="value" style="color: #27ae60;">{p_val}</div>
                </div>
                <div class="metric-divider"></div>
                <div class="metric-item">
                    <label>TRADES</label>
                    <div class="value">{t_val}</div>
                </div>
                <div class="metric-divider"></div>
                <div class="metric-item">
                    <label>WIN RATE</label>
                    <div class="value">{w_val}</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>ACTIVE TRADES</div>", unsafe_allow_html=True)

    if st.session_state.bot_running:
        trades_html = """
            <div class="trade-item"><span>XAUUSD</span> <span class="trade-side trade-sell">SELL 0.50 lot</span></div>
            <div class="trade-item"><span>BTCUSD</span> <span class="trade-side trade-buy">BUY 0.10 lot</span></div>
            <div class="trade-item"><span>EURUSD</span> <span class="trade-side trade-sell">SELL 1.00 lot</span></div>
        """
    else:
        trades_html = '<div class="no-trades">No active trades running</div>'

    st.markdown(f"""
        <div class="glass-card" style="margin-bottom: 2rem;">
            {trades_html}
        </div>
    """, unsafe_allow_html=True)

elif st.session_state.nav_tab == "Trades":
    st.markdown("### Trade History")
    st.markdown("""
        <div class="glass-card">
            <div class="no-trades">Closed trade execution logs will appear here.</div>
        </div>
    """, unsafe_allow_html=True)

elif st.session_state.nav_tab == "Settings":
    st.markdown("### Configuration")
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.text_input("MT5 Account ID", value="10293847")
    st.text_input("Broker Server", value="MetaQuotes-Demo")
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")
    st.markdown('</div>', unsafe_allow_html=True)

# --- BOTTOM NAVIGATION ---
st.markdown("<div class='nav-spacer'></div>", unsafe_allow_html=True)
with st.container(key="bottom_nav"):
    nav1, nav2, nav3 = st.columns(3)
    with nav1:
        if st.button("🏠\nHome", key="nav_home", use_container_width=True):
            st.session_state.nav_tab = "Home"
            st.rerun()
    with nav2:
        if st.button("📈\nTrades", key="nav_trades", use_container_width=True):
            st.session_state.nav_tab = "Trades"
            st.rerun()
    with nav3:
        if st.button("⚙️\nSettings", key="nav_settings", use_container_width=True):
            st.session_state.nav_tab = "Settings"
            st.rerun()
