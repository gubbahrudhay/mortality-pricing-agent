import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sys
import os

# -----------------------------------------------------------------------------
# IMPORT CONFIGURATION & ENGINES
# -----------------------------------------------------------------------------
try:
    import config
    from engine.pricing import calculate_pricing
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    import config
    from engine.pricing import calculate_pricing

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
# DATA LOADING & VALIDATION (NO HARDCODED FALLBACKS)
# -----------------------------------------------------------------------------
@st.cache_data
def load_mortality_data():
    csv_path = 'data/morality_table.csv'
    try:
        if not os.path.exists(csv_path):
            st.error(f"❌ Critical Error: The mortality dataset file was not found at `{csv_path}`.")
            st.stop()
            
        df = pd.read_csv(csv_path)
        
        # Validate columns
        required_cols = ['Age', 'qx']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            st.error(f"❌ Critical Error: The dataset is missing required columns: {missing_cols}. Provided columns: {list(df.columns)}")
            st.stop()
            
        return df
    except Exception as e:
        st.error(f"❌ Failed to load or parse the mortality dataset: {e}")
        st.stop()

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

# Select gender from config options
gender_list = list(config.GENDER_FACTORS.keys())
policyholder_gender = st.sidebar.selectbox("Gender", options=gender_list)

# Select mortality improvement scenario from config
scenario_name = st.sidebar.selectbox(
    "Mortality Improvement Scenario",
    options=list(config.IMPROVEMENT_SCENARIOS.keys())
)
improvement_rate = config.IMPROVEMENT_SCENARIOS[scenario_name]

# -----------------------------------------------------------------------------
# CALL MODULAR PRICING ENGINE
# -----------------------------------------------------------------------------
res = calculate_pricing(
    age=age,
    gender=policyholder_gender,
    term=term,
    sum_assured=sum_assured,
    interest_rate=interest_rate,
    improvement_rate=improvement_rate,
    df_mort=df_mort,
    gender_factors=config.GENDER_FACTORS
)

# -----------------------------------------------------------------------------
# MAIN APP VIEW
# -----------------------------------------------------------------------------
st.title("📊 Actuarial Mortality Pricing Dashboard")
st.markdown(
    f"Simulating net premiums for a **{age}-year-old {policyholder_gender}** with **₹{sum_assured:,.2f}** coverage under the **{scenario_name}** mortality scenario."
)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="premium-card">
        <div class="card-title">🛡️ Term Life Insurance ({term}-Year Term)</div>
        <div class="card-value">₹{res['lap_term']:,.2f} <span style="font-size:1rem; font-weight:normal; color:#64748b;">/ Year</span></div>
        <div class="card-subtext">Net Single Premium (Lump Sum): <b>₹{res['nsp_term']:,.2f}</b></div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="premium-card">
        <div class="card-title">♾️ Whole Life Insurance</div>
        <div class="card-value">₹{res['lap_whole']:,.2f} <span style="font-size:1rem; font-weight:normal; color:#64748b;">/ Year</span></div>
        <div class="card-subtext">Net Single Premium (Lump Sum): <b>₹{res['nsp_whole']:,.2f}</b></div>
    </div>
    """, unsafe_allow_html=True)

# Graph Columns
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    fig_surv = go.Figure()
    fig_surv.add_trace(go.Scatter(
        x=res['ages_axis'],
        y=res['tpx'],
        mode='lines+markers',
        name='Survival Probability',
        line=dict(color='#0ea5e9', width=3),
        marker=dict(size=6)
    ))
    fig_surv.update_layout(
        title=f"Survival Probability Curve over the Policy Term ({term} Years)",
        xaxis_title="Age",
        yaxis_title="Survival Probability (tpx)",
        template="plotly_dark",
        height=380,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    st.plotly_chart(fig_surv, use_container_width=True)

with chart_col2:
    fig_mort = go.Figure()
    # Baseline (unadjusted by gender)
    fig_mort.add_trace(go.Scatter(
        x=res['ages_axis'][:-1],
        y=res['base_rates'],
        mode='lines',
        name='Baseline Mortality (qx)',
        line=dict(color='#64748b', width=2, dash='dash')
    ))
    # Improved/Adjusted
    fig_mort.add_trace(go.Scatter(
        x=res['ages_axis'][:-1],
        y=res['improved_rates'],
        mode='lines+markers',
        name='Scenario Mortality (qx)',
        line=dict(color='#f43f5e', width=3),
        marker=dict(size=6)
    ))
    fig_mort.update_layout(
        title=f"Mortality Probability Comparison (qx) - {policyholder_gender}",
        xaxis_title="Age",
        yaxis_title="Mortality Probability (qx)",
        template="plotly_dark",
        height=380,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    st.plotly_chart(fig_mort, use_container_width=True)
