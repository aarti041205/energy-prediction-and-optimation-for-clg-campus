import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from dashboard.api_client import get_analytics_data, post_generate_report, API_BASE_URL
from dashboard.dashboard_utils import load_dataset
from dashboard.components.theme_manager import apply_saas_theme
from dashboard.components.navbar import render_navbar
from dashboard.components.footer import render_footer

st.set_page_config(page_title="Analytics Center", page_icon="📊", layout="wide")
apply_saas_theme()
render_navbar("Analytics & Energy Intelligence", "Comprehensive Interactive Data Analytics Platform")

df = load_dataset()
energy_col = "Energy_kWh" if "Energy_kWh" in df.columns else df.columns[0]

# KPIs
k1, k2, k3, k4 = st.columns(4)
k1.metric("Cumulative Energy", f"{df[energy_col].sum():,.0f} kWh")
k2.metric("Average Load", f"{df[energy_col].mean():.1f} kWh")
k3.metric("Peak Demand", f"{df[energy_col].max():.1f} kWh")
k4.metric("Total Expenditure", f"₹ {df[energy_col].sum()*8.5:,.0f}")

st.markdown('<div class="saas-card">', unsafe_allowed_html=True)
st.subheader("📈 Multi-Dimensional Interactive Charts")
tab1, tab2, tab3, tab4 = st.tabs(["24-Hour Line Profile", "Building Distribution", "Temperature Scatter", "Solar Output Area"])

with tab1:
    hourly = df.groupby("Hour")[energy_col].mean().reset_index()
    fig1 = px.line(hourly, x="Hour", y=energy_col, markers=True, template="plotly_dark")
    fig1.update_traces(line_color="#3B82F6", line_width=3)
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    bldg = df.groupby("Building")[energy_col].sum().reset_index()
    fig2 = px.bar(bldg, x="Building", y=energy_col, color="Building", template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    fig3 = px.scatter(df.head(400), x="Temperature", y=energy_col, color="Building", template="plotly_dark")
    st.plotly_chart(fig3, use_container_width=True)

with tab4:
    if "Solar_Output" in df.columns:
        solar = df.groupby("Hour")["Solar_Output"].mean().reset_index()
        fig4 = px.area(solar, x="Hour", y="Solar_Output", template="plotly_dark")
        st.plotly_chart(fig4, use_container_width=True)

st.markdown('</div>', unsafe_allowed_html=True)

render_footer()
