"""
Streamlit Page: Scenario Analysis
"""

import streamlit as st
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import config
from actuarial.mortality import load_raw_table
from actuarial.scenarios import get_scenarios_comparison_df
from analytics.sensitivity_analysis import analyze_interest_rate_sensitivity, analyze_mortality_shock_sensitivity
from app.components.inputs import render_sidebar_inputs
from app.components.charts import render_scenario_comparison, render_interest_sensitivity, render_mortality_shock_sensitivity
from app.components.tables import render_scenario_table
from analytics.insights import generate_sensitivity_insights
from app.theme import inject_theme

st.set_page_config(page_title="Scenario & Sensitivity Analysis", page_icon="📈", layout="wide")
inject_theme()

df_mort = load_raw_table()
inputs = render_sidebar_inputs()

# -----------------------------------------------------------------------------
# HEADER
# -----------------------------------------------------------------------------
st.markdown("""
<div class="hero-dark" style="padding: 40px 50px;">
    <div class="hero-dark-content">
        <div class="hero-dark-title" style="font-size: 1.7rem;">📈 Scenario &amp; Sensitivity Analysis Dashboard</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    "<p style='color:#6b7280; font-size:0.95rem; margin-top:18px;'>"
    "Compare premium rates under multiple mortality improvement scenarios and evaluate policy "
    "sensitivity to economic and underwriting risk factors.</p>",
    unsafe_allow_html=True
)

st.markdown('<hr class="glass-divider">', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SCENARIO COMPARISON SECTION
# -----------------------------------------------------------------------------
st.markdown('<div class="section-tag">Scenario Comparison</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title" style="font-size:1.4rem; text-align:left;">Mortality Improvement Scenarios</div>', unsafe_allow_html=True)
st.markdown(
    "<p style='color:#6b7280; font-size:0.9rem; margin-bottom:20px;'>"
    "Evaluates premium rates and cumulative savings across baseline and improved mortality models.</p>",
    unsafe_allow_html=True
)

df_compare = get_scenarios_comparison_df(
    age=inputs['age'],
    term=inputs['term'],
    sum_assured=inputs['sum_assured'],
    interest_rate_pct=inputs['interest_rate'],
    df_mort=df_mort
)

col1, col2 = st.columns([3, 2])

with col1:
    render_scenario_table(df_compare)

with col2:
    render_scenario_comparison(df_compare)

# -----------------------------------------------------------------------------
# SENSITIVITY ANALYSIS SECTION
# -----------------------------------------------------------------------------
st.markdown('<hr class="glass-divider">', unsafe_allow_html=True)
st.markdown('<div class="section-tag">Risk Elasticity</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title" style="font-size:1.4rem; text-align:left;">Sensitivity &amp; Risk Elasticity Curves</div>', unsafe_allow_html=True)
st.markdown(
    "<p style='color:#6b7280; font-size:0.9rem; margin-bottom:20px;'>"
    "Model how premiums react to shifts in interest rates (macroeconomic variable) and mortality "
    "shocks (underwriting risk variable).</p>",
    unsafe_allow_html=True
)

int_sensitivity = analyze_interest_rate_sensitivity(
    age=inputs['age'],
    term=inputs['term'],
    sum_assured=inputs['sum_assured'],
    improvement_rate=inputs['improvement_rate'],
    df_mort=df_mort
)

shock_sensitivity = analyze_mortality_shock_sensitivity(
    age=inputs['age'],
    term=inputs['term'],
    sum_assured=inputs['sum_assured'],
    interest_rate_pct=inputs['interest_rate'],
    df_mort=df_mort
)

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    render_interest_sensitivity(int_sensitivity)

with chart_col2:
    render_mortality_shock_sensitivity(shock_sensitivity)

# -----------------------------------------------------------------------------
# INSIGHTS
# -----------------------------------------------------------------------------
st.markdown('<hr class="glass-divider">', unsafe_allow_html=True)
st.markdown('<div class="glass-label">Premium Elasticity Insights</div>', unsafe_allow_html=True)
st.write("")

insights = generate_sensitivity_insights(int_sensitivity, shock_sensitivity)
for insight in insights:
    st.info(insight)