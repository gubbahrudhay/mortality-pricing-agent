"""
Streamlit Page: Reserving

This page computes the Prospective Gross Premium Reserve for a Term Life
policy at every duration, visualizing the classic reserve build-up and
run-off curve.
"""

import streamlit as st
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import config
import pandas as pd
import plotly.graph_objects as go

from actuarial.mortality import load_raw_table
from actuarial.reserving import calculate_reserve_schedule
from actuarial.utils import format_currency
from app.theme import inject_theme, metric_card

st.set_page_config(page_title="Reserving", page_icon="🏦", layout="wide")
inject_theme()

df_mort = load_raw_table()

# -----------------------------------------------------------------------------
# SIDEBAR INPUTS
# -----------------------------------------------------------------------------
st.sidebar.title("🏦 Reserving Inputs")

age = st.sidebar.slider("Entry Age (x)", min_value=int(config.MIN_AGE), max_value=int(config.MAX_AGE - 5), value=40)
term = st.sidebar.slider("Policy Term (n)", min_value=1, max_value=int(config.MAX_AGE - age), value=30)
sum_assured = st.sidebar.number_input("Sum Assured (₹)", min_value=10000, max_value=100000000, value=1000000, step=50000)
interest_rate = st.sidebar.slider("Discount Rate (%)", min_value=0.5, max_value=15.0, value=6.0, step=0.25)

st.sidebar.markdown("#### Expense Assumptions")
st.sidebar.caption("Note: reserving uses % of PREMIUM (not % of Sum Assured).")
initial_expense_pct = st.sidebar.slider("Initial Expense (% of 1st yr premium)", min_value=0.0, max_value=100.0, value=50.0, step=5.0) / 100
renewal_expense_pct = st.sidebar.slider("Renewal Expense (% of premium)", min_value=0.0, max_value=20.0, value=5.0, step=0.5) / 100
fixed_fee = st.sidebar.number_input("Fixed Annual Fee (₹/yr)", min_value=0, max_value=10000, value=500, step=50)

improvement_rate = st.sidebar.selectbox(
    "Mortality Improvement Rate",
    options=[0.0, 0.005, 0.01, 0.015],
    format_func=lambda x: f"{x:.1%}"
)

duration_to_inspect = st.sidebar.slider("Inspect Duration (t)", min_value=0, max_value=term, value=min(10, term))

# -----------------------------------------------------------------------------
# COMPUTATION
# -----------------------------------------------------------------------------
result = calculate_reserve_schedule(
    age=age, term=term, sum_assured=sum_assured,
    interest_rate_pct=interest_rate, improvement_rate=improvement_rate, df_mort=df_mort,
    initial_expense_pct=initial_expense_pct, renewal_expense_pct=renewal_expense_pct,
    fixed_fee=fixed_fee,
)

gross_premium = result['gross_premium']
schedule = result['schedule']
df_schedule = pd.DataFrame(schedule)

inspected_row = next(r for r in schedule if r['t'] == duration_to_inspect)

# -----------------------------------------------------------------------------
# HEADER
# -----------------------------------------------------------------------------
st.markdown("""
<div class="hero-dark" style="padding: 40px 50px;">
    <div class="hero-dark-content">
        <div class="hero-dark-title" style="font-size: 1.7rem;">🏦 Gross Premium Reserve</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    f"<p style='color:#9fb2bb; font-size:0.95rem; margin-top:18px;'>"
    f"Prospective Gross Premium Reserve for a <strong>{age}-year-old</strong>, {term}-year Term Life policy, "
    f"<strong>{format_currency(sum_assured)}</strong> sum assured, at a "
    f"<strong>{improvement_rate:.1%}</strong> mortality improvement rate.</p>",
    unsafe_allow_html=True
)

st.markdown('<hr class="glass-divider">', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# METRIC CARDS
# -----------------------------------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    metric_card(
        label="Gross Annual Premium",
        value=format_currency(gross_premium),
        sub="Solved via the equivalence principle",
        color="dark"
    )

with col2:
    metric_card(
        label=f"Reserve at t={duration_to_inspect} (Age {inspected_row['age_t']})",
        value=format_currency(inspected_row['gross_premium_reserve']),
        sub=f"Annuity-Due Factor: {inspected_row['annuity_due']:.4f}",
        color="teal"
    )

with col3:
    peak_row = max(schedule, key=lambda r: r['gross_premium_reserve'])
    metric_card(
        label="Peak Reserve",
        value=format_currency(peak_row['gross_premium_reserve']),
        sub=f"Occurs at t={peak_row['t']} (Age {peak_row['age_t']})",
        color="amber"
    )

st.write("")

# -----------------------------------------------------------------------------
# RESERVE CURVE CHART
# -----------------------------------------------------------------------------
st.markdown('<hr class="glass-divider">', unsafe_allow_html=True)
st.markdown('<div class="section-tag">Reserve Build-Up &amp; Run-Off</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title" style="font-size:1.4rem; text-align:left;">Gross Premium Reserve Over the Policy Term</div>', unsafe_allow_html=True)
st.markdown(
    "<p style='color:#9fb2bb; font-size:0.9rem; margin-bottom:20px;'>"
    "The reserve starts and ends at zero — zero at issue because the premium is solved by the equivalence "
    "principle, and zero at maturity because a term assurance pays no maturity benefit. In between, the "
    "reserve builds up as accumulated future-benefit cost outpaces remaining premium income (mortality risk "
    "rises with age), then runs off as the remaining term shortens.</p>",
    unsafe_allow_html=True
)

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df_schedule['t'],
    y=df_schedule['gross_premium_reserve'],
    mode="lines+markers",
    name="Gross Premium Reserve",
    line=dict(color="#2dd4bf", width=3),
    fill="tozeroy",
    fillcolor="rgba(45,212,191,0.12)",
))
fig.add_trace(go.Scatter(
    x=[duration_to_inspect],
    y=[inspected_row['gross_premium_reserve']],
    mode="markers",
    name=f"Inspected (t={duration_to_inspect})",
    marker=dict(color="#f59e0b", size=12, symbol="diamond"),
))
fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#eef2f4"),
    margin=dict(l=10, r=10, t=30, b=10),
    height=420,
    xaxis=dict(title="Policy Duration (t, years)"),
    yaxis=dict(title="Gross Premium Reserve (₹)"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)
st.plotly_chart(fig, width="stretch")

# -----------------------------------------------------------------------------
# FULL SCHEDULE TABLE
# -----------------------------------------------------------------------------
st.markdown('<hr class="glass-divider">', unsafe_allow_html=True)
st.markdown('<div class="glass-label">Full Reserve Schedule</div>', unsafe_allow_html=True)

df_display = df_schedule.copy()
df_display = df_display.rename(columns={
    't': 'Duration (t)',
    'age_t': 'Age',
    'annuity_due': 'Annuity-Due',
    'term_assurance_factor': 'A¹ Factor',
    'pv_future_benefits': 'PV Future Benefits',
    'pv_future_expenses': 'PV Future Expenses',
    'pv_future_premiums': 'PV Future Premiums',
    'gross_premium_reserve': 'Gross Premium Reserve',
})
for col in ['PV Future Benefits', 'PV Future Expenses', 'PV Future Premiums', 'Gross Premium Reserve']:
    df_display[col] = df_display[col].apply(lambda x: f"₹{x:,.2f}")
df_display['Annuity-Due'] = df_display['Annuity-Due'].apply(lambda x: f"{x:.4f}")
df_display['A¹ Factor'] = df_display['A¹ Factor'].apply(lambda x: f"{x:.6f}")

st.dataframe(df_display, hide_index=True, width="stretch")