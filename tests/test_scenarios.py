import os
import sys
import pytest
import pandas as pd

# Add parent directory to path to support config/pricing imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from actuarial.mortality import load_raw_table
from actuarial.scenarios import compare_scenarios
from analytics.sensitivity_analysis import analyze_interest_rate_sensitivity, analyze_mortality_shock_sensitivity

def test_compare_scenarios():
    df = load_raw_table()
    results = compare_scenarios(
        age=35,
        gender='Male',
        term=20,
        sum_assured=1000000,
        interest_rate_pct=6.0,
        df_mort=df
    )
    
    assert len(results) > 0
    scenarios = [r['Scenario'] for r in results]
    assert '0% (Base)' in scenarios
    assert '2.0%' in scenarios
    
    # 2% improvement scenario should have lower Term LAP than 0% Base scenario
    base_lap = next(r['Term_LAP'] for r in results if r['Scenario'] == '0% (Base)')
    imp_lap = next(r['Term_LAP'] for r in results if r['Scenario'] == '2.0%')
    assert imp_lap < base_lap

def test_interest_sensitivity():
    df = load_raw_table()
    res = analyze_interest_rate_sensitivity(
        age=35,
        gender='Male',
        term=20,
        sum_assured=1000000,
        improvement_rate=0.01,
        df_mort=df
    )
    
    # Higher interest rate should yield lower premiums (more discounting)
    assert res[0]['Interest_Rate'] < res[-1]['Interest_Rate']
    assert res[0]['Term_LAP'] > res[-1]['Term_LAP']

def test_mortality_shock():
    df = load_raw_table()
    res = analyze_mortality_shock_sensitivity(
        age=35,
        gender='Male',
        term=20,
        sum_assured=1000000,
        interest_rate_pct=6.0,
        df_mort=df
    )
    
    # Higher mortality multiplier (worse mortality) should yield higher premiums
    assert res[0]['Mortality_Multiplier'] < res[-1]['Mortality_Multiplier']
    assert res[0]['Term_LAP'] < res[-1]['Term_LAP']
