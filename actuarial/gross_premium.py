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

Supports both Term Life and Whole Life products via the `product_type`
parameter ("term" or "whole").

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
    calculate_nsp_whole,
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
    product_type="term",
):
    """
    Computes Net Premium, Loaded Premium, Gross Premium, and Profit Loading
    for a Term Life or Whole Life policy under a given mortality improvement rate.

    product_type: "term" (default) or "whole".
        - "term": uses the supplied `term` years.
        - "whole": ignores `term` for the death-benefit calculation and instead
          covers the policyholder for the remaining lifetime (to the end of
          the mortality table); the annuity-due factor is likewise computed
          over the full remaining lifetime.

    initial_expense_pct: % of Sum Assured (per pricing formula)
    renewal_expense: flat Rs. amount per policy per year
    """
    improved_rates = get_improved_mortality_rates(df_mort, improvement_rate, entry_age=age)

    if product_type == "whole":
        max_periods = len(improved_rates) - age
        tpx = get_survival_probabilities(improved_rates, age, max_periods)
        nsp = calculate_nsp_whole(age, sum_assured, interest_rate_pct, improved_rates, tpx)
        effective_term = max_periods
    else:
        tpx = get_survival_probabilities(improved_rates, age, term)
        nsp = calculate_nsp_term(age, term, sum_assured, interest_rate_pct, improved_rates, tpx)
        effective_term = term

    a_due = calculate_annuity_due_factor(tpx, interest_rate_pct)

    net_premium = nsp / a_due if a_due > 0 else nsp
    initial_expense_amount = initial_expense_pct * sum_assured
    initial_expense_per_year = initial_expense_amount / a_due if a_due > 0 else 0.0
    loaded_premium = net_premium + initial_expense_per_year + renewal_expense
    gross_premium = loaded_premium / (1 - contingency_pct - profit_margin_pct)
    profit_loading = gross_premium * profit_margin_pct

    return {
        'age': age,
        'term': effective_term,
        'product_type': product_type,
        'sum_assured': sum_assured,
        'interest_rate': interest_rate_pct,
        'improvement_rate': improvement_rate,
        'nsp_term': nsp,
        'annuity_due_factor': a_due,
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

    print("--- TERM LIFE ---")
    result = calculate_gross_premium(
        age=40, term=10, sum_assured=1_000_000,
        interest_rate_pct=4.0, improvement_rate=0.0, df_mort=df_mort,
        product_type="term",
    )
    for k, v in result.items():
        print(f"{k}: {v}")

    print("\n--- WHOLE LIFE ---")
    result = calculate_gross_premium(
        age=40, term=10, sum_assured=1_000_000,
        interest_rate_pct=4.0, improvement_rate=0.0, df_mort=df_mort,
        product_type="whole",
    )
    for k, v in result.items():
        print(f"{k}: {v}")