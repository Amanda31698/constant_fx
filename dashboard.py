import streamlit as st
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="AlgoFX Control Panel", page_icon="🤖", layout="centered")

# --- UI HEADER ---
st.image("https://img.icons8.com/fluency/96/chatbot.png", width=80)
st.title("AlgoFX Control Panel")
st.markdown("### **Bot Name:** constant_fx_bot")

# --- ROBOT STATUS SECTION ---
st.markdown("---")
status_container = st.empty()

# Simulated state (in production, this checks if your background script is running)
if 'bot_running' not in st.session_state:
    st.session_state.bot_running = False

if st.session_state.bot_running:
    status_container.success("ROBOT STATUS: 🟢 Connected & Scanning")
else:
    status_container.warning("ROBOT STATUS: 🔴 Stopped")

# --- CONTROL BUTTONS ---
col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 START ROBOT", use_container_width=True):
        st.session_state.bot_running = True
        st.rerun()

with col2:
    if st.button("🛑 STOP ROBOT", use_container_width=True):
        st.session_state.bot_running = False
        st.rerun()

# --- PERFORMANCE METRICS OVERVIEW ---
st.markdown("---")
st.markdown("### **Performance Overview**")

m1, m2, m3 = st.columns(3)
m1.metric(label="Profit", value="+25.4%", delta="2.1%")
m2.metric(label="Trades", value="152")
m3.metric(label="Win Rate", value="78.6%")

st.markdown("---")
st.caption("Last Update: Just now • MT5 Demo Engine Active")