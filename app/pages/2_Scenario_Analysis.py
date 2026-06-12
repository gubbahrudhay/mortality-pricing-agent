"""
Streamlit Page: Scenario Analysis

This page evaluates scenario comparisons and plots sensitivity curves for discount rates and mortality shocks.
"""

import streamlit as st
import os
import sys

# Add parent directory to path to support config/pricing imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import config
from actuarial.mortality import load_raw_table
from actuarial.scenarios import get_scenarios_comparison_df
from analytics.sensitivity_analysis import analyze_interest_rate_sensitivity, analyze_mortality_shock_sensitivity
from app.components.inputs import render_sidebar_inputs
from app.components.charts import render_scenario_comparison, render_interest_sensitivity, render_mortality_shock_sensitivity
from app.components.tables import render_scenario_table
from analytics.insights import generate_sensitivity_insights

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Scenario & Sensitivity Analysis",
    page_icon="📈",
    layout="wide"
)

# Load raw mortality table
df_mort = load_raw_table()

# Render inputs in sidebar
inputs = render_sidebar_inputs()

st.title("📈 Scenario & Sensitivity Analysis Dashboard")
st.markdown("Compare premium rates under multiple mortality improvement scenarios and evaluate policy sensitivity to economic and underwriting risk factors.")

st.markdown("---")

# -----------------------------------------------------------------------------
# SCENARIO COMPARISON SECTION
# -----------------------------------------------------------------------------
st.subheader("🧬 Mortality Improvement Scenarios")
st.markdown("Evaluates premium rates and cumulative savings across baseline and improved mortality models.")

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
st.markdown("---")
st.subheader("⚡ Sensitivity & Risk Elasticity Curves")
st.markdown("Model how premiums react to shifts in interest rates (macroeconomic variable) and mortality shocks (underwriting risk variable).")

# Perform analyses
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

# Display Analytics Insights
st.subheader("💡 Premium Elasticity Insights")
insights = generate_sensitivity_insights(int_sensitivity, shock_sensitivity)

for insight in insights:
    st.info(insight)
