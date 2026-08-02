import os
import sys
import streamlit as st

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from dashboard.components.theme_manager import apply_saas_theme
from dashboard.components.navbar import render_navbar
from dashboard.components.footer import render_footer

st.set_page_config(page_title="Settings Panel", page_icon="⚙️", layout="wide")
apply_saas_theme()
render_navbar("System Settings & Configuration", "API Credentials, Alert Thresholds & Database Connections")

st.markdown('<div class="saas-card">', unsafe_allowed_html=True)
st.subheader("🤖 Gemini RAG & AI Configuration")
gemini_key = st.text_input("GOOGLE_API_KEY", type="password", value="****************************************")

st.subheader("🗄️ Database Connection Settings")
db_url = st.text_input("DATABASE_URL", value="postgresql://postgres:***@localhost:5432/campus_energy_db")

st.subheader("🚨 Alert Threshold Controls")
high_energy = st.slider("High Energy Threshold (kWh)", 300, 800, 450)
high_temp = st.slider("High Temperature Threshold (°C)", 25, 50, 35)

st.subheader("📧 SMTP Notification Server")
col1, col2 = st.columns(2)
col1.text_input("SMTP Server", value="smtp.gmail.com")
col2.text_input("SMTP Port", value="587")

if st.button("💾 Save System Configuration"):
    st.success("Configuration updated successfully.")

st.markdown('</div>', unsafe_allowed_html=True)

render_footer()
