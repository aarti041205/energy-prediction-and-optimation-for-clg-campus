import os
import sys
import streamlit as st

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from dashboard.api_client import get_health_status
from dashboard.components.theme_manager import apply_saas_theme
from dashboard.components.navbar import render_navbar
from dashboard.components.footer import render_footer

st.set_page_config(page_title="System Health", page_icon="🩺", layout="wide")
apply_saas_theme()
render_navbar("System Health Diagnostics", "Real-Time Telemetry & Service Health Metrics")

with st.spinner("Checking FastAPI Service Status..."):
    health = get_health_status()

status_str = health.get("status", "unknown").upper()
status_color = "#22C55E" if status_str == "HEALTHY" else "#EF4444"

st.markdown(f"""
<div class="saas-card" style="border-left: 5px solid {status_color};">
    <h2>System Health Status: <span style="color: {status_color};">{status_str}</span></h2>
</div>
""", unsafe_allowed_html=True)

m1, m2, m3, m4 = st.columns(4)
m1.metric("FastAPI Server", "ONLINE" if health.get("status") else "OFFLINE")
m2.metric("Random Forest Model", "LOADED" if health.get("model_loaded") else "DEGRADED")
m3.metric("Isolation Forest", "LOADED" if health.get("anomaly_model_loaded") else "DEGRADED")
m4.metric("Vector DB Index", "READY" if health.get("vector_db_ready") else "DEGRADED")

st.markdown('<div class="saas-card">', unsafe_allowed_html=True)
st.subheader("🖥️ Microservice Diagnostics")
st.json(health)
st.markdown('</div>', unsafe_allowed_html=True)

render_footer()
