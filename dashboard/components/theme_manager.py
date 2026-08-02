"""
Theme Manager Module for Injecting SaaS CSS Files into Streamlit Pages.
"""

import os
import streamlit as st

def apply_saas_theme():
    """Reads all CSS stylesheets in dashboard/styles/ and injects them into the Streamlit session."""
    styles_dir = os.path.join(os.path.dirname(__file__), "..", "styles")
    combined_css = ""
    if os.path.exists(styles_dir):
        for filename in sorted(os.listdir(styles_dir)):
            if filename.endswith(".css"):
                filepath = os.path.join(styles_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        combined_css += f"\n/* --- {filename} --- */\n" + f.read()
                except Exception:
                    pass

    if combined_css:
        # pyrefly: ignore [unexpected-keyword]
        st.markdown(f"<style>{combined_css}</style>", unsafe_allowed_html=True)
