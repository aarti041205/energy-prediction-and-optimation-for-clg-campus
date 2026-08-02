"""
Building Monitoring Card Component.
"""

import streamlit as st

def render_building_card(building_name: str, category: str, current_usage: float, predicted_usage: float, efficiency_score: int, alert_status: str = "Nominal", icon: str = "🏢"):
    """Renders a single Building Monitoring Card with telemetry metrics."""
    status_color = "#22C55E" if alert_status == "Nominal" else "#EF4444"
    card_html = f"""
    <div class="saas-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div class="saas-icon-badge" style="background: rgba(59, 130, 246, 0.15); color: #3B82F6;">{icon}</div>
                <div>
                    <div style="font-size: 15px; font-weight: 700; color: #F8FAFC;">{building_name}</div>
                    <div style="font-size: 11px; color: #94A3B8;">{category}</div>
                </div>
            </div>
            <div style="background: {status_color}22; color: {status_color}; border: 1px solid {status_color}44; font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 6px;">
                {alert_status}
            </div>
        </div>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 14px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.08);">
            <div>
                <div style="font-size: 11px; color: #94A3B8;">Current Load</div>
                <div style="font-size: 16px; font-weight: 700; color: #F8FAFC;">{current_usage:.1f} kWh</div>
            </div>
            <div>
                <div style="font-size: 11px; color: #94A3B8;">Predicted</div>
                <div style="font-size: 16px; font-weight: 700; color: #06B6D4;">{predicted_usage:.1f} kWh</div>
            </div>
            <div>
                <div style="font-size: 11px; color: #94A3B8;">Efficiency</div>
                <div style="font-size: 16px; font-weight: 700; color: #22C55E;">{efficiency_score}%</div>
            </div>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allowed_html=True)
