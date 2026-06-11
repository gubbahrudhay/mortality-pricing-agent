import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sys
import os

# -----------------------------------------------------------------------------
# IMPORT CONFIGURATION
# -----------------------------------------------------------------------------
try:
    import config
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    import config

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & THEME
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Mortality Pricing Engine",
    page_icon="📊",
    layout="wide"
)

# Premium Card Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    .premium-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.15);
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
        font-size: 1.8rem;
        font-weight: 700;
        color: #6366f1;
        margin-bottom: 4px;
    }
    .card-subtext {
        font-size: 0.8rem;
        color: #64748b;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATA LOADING
# -----------------------------------------------------------------------------
@st.cache_data
def load_mortality_data():
    return pd.read_csv('data/morality_table.csv')

df_mort = load_mortality_data()

# -----------------------------------------------------------------------------
# SIDEBAR CONTROL PANEL
# -----------------------------------------------------------------------------
st.sidebar.title("🎛️ Control Panel")

age = st.sidebar.slider(
    "Entry Age (x)",
    min_value=int(config.MIN_AGE),
    max_value=int(config.MAX_AGE - 5),
    value=int(config.DEFAULT_AGE)
)

term = st.sidebar.slider(
    "Policy Term (n)",
    min_value=1,
    max_value=int(config.MAX_AGE - age),
    value=int(config.DEFAULT_TERM)
)

sum_assured = st.sidebar.number_input(
    "Sum Assured (₹)",
    min_value=10000,
    max_value=100000000,
    value=int(config.SUM_ASSURED),
    step=50000
)

interest_rate = st.sidebar.slider(
    "Discount Rate (%)",
    min_value=0.5,
    max_value=15.0,
    value=float(config.INTEREST_RATE * 100),
    step=0.25
)

# Select mortality improvement scenario from config
scenario_name = st.sidebar.selectbox(
    "Mortality Improvement Scenario",
    options=list(config.IMPROVEMENT_SCENARIOS.keys())
)
improvement_rate = config.IMPROVEMENT_SCENARIOS[scenario_name]

# -----------------------------------------------------------------------------
# PRICING ENGINE
# -----------------------------------------------------------------------------
i = interest_rate / 100.0
v = 1 / (1 + i)

# Extract baseline qx rates
base_rates = df_mort['qx'].values

# Apply mortality improvement: q_x_improved = q_x * (1 - improvement_rate)
improved_rates = np.clip(base_rates * (1.0 - improvement_rate), 0.0, 1.0)

# Calculate survival probabilities tpx from starting age
# tpx[t] is probability of surviving t years from starting age
max_periods = len(df_mort) - age
tpx = np.zeros(max_periods)
tpx[0] = 1.0
for t in range(1, max_periods):
    tpx[t] = tpx[t-1] * (1.0 - improved_rates[age + t - 1])

# Calculate Term Life net single premium (NSP)
n = min(term, max_periods - 1)
nsp_term = 0.0
for t in range(n):
    nsp_term += (v ** (t + 1)) * tpx[t] * improved_rates[age + t]
nsp_term_val = nsp_term * sum_assured

# Calculate Whole Life net single premium (NSP)
nsp_whole = 0.0
for t in range(max_periods - 1):
    nsp_whole += (v ** (t + 1)) * tpx[t] * improved_rates[age + t]
nsp_whole_val = nsp_whole * sum_assured

# Calculate temporary life annuity due factor (for Term LAP conversion)
a_due_term = 0.0
for t in range(n):
    a_due_term += (v ** t) * tpx[t]
lap_term_val = nsp_term_val / a_due_term if a_due_term > 0 else nsp_term_val

# Calculate whole life annuity due factor (for Whole Life LAP conversion)
a_due_whole = 0.0
for t in range(max_periods - 1):
    a_due_whole += (v ** t) * tpx[t]
lap_whole_val = nsp_whole_val / a_due_whole if a_due_whole > 0 else nsp_whole_val

# -----------------------------------------------------------------------------
# MAIN APP VIEW
# -----------------------------------------------------------------------------
st.title("📊 Actuarial Mortality Pricing Dashboard")
st.markdown(
    f"Simulating net premiums for a **{age}-year-old** policyholder with **₹{sum_assured:,.2f}** coverage under the **{scenario_name}** mortality scenario."
)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="premium-card">
        <div class="card-title">🛡️ Term Life Insurance ({n}-Year Term)</div>
        <div class="card-value">₹{lap_term_val:,.2f} <span style="font-size:1rem; font-weight:normal; color:#64748b;">/ Year</span></div>
        <div class="card-subtext">Net Single Premium (Lump Sum): <b>₹{nsp_term_val:,.2f}</b></div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="premium-card">
        <div class="card-title">♾️ Whole Life Insurance</div>
        <div class="card-value">₹{lap_whole_val:,.2f} <span style="font-size:1rem; font-weight:normal; color:#64748b;">/ Year</span></div>
        <div class="card-subtext">Net Single Premium (Lump Sum): <b>₹{nsp_whole_val:,.2f}</b></div>
    </div>
    """, unsafe_allow_html=True)

# Graph Columns
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    fig_surv = go.Figure()
    fig_surv.add_trace(go.Scatter(
        x=list(range(age, age + n + 1)),
        y=tpx[:n+1],
        mode='lines+markers',
        name='Survival Probability',
        line=dict(color='#0ea5e9', width=3),
        marker=dict(size=6)
    ))
    fig_surv.update_layout(
        title=f"Survival Probability Curve over the Policy Term ({n} Years)",
        xaxis_title="Age",
        yaxis_title="Survival Probability (tpx)",
        template="plotly_dark",
        height=380,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    st.plotly_chart(fig_surv, use_container_width=True)

with chart_col2:
    fig_mort = go.Figure()
    # Baseline
    fig_mort.add_trace(go.Scatter(
        x=list(range(age, age + n)),
        y=base_rates[age:age+n],
        mode='lines',
        name='Baseline Mortality (qx)',
        line=dict(color='#64748b', width=2, dash='dash')
    ))
    # Improved/Adjusted
    fig_mort.add_trace(go.Scatter(
        x=list(range(age, age + n)),
        y=improved_rates[age:age+n],
        mode='lines+markers',
        name='Scenario Mortality (qx)',
        line=dict(color='#f43f5e', width=3),
        marker=dict(size=6)
    ))
    fig_mort.update_layout(
        title="Mortality Probability Comparison (qx)",
        xaxis_title="Age",
        yaxis_title="Mortality Probability (qx)",
        template="plotly_dark",
        height=380,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    st.plotly_chart(fig_mort, use_container_width=True)
