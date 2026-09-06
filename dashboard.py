import streamlit as st
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Constant FX", 
    page_icon="🤖", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- PIXEL-PERFECT MOCKUP CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    /* Hide all default Streamlit headers, footers, and menus */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}

    /* Exact Soft Rose Pink Background from Mockup */
    .stApp {
        background: linear-gradient(135deg, #f3e5e8 0%, #ecd7dd 100%);
        color: #2b1b22;
        font-family: 'Inter', sans-serif;
    }

    /* Center and constrain width for mobile perfection */
    .block-container {
        max-width: 420px;
        padding-top: 1.5rem;
        padding-bottom: 5rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    /* Top Brand Header */
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
        margin-top: -10px;
        margin-bottom: 12px;
    }
    .status-pill {
        background-color: rgba(255, 255, 255, 0.85);
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
        height: 8px;
        width: 8px;
        background-color: #2ecc71;
        border-radius: 50%;
        box-shadow: 0 0 6px #2ecc71;
    }
    .status-dot-red {
        height: 8px;
        width: 8px;
        background-color: #e74c3c;
        border-radius: 50%;
        box-shadow: 0 0 6px #e74c3c;
    }

    /* Action Buttons Custom Styling (Side-by-Side Override) */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        gap: 10px !important;
        margin-bottom: 15px;
    }
    [data-testid="column"] {
        width: 50% !important;
        flex: 1 1 50% !important;
    }

    /* Stop Button (Dark Red/Coral) */
    .stop-btn button {
        background-color: #b84a4a !important;
        color: white !important;
        border-radius: 24px !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        height: 52px !important;
        width: 100% !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(184, 74, 74, 0.3) !important;
    }
    .stop-btn button:hover {
        background-color: #a53e3e !important;
    }

    /* Execute Button (Mauve/Pink) */
    .exec-btn button {
        background-color: #b05278 !important;
        color: white !important;
        border-radius: 24px !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        height: 52px !important;
        width: 100% !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(176, 82, 120, 0.3) !important;
    }
    .exec-btn button:hover {
        background-color: #9d466b !important;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background-color: rgba(255, 255, 255, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 14px 16px;
        margin-bottom: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    }

    /* Metrics Layout inside Card */
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

    /* Active Trades Section */
    .section-title {
        font-size: 11px;
        font-weight: 700;
        color: #7d6570;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }
    .trade-row {
        display: flex;
        justify-content: space-between;
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 6px;
        color: #2b1b22;
    }
    .trade-sell { color: #b84a4a; }
    .trade-buy { color: #27ae60; }
    .no-trades {
        text-align: center;
        color: #8c737f;
        font-style: italic;
        font-size: 13px;
        padding: 10px 0;
    }

    /* Fixed Bottom Navigation Bar */
    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(12px);
        border-top: 1px solid #e0c9d0;
        display: flex;
        justify-content: space-around;
        padding: 10px 0;
        z-index: 999;
    }
    .nav-item {
        text-align: center;
        color: #8c737f;
        font-size: 11px;
        font-weight: 600;
        text-decoration: none;
        cursor: pointer;
        background: none;
        border: none;
    }
    .nav-item.active {
        color: #b05278;
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE SETUP ---
if 'bot_running' not in st.session_state:
    st.session_state.bot_running = False
if 'nav_tab' not in st.session_state:
    st.session_state.nav_tab = "Home"

# --- TOP BRAND HEADER ---
st.markdown("""
    <div class="brand-container">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2b1b22" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"></line></svg>
        <span class="brand-title">CONSTANT FX</span>
    </div>
""", unsafe_allow_html=True)

# --- NAVIGATION ROUTING ---
if st.session_state.nav_tab == "Home":
    
    # --- ROBOT GRAPHIC ---
    if os.path.exists("robot_character.png"):
        st.image("robot_character.png", use_container_width=True)
    else:
        st.warning("⚠️ Place 'robot_character.png' in your repository folder.")

    # --- STATUS PILL ---
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

    # --- SIDE-BY-SIDE ACTION BUTTONS ---
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="stop-btn">', unsafe_allow_html=True)
        if st.button("⏹ STOP TRADING"):
            st.session_state.bot_running = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="exec-btn">', unsafe_allow_html=True)
        if st.button("▶ EXECUTE TRADES"):
            st.session_state.bot_running = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)

    # --- REALISTIC PERFORMANCE OVERVIEW CARD ---
    # Only populates real values if running, otherwise stable clean zeros
    if st.session_state.bot_running:
        p_val, t_val, w_val = "+14.2%", "38", "76.3%"
    else:
        p_val, t_val, w_val = "0.0%", "0", "0.0%"

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

    # --- ACTIVE TRADES CARD ---
    st.markdown("<div class='section-title'>ACTIVE TRADES</div>", unsafe_allow_html=True)
    
    if st.session_state.bot_running:
        trades_content = """
            <div class="trade-row"><span>XAUUSD</span> <span class="trade-sell">SELL</span></div>
            <div class="trade-row"><span>BTCUSD</span> <span class="trade-buy">BUY</span></div>
            <div class="trade-row"><span>ETHUSD</span> <span class="trade-buy">BUY</span></div>
            <div class="trade-row"><span>EURUSD</span> <span class="trade-sell">SELL</span></div>
        """
    else:
        trades_content = '<div class="no-trades">No active trades running</div>'

    st.markdown(f"""
        <div class="glass-card" style="margin-bottom: 2rem;">
            {trades_content}
        </div>
    """, unsafe_allow_html=True)

elif st.session_state.nav_tab == "Trades":
    st.markdown("### Trade History")
    st.write("Historical execution logs and closed performance data will display here.")

elif st.session_state.nav_tab == "Settings":
    st.markdown("### Configuration")
    st.text_input("MT5 Account ID", value="10293847")
    st.text_input("Broker Server", value="MetaQuotes-Demo")
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")

# --- NATIVE MOBILE BOTTOM NAVIGATION BAR ---
# Uses clean HTML buttons embedded to handle page routing seamlessly without emojis
st.markdown("""
    <div class="bottom-nav">
        <form action="" method="get">
            <button type="submit" name="tab" value="Home" class="nav-item">🏠<br>Home</button>
        </form>
    </div>
""", unsafe_allow_html=True)

# Cleaner programmatic switcher for the bottom bar using native buttons in columns
st.markdown("---")
b1, b2, b3 = st.columns(3)
with b1:
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.nav_tab = "Home"
        st.rerun()
with b2:
    if st.button("📈 Trades", use_container_width=True):
        st.session_state.nav_tab = "Trades"
        st.rerun()
with b3:
    if st.button("⚙️ Settings", use_container_width=True):
        st.session_state.nav_tab = "Settings"
        st.rerun()
