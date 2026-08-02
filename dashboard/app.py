import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from dashboard.api_client import (
    get_api_health, post_prediction, post_chat, get_analytics_data, get_alerts_data
)
from dashboard.dashboard_utils import load_dataset, total_energy, total_cost, total_carbon
from dashboard.components.theme_manager import apply_saas_theme
from dashboard.components.navbar import render_navbar
from dashboard.components.metric_cards import render_metric_card
from dashboard.components.footer import render_footer

st.set_page_config(
    page_title="Campus Energy Ops Platform",
    page_icon="⚡",
    layout="wide"
)

apply_saas_theme()
render_navbar("Campus Energy Command Center", "Enterprise Telemetry, Predictive Analytics & AI Command Operations")

# Check FastAPI Backend Health
health = get_api_health()
api_status = health.get("status", "offline")

# Sidebar Status
with st.sidebar:
    # pyrefly: ignore [unexpected-keyword]
    st.markdown('<div style="font-weight:700; color:#3B82F6; margin-bottom:10px;">SYSTEM STATUS</div>', unsafe_allowed_html=True)
    if api_status == "healthy":
        st.success("FastAPI Engine: Live 🟢")
    elif api_status == "degraded":
        st.warning("FastAPI Engine: Degraded 🟡")
    else:
        st.error("FastAPI Engine: Offline 🔴")

    # pyrefly: ignore [unexpected-keyword]
    st.markdown('<div style="font-weight:700; color:#3B82F6; margin-top:20px; margin-bottom:10px;">AI PIPELINE</div>', unsafe_allowed_html=True)
    st.info("LLM: Gemini 3.6 Flash")
    st.caption("Vector DB: FAISS Top-5")
    st.caption("ML: Random Forest + Isolation Forest")

# Dataset
df = load_dataset()
tot_e = total_energy(df)
tot_c = total_cost(df)
tot_car = total_carbon(df)

# Top Metric Cards
c1, c2, c3, c4 = st.columns(4)
with c1:
    render_metric_card("TOTAL ENERGY LOAD", f"{tot_e:,.0f} kWh", "12%", True, "⚡", "rgba(245, 158, 11, 0.15)", "#F59E0B", [320, 340, 310, 380, 420, 390, 450])
with c2:
    render_metric_card("TOTAL EXPENDITURE", f"₹ {tot_c:,.0f}", "5%", True, "💰", "rgba(34, 197, 94, 0.15)", "#22C55E", [15, 18, 16, 22, 25, 24, 29])
with c3:
    render_metric_card("CARBON FOOTPRINT", f"{tot_car:,.1f} Tons", "8%", True, "🌱", "rgba(59, 130, 246, 0.15)", "#3B82F6", [80, 85, 82, 90, 95, 92, 102])
with c4:
    render_metric_card("ANOMALY RATE", "1.4%", "2%", False, "🚨", "rgba(239, 68, 68, 0.15)", "#EF4444", [4, 3, 5, 2, 3, 2, 1])

# pyrefly: ignore [unexpected-keyword]
st.markdown("<br/>", unsafe_allowed_html=True)

# Main Dashboard Content
col_left, col_right = st.columns([1.2, 1.4])

with col_left:
    # pyrefly: ignore [unexpected-keyword]
    st.markdown('<div class="saas-card">', unsafe_allowed_html=True)
    st.subheader("⚡ Quick Prediction Simulator")
    building = st.selectbox("Facility Building", ["AI Lab", "Library", "Hostel", "Administration", "Classroom Block"])
    building_type = st.selectbox("Facility Category", ["Laboratory", "Academic", "Hostel", "Office"])

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        temperature = st.slider("Temperature (°C)", 10, 48, 28)
        hour = st.slider("Hour (0-23)", 0, 23, 14)
    with col_s2:
        humidity = st.slider("Humidity (%)", 10, 100, 65)
        equipment = st.slider("Equipment Load", 0.0, 1.0, 0.85)

    if st.button("⚡ Run ML Load Prediction", use_container_width=True):
        payload = {
            "Building": building,
            "Building_Type": building_type,
            "Temperature": temperature,
            "Humidity": humidity,
            "Hour": hour,
            "Day": 15,
            "Month": 8,
            "Weekend": 0,
            "Holiday": 0,
            "Equipment_Load": equipment
        }
        with st.spinner("Executing FastAPI Random Forest Model..."):
            res = post_prediction(payload)
            if res.get("success"):
                data = res["data"]
                st.success(
                    f"**Predicted Load:** {data['predicted_energy_kwh']:.2f} kWh  |  **Confidence:** {data['confidence_score']*100:.1f}%\n\n"
                    f"**Estimated Cost:** ₹{data['electricity_cost_inr']:,.2f}  |  **Carbon:** {data['carbon_emission_kg']:.1f} kg CO₂"
                )
            else:
                st.error(res.get("error"))
    # pyrefly: ignore [unexpected-keyword]
    st.markdown('</div>', unsafe_allowed_html=True)

with col_right:
    # pyrefly: ignore [unexpected-keyword]
    st.markdown('<div class="saas-card">', unsafe_allowed_html=True)
    st.subheader("📈 24-Hour Telemetry Load Profile")
    hourly_df = df.groupby("Hour")["Energy_kWh"].mean().reset_index()
    fig1 = px.line(hourly_df, x="Hour", y="Energy_kWh", markers=True, template="plotly_dark")
    fig1.update_traces(line_color="#3B82F6", line_width=3)
    st.plotly_chart(fig1, use_container_width=True)
    # pyrefly: ignore [unexpected-keyword]
    st.markdown('</div>', unsafe_allowed_html=True)

render_footer()