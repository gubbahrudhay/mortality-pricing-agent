import os
import numpy as np
import pandas as pd
import sys

# Add parent directory to path to support sibling/config imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
from actuarial.pricing import calculate_all_pricing

def analyze_interest_rate_sensitivity(age, gender, term, sum_assured, improvement_rate, df_mort, rate_range=None):
    """
    Computes Term and Whole Life premiums for a range of interest/discount rates.
    """
    if rate_range is None:
        # Default range from 1.0% to 12.0% in 12 steps
        rate_range = np.linspace(1.0, 12.0, 12)
        
    results = []
    for rate in rate_range:
        pricing = calculate_all_pricing(
            age=age,
            gender=gender,
            term=term,
            sum_assured=sum_assured,
            interest_rate_pct=rate,
            improvement_rate=improvement_rate,
            df_mort=df_mort
        )
        
        results.append({
            'Interest_Rate': rate,
            'Term_NSP': pricing['nsp_term'],
            'Term_LAP': pricing['lap_term'],
            'Whole_NSP': pricing['nsp_whole'],
            'Whole_LAP': pricing['lap_whole']
        })
        
    return results

def analyze_mortality_shock_sensitivity(age, gender, term, sum_assured, interest_rate_pct, df_mort, shock_range=None):
    """
    Computes Term and Whole Life premiums under various mortality shocks (multipliers).
    A shock multiplier of 1.2 means qx is increased by 20% (worse mortality).
    This is modelled by setting improvement_rate = 1.0 - shock_factor.
    """
    if shock_range is None:
        # Default range from 0.8 to 1.5 in 8 steps
        shock_range = np.linspace(0.8, 1.5, 8)
        
    results = []
    for shock in shock_range:
        improvement_rate = 1.0 - shock
        pricing = calculate_all_pricing(
            age=age,
            gender=gender,
            term=term,
            sum_assured=sum_assured,
            interest_rate_pct=interest_rate_pct,
            improvement_rate=improvement_rate,
            df_mort=df_mort
        )
        
        results.append({
            'Mortality_Multiplier': shock,
            'Term_NSP': pricing['nsp_term'],
            'Term_LAP': pricing['lap_term'],
            'Whole_NSP': pricing['nsp_whole'],
            'Whole_LAP': pricing['lap_whole']
        })
        
    return results
