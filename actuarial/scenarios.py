"""
Actuarial Scenarios Module

This module evaluates and compares premium rates and total cumulative savings across baseline
and multiple mortality improvement scenarios (e.g. 0%, 0.5%, 1.0%, 2.0%).
"""

import os
import pandas as pd
import sys

# Add parent directory to path to support config/pricing imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
from actuarial.pricing import calculate_all_pricing

def compare_scenarios(age, term, sum_assured, interest_rate_pct, df_mort, scenarios=None):
    """
    Evaluates pricing across different mortality improvement scenarios.
    Returns a list of dicts with comparison metrics.
    """
    if scenarios is None:
        scenarios = config.IMPROVEMENT_SCENARIOS
        
    results = []
    
    # Establish baseline pricing (0% improvement)
    # Find base scenario key or default to 0.0
    base_rate = 0.0
    for rate in scenarios.values():
        if rate == 0.0:
            base_rate = 0.0
            break
            
    base_pricing = calculate_all_pricing(
        age=age,
        term=term,
        sum_assured=sum_assured,
        interest_rate_pct=interest_rate_pct,
        improvement_rate=base_rate,
        df_mort=df_mort
    )
    
    base_lap_term = base_pricing['lap_term']
    base_lap_whole = base_pricing['lap_whole']
    
    for scenario_name, improvement_rate in scenarios.items():
        pricing = calculate_all_pricing(
            age=age,
            term=term,
            sum_assured=sum_assured,
            interest_rate_pct=interest_rate_pct,
            improvement_rate=improvement_rate,
            df_mort=df_mort
        )
        
        lap_term = pricing['lap_term']
        lap_whole = pricing['lap_whole']
        
        # Savings relative to baseline
        savings_term_abs = base_lap_term - lap_term
        savings_term_pct = (savings_term_abs / base_lap_term * 100.0) if base_lap_term > 0 else 0.0
        
        savings_whole_abs = base_lap_whole - lap_whole
        savings_whole_pct = (savings_whole_abs / base_lap_whole * 100.0) if base_lap_whole > 0 else 0.0
        
        results.append({
            'Scenario': scenario_name,
            'Improvement_Rate': improvement_rate,
            'Term_NSP': pricing['nsp_term'],
            'Term_LAP': lap_term,
            'Term_Savings_Abs': savings_term_abs,
            'Term_Savings_Pct': savings_term_pct,
            'Whole_NSP': pricing['nsp_whole'],
            'Whole_LAP': lap_whole,
            'Whole_Savings_Abs': savings_whole_abs,
            'Whole_Savings_Pct': savings_whole_pct
        })
        
    return results

def get_scenarios_comparison_df(age, term, sum_assured, interest_rate_pct, df_mort, scenarios=None):
    """
    Returns the scenario comparison as a formatted pandas DataFrame.
    """
    results = compare_scenarios(age, term, sum_assured, interest_rate_pct, df_mort, scenarios)
    return pd.DataFrame(results)
