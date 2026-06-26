"""
Streamlit Theme Helper Component

This module manages theme configuration (Light / Dark) for the application,
providing consistent styles and styling hooks across all pages.
"""

import streamlit as st

def setup_theme():
    """
    Initializes the theme in session state, renders a sidebar theme toggle,
    and injects CSS rules matching the active theme.
    """
    if "theme" not in st.session_state:
        st.session_state.theme = "Light"

    theme_options = ["Light", "Dark"]
    current_index = theme_options.index(st.session_state.theme)

    st.sidebar.markdown("---")
    
    # Callback to update state cleanly on user interaction
    def handle_theme_selection():
        st.session_state.theme = st.session_state.theme_selector_widget

    selected_theme = st.sidebar.selectbox(
        "🎨 App Theme",
        options=theme_options,
        index=current_index,
        key="theme_selector_widget",
        on_change=handle_theme_selection
    )

    # Injecting clean and responsive styling based on selected theme
    if st.session_state.theme == "Light":
        st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
            html, body, [class*="css"] {
                font-family: 'Outfit', sans-serif;
            }
            [data-testid="stAppViewContainer"] {
                background-color: #ffffff !important;
            }
            [data-testid="stSidebar"] {
                background-color: #f8fafc !important;
                border-right: 1px solid #e2e8f0;
            }
            .stMarkdown p, .stMarkdown li, .stMarkdown ul, .stMarkdown ol, h1, h2, h3, h4, h5, h6, [data-testid="stHeader"] {
                color: #0f172a !important;
            }
            .stMarkdown a {
                color: #4f46e5 !important;
            }
            [data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
                color: #334155 !important;
            }
            hr {
                border-color: rgba(0, 0, 0, 0.08) !important;
            }
            .hero-container {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 30px;
                margin-bottom: 25px;
                box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
            }
            .hero-title {
                font-size: 2.2rem;
                font-weight: 700;
                color: #1e1b4b !important;
                margin-bottom: 10px;
            }
            .hero-subtitle {
                font-size: 1.1rem;
                color: #475569 !important;
                margin-bottom: 15px;
                line-height: 1.6;
            }
            .feature-card {
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                padding: 20px;
                height: 100%;
                box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .feature-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
                border-color: #6366f1;
            }
            .feature-icon {
                font-size: 2rem;
                margin-bottom: 10px;
            }
            .feature-title {
                font-size: 1.1rem;
                font-weight: 600;
                color: #0f172a !important;
                margin-bottom: 8px;
            }
            .feature-text {
                font-size: 0.9rem;
                color: #475569 !important;
                line-height: 1.5;
            }
            .premium-card {
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
                margin-bottom: 20px;
            }
            .card-title {
                font-size: 0.9rem;
                color: #475569 !important;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin-bottom: 8px;
                font-weight: 600;
            }
            .card-value {
                font-size: 1.8rem;
                font-weight: 700;
                color: #4f46e5 !important;
                margin-bottom: 4px;
            }
            .card-subtext {
                font-size: 0.85rem;
                color: #64748b !important;
            }
            .card-unit {
                font-size: 1rem;
                font-weight: normal;
                color: #64748b !important;
            }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
            html, body, [class*="css"] {
                font-family: 'Outfit', sans-serif;
            }
            [data-testid="stAppViewContainer"] {
                background-color: #0f172a !important;
            }
            [data-testid="stSidebar"] {
                background-color: #0b0f19 !important;
                border-right: 1px solid #1e293b;
            }
            .stMarkdown p, .stMarkdown li, .stMarkdown ul, .stMarkdown ol, h1, h2, h3, h4, h5, h6, [data-testid="stHeader"] {
                color: #f8fafc !important;
            }
            .stMarkdown a {
                color: #818cf8 !important;
            }
            [data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
                color: #e2e8f0 !important;
            }
            hr {
                border-color: rgba(255, 255, 255, 0.08) !important;
            }
            .hero-container {
                background: #0f172a;
                border: 1px solid #1e293b;
                border-radius: 12px;
                padding: 30px;
                margin-bottom: 25px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
            }
            .hero-title {
                font-size: 2.2rem;
                font-weight: 700;
                color: #f8fafc !important;
                margin-bottom: 10px;
            }
            .hero-subtitle {
                font-size: 1.1rem;
                color: #94a3b8 !important;
                margin-bottom: 15px;
                line-height: 1.6;
            }
            .feature-card {
                background: #1e293b;
                border: 1px solid #334155;
                border-radius: 10px;
                padding: 20px;
                height: 100%;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .feature-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 10px -1px rgba(0, 0, 0, 0.3);
                border-color: #818cf8;
            }
            .feature-icon {
                font-size: 2rem;
                margin-bottom: 10px;
            }
            .feature-title {
                font-size: 1.1rem;
                font-weight: 600;
                color: #f8fafc !important;
                margin-bottom: 8px;
            }
            .feature-text {
                font-size: 0.9rem;
                color: #94a3b8 !important;
                line-height: 1.5;
            }
            .premium-card {
                background: #1e293b;
                border: 1px solid #334155;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
                margin-bottom: 20px;
            }
            .card-title {
                font-size: 0.9rem;
                color: #94a3b8 !important;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin-bottom: 8px;
                font-weight: 600;
            }
            .card-value {
                font-size: 1.8rem;
                font-weight: 700;
                color: #818cf8 !important;
                margin-bottom: 4px;
            }
            .card-subtext {
                font-size: 0.85rem;
                color: #94a3b8 !important;
            }
            .card-unit {
                font-size: 1rem;
                font-weight: normal;
                color: #94a3b8 !important;
            }
        </style>
        """, unsafe_allow_html=True)

    return st.session_state.theme
