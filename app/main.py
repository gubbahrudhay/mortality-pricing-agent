"""
Streamlit Main Page

Landing page for the Mortality Pricing Suite — QDT-inspired.
"""

import streamlit as st
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.theme import inject_theme

st.set_page_config(
    page_title="Mortality Improvement Analyzer",
    page_icon="🧬",
    layout="wide"
)

inject_theme()

# -----------------------------------------------------------------------------
# DARK HALFTONE HERO
# -----------------------------------------------------------------------------
st.markdown("""
<div class="hero-dark">
    <div class="hero-dark-content">
        <div class="hero-dark-title">Mortality Improvement Pricing &amp; Sensitivity Analyzer</div>
        <div class="hero-dark-sub">Actuarial pricing, powered by AI</div>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# LIGHT INTRO BAND
# -----------------------------------------------------------------------------
st.markdown("""
<div class="hero-light">
    <div class="hero-light-title">An advanced, modular actuarial pricing suite integrated with an AI consultant</div>
    <div class="hero-light-desc">
        Simulate Net Single and Net Level Annual premiums, compute survival probability matrices,
        model sensitivity to economic and mortality shocks, and get natural-language explanations
        for every result.
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# FEATURE CARDS
# -----------------------------------------------------------------------------
st.markdown('<div class="section-tag">Application Features</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Explore the pricing, scenario, and AI assistant tools</div>', unsafe_allow_html=True)

st.write("")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.page_link(
        "pages/1_Net_Premium_Pricing.py",
        label="**Net Premium Pricing**\n\nCompute Net Single Premiums (NSP) and Net Level Annual Premiums (LAP) for Term Life and Whole Life products, with interactive survival and mortality charts."
    )

with col2:
    st.page_link(
        "pages/2_Scenario_Analysis.py",
        label="**Scenario & Sensitivity**\n\nEvaluate premium reactions to mortality improvement scenarios and simulate sensitivity under discount rate and mortality shocks."
    )

with col3:
    st.page_link(
        "pages/3_AI_Assistant.py",
        label="**AI Actuarial Assistant**\n\nChat with a conversational agent that calculates premiums, runs scenarios, performs sensitivity analyses, and compiles formal reports."
    )

with col4:
    st.page_link(
        "pages/4_Gross_Premium_Pricing.py",
        label="**Gross Premium Pricing**\n\nCalculate Gross Premium and Profit Loading with expense assumptions, and see how mortality improvement impacts profitability."
    )

with col5:
    st.page_link(
        "pages/5_Reserving.py",
        label="**Reserving**\n\nCompute the Prospective Gross Premium Reserve at any policy duration, and visualize the reserve build-up and run-off curve."
    )

# -----------------------------------------------------------------------------
# ARCHITECTURE & TEAM
# -----------------------------------------------------------------------------
st.markdown('<hr class="glass-divider">', unsafe_allow_html=True)
arch_col, team_col = st.columns([3, 2])

with arch_col:
    st.markdown('<div class="glass-label">System Architecture</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="arch-block">
    <p style="font-size:0.95rem; line-height:1.9; margin-top:12px;">
    <code>data/</code> &mdash; structured raw inputs (mortality tables) and processed outputs.<br>
    <code>actuarial/</code> &mdash; core life table mathematics, pricing formulas, and scenario algorithms.<br>
    <code>analytics/</code> &mdash; sensitivity matrices, risk elasticity analyses, and chart builders.<br>
    <code>tools/</code> &mdash; custom LangChain tools binding actuarial logic to the LLM agent.<br>
    <code>agents/</code> &mdash; Gemini agent configuration, conversational memory, and routing.<br>
    <code>app/</code> &mdash; multi-page Streamlit UI.
    </p>
    </div>
    """, unsafe_allow_html=True)

with team_col:
    st.markdown('<div class="glass-label">Project Team</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="team-block">
    <p style="font-size:0.95rem; line-height:1.9; margin-top:12px;">
    <strong>AI Assistant / Agent</strong> &mdash; conversational AI, tool calling, and report generation.<br><br>
    <strong>Teammate 2 (Actuarial)</strong> &mdash; life table formulas, compound improvement projections, premium calculations.<br><br>
    <strong>Teammate 3 (Analytics)</strong> &mdash; sensitivity engines, visualizations, data-driven insights.
    </p>
    </div>
    """, unsafe_allow_html=True)