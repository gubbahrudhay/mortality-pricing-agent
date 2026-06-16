"""
Actuarial Gross Premium Module

Extends the existing Net Premium engine (actuarial/pricing.py) with expense
loadings, contingency margin, and profit margin to compute the Gross Premium
and Profit Loading, per the actuarial illustration
(gross_premium_calculation_Illustration.xlsx):

    Net Premium (NP)            = NSP / Annuity-due factor   (already computed in pricing.py)
    Initial Expense ($)         = Initial Expense % x Sum Assured
    Initial Expense per yr      = Initial Expense ($) / Annuity-due factor
    Loaded Premium               = NP + Initial Expense per yr + Renewal Expense
    Gross Premium (GP)          = Loaded Premium / (1 - Contingency% - Profit%)
    Profit Loading ($)          = GP x Profit Margin %

Uses the real IALM 2012-14 mortality table (via actuarial.mortality /
actuarial.pricing) with compound mortality improvement, instead of the
flat illustrative qx used in the Excel sheet.
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
from actuarial.mortality import get_improved_mortality_rates, get_survival_probabilities
from actuarial.pricing import (
    calculate_annuity_due_factor,
    calculate_nsp_term,
)


def calculate_gross_premium(
    age,
    term,
    sum_assured,
    interest_rate_pct,
    improvement_rate,
    df_mort,
    initial_expense_pct=0.02,
    renewal_expense=500,
    contingency_pct=0.02,
    profit_margin_pct=0.08,
):
    """
    Computes Net Premium, Loaded Premium, Gross Premium, and Profit Loading
    for a term policy under a given mortality improvement rate.

    initial_expense_pct: % of Sum Assured (per pricing formula)
    renewal_expense: flat Rs. amount per policy per year
    """
    improved_rates = get_improved_mortality_rates(df_mort, improvement_rate, entry_age=age)
    tpx_term = get_survival_probabilities(improved_rates, age, term)

    nsp_term = calculate_nsp_term(age, term, sum_assured, interest_rate_pct, improved_rates, tpx_term)
    a_due_term = calculate_annuity_due_factor(tpx_term, interest_rate_pct)

    net_premium = nsp_term / a_due_term if a_due_term > 0 else nsp_term

    initial_expense_amount = initial_expense_pct * sum_assured
    initial_expense_per_year = initial_expense_amount / a_due_term if a_due_term > 0 else 0.0

    loaded_premium = net_premium + initial_expense_per_year + renewal_expense

    gross_premium = loaded_premium / (1 - contingency_pct - profit_margin_pct)
    profit_loading = gross_premium * profit_margin_pct

    return {
        'age': age,
        'term': term,
        'sum_assured': sum_assured,
        'interest_rate': interest_rate_pct,
        'improvement_rate': improvement_rate,
        'nsp_term': nsp_term,
        'annuity_due_factor': a_due_term,
        'net_premium': net_premium,
        'initial_expense_amount': initial_expense_amount,
        'initial_expense_per_year': initial_expense_per_year,
        'renewal_expense': renewal_expense,
        'loaded_premium': loaded_premium,
        'contingency_pct': contingency_pct,
        'profit_margin_pct': profit_margin_pct,
        'gross_premium': gross_premium,
        'profit_loading': profit_loading,
        'profit_loading_pct_of_np': profit_loading / net_premium if net_premium else 0.0,
    }


if __name__ == "__main__":
    from actuarial.mortality import load_raw_table
    df_mort = load_raw_table()
    result = calculate_gross_premium(
        age=40,
        term=10,
        sum_assured=1_000_000,
        interest_rate_pct=4.0,
        improvement_rate=0.0,
        df_mort=df_mort,
    )
    for k, v in result.items():
        print(f"{k}: {v}")