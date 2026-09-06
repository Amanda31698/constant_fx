import streamlit as st
import os
from gtts import gTTS

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Constant FX", 
    page_icon="🤖", 
    layout="centered"
)

# --- ADVANCED CYBERPUNK PINK CSS OVERRIDES ---
st.markdown("""
    <style>
    /* Force Dark Cyberpunk Background */
    .stApp {
        background-color: #160e12;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }

    /* Hide default Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main Container & Cards Styling */
    .metric-card {
        background-color: #261821;
        border: 1px solid #4a2c3a;
        padding: 15px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0px 4px 15px rgba(219, 112, 147, 0.1);
    }

    /* Status Pill Matching Mockup */
    .status-pill {
        background-color: #2b1b22;
        border: 1.5px solid #db7093;
        color: #ffb6c1;
        padding: 10px 20px;
        border-radius: 40px;
        text-align: center;
        font-weight: 700;
        letter-spacing: 1.5px;
        font-size: 14px;
        margin-bottom: 25px;
        box-shadow: 0 0 15px rgba(219, 112, 147, 0.25);
    }

    /* Custom Button Styling to match Pink & Red theme */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #db7093, #c71585);
        color: white;
        border-radius: 20px;
        font-weight: bold;
        height: 3.5em;
        width: 100%;
        border: none;
        box-shadow: 0px 4px 15px rgba(219, 112, 147, 0.4);
        transition: 0.3s ease;
    }
    
    div.stButton > button:first-child:hover {
        opacity: 0.9;
        transform: scale(1.02);
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        justify-content: center;
        background-color: #1f141a;
        border-radius: 30px;
        padding: 6px;
        border: 1px solid #3d222e;
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

# --- APP HEADER ---
st.markdown("<h2 style='text-align: center; color: #ffb6c1; letter-spacing: 3px; font-weight: 800;'>CONSTANT FX</h2>", unsafe_allow_html=True)
st.markdown("<hr style='border: 0.5px solid #3d222e; margin-bottom: 25px;'>", unsafe_allow_html=True)

# --- NAVIGATION TABS ---
tab_home, tab_trades, tab_settings = st.tabs(["🏠 Home", "📈 Trades", "⚙️ Settings"])

with tab_home:
    # --- ROBOT IMAGE DISPLAY ---
    if os.path.exists("robot_character.png"):
        st.image("robot_character.png", use_container_width=True)
    else:
        st.warning("⚠️ 'robot_character.png' not found in your folder. Drop your robot graphic in to complete the look!")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- SESSION STATE ---
    if 'bot_running' not in st.session_state:
        st.session_state.bot_running = False

    # --- STATUS PILL ---
    if st.session_state.bot_running:
        st.markdown('<div class="status-pill">🟢 STATUS: CONNECTED & RUNNING</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-pill" style="border-color: #ff4d4d; color: #ff9999; box-shadow: 0 0 15px rgba(255, 77, 77, 0.25);">🔴 STATUS: STOPPED</div>', unsafe_allow_html=True)

    # --- ACTION BUTTONS ---
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⏹ STOP TRADING"):
            st.session_state.bot_running = False
            speak_status("Constant trades stopped")
            st.rerun()
            
    with col2:
        if st.button("▶ EXECUTE TRADES"):
            st.session_state.bot_running = True
            speak_status("Constant trades begin")
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # --- PERFORMANCE METRICS ---
    st.markdown("<h4 style='color: #ffb6c1; font-size: 16px; margin-bottom: 10px;'>Performance Overview</h4>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="PROFIT", value="+32.8%")
    with m2:
        st.metric(label="TRADES", value="214")
    with m3:
        st.metric(label="WIN RATE", value="80.5%")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- ACTIVE TRADES FEED ---
    st.markdown("<h4 style='color: #ffb6c1; font-size: 16px; margin-bottom: 10px;'>Active Trades</h4>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background-color: #21151b; padding: 18px; border-radius: 14px; border: 1px solid #422633;'>
        <div style='display: flex; justify-content: space-between; margin-bottom: 8px;'><b>XAUUSD</b> <span style='color: #ff6b6b; font-weight: bold;'>SELL</span></div>
        <div style='display: flex; justify-content: space-between; margin-bottom: 8px;'><b>BTCUSD</b> <span style='color: #51cf66; font-weight: bold;'>BUY</span></div>
        <div style='display: flex; justify-content: space-between; margin-bottom: 8px;'><b>ETHUSD</b> <span style='color: #51cf66; font-weight: bold;'>BUY</span></div>
        <div style='display: flex; justify-content: space-between;'><b>EURUSD</b> <span style='color: #ff6b6b; font-weight: bold;'>SELL</span></div>
    </div>
    """, unsafe_allow_html=True)

with tab_trades:
    st.markdown("### **Trade History**")
    st.write("All historical and closed executions will display here.")

with tab_settings:
    st.markdown("### **Bot Configuration**")
    st.text_input("MT5 Account ID", value="10293847")
    st.text_input("Broker Server", value="MetaQuotes-Demo")
    if st.button("Save Configuration"):
        st.success("Settings updated successfully!")
