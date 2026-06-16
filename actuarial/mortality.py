"""
Actuarial Mortality Module

This module handles loading the raw mortality table data and computing
compound annual mortality improvement projections and survival probability curves.
Gender factor has been removed — single unified mortality table is used.
"""

import os
import pandas as pd
import numpy as np
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config


def load_raw_table(csv_path="data/raw/mortality_table.csv"):
    if not os.path.exists(csv_path):
        resolved_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', csv_path))
        if os.path.exists(resolved_path):
            csv_path = resolved_path
        else:
            raise FileNotFoundError(f"Mortality table file not found at {csv_path}")

    df = pd.read_csv(csv_path)

    if 'Age' not in df.columns or 'qx' not in df.columns:
        raise ValueError("Mortality table must contain 'Age' and 'qx' columns.")

    return df


def get_improved_mortality_rates(df_mort, improvement_rate, entry_age=None):
    """
    Applies annual compound mortality improvement to baseline qx rates.
    qx_improved = qx_base * (1 - improvement_rate)
    Gender factor removed — single unified table used.
    """
    ages = df_mort['Age'].values
    base_qx = df_mort['qx'].values

    max_age = int(ages.max())
    full_rates = np.zeros(max_age + 1)
    for a, q in zip(ages, base_qx):
        full_rates[int(a)] = q

    min_age = int(ages.min())
    full_rates[:min_age] = base_qx[0]

    improved_rates = np.clip(full_rates * (1.0 - improvement_rate), 0.0, 1.0)
    return improved_rates


def get_survival_probabilities(improved_rates, age, term):
    """
    Computes survival probability (tpx) for each policy year t.
    tpx = product_{s=0}^{t-1} (1 - q_{x+s})
    Returns a numpy array of length term + 1.
    """
    max_periods = len(improved_rates) - age
    n = min(term, max_periods - 1)

    tpx = np.zeros(n + 1)
    tpx[0] = 1.0

    for t in range(1, n + 1):
        tpx[t] = tpx[t - 1] * (1.0 - improved_rates[age + t - 1])

    return tpx


if __name__ == "__main__":
    df = load_raw_table()
    print(f"Loaded {len(df)} rows from raw table successfully.")