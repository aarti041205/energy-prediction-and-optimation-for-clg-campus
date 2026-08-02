import os
import sys
import streamlit as st

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from dashboard.components.theme_manager import apply_saas_theme
from dashboard.components.navbar import render_navbar
from dashboard.components.building_cards import render_building_card
from dashboard.components.footer import render_footer

st.set_page_config(page_title="Building Monitoring", page_icon="🏢", layout="wide")
apply_saas_theme()
render_navbar("Building Telemetry & Facility Monitoring", "Real-Time Facility Baseline & Efficiency Tracking")

buildings = [
    {"name": "AI Supercomputing Lab", "cat": "Laboratory", "current": 450.0, "pred": 462.5, "eff": 88, "status": "Active Alert", "icon": "🖥️"},
    {"name": "Student Residence Hostel", "cat": "Residential", "current": 510.0, "pred": 498.0, "eff": 92, "status": "Nominal", "icon": "🏠"},
    {"name": "Central University Library", "cat": "Academic", "current": 290.0, "pred": 285.0, "eff": 95, "status": "Nominal", "icon": "📚"},
    {"name": "Administration Complex", "cat": "Administrative", "current": 260.0, "pred": 268.0, "eff": 89, "status": "Nominal", "icon": "🏢"},
    {"name": "Main Classroom Block", "cat": "Academic", "current": 390.0, "pred": 405.0, "eff": 91, "status": "Nominal", "icon": "🏫"}
]

col1, col2 = st.columns(2)
for i, b in enumerate(buildings):
    with col1 if i % 2 == 0 else col2:
        render_building_card(b["name"], b["cat"], b["current"], b["pred"], b["eff"], b["status"], b["icon"])

render_footer()
