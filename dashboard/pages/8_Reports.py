import os
import sys
import streamlit as st

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from dashboard.api_client import post_generate_report, API_BASE_URL
from dashboard.components.theme_manager import apply_saas_theme
from dashboard.components.navbar import render_navbar
from dashboard.components.footer import render_footer

st.set_page_config(page_title="Report Center", page_icon="📄", layout="wide")
apply_saas_theme()
render_navbar("AI Report Generation & Export Center", "Automated PDF, DOCX, CSV & Markdown Synthesis Engine")

st.markdown('<div class="saas-card">', unsafe_allowed_html=True)
st.subheader("📝 Generate Comprehensive Campus Energy Report")
st.write("Synthesizes 10 technical sections covering baseline energy, peak demand, equipment loads, carbon footprint, and optimization strategies.")

if st.button("✨ Synthesize AI Executive Report", use_container_width=True):
    with st.spinner("Generating 10-Section AI Report via Gemini LLM & ReportLab..."):
        res = post_generate_report("Campus Energy Executive Report")
        if res.get("success"):
            st.session_state.report_data = res["data"]
            st.success("Report successfully generated!")
        else:
            st.error(res.get("error"))

if "report_data" in st.session_state:
    rep = st.session_state.report_data
    st.info(f"**Report Summary Preview:**\n\n{rep.get('report_summary')}")

    col1, col2, col3 = st.columns(3)
    if rep.get("pdf_url"):
        col1.markdown(f"[📥 Download PDF Document]({API_BASE_URL}{rep['pdf_url']})")
    if rep.get("docx_url"):
        col2.markdown(f"[📥 Download Word DOCX]({API_BASE_URL}{rep['docx_url']})")
    if rep.get("md_url"):
        col3.markdown(f"[📥 Download Markdown File]({API_BASE_URL}{rep['md_url']})")

st.divider()
st.subheader("📊 Data Exports")
ex1, ex2, ex3 = st.columns(3)
ex1.markdown(f"[📥 Export Analytics CSV]({API_BASE_URL}/export-csv?type=analytics)")
ex2.markdown(f"[📥 Export Optimization CSV]({API_BASE_URL}/export-csv?type=optimization)")
ex3.markdown(f"[📥 Export Anomalies CSV]({API_BASE_URL}/export-csv?type=anomalies)")
st.markdown('</div>', unsafe_allowed_html=True)

render_footer()
