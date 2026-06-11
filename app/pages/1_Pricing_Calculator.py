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

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Pricing Calculator",
    page_icon="🛡️",
    layout="wide"
)

# Custom premium styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    .premium-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(8px);
        margin-bottom: 20px;
    }
    .card-title {
        font-size: 0.95rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }
    .card-value {
        font-size: 2.0rem;
        font-weight: 700;
        color: #6366f1;
        margin-bottom: 4px;
    }
    .card-subtext {
        font-size: 0.85rem;
        color: #64748b;
    }
</style>
""", unsafe_allow_html=True)

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
# MAIN APP VIEW
# -----------------------------------------------------------------------------
st.title("🛡️ Actuarial Life Insurance Pricing Calculator")
st.markdown(
    f"Simulating net premiums for a **{inputs['age']}-year-old {inputs['gender']}** with **{format_currency(inputs['sum_assured'])}** coverage under the **{inputs['scenario_name']}** mortality scenario."
)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="premium-card">
        <div class="card-title">🛡️ Term Life Insurance ({inputs['term']}-Year Term)</div>
        <div class="card-value">{format_currency(res['lap_term'])} <span style="font-size:1rem; font-weight:normal; color:#64748b;">/ Year</span></div>
        <div class="card-subtext">Net Single Premium (Lump Sum): <b>{format_currency(res['nsp_term'])}</b></div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="premium-card">
        <div class="card-title">♾️ Whole Life Insurance</div>
        <div class="card-value">{format_currency(res['lap_whole'])} <span style="font-size:1rem; font-weight:normal; color:#64748b;">/ Year</span></div>
        <div class="card-subtext">Net Single Premium (Lump Sum): <b>{format_currency(res['nsp_whole'])}</b></div>
    </div>
    """, unsafe_allow_html=True)

# Graph Columns
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    render_survival_curve(res['ages_axis'], res['tpx'], inputs['term'])

with chart_col2:
    render_mortality_rate_comparison(res['ages_axis'][:-1], res['base_rates'], res['improved_rates'], inputs['gender'])

# Expected Claims Projection
st.subheader("🔮 Expected Claims Projections (First 10 Years)")
st.markdown("This table projects the expected annual claim payment amounts based on the survival and mortality probabilities.")
render_claims_projection_table(res['claims_projection'][:10])
