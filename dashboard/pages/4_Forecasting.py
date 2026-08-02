import os
import sys
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from dashboard.components.theme_manager import apply_saas_theme
from dashboard.components.navbar import render_navbar
from dashboard.components.footer import render_footer

st.set_page_config(page_title="Energy Forecasting", page_icon="📈", layout="wide")
apply_saas_theme()
render_navbar("Predictive Load Forecasting", "24-Hour, 7-Day & 30-Day Predictive Trend Analysis")

horizon = st.selectbox("Select Forecast Horizon", ["24-Hour Forecast", "7-Day Forecast", "30-Day Forecast"])

steps = 24 if "24" in horizon else (168 if "7" in horizon else 720)
base = 320.0
time_index = pd.date_range(start=pd.Timestamp.now(), periods=steps, freq="h")
values = base + np.sin(np.linspace(0, 10 * np.pi, steps)) * 80 + np.random.normal(0, 15, steps)

df_forecast = pd.DataFrame({"Timestamp": time_index, "Forecasted_Load_kWh": values})

st.markdown('<div class="saas-card">', unsafe_allowed_html=True)
fig = px.line(df_forecast, x="Timestamp", y="Forecasted_Load_kWh", title=f"Predictive Energy Curve ({horizon})", template="plotly_dark")
fig.update_traces(line_color="#06B6D4", line_width=2.5)
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allowed_html=True)

render_footer()
