import os
import sys
import streamlit as st
import pandas as pd

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from dashboard.api_client import post_optimization, API_BASE_URL
from dashboard.components.theme_manager import apply_saas_theme
from dashboard.components.navbar import render_navbar
from dashboard.components.recommendation_cards import render_recommendation_card
from dashboard.components.footer import render_footer

st.set_page_config(page_title="Energy Optimization", page_icon="💡", layout="wide")
apply_saas_theme()
render_navbar("Optimization Strategy Engine", "AI Load Shifting, HVAC Setpoint & Annual Savings Projections")

building = st.selectbox("Target Facility", ["Main Campus", "AI Lab", "Library", "Hostel", "Administration"])
energy_val = st.number_input("Current Energy Baseline (kWh)", value=380.0, step=10.0)

if st.button("🚀 Calculate Optimization Strategies", use_container_width=True):
    with st.spinner("Executing Optimization Engine via FastAPI..."):
        res = post_optimization({"Building": building, "Energy_kWh": energy_val})
        if res.get("success"):
            st.session_state.opt_data = res["data"]
            st.success("Optimization analysis complete!")
        else:
            st.error(res.get("error"))

if "opt_data" in st.session_state:
    data = st.session_state.opt_data

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Potential Energy Savings", f"{data['total_potential_savings_kwh']} kWh")
    m2.metric("Estimated Cost Savings", f"₹ {data['total_potential_savings_inr']:,.2f}")
    m3.metric("CO₂ Carbon Reduction", f"{data['total_carbon_reduction_kg']} kg")
    m4.metric("Expected Annual Savings", f"₹ {data['expected_annual_savings_inr']:,.0f}")

    st.divider()

    recs = data.get("recommendations", [])
    for r in recs:
        render_recommendation_card(
            r["category"], r["recommendation"], r["energy_saving_pct"],
            r["estimated_savings_kwh"], r["estimated_savings_inr"],
            r["carbon_reduction_kg"], r["priority"]
        )

    st.markdown(f"[📥 Download Optimization CSV Report]({API_BASE_URL}/export-csv?type=optimization)")

render_footer()
