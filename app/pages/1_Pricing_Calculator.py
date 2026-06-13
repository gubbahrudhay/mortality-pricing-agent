"""
Streamlit Page: Pricing Calculator

This page renders the core interactive pricing calculator, detailing premium card metrics,
survival curves, mortality comparisons, and claims projection tables.
"""

import streamlit as st
import os
import sys

# Add parent directory to path to support config/pricing imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import config
from actuarial.mortality import load_raw_table
from actuarial.pricing import calculate_all_pricing
from app.components.inputs import render_sidebar_inputs
from app.components.charts import render_survival_curve, render_mortality_rate_comparison
from app.components.tables import render_claims_projection_table
from actuarial.utils import format_currency
from app.theme import inject_theme, metric_card

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Pricing Calculator",
    page_icon="🛡️",
    layout="wide"
)

inject_theme()

# Load raw mortality table
df_mort = load_raw_table()

# Render inputs in sidebar
inputs = render_sidebar_inputs()

# -----------------------------------------------------------------------------
# COMPUTATIONS
# -----------------------------------------------------------------------------
res = calculate_all_pricing(
    age=inputs['age'],
    gender=inputs['gender'],
    term=inputs['term'],
    sum_assured=inputs['sum_assured'],
    interest_rate_pct=inputs['interest_rate'],
    improvement_rate=inputs['improvement_rate'],
    df_mort=df_mort,
    gender_factors=config.GENDER_FACTORS
)

# -----------------------------------------------------------------------------
# HEADER
# -----------------------------------------------------------------------------
st.markdown("""
<div class="hero-dark" style="padding: 40px 50px;">
    <div class="hero-dark-content">
        <div class="hero-dark-title" style="font-size: 1.7rem;">🛡️ Actuarial Life Insurance Pricing Calculator</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    f"<p style='color:#6b7280; font-size:0.95rem; margin-top:18px;'>"
    f"Simulating net premiums for a <strong>{inputs['age']}-year-old {inputs['gender']}</strong> "
    f"with <strong>{format_currency(inputs['sum_assured'])}</strong> coverage under the "
    f"<strong>{inputs['scenario_name']}</strong> mortality scenario.</p>",
    unsafe_allow_html=True
)

st.markdown('<hr class="glass-divider">', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PREMIUM METRIC CARDS
# -----------------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    metric_card(
        label=f"🛡️ Term Life Insurance ({inputs['term']}-Year Term)",
        value=f"{format_currency(res['lap_term'])} / Year",
        sub=f"Net Single Premium (Lump Sum): {format_currency(res['nsp_term'])}",
        color="teal"
    )

with col2:
    metric_card(
        label="♾️ Whole Life Insurance",
        value=f"{format_currency(res['lap_whole'])} / Year",
        sub=f"Net Single Premium (Lump Sum): {format_currency(res['nsp_whole'])}",
        color="dark"
    )

st.write("")

# -----------------------------------------------------------------------------
# CHARTS
# -----------------------------------------------------------------------------
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    render_survival_curve(res['ages_axis'], res['tpx'], inputs['term'])

with chart_col2:
    render_mortality_rate_comparison(res['ages_axis'][:-1], res['base_rates'], res['improved_rates'], inputs['gender'])

# -----------------------------------------------------------------------------
# EXPECTED CLAIMS PROJECTION
# -----------------------------------------------------------------------------
st.markdown('<hr class="glass-divider">', unsafe_allow_html=True)
st.markdown('<div class="glass-label">Expected Claims Projections (First 10 Years)</div>', unsafe_allow_html=True)
st.markdown(
    "<p style='color:#6b7280; font-size:0.92rem; margin-top:8px; margin-bottom:18px;'>"
    "This table projects the expected annual claim payment amounts based on the survival and mortality probabilities.</p>",
    unsafe_allow_html=True
)
render_claims_projection_table(res['claims_projection'][:10])
