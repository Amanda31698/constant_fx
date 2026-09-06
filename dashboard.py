import streamlit as st
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Constant FX", 
    page_icon="🤖", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- BULLETPROOF MOBILE & DESKTOP CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}

    /* Soft Rose Pink Background */
    .stApp {
        background: linear-gradient(135deg, #f3e5e8 0%, #ecd7dd 100%);
        color: #2b1b22;
        font-family: 'Inter', sans-serif;
    }

    /* Container constraints for mobile perfection */
    .block-container {
        max-width: 420px;
        padding-top: 1.2rem;
        padding-bottom: 6rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    /* Brand Header */
    .brand-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        margin-bottom: 5px;
    }
    .brand-title {
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        font-size: 22px;
        color: #2b1b22;
        letter-spacing: 2px;
    }

    /* Status Pill */
    .status-container {
        display: flex;
        justify-content: center;
        margin-top: -5px;
        margin-bottom: 12px;
    }
    .status-pill {
        background-color: rgba(255, 255, 255, 0.9);
        border: 1px solid #d4a5b3;
        color: #2b1b22;
        padding: 6px 18px;
        border-radius: 30px;
        font-weight: 700;
        font-size: 11px;
        letter-spacing: 1px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .status-dot-green {
        height: 8px; width: 8px; background-color: #2ecc71; border-radius: 50%; box-shadow: 0 0 6px #2ecc71;
    }
    .status-dot-red {
        height: 8px; width: 8px; background-color: #e74c3c; border-radius: 50%; box-shadow: 0 0 6px #e74c3c;
    }

    /* Side-by-Side Action Buttons */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        gap: 10px !important;
        margin-bottom: 12px;
    }
    [data-testid="column"] {
        width: 50% !important;
        flex: 1 1 50% !important;
    }

    /* Force Stop Button Styling (Prevents mobile dark-mode override) */
    div.stButton > button[kind="secondary"] {
        background-color: #b84a4a !important;
        color: #ffffff !important;
        border-radius: 20px !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        height: 50px !important;
        width: 100% !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(184, 74, 74, 0.3) !important;
    }

    /* Force Execute Button Styling */
    div.stButton > button[kind="primary"], div.stButton > button {
        background-color: #b05278 !important;
        color: #ffffff !important;
        border-radius: 20px !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        height: 50px !important;
        width: 100% !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(176, 82, 120, 0.3) !important;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background-color: rgba(255, 255, 255, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 14px 16px;
        margin-bottom: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    }

    /* Metrics Layout */
    .metrics-row {
        display: flex;
        justify-content: space-between;
        text-align: center;
    }
    .metric-item label {
        font-size: 10px;
        font-weight: 700;
        color: #7d6570;
        letter-spacing: 0.5px;
        display: block;
        margin-bottom: 2px;
    }
    .metric-item value {
        font-size: 16px;
        font-weight: 800;
        color: #2b1b22;
    }

    /* Active Trades UI */
    .section-title {
        font-size: 11px;
        font-weight: 700;
        color: #7d6570;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }
    .trade-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #fdf8f9;
        padding: 8px 12px;
        border-radius: 10px;
        margin-bottom: 6px;
        font-size: 13px;
        font-weight: 700;
        border: 1px solid #ebd7df;
    }
    .trade-sell { color: #b84a4a; }
    .trade-buy { color: #27ae60; }
    .no-trades {
        text-align: center;
        color: #8c737f;
        font-style: italic;
        font-size: 13px;
        padding: 8px 0;
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'bot_running' not in st.session_state:
    st.session_state.bot_running = False
if 'nav_tab' not in st.session_state:
    st.session_state.nav_tab = "Home"

# --- TOP HEADER ---
st.markdown("""
    <div class="brand-container">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2b1b22" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"></line></svg>
        <span class="brand-title">CONSTANT FX</span>
    </div>
""", unsafe_allow_html=True)

# --- CONTENT ROUTING ---
if st.session_state.nav_tab == "Home":
    
    # Robot Image
    if os.path.exists("robot_character.png"):
        st.image("robot_character.png", use_container_width=True)
    else:
        st.warning("⚠️ Place 'robot_character.png' in repository.")

    # Status Pill
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

    # Action Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⏹ STOP TRADING", key="stop_btn"):
            st.session_state.bot_running = False
            st.rerun()
    with col2:
        if st.button("▶ EXECUTE TRADES", key="exec_btn"):
            st.session_state.bot_running = True
            st.rerun()

    st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)

    # Performance Overview Card
    p_val = "+14.2%" if st.session_state.bot_running else "0.0%"
    t_val = "38" if st.session_state.bot_running else "0"
    w_val = "76.3%" if st.session_state.bot_running else "0.0%"

    st.markdown(f"""
        <div class="glass-card">
            <div class="metrics-row">
                <div class="metric-item">
                    <label>PROFIT</label>
                    <value style="color: #27ae60;">{p_val}</value>
                </div>
                <div class="metric-item">
                    <label>TRADES</label>
                    <value>{t_val}</value>
                </div>
                <div class="metric-item">
                    <label>WIN RATE</label>
                    <value>{w_val}</value>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Active Trades Section (User-friendly cards instead of raw text)
    st.markdown("<div class='section-title'>ACTIVE TRADES</div>", unsafe_allow_html=True)
    
    if st.session_state.bot_running:
        trades_html = """
            <div class="trade-item"><span>XAUUSD</span> <span class="trade-sell">SELL 0.50 lot</span></div>
            <div class="trade-item"><span>BTCUSD</span> <span class="trade-buy">BUY 0.10 lot</span></div>
            <div class="trade-item"><span>EURUSD</span> <span class="trade-sell">SELL 1.00 lot</span></div>
        """
    else:
        trades_html = '<div class="no-trades">No active trades running</div>'

    st.markdown(f"""
        <div class="glass-card" style="margin-bottom: 2rem;">
            {trades_html}
        </div>
    """, unsafe_allow_html=True)

elif st.session_state.nav_tab == "Trades":
    st.markdown("### **Trade History**")
    st.write("Closed trade execution logs will appear here.")

elif st.session_state.nav_tab == "Settings":
    st.markdown("### **Configuration**")
    st.text_input("MT5 Account ID", value="10293847")
    st.text_input("Broker Server", value="MetaQuotes-Demo")
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")

# --- WIDE BOTTOM NAVIGATION BAR (Liked by user) ---
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
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
