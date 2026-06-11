"""
Unit Tests: Actuarial Pricing

This module executes pytest tests validating raw table loading, discount factors, improved mortality rates,
survival probabilities, and premium calculations.
"""

import os
import sys
import pytest
import pandas as pd
import numpy as np

# Add parent directory to path to support config/pricing imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config
from actuarial.mortality import load_raw_table, get_improved_mortality_rates, get_survival_probabilities
from actuarial.pricing import calculate_discount_factor, calculate_annuity_due_factor, calculate_all_pricing

def test_load_raw_table():
    df = load_raw_table()
    assert isinstance(df, pd.DataFrame)
    assert 'Age' in df.columns
    assert 'qx' in df.columns
    assert len(df) > 0

def test_discount_factor():
    v = calculate_discount_factor(6.0)
    assert abs(v - 1/1.06) < 1e-6

def test_improved_mortality_rates():
    df = load_raw_table()
    gender = 'Male'
    improvement_rate = 0.01
    
    improved_rates = get_improved_mortality_rates(df, gender, improvement_rate, config.GENDER_FACTORS)
    base_rate = df['qx'].values[35]
    expected_improved_rate = base_rate * config.GENDER_FACTORS[gender] * (1.0 - improvement_rate)
    
    assert abs(improved_rates[35] - expected_improved_rate) < 1e-6

def test_survival_probabilities():
    # Constant qx = 0.1 for testing
    rates = np.full(100, 0.1)
    tpx = get_survival_probabilities(rates, age=30, term=5)
    
    # tpx size should be term + 1 = 6
    assert len(tpx) == 6
    assert tpx[0] == 1.0
    assert abs(tpx[1] - 0.9) < 1e-6
    assert abs(tpx[2] - 0.81) < 1e-6
    assert abs(tpx[3] - 0.729) < 1e-6

def test_pricing_calculations():
    df = load_raw_table()
    res = calculate_all_pricing(
        age=35,
        gender='Male',
        term=20,
        sum_assured=1000000,
        interest_rate_pct=6.0,
        improvement_rate=0.0,
        df_mort=df
    )
    
    assert res['nsp_term'] > 0
    assert res['lap_term'] > 0
    assert res['nsp_whole'] > 0
    assert res['lap_whole'] > 0
    assert res['lap_whole'] > res['lap_term']
