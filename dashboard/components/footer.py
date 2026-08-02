"""
SaaS Application Footer Component.
"""

import streamlit as st

def render_footer():
    """Renders clean SaaS footer with copyright and system information."""
    html = """
    <div style="margin-top: 40px; padding: 20px 0; border-top: 1px solid rgba(255,255,255,0.08); text-align: center; color: #64748B; font-size: 12px;">
        © 2026 Campus Energy Operations Platform • Enterprise SaaS Suite • Powered by FastAPI & Gemini 3.6 Flash RAG
    </div>
    """
    st.markdown(html, unsafe_allowed_html=True)
