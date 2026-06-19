"""
Streamlit Page: Gross Premium & Profit Loading Agent

This page computes Gross Premium and Profit Loading for both Term Life and
Whole Life policies side-by-side, and shows how mortality improvement
affects both, using the IALM 2012-14 mortality table.
"""

import streamlit as st
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import config
from actuarial.mortality import load_raw_table
from actuarial.gross_premium import calculate_gross_premium
from analytics.gross_premium_sensitivity import analyze_gross_premium_mortality_sensitivity
from actuarial.utils import format_currency
from app.theme import inject_theme, metric_card

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Gross Premium & Profit Loading",
    page_icon="💰",
    layout="wide"
)

inject_theme()

df_mort = load_raw_table()

# -----------------------------------------------------------------------------
# SIDEBAR INPUTS (shared across Term and Whole Life)
# -----------------------------------------------------------------------------
st.sidebar.title("💰 Gross Premium Inputs")

age = st.sidebar.slider("Entry Age (x)", min_value=int(config.MIN_AGE), max_value=int(config.MAX_AGE - 5), value=40)
term = st.sidebar.slider("Policy Term (n) — Term Life only", min_value=1, max_value=int(config.MAX_AGE - age), value=10)
sum_assured = st.sidebar.number_input("Sum Assured (₹)", min_value=10000, max_value=100000000, value=1000000, step=50000)
interest_rate = st.sidebar.slider("Discount Rate (%)", min_value=0.5, max_value=15.0, value=4.0, step=0.25)

st.sidebar.markdown("#### Expense & Margin Assumptions")
initial_expense_pct = st.sidebar.slider("Initial Expense (% of SA)", min_value=0.0, max_value=10.0, value=2.0, step=0.5) / 100
renewal_expense = st.sidebar.number_input("Renewal Expense (₹/yr)", min_value=0, max_value=10000, value=500, step=50)
contingency_pct = st.sidebar.slider("Contingency Margin (%)", min_value=0.0, max_value=10.0, value=2.0, step=0.5) / 100
profit_margin_pct = st.sidebar.slider("Target Profit Margin (%)", min_value=0.0, max_value=20.0, value=8.0, step=0.5) / 100

improvement_rate = st.sidebar.selectbox(
    "Mortality Improvement Rate (base case)",
    options=[0.0, 0.005, 0.01, 0.015],
    format_func=lambda x: f"{x:.1%}"
)

# -----------------------------------------------------------------------------
# COMPUTATION — both product types
# -----------------------------------------------------------------------------
res_term = calculate_gross_premium(
    age=age, term=term, sum_assured=sum_assured,
    interest_rate_pct=interest_rate, improvement_rate=improvement_rate, df_mort=df_mort,
    initial_expense_pct=initial_expense_pct, renewal_expense=renewal_expense,
    contingency_pct=contingency_pct, profit_margin_pct=profit_margin_pct,
    product_type="term",
)

res_whole = calculate_gross_premium(
    age=age, term=term, sum_assured=sum_assured,
    interest_rate_pct=interest_rate, improvement_rate=improvement_rate, df_mort=df_mort,
    initial_expense_pct=initial_expense_pct, renewal_expense=renewal_expense,
    contingency_pct=contingency_pct, profit_margin_pct=profit_margin_pct,
    product_type="whole",
)

