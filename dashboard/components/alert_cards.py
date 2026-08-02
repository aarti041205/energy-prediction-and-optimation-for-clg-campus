"""
Enterprise Alert Card Component with Severity Color Coding.
"""

import streamlit as st

def render_alert_card(alert_id: str, timestamp: str, severity: str, building: str, category: str, message: str, recommended_action: str, acknowledged: bool, color: str = "#EF4444", icon: str = "🚨", on_acknowledge=None):
    """Renders a single Enterprise Alert card with status indicators and action buttons."""
    status_str = "Acknowledged ✅" if acknowledged else "Active 🚨"
    card_html = f"""
    <div style="background: #1E293B; border-left: 5px solid {color}; border-top: 1px solid rgba(255,255,255,0.08); border-right: 1px solid rgba(255,255,255,0.08); border-bottom: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 16px; margin-bottom: 14px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <div style="font-size: 15px; font-weight: 700; color: #F8FAFC; display: flex; align-items: center; gap: 8px;">
                <span>{icon}</span> <span>[{severity.upper()}] {category}</span>
            </div>
            <div style="font-size: 11px; color: #94A3B8; font-weight: 600;">{building} • {timestamp}</div>
        </div>
        <div style="font-size: 13px; color: #CBD5E1; margin-bottom: 10px;">{message}</div>
        <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.2); border-radius: 6px; padding: 8px 12px; font-size: 12px; color: #F8FAFC;">
            <strong style="color: #EF4444;">Recommended Action:</strong> {recommended_action}
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allowed_html=True)
