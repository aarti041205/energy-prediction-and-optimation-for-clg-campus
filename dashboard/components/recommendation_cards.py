"""
Optimization Strategy Recommendation Card Component.
"""

import streamlit as st

def render_recommendation_card(category: str, recommendation: str, energy_saving_pct: float, savings_kwh: float, savings_inr: float, carbon_reduction_kg: float, priority: str = "High"):
    """Renders a single Optimization Recommendation Strategy Card."""
    priority_color = "#EF4444" if priority == "High" else ("#F59E0B" if priority == "Medium" else "#3B82F6")
    card_html = f"""
    <div class="saas-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <div style="font-size: 16px; font-weight: 700; color: #F8FAFC;">💡 {category}</div>
            <div style="background: {priority_color}22; color: {priority_color}; border: 1px solid {priority_color}44; font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 20px;">
                {priority} Priority
            </div>
        </div>
        <div style="font-size: 13px; color: #CBD5E1; line-height: 1.5; margin-bottom: 14px;">{recommendation}</div>
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.08);">
            <div>
                <div style="font-size: 11px; color: #94A3B8;">Saving %</div>
                <div style="font-size: 15px; font-weight: 700; color: #22C55E;">{energy_saving_pct:.1f}%</div>
            </div>
            <div>
                <div style="font-size: 11px; color: #94A3B8;">kWh Reduced</div>
                <div style="font-size: 15px; font-weight: 700; color: #06B6D4;">{savings_kwh:.1f} kWh</div>
            </div>
            <div>
                <div style="font-size: 11px; color: #94A3B8;">Cost Saved</div>
                <div style="font-size: 15px; font-weight: 700; color: #F59E0B;">₹ {savings_inr:,.2f}</div>
            </div>
            <div>
                <div style="font-size: 11px; color: #94A3B8;">CO₂ Offset</div>
                <div style="font-size: 15px; font-weight: 700; color: #3B82F6;">{carbon_reduction_kg:.1f} kg</div>
            </div>
        </div>
    </div>
    """
    # pyrefly: ignore [unexpected-keyword]
    st.markdown(card_html, unsafe_allowed_html=True)