# -----------------------------------------------------------------------------
# HEADER
# -----------------------------------------------------------------------------
st.markdown("""
<div class="hero-dark" style="padding: 40px 50px;">
    <div class="hero-dark-content">
        <div class="hero-dark-title" style="font-size: 1.7rem;">💰 Gross Premium &amp; Profit Loading Agent</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    f"<p style='color:#9fb2bb; font-size:0.95rem; margin-top:18px;'>"
    f"Computing Gross Premium for a <strong>{age}-year-old</strong> with "
    f"<strong>{format_currency(sum_assured)}</strong> sum assured, at a "
    f"<strong>{improvement_rate:.1%}</strong> mortality improvement rate — "
    f"Term Life ({term}-year term) and Whole Life shown side-by-side.</p>",
    unsafe_allow_html=True
)

st.markdown('<hr class="glass-divider">', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# METRIC CARDS — TERM LIFE
# -----------------------------------------------------------------------------
st.markdown(f'<div class="glass-label">🛡️ Term Life Insurance ({term}-Year Term)</div>', unsafe_allow_html=True)
st.write("")

col1, col2, col3 = st.columns(3)

with col1:
    metric_card(
        label="Net Premium",
        value=format_currency(res_term['net_premium']),
        sub=f"NSP: {format_currency(res_term['nsp_term'])}",
        color="dark"
    )

with col2:
    metric_card(
        label="Gross Premium",
        value=format_currency(res_term['gross_premium']),
        sub=f"Loaded Premium: {format_currency(res_term['loaded_premium'])}",
        color="teal"
    )

with col3:
    metric_card(
        label="Profit Loading",
        value=format_currency(res_term['profit_loading']),
        sub=f"{res_term['profit_loading_pct_of_np']:.2%} of Net Premium",
        color="amber"
    )

st.write("")

# -----------------------------------------------------------------------------
# METRIC CARDS — WHOLE LIFE
# -----------------------------------------------------------------------------
st.markdown('<div class="glass-label">♾️ Whole Life Insurance</div>', unsafe_allow_html=True)
st.write("")

col4, col5, col6 = st.columns(3)

with col4:
    metric_card(
        label="Net Premium",
        value=format_currency(res_whole['net_premium']),
        sub=f"NSP: {format_currency(res_whole['nsp_term'])}",
        color="dark"
    )

with col5:
    metric_card(
        label="Gross Premium",
        value=format_currency(res_whole['gross_premium']),
        sub=f"Loaded Premium: {format_currency(res_whole['loaded_premium'])}",
        color="teal"
    )

with col6:
    metric_card(
        label="Profit Loading",
        value=format_currency(res_whole['profit_loading']),
        sub=f"{res_whole['profit_loading_pct_of_np']:.2%} of Net Premium",
        color="amber"
    )

st.write("")

# -----------------------------------------------------------------------------
# EXPENSE BREAKDOWN — SIDE BY SIDE
# -----------------------------------------------------------------------------
st.markdown('<hr class="glass-divider">', unsafe_allow_html=True)
st.markdown('<div class="glass-label">Premium Build-Up</div>', unsafe_allow_html=True)

import pandas as pd

breakdown_col1, breakdown_col2 = st.columns(2)

with breakdown_col1:
    st.markdown(f"**Term Life ({term}-Year Term)**")
    rows_term = [
        ("Net Premium (NP)", res_term['net_premium']),
        ("Initial Expense (per yr)", res_term['initial_expense_per_year']),
        ("Renewal Expense (per yr)", res_term['renewal_expense']),
        ("Loaded Premium", res_term['loaded_premium']),
        ("Gross Premium (GP)", res_term['gross_premium']),
        ("Profit Loading", res_term['profit_loading']),
    ]
    df_term = pd.DataFrame(rows_term, columns=["Component", "Amount (₹)"])
    df_term["Amount (₹)"] = df_term["Amount (₹)"].apply(lambda x: f"₹{x:,.2f}")
    st.dataframe(df_term, hide_index=True, width="stretch")

with breakdown_col2:
    st.markdown("**Whole Life**")
    rows_whole = [
        ("Net Premium (NP)", res_whole['net_premium']),
        ("Initial Expense (per yr)", res_whole['initial_expense_per_year']),
        ("Renewal Expense (per yr)", res_whole['renewal_expense']),
        ("Loaded Premium", res_whole['loaded_premium']),
        ("Gross Premium (GP)", res_whole['gross_premium']),
        ("Profit Loading", res_whole['profit_loading']),
    ]
    df_whole = pd.DataFrame(rows_whole, columns=["Component", "Amount (₹)"])
    df_whole["Amount (₹)"] = df_whole["Amount (₹)"].apply(lambda x: f"₹{x:,.2f}")
    st.dataframe(df_whole, hide_index=True, width="stretch")

# -----------------------------------------------------------------------------
# MORTALITY IMPROVEMENT SENSITIVITY — TERM LIFE
# -----------------------------------------------------------------------------
st.markdown('<hr class="glass-divider">', unsafe_allow_html=True)
st.markdown('<div class="section-tag">Risk Sensitivity</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title" style="font-size:1.4rem; text-align:left;">Impact of Mortality Improvement on Gross Premium &amp; Profit Loading</div>', unsafe_allow_html=True)
st.markdown(
    "<p style='color:#9fb2bb; font-size:0.9rem; margin-bottom:20px;'>"
    "Compares Gross Premium and Profit Loading at 0%, 0.5%, 1%, and 1.5% compound mortality improvement rates.</p>",
    unsafe_allow_html=True
)

tab_term, tab_whole = st.tabs(["🛡️ Term Life", "♾️ Whole Life"])

import plotly.graph_objects as go

def render_sensitivity_tab(df_sensitivity):
    col_table, col_chart = st.columns([3, 2])

    with col_table:
        st.dataframe(df_sensitivity, hide_index=True, width="stretch")

    with col_chart:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_sensitivity["Improvement Rate"],
            y=df_sensitivity["Gross Premium"],
            mode="lines+markers",
            name="Gross Premium",
            line=dict(color="#2dd4bf", width=3),
        ))
        fig.add_trace(go.Scatter(
            x=df_sensitivity["Improvement Rate"],
            y=df_sensitivity["Profit Loading ($)"],
            mode="lines+markers",
            name="Profit Loading",
            line=dict(color="#f59e0b", width=3),
            yaxis="y2",
        ))
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#eef2f4"),
            margin=dict(l=10, r=10, t=30, b=10),
            height=380,
            yaxis=dict(title="Gross Premium (₹)"),
            yaxis2=dict(title="Profit Loading (₹)", overlaying="y", side="right"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(fig, width="stretch")

    base_row = df_sensitivity.iloc[0]
    worst_row = df_sensitivity.iloc[-1]
    st.info(
        f"At {worst_row['Improvement Rate']} mortality improvement, Gross Premium changes by "
        f"{worst_row['Gross Premium Δ vs Base']} and Profit Loading changes by "
        f"{worst_row['Profit Loading Δ vs Base']} relative to the 0% base case."
    )

with tab_term:
    df_sensitivity_term = analyze_gross_premium_mortality_sensitivity(
        age=age, term=term, sum_assured=sum_assured, interest_rate_pct=interest_rate,
        df_mort=df_mort, initial_expense_pct=initial_expense_pct,
        renewal_expense=renewal_expense, contingency_pct=contingency_pct,
        profit_margin_pct=profit_margin_pct, product_type="term",
    )
    render_sensitivity_tab(df_sensitivity_term)

with tab_whole:
    df_sensitivity_whole = analyze_gross_premium_mortality_sensitivity(
        age=age, term=term, sum_assured=sum_assured, interest_rate_pct=interest_rate,
        df_mort=df_mort, initial_expense_pct=initial_expense_pct,
        renewal_expense=renewal_expense, contingency_pct=contingency_pct,
        profit_margin_pct=profit_margin_pct, product_type="whole",
    )
    render_sensitivity_tab(df_sensitivity_whole)