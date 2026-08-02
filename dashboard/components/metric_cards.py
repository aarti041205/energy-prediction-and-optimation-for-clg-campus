"""
SaaS Metric Card Component Generator with Micro Sparklines.
"""

import streamlit as st
import plotly.graph_objects as go

def _generate_sparkline(y_data, color="#22C55E"):
    """Creates a minimal dark sparkline SVG figure."""
    fig = go.Figure(data=go.Scatter(
        y=y_data,
        mode='lines',
        line=dict(color=color, width=2.5),
        hoverinfo='none'
    ))
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=32,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )
    return fig

def render_metric_card(title: str, value: str, trend: str, is_positive: bool = True, icon: str = "⚡", icon_bg: str = "rgba(59, 130, 246, 0.15)", icon_color: str = "#3B82F6", sparkline_data=None):
    """Renders a single premium SaaS Metric Card."""
    trend_class = "up" if is_positive else "down"
    arrow = "▲" if is_positive else "▼"
    if sparkline_data is None:
        sparkline_data = [10, 14, 12, 18, 22, 20, 26]

    card_html = f"""
    <div class="saas-card saas-metric-card">
        <div class="saas-metric-header">
            <div class="saas-icon-badge" style="background: {icon_bg}; color: {icon_color};">{icon}</div>
            <div class="saas-trend-badge {trend_class}">{arrow} {trend}</div>
        </div>
        <div class="saas-metric-title">{title}</div>
        <div class="saas-metric-value">{value}</div>
    </div>
    """
    # pyrefly: ignore [unexpected-keyword]
    st.markdown(card_html, unsafe_allowed_html=True)
    st.plotly_chart(_generate_sparkline(sparkline_data, "#22C55E" if is_positive else "#EF4444"), use_container_width=True, config={'displayModeBar': False})
