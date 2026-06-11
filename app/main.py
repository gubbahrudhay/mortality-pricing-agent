import streamlit as st
import os
import sys

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & THEME
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Mortality Improvement Analyzer",
    page_icon="🧬",
    layout="wide"
)

# Custom premium styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    .hero-container {
        background: linear-gradient(135deg, #1e1e38 0%, #0f0f1b 100%);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 40px;
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.3);
        margin-bottom: 30px;
    }
    .hero-title {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 15px;
    }
    .hero-subtitle {
        font-size: 1.25rem;
        color: #94a3b8;
        margin-bottom: 25px;
        line-height: 1.6;
    }
    .feature-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 24px;
        transition: all 0.3s ease;
        height: 100%;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        border-color: #6366f1;
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.15);
    }
    .feature-icon {
        font-size: 2.2rem;
        margin-bottom: 15px;
    }
    .feature-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #f8fafc;
        margin-bottom: 10px;
    }
    .feature-text {
        font-size: 0.95rem;
        color: #94a3b8;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# HERO SECTION
# -----------------------------------------------------------------------------
st.markdown("""
<div class="hero-container">
    <div class="hero-title">📊 Mortality Improvement Pricing & Sensitivity Analyzer</div>
    <div class="hero-subtitle">
        An advanced, modular actuarial pricing suite integrated with an AI Consultant. This system simulates Net Single 
        and Net Level Annual premiums, computes survival probability matrices, models sensitivity to economic and mortality shocks, 
        and provides natural language explanations.
    </div>
    <p style="color: #64748b; font-size: 0.9rem;">
        👈 <b>Get Started:</b> Use the sidebar on the left to navigate through the calculator, scenario dashboards, or the conversational AI assistant.
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PAGES OVERVIEW
# -----------------------------------------------------------------------------
st.subheader("💡 Application Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🛡️</div>
        <div class="feature-title">Pricing Calculator</div>
        <div class="feature-text">
            Compute Net Single Premiums (NSP) and Net Level Annual Premiums (LAP) dynamically for Term Life and Whole Life products. 
            Interactive Plotly charts render survival probabilities (tpx) and comparative mortality rates (qx).
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📈</div>
        <div class="feature-title">Scenario & Sensitivity Analysis</div>
        <div class="feature-text">
            Evaluate premium reactions to mortality improvement scenarios (0%, 0.5%, 1%, 2%). Simulate sensitivity 
            under discount rate fluctuations and custom mortality shocks, generating risk elasticities.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">💬</div>
        <div class="feature-title">AI Actuarial Assistant</div>
        <div class="feature-text">
            Chat with a conversational agent integrated with Gemini and LangChain. The agent utilizes custom actuarial 
            tools to calculate premiums, run scenarios, perform sensitivity analyses, and compile formal reports.
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TEAM ALLOCATION & ARCHITECTURE
# -----------------------------------------------------------------------------
st.markdown("---")
arch_col, team_col = st.columns([3, 2])

with arch_col:
    st.subheader("⚙️ System Architecture")
    st.markdown("""
    This project is built using a clean, decoupled modular directory structure:
    - **`data/`**: Structured raw inputs (mortality tables) and processed outputs.
    - **`actuarial/`**: Encapsulates core life table mathematics, pricing formulas, and scenario algorithms.
    - **`analytics/`**: Runs sensitivity matrices, risk elasticity analyses, and builds plotly charts.
    - **`tools/`**: Implements custom LangChain tools that bind the actuarial logic directly to the LLM agent.
    - **`agents/`**: Configures the ChatGoogleGenerativeAI (Gemini) agent, conversational memory, and routing.
    - **`app/`**: Builds the premium user interface using multi-page Streamlit dashboards.
    """)

with team_col:
    st.subheader("👥 Project Team")
    st.markdown("""
    - **AI Assistant / Agent (You)**: Handles conversational AI, tool calling, and report generation.
    - **Teammate 2 (Actuarial)**: Designed life table formulas, compound improvement projections, and premium calculations.
    - **Teammate 3 (Analytics)**: Engineered sensitivity engines, Plotly visualizations, and data-driven insights.
    """)
