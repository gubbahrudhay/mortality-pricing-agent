"""
Actuarial Pricing Module

Calculates NSP and LAP for Term Life and Whole Life products.
Death benefits payable at mid-year (v^(t+0.5)).
Premiums payable at start of year (v^t, annuity-due).
Gender factor removed — single unified mortality table used.
"""

import os
import numpy as np
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
from actuarial.mortality import get_improved_mortality_rates, get_survival_probabilities


def calculate_discount_factor(interest_rate_pct):
    i = interest_rate_pct / 100.0
    return 1.0 / (1.0 + i)


def calculate_annuity_due_factor(tpx, interest_rate_pct):
    v = calculate_discount_factor(interest_rate_pct)
    n = len(tpx) - 1
    a_due = 0.0
    for t in range(n):
        a_due += (v ** t) * tpx[t]
    return a_due


def calculate_nsp_term(age, term, sum_assured, interest_rate_pct, improved_rates, tpx):
    v = calculate_discount_factor(interest_rate_pct)
    max_periods = len(improved_rates) - age
    n = min(term, max_periods - 1)
    nsp_factor = 0.0
    for t in range(n):
        nsp_factor += (v ** (t + 0.5)) * tpx[t] * improved_rates[age + t]
    return nsp_factor * sum_assured


def calculate_lap_term(nsp_term, annuity_due_factor):
    if annuity_due_factor > 0:
        return nsp_term / annuity_due_factor
    return nsp_term


def calculate_nsp_whole(age, sum_assured, interest_rate_pct, improved_rates, tpx_whole):
    v = calculate_discount_factor(interest_rate_pct)
    max_periods = len(improved_rates) - age
    nsp_factor = 0.0
    for t in range(max_periods - 1):
        nsp_factor += (v ** (t + 0.5)) * tpx_whole[t] * improved_rates[age + t]
    return nsp_factor * sum_assured


def calculate_lap_whole(nsp_whole, annuity_due_whole_factor):
    if annuity_due_whole_factor > 0:
        return nsp_whole / annuity_due_whole_factor
    return nsp_whole


def project_expected_claims(age, term, sum_assured, interest_rate_pct, improved_rates, tpx):
    v = calculate_discount_factor(interest_rate_pct)
    max_periods = len(improved_rates) - age
    n = min(term, max_periods - 1)
    projections = []
    for t in range(n):
        qx_t = improved_rates[age + t]
        prob_death = tpx[t] * qx_t
        expected_claim = prob_death * sum_assured
        pv_factor = v ** (t + 0.5)
        pv_expected_claim = expected_claim * pv_factor
        projections.append({
            'Year': t + 1,
            'Age': age + t,
            'Survival_Prob_tpx': tpx[t],
            'Mortality_Prob_qx': qx_t,
            'Probability_of_Death': prob_death,
            'Expected_Claim_Amount': expected_claim,
            'PV_Expected_Claim': pv_expected_claim
        })
    return projections


def calculate_all_pricing(age, term, sum_assured, interest_rate_pct, improvement_rate, df_mort):
    """
    Convenience function to perform all pricing calculations.
    Gender parameter removed — single unified mortality table.
    """
    improved_rates = get_improved_mortality_rates(df_mort, improvement_rate, entry_age=age)

    tpx_term = get_survival_probabilities(improved_rates, age, term)

    max_periods = len(improved_rates) - age
    tpx_whole = get_survival_probabilities(improved_rates, age, max_periods)

    nsp_term = calculate_nsp_term(age, term, sum_assured, interest_rate_pct, improved_rates, tpx_term)
    a_due_term = calculate_annuity_due_factor(tpx_term, interest_rate_pct)
    lap_term = calculate_lap_term(nsp_term, a_due_term)

    nsp_whole = calculate_nsp_whole(age, sum_assured, interest_rate_pct, improved_rates, tpx_whole)
    a_due_whole = calculate_annuity_due_factor(tpx_whole, interest_rate_pct)
    lap_whole = calculate_lap_whole(nsp_whole, a_due_whole)

    claims_projection = project_expected_claims(age, term, sum_assured, interest_rate_pct, improved_rates, tpx_term)

    base_rates = df_mort['qx'].values
    n = len(tpx_term) - 1

    return {
        'age': age,
        'term': term,
        'sum_assured': sum_assured,
        'interest_rate': interest_rate_pct,
        'improvement_rate': improvement_rate,
        'nsp_term': nsp_term,
        'lap_term': lap_term,
        'a_due_term': a_due_term,
        'nsp_whole': nsp_whole,
        'lap_whole': lap_whole,
        'a_due_whole': a_due_whole,
        'tpx': tpx_term,
        'ages_axis': list(range(age, age + n + 1)),
        'improved_rates': improved_rates[age:age+n],
        'base_rates': base_rates[age:age+n],
        'claims_projection': claims_projection
    }