"""
Modern Dark Theme UI Component Generator for Streamlit Dashboard.
Replicates high-end dark operations dashboard aesthetic with custom CSS, KPI metric cards, trend sparklines, and activity feeds.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def inject_custom_theme():
    """Injects dark operations dashboard CSS styling into Streamlit."""
    st.markdown(
        """
        <style>
        /* Import Outfit / Inter Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* Main App Background */
        .stApp {
            background-color: #0B0E14;
            color: #E2E8F0;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #121621 !important;
            border-right: 1px solid #1E2638 !important;
        }

        /* Sidebar Section Titles */
        .sidebar-section-header {
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1.2px;
            color: #64748B;
            text-transform: uppercase;
            margin-top: 20px;
            margin-bottom: 8px;
        }

        /* Top Header */
        .main-header-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 24px;
        }
        .main-title {
            font-size: 28px;
            font-weight: 700;
            color: #F8FAFC;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .live-badge {
            background: rgba(16, 185, 129, 0.15);
            color: #10B981;
            border: 1px solid rgba(16, 185, 129, 0.3);
            font-size: 12px;
            font-weight: 600;
            padding: 3px 10px;
            border-radius: 20px;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }
        .live-dot {
            width: 7px;
            height: 7px;
            background-color: #10B981;
            border-radius: 50%;
            box-shadow: 0 0 8px #10B981;
        }
        .header-subtext {
            color: #94A3B8;
            font-size: 14px;
            margin-top: 4px;
        }

        /* Custom Cards */
        .ops-card {
            background: #161B26;
            border: 1px solid #232D3F;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 16px;
            transition: all 0.2s ease-in-out;
        }
        .ops-card:hover {
            border-color: #334155;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }

        /* KPI Card Details */
        .kpi-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }
        .kpi-icon-box {
            width: 38px;
            height: 38px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
        }
        .kpi-trend {
            font-size: 12px;
            font-weight: 600;
            padding: 3px 8px;
            border-radius: 6px;
            display: flex;
            align-items: center;
            gap: 4px;
        }
        .trend-up {
            background: rgba(16, 185, 129, 0.15);
            color: #10B981;
        }
        .trend-down {
            background: rgba(244, 63, 94, 0.15);
            color: #F43F5E;
        }
        .kpi-title {
            font-size: 12px;
            font-weight: 600;
            color: #94A3B8;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }
        .kpi-value {
            font-size: 26px;
            font-weight: 700;
            color: #F8FAFC;
            margin-top: 4px;
            margin-bottom: 8px;
        }

        /* Activity Items */
        .activity-item {
            display: flex;
            align-items: flex-start;
            gap: 14px;
            padding: 12px 0;
            border-bottom: 1px solid #1E2638;
        }
        .activity-item:last-child {
            border-bottom: none;
        }
        .activity-icon {
            width: 36px;
            height: 36px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            flex-shrink: 0;
        }
        .activity-content {
            flex-grow: 1;
        }
        .activity-title {
            font-size: 14px;
            font-weight: 600;
            color: #F1F5F9;
        }
        .activity-desc {
            font-size: 12px;
            color: #94A3B8;
            margin-top: 2px;
        }
        .activity-time {
            font-size: 12px;
            color: #64748B;
            white-space: nowrap;
        }

        /* Progress Bar Item */
        .progress-stat {
            margin-bottom: 16px;
        }
        .progress-header {
            display: flex;
            justify-content: space-between;
            font-size: 13px;
            font-weight: 500;
            color: #CBD5E1;
            margin-bottom: 6px;
        }
        .progress-bar-bg {
            height: 8px;
            background: #1E2638;
            border-radius: 4px;
            overflow: hidden;
        }
        .progress-bar-fill {
            height: 100%;
            border-radius: 4px;
        }

        /* Hide Streamlit Default Headers */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header[data-testid="stHeader"] {background-color: transparent;}
        </style>
        """,
        unsafe_allowed_html=True
    )

def render_sparkline(y_values, color="#10B981"):
    """Generates a minimalistic dark sparkline SVG/Plotly figure."""
    fig = go.Figure(data=go.Scatter(
        y=y_values,
        mode='lines',
        line=dict(color=color, width=2.5),
        hoverinfo='none'
    ))
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=35,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )
    return fig

def render_header(title="Dashboard", subtitle="Campus Energy Operations Baseline"):
    """Renders the top dark header with Live Status badge."""
    st.markdown(
        f"""
        <div class="main-header-container">
            <div>
                <div class="main-title">
                    {title}
                    <span class="live-badge"><span class="live-dot"></span> Live System</span>
                </div>
                <div class="header-subtext">{subtitle}</div>
            </div>
        </div>
        """,
        unsafe_allowed_html=True
    )

def render_kpi_card(title, value, trend_text, is_positive=True, icon="⚡", icon_bg="rgba(245, 158, 11, 0.15)", icon_color="#F59E0B", spark_values=[10, 15, 12, 18, 24, 20, 28]):
    """Renders a single KPI Card matching the Northwind Ops style."""
    trend_class = "trend-up" if is_positive else "trend-down"
    arrow = "▲" if is_positive else "▼"

    card_html = f"""
    <div class="ops-card">
        <div class="kpi-header">
            <div class="kpi-icon-box" style="background: {icon_bg}; color: {icon_color};">{icon}</div>
            <div class="kpi-trend {trend_class}">{arrow} {trend_text}</div>
        </div>
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """
    st.markdown(card_html, unsafe_allowed_html=True)
    st.plotly_chart(render_sparkline(spark_values, "#10B981" if is_positive else "#F43F5E"), use_container_width=True, config={'displayModeBar': False})
