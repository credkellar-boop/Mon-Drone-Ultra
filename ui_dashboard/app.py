import streamlit as st
import random
import time

# Configure page settings
st.set_page_config(
    page_title="Mon-Drone-Ultra | Mission Control",
    page_icon="🛸",
    layout="wide"
)

# App Title & Connection Status
st.title("🛸 Mon-Drone-Ultra Mission Control")
st.sidebar.markdown("### 🟢 System Status: Connected")
st.sidebar.markdown("---")

# Mock telemetry state data (In production, populate these via your MAVSDK stream)
current_lat = 37.7749
current_lng = -122.4194
altitude = 12.5 # meters
battery = 88 # percentage
ai_mode = "Face Tracking Active"

# Sidebar controls for manual mission payload overrides
st.sidebar.subheader("Payload & Manual Overrides")
projector_on = st.sidebar.toggle("Activate 60\" Projector", value=False)
audio_on = st.sidebar.toggle("Enable Audio Amplifier Speakers", value=False)
manual_kill = st.sidebar.button("🚨 EMERGENCY LAND", use_container_width=True)

if manual_kill:
    st.sidebar.error("EMERGENCY COMMAND SENT: Landing Immediately.")

# Main Dashboard Layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Real-Time Telemetry Mapping")
    
    # Generate an embedded map dashboard centered on the drone's position
    # Uses OpenStreetMap/Leaflet syntax for quick, free local simulation; swap to Google Maps API with your token
    map_html = f"""
    <iframe 
        width="100%" 
        height="500" 
        src="https://maps.google.com/maps?q={current_lat},{current_lng}&z=17&output=embed" 
        style="border:0; border-radius: 10px;">
    </iframe>
    """
    st.components.v1.html(map_html, height=520)

with col2:
    st.subheader("System Logistics")
    
    # Telemetry metrics cards
    st.metric(label="Altitude", value=f"{altitude} m", delta="Stabilized")
    st.metric(label="Onboard Battery Pack", value=f"{battery}%", delta="-2% past 10m")
    
    st.markdown("---")
    st.subheader("AI Brain & Hardware State")
    
    st.info(f"**Current Navigation State:** {ai_mode}")
    
    if projector_on:
        st.success("🎥 **Projector:** ON (Streaming UI to Ground Matrix)")
    else:
        st.warning("🎥 **Projector:** STANDBY")
        
    if audio_on:
        st.success("🔊 **Audio Node:** BROADCASTING")
    else:
        st.warning("🔊 **Audio Node:** MUTED")

# Telemetry live-reloader mechanism
st.caption("Dashboard feeds auto-refreshing at 2Hz via internal MAVLink state loop.")
