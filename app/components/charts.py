"""
Streamlit UI Chart Component

This module houses wrappers to render Plotly chart objects inside Streamlit columns.
"""

import streamlit as st
import os
import sys

# Add parent directory to path to support analytics/charts imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from analytics.charts import (
    build_survival_curve_chart,
    build_mortality_rate_chart,
    build_interest_rate_sensitivity_chart,
    build_mortality_shock_chart,
    build_scenario_comparison_chart
)

def render_survival_curve(ages, tpx, term):
    fig = build_survival_curve_chart(ages, tpx, term)
    st.plotly_chart(fig, width="stretch")

def render_mortality_rate_comparison(ages, base_rates, improved_rates, gender):
    fig = build_mortality_rate_chart(ages, base_rates, improved_rates, gender)
    st.plotly_chart(fig, width="stretch")

def render_interest_sensitivity(sensitivity_data):
    fig = build_interest_rate_sensitivity_chart(sensitivity_data)
    st.plotly_chart(fig, width="stretch")

def render_mortality_shock_sensitivity(sensitivity_data):
    fig = build_mortality_shock_chart(sensitivity_data)
    st.plotly_chart(fig, width="stretch")

def render_scenario_comparison(comparison_data):
    fig = build_scenario_comparison_chart(comparison_data)
    st.plotly_chart(fig, width="stretch")
