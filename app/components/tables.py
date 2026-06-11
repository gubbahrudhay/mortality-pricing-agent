"""
Streamlit UI Table Component

This module provides helper components to display formatted dataframes and projection tables.
"""

import streamlit as st
import pandas as pd
import os
import sys

# Add parent directory to path to support config imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from actuarial.utils import format_currency, format_percentage

def render_scenario_table(df_comparison):
    """
    Renders scenario comparison table.
    """
    df_display = df_comparison.copy()
    
    # Format columns for display
    df_display['Term_NSP'] = df_display['Term_NSP'].apply(lambda x: format_currency(x))
    df_display['Term_LAP'] = df_display['Term_LAP'].apply(lambda x: format_currency(x))
    df_display['Term_Savings_Abs'] = df_display['Term_Savings_Abs'].apply(lambda x: format_currency(x))
    df_display['Term_Savings_Pct'] = df_display['Term_Savings_Pct'].apply(lambda x: f"{x:.2f}%")
    
    df_display['Whole_NSP'] = df_display['Whole_NSP'].apply(lambda x: format_currency(x))
    df_display['Whole_LAP'] = df_display['Whole_LAP'].apply(lambda x: format_currency(x))
    df_display['Whole_Savings_Abs'] = df_display['Whole_Savings_Abs'].apply(lambda x: format_currency(x))
    df_display['Whole_Savings_Pct'] = df_display['Whole_Savings_Pct'].apply(lambda x: f"{x:.2f}%")
    
    # Rename columns for layout
    df_display.columns = [
        'Scenario', 'Improvement Rate', 'Term NSP', 'Term Annual Premium (LAP)', 'Term Savings (Abs)', 
        'Term Savings (%)', 'Whole NSP', 'Whole Annual Premium (LAP)', 'Whole Savings (Abs)', 'Whole Savings (%)'
    ]
    
    st.dataframe(df_display, use_container_width=True, hide_index=True)

def render_claims_projection_table(projections):
    """
    Renders the claims projection table.
    """
    df = pd.DataFrame(projections)
    df_display = pd.DataFrame()
    
    df_display['Year'] = df['Year']
    df_display['Age'] = df['Age']
    df_display['Survival Probability (tpx)'] = df['Survival_Prob_tpx'].apply(lambda x: f"{x:.5f}")
    df_display['Mortality Probability (qx)'] = df['Mortality_Prob_qx'].apply(lambda x: f"{x:.5f}")
    df_display['Probability of Death (tpx * qx)'] = df['Probability_of_Death'].apply(lambda x: f"{x:.5f}")
    df_display['Expected Claims Amount'] = df['Expected_Claim_Amount'].apply(lambda x: format_currency(x))
    df_display['Present Value (PV) of Claims'] = df['PV_Expected_Claim'].apply(lambda x: format_currency(x))
    
    st.dataframe(df_display, use_container_width=True, hide_index=True)
