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
# -----------------------------------------------------------------------------
# GROSS PREMIUM & PROFIT LOADING SCENARIOS (NEW SECTION)
# -----------------------------------------------------------------------------
st.markdown('<hr class="glass-divider">', unsafe_allow_html=True)
st.markdown('<div class="section-tag">Profitability Impact</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title" style="font-size:1.4rem; text-align:left;">Gross Premium &amp; Profit Loading Across Scenarios</div>', unsafe_allow_html=True)
st.markdown(
    "<p style='color:#6b7280; font-size:0.9rem; margin-bottom:20px;'>"
    "Extends the mortality improvement comparison to the Gross Premium and Profit Loading, "
    "using the default expense assumptions (2% initial expense, ₹500 renewal expense, "
    "2% contingency margin, 8% target profit margin).</p>",
    unsafe_allow_html=True
)

from actuarial.gross_premium_scenarios import get_gross_premium_scenarios_df

df_gp_compare = get_gross_premium_scenarios_df(
    age=inputs['age'],
    term=inputs['term'],
    sum_assured=inputs['sum_assured'],
    interest_rate_pct=inputs['interest_rate'],
    df_mort=df_mort,
)

gp_table_col, gp_chart_col = st.columns([3, 2])

with gp_table_col:
    df_gp_display = df_gp_compare.copy()
    df_gp_display['Net_Premium'] = df_gp_display['Net_Premium'].apply(lambda x: f"₹{x:,.2f}")
    df_gp_display['Gross_Premium'] = df_gp_display['Gross_Premium'].apply(lambda x: f"₹{x:,.2f}")
    df_gp_display['GP_Savings_Abs'] = df_gp_display['GP_Savings_Abs'].apply(lambda x: f"₹{x:,.2f}")
    df_gp_display['GP_Savings_Pct'] = df_gp_display['GP_Savings_Pct'].apply(lambda x: f"{x:.2f}%")
    df_gp_display['Profit_Loading'] = df_gp_display['Profit_Loading'].apply(lambda x: f"₹{x:,.2f}")
    df_gp_display['Profit_Change_Abs'] = df_gp_display['Profit_Change_Abs'].apply(lambda x: f"₹{x:,.2f}")
    df_gp_display['Profit_Change_Pct'] = df_gp_display['Profit_Change_Pct'].apply(lambda x: f"{x:.2f}%")
    df_gp_display = df_gp_display.drop(columns=['Improvement_Rate'])
    df_gp_display.columns = [
        "Scenario", "Net Premium", "Gross Premium", "GP Savings (Abs)",
        "GP Savings (%)", "Profit Loading", "Profit Δ (Abs)", "Profit Δ (%)"
    ]
    st.dataframe(df_gp_display, hide_index=True, width="stretch")

with gp_chart_col:
    import plotly.graph_objects as go

    fig_gp = go.Figure()
    fig_gp.add_trace(go.Bar(
        x=df_gp_compare["Scenario"],
        y=df_gp_compare["Gross_Premium"],
        name="Gross Premium",
        marker_color="#2dd4bf",
    ))
    fig_gp.add_trace(go.Bar(
        x=df_gp_compare["Scenario"],
        y=df_gp_compare["Profit_Loading"],
        name="Profit Loading",
        marker_color="#f59e0b",
    ))
    fig_gp.update_layout(
        barmode="group",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#eef2f4"),
        margin=dict(l=10, r=10, t=30, b=10),
        height=380,
        yaxis=dict(title="Amount (₹)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        title="Gross Premium &amp; Profit Loading by Scenario",
    )
    st.plotly_chart(fig_gp, width="stretch")

# Insight for gross premium scenarios
worst_gp_row = df_gp_compare.iloc[-1]
st.info(
    f"At {worst_gp_row['Scenario']} mortality improvement, Gross Premium changes by "
    f"₹{worst_gp_row['GP_Savings_Abs']:,.2f} ({worst_gp_row['GP_Savings_Pct']:.2f}%) and "
    f"Profit Loading changes by ₹{worst_gp_row['Profit_Change_Abs']:,.2f} "
    f"({worst_gp_row['Profit_Change_Pct']:.2f}%) relative to the 0% base case."
)