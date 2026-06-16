"""
Actuarial Gross Premium Scenarios Module

This module evaluates and compares Gross Premium and Profit Loading across
baseline and multiple mortality improvement scenarios (e.g. 0%, 0.5%, 1.0%, 2.0%),
following the same pattern as actuarial/scenarios.py but for the loaded
(Gross) premium rather than the Net premium.
"""

import os
import pandas as pd
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
from actuarial.gross_premium import calculate_gross_premium


def compare_gross_premium_scenarios(
    age,
    term,
    sum_assured,
    interest_rate_pct,
    df_mort,
    initial_expense_pct=0.02,
    renewal_expense=500,
    contingency_pct=0.02,
    profit_margin_pct=0.08,
    scenarios=None,
):
    """
    Evaluates Gross Premium and Profit Loading across different mortality
    improvement scenarios. Returns a list of dicts with comparison metrics.
    """
    if scenarios is None:
        scenarios = config.IMPROVEMENT_SCENARIOS

    results = []

    base_rate = 0.0
    for rate in scenarios.values():
        if rate == 0.0:
            base_rate = 0.0
            break

    base_result = calculate_gross_premium(
        age=age,
        term=term,
        sum_assured=sum_assured,
        interest_rate_pct=interest_rate_pct,
        improvement_rate=base_rate,
        df_mort=df_mort,
        initial_expense_pct=initial_expense_pct,
        renewal_expense=renewal_expense,
        contingency_pct=contingency_pct,
        profit_margin_pct=profit_margin_pct,
    )

    base_gp = base_result['gross_premium']
    base_profit = base_result['profit_loading']

    for scenario_name, improvement_rate in scenarios.items():
        result = calculate_gross_premium(
            age=age,
            term=term,
            sum_assured=sum_assured,
            interest_rate_pct=interest_rate_pct,
            improvement_rate=improvement_rate,
            df_mort=df_mort,
            initial_expense_pct=initial_expense_pct,
            renewal_expense=renewal_expense,
            contingency_pct=contingency_pct,
            profit_margin_pct=profit_margin_pct,
        )

        gross_premium = result['gross_premium']
        profit_loading = result['profit_loading']

        gp_savings_abs = base_gp - gross_premium
        gp_savings_pct = (gp_savings_abs / base_gp * 100.0) if base_gp > 0 else 0.0

        profit_change_abs = profit_loading - base_profit
        profit_change_pct = (profit_change_abs / base_profit * 100.0) if base_profit > 0 else 0.0

        results.append({
            'Scenario': scenario_name,
            'Improvement_Rate': improvement_rate,
            'Net_Premium': result['net_premium'],
            'Gross_Premium': gross_premium,
            'GP_Savings_Abs': gp_savings_abs,
            'GP_Savings_Pct': gp_savings_pct,
            'Profit_Loading': profit_loading,
            'Profit_Change_Abs': profit_change_abs,
            'Profit_Change_Pct': profit_change_pct,
        })

    return results


def get_gross_premium_scenarios_df(
    age,
    term,
    sum_assured,
    interest_rate_pct,
    df_mort,
    initial_expense_pct=0.02,
    renewal_expense=500,
    contingency_pct=0.02,
    profit_margin_pct=0.08,
    scenarios=None,
):
    """
    Returns the Gross Premium scenario comparison as a formatted pandas DataFrame.
    """
    results = compare_gross_premium_scenarios(
        age, term, sum_assured, interest_rate_pct, df_mort,
        initial_expense_pct, renewal_expense, contingency_pct, profit_margin_pct,
        scenarios,
    )
    return pd.DataFrame(results)