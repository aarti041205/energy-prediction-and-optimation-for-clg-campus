import os
import sys
import streamlit as st

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from dashboard.api_client import get_alerts_data, post_acknowledge_alert, post_anomaly
from dashboard.components.theme_manager import apply_saas_theme
from dashboard.components.navbar import render_navbar
from dashboard.components.alert_cards import render_alert_card
from dashboard.components.footer import render_footer

st.set_page_config(page_title="Alert Center", page_icon="🚨", layout="wide")
apply_saas_theme()
render_navbar("Enterprise Alert Center & Anomaly Detection", "Real-Time System Alerts & Isolation Forest Anomaly Engine")

tab_alerts, tab_anomaly = st.tabs(["🚨 Alert Command Center", "🔍 Isolation Forest Anomaly Tool"])

with tab_alerts:
    f1, f2 = st.columns(2)
    with f1:
        sev_filter = st.selectbox("Severity Filter", ["All", "Critical", "High", "Medium", "Low"])
    with f2:
        bldg_filter = st.selectbox("Building Filter", ["All", "AI Lab", "Library", "Hostel", "Administration"])

    alerts = get_alerts_data(severity=sev_filter, building=bldg_filter)

    m1, m2, m3 = st.columns(3)
    m1.metric("Total Alerts Logged", len(alerts))
    m2.metric("Active Alerts", sum(1 for a in alerts if not a.get("acknowledged")))
    m3.metric("Critical Alerts", sum(1 for a in alerts if a.get("severity") == "Critical"))

    st.divider()

    for alert in alerts:
        render_alert_card(
            alert["id"], alert["timestamp"], alert["severity"], alert["building"],
            alert["category"], alert["message"], alert["recommended_action"],
            alert["acknowledged"], alert.get("color", "#EF4444"), alert.get("notification_icon", "🚨")
        )
        if not alert.get("acknowledged"):
            if st.button(f"Acknowledge Alert #{alert['id'][:8]}", key=alert["id"]):
                if post_acknowledge_alert(alert["id"]):
                    st.success("Alert acknowledged!")
                    st.rerun()

with tab_anomaly:
    st.markdown('<div class="saas-card">', unsafe_allowed_html=True)
    st.subheader("Compare Actual Telemetry against Isolation Forest")
    col1, col2 = st.columns(2)
    with col1:
        bldg_in = st.selectbox("Facility Building", ["Library", "Hostel", "AI Lab", "Admin"])
        temp_in = st.slider("Temperature (°C)", 15, 45, 32)
    with col2:
        load_in = st.slider("Equipment Load Factor", 0.0, 1.0, 0.90)
        actual_in = st.number_input("Actual Measured kWh", value=480.0, step=10.0)

    if st.button("🚨 Run Anomaly Check", use_container_width=True):
        res = post_anomaly({
            "Building": bldg_in,
            "Building_Type": "Academic",
            "Temperature": temp_in,
            "Humidity": 65.0,
            "Equipment_Load": load_in,
            "Actual_Energy_kWh": actual_in
        })
        if res.get("success"):
            data = res["data"]
            if data["is_anomaly"]:
                st.error(f"🚨 ANOMALY DETECTED! Difference: {data['difference_kwh']:.1f} kWh\n\n*Action:* {data['recommendation']}")
            else:
                st.success("✅ Telemetry baseline normal")
        else:
            st.error(res.get("error"))
    st.markdown('</div>', unsafe_allowed_html=True)

render_footer()
