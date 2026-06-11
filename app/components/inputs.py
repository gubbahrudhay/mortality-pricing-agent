"""
Streamlit UI Input Component

This module renders reusable policy parameters (age, term, sum assured, discount, gender, scenario)
in the Streamlit sidebar control panel.
"""

import streamlit as st
import os
import sys

# Add parent directory to path to support config imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import config

def render_sidebar_inputs():
    """
    Renders policy parameters inputs in the sidebar.
    """
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
    
    gender_list = list(config.GENDER_FACTORS.keys())
    gender = st.sidebar.selectbox("Gender", options=gender_list)
    
    scenario_list = list(config.IMPROVEMENT_SCENARIOS.keys())
    scenario_name = st.sidebar.selectbox("Mortality Improvement Scenario", options=scenario_list)
    improvement_rate = config.IMPROVEMENT_SCENARIOS[scenario_name]
    
    return {
        "age": age,
        "term": term,
        "sum_assured": sum_assured,
        "interest_rate": interest_rate,
        "gender": gender,
        "scenario_name": scenario_name,
        "improvement_rate": improvement_rate
    }
