import os
import sys
import streamlit as st

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from dashboard.api_client import post_prediction
from dashboard.components.theme_manager import apply_saas_theme
from dashboard.components.navbar import render_navbar
from dashboard.components.footer import render_footer

st.set_page_config(page_title="Energy Prediction Engine", page_icon="⚡", layout="wide")
apply_saas_theme()
render_navbar("Energy Load Forecasting", "Machine Learning Random Forest Energy Load Prediction")

st.markdown('<div class="saas-card">', unsafe_allowed_html=True)
st.subheader("⚙️ Input Telemetry Parameters")
col1, col2 = st.columns(2)

with col1:
    building = st.selectbox("Target Facility Building", ["AI Lab", "Library", "Hostel", "Administration", "Classroom Block"])
    building_type = st.selectbox("Facility Classification", ["Laboratory", "Academic", "Hostel", "Office"])
    temperature = st.slider("Ambient Temperature (°C)", 10, 48, 28)
    humidity = st.slider("Relative Humidity (%)", 10, 100, 65)
    occupancy = st.slider("Facility Occupancy Count", 0, 600, 180)

with col2:
    hour = st.slider("Hour of Day (0-23)", 0, 23, 14)
    day = st.slider("Day of Month (1-31)", 1, 31, 15)
    month = st.slider("Month of Year (1-12)", 1, 12, 8)
    weekend = st.selectbox("Weekend Baseline", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    holiday = st.selectbox("Holiday Baseline", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    equipment_load = st.slider("Equipment Load Ratio", 0.0, 1.0, 0.85)

st.markdown('</div>', unsafe_allowed_html=True)

if st.button("🚀 Run ML Load Prediction Engine", use_container_width=True):
    payload = {
        "Building": building,
        "Building_Type": building_type,
        "Temperature": temperature,
        "Humidity": humidity,
        "Hour": hour,
        "Day": day,
        "Month": month,
        "Weekend": weekend,
        "Holiday": holiday,
        "Equipment_Load": equipment_load,
        "Occupancy": occupancy,
        "Solar_Output": 120.0
    }

    with st.spinner("Executing FastAPI Random Forest Model..."):
        res = post_prediction(payload)
        if res.get("success"):
            data = res["data"]
            st.markdown('<div class="saas-card">', unsafe_allowed_html=True)
            st.success(f"### Predicted Energy Load: {data['predicted_energy_kwh']:.2f} kWh")

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Prediction ID", data["id"][:8] + "...")
            m2.metric("Confidence Score", f"{data['confidence_score']*100:.1f}%")
            m3.metric("Estimated Cost", f"₹ {data['electricity_cost_inr']:,.2f}")
            m4.metric("Carbon Emission", f"{data['carbon_emission_kg']:.1f} kg CO₂")

            if data.get("alerts_triggered"):
                st.subheader("🚨 Triggered Real-Time Alerts")
                for a in data["alerts_triggered"]:
                    st.error(f"**[{a['severity']}] {a['notification_icon']} {a['category']}**: {a['message']}\n\n*Action:* {a['recommended_action']}")
            st.markdown('</div>', unsafe_allowed_html=True)
        else:
            st.error(res.get("error"))

render_footer()
