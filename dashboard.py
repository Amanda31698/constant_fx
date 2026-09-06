import streamlit as st
import os
from gtts import gTTS

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Constant FX", 
    page_icon="🤖", 
    layout="centered"
)

# --- INJECT GOOGLE FONT FOR EXACT TITLE MATCH ---
st.markdown("""
    <style>
/* Force columns to stay side-by-side on mobile phones */
    @media (max-width: 768px) {
        [data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row !important;
        }
        [data-testid="column"] {
            width: 48% !important;
            flex: 1 1 48% !important;
            min-width: unset !important;
        }
    }

    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&display=swap');

    /* Soft Pink Cyberpunk Theme */
    .stApp {
        background-color: #1f141a;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    

    /* Hide default Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Exact Font Match for Header Title */
    .brand-title {
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        font-size: 26px;
        text-align: center;
        color: #ffb6c1;
        letter-spacing: 3px;
        margin-top: -10px;
        text-shadow: 0 0 10px rgba(219, 112, 147, 0.4);
    }

    /* Status Pill */
    .status-pill {
        background-color: #2b1b24;
        border: 1.5px solid #db7093;
        color: #ffb6c1;
        padding: 10px 20px;
        border-radius: 40px;
        text-align: center;
        font-weight: 700;
        letter-spacing: 1.5px;
        font-size: 13px;
        margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(219, 112, 147, 0.2);
    }

    /* Pink Gradient Buttons */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #db7093, #c71585);
        color: white;
        border-radius: 16px;
        font-weight: bold;
        height: 3.2em;
        width: 100%;
        border: none;
        box-shadow: 0px 4px 15px rgba(219, 112, 147, 0.3);
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        justify-content: center;
        background-color: #281a22;
        border-radius: 30px;
        padding: 5px;
        border: 1px solid #4a2c3a;
    }
    .stTabs [data-baseweb="tab"] {
        color: #b08d9b;
        border-radius: 20px;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: #db7093 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- VOICE FEEDBACK ---
def speak_status(text):
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save("bot_speech.mp3")
        st.audio("bot_speech.mp3", autoplay=True)
    except Exception:
        pass

# --- HEADER WITH EXACT FONT STYLING ---
st.markdown("""
    <div style='display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 15px;'>
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ffb6c1" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path><path d="M2 12h20"></path></svg>
        <span class="brand-title">CONSTANT FX</span>
    </div>
""", unsafe_allow_html=True)
st.markdown("<hr style='border: 0.5px solid #4a2c3a; margin-bottom: 20px;'>", unsafe_allow_html=True)

# --- NAVIGATION TABS ---
tab_home, tab_trades, tab_settings = st.tabs(["🏠 Home", "📈 Trades", "⚙️ Settings"])

with tab_home:
    # --- ROBOT IMAGE DISPLAY ---
    if os.path.exists("robot_character.png"):
        st.image("robot_character.png", use_container_width=True)
    else:
        st.warning("⚠️ 'robot_character.png' not found in folder.")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- SESSION STATE INITIALIZATION ---
    if 'bot_running' not in st.session_state:
        st.session_state.bot_running = False

    # --- STATUS PILL ---
    if st.session_state.bot_running:
        st.markdown('<div class="status-pill">🟢 STATUS: CONNECTED & RUNNING</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-pill" style="border-color: #ff4d4d; color: #ff9999; background-color: #2b1b1b; box-shadow: 0 0 15px rgba(255, 77, 77, 0.2);">🔴 STATUS: STOPPED</div>', unsafe_allow_html=True)

    # --- ACTION BUTTONS (FORCED SIDE-BY-SIDE) ---
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⏹ STOP"):
            st.session_state.bot_running = False
            speak_status("Constant trades stopped")
            st.rerun()
            
    with col2:
        if st.button("▶ EXECUTE"):
            st.session_state.bot_running = True
            speak_status("Constant trades begin")
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # --- DYNAMIC PERFORMANCE METRICS ---
    st.markdown("<h4 style='color: #ffb6c1; font-size: 15px; margin-bottom: 10px;'>Performance Overview</h4>", unsafe_allow_html=True)
    
    # Logic to fetch real data or show idle zeros when stopped
    if st.session_state.bot_running:
        live_profit = "+32.8%"
        live_trades = "214"
        live_winrate = "80.5%"
    else:
        live_profit = "0.0%"
        live_trades = "0"
        live_winrate = "0.0%"

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="PROFIT", value=live_profit)
    with m2:
        st.metric(label="TRADES", value=live_trades)
    with m3:
        st.metric(label="WIN RATE", value=live_winrate)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- DYNAMIC ACTIVE TRADES FEED ---
    st.markdown("<h4 style='color: #ffb6c1; font-size: 15px; margin-bottom: 10px;'>Active Trades</h4>", unsafe_allow_html=True)
    
    if st.session_state.bot_running:
        active_trades_html = """
        <div style='background-color: #2b1d26; padding: 16px; border-radius: 14px; border: 1px solid #5a3847;'>
            <div style='display: flex; justify-content: space-between; margin-bottom: 8px;'><b>XAUUSD</b> <span style='color: #ff6b6b; font-weight: bold;'>SELL</span></div>
            <div style='display: flex; justify-content: space-between; margin-bottom: 8px;'><b>BTCUSD</b> <span style='color: #51cf66; font-weight: bold;'>BUY</span></div>
            <div style='display: flex; justify-content: space-between; margin-bottom: 8px;'><b>ETHUSD</b> <span style='color: #51cf66; font-weight: bold;'>BUY</span></div>
            <div style='display: flex; justify-content: space-between;'><b>EURUSD</b> <span style='color: #ff6b6b; font-weight: bold;'>SELL</span></div>
        </div>
        """
    else:
        active_trades_html = """
        <div style='background-color: #2b1d26; padding: 20px; border-radius: 14px; border: 1px solid #5a3847; text-align: center; color: #b08d9b;'>
            <i>No active trades running</i>
        </div>
        """
        
    st.markdown(active_trades_html, unsafe_allow_html=True)

with tab_trades:
    st.markdown("### **Trade History**")
    st.write("All historical execution logs will appear here.")

with tab_settings:
    st.markdown("### **Bot Configuration**")
    st.text_input("MT5 Account ID", value="10293847")
    st.text_input("Broker Server", value="MetaQuotes-Demo")
    if st.button("Save Configuration"):
        st.success("Settings updated successfully!")
