"""
Top Navbar Component for Enterprise SaaS Application.
"""

from datetime import datetime
import streamlit as st

def render_navbar(title: str = "Dashboard", subtitle: str = "Campus Energy Operations Baseline"):
    """Renders the top navbar with live status badge, current time, and subtitle."""
    now_str = datetime.now().strftime("%B %d, %Y • %H:%M UTC")
    html = f"""
    <div class="saas-navbar">
        <div class="saas-navbar-brand">
            <div>
                <div class="saas-navbar-title">
                    {title}
                    <span class="saas-live-badge"><span class="saas-live-dot"></span> Live System</span>
                </div>
                <div class="saas-navbar-subtitle">{subtitle}</div>
            </div>
        </div>
        <div class="saas-navbar-right">
            <div class="saas-time-pill">🕒 {now_str}</div>
        </div>
    </div>
    """
    # pyrefly: ignore [unexpected-keyword]
    st.markdown(html, unsafe_allowed_html=True)
