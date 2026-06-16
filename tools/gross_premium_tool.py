"""
Agent Tool: Gross Premium Tool

This module defines a LangChain tool wrapper around the Gross Premium and
Profit Loading calculations, returning a formatted summary for a given
client scenario, including expense loadings, contingency margin, and
target profit margin.
"""

import os
import sys
from langchain_core.tools import tool

# Add parent directory to path to support config/pricing imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from actuarial.mortality import load_raw_table
from actuarial.gross_premium import calculate_gross_premium
from actuarial.utils import format_currency


@tool
def gross_premium_tool(
    age: int,
    term: int,
    sum_assured: float,
    interest_rate: float,
    improvement_rate: float = 0.0,
    initial_expense_pct: float = 0.02,
    renewal_expense: float = 500,
    contingency_pct: float = 0.02,
    profit_margin_pct: float = 0.08,
) -> str:
    """
    Computes the Gross Premium and Profit Loading for a Term Life policy,
    building on the Net Premium by adding initial expenses, renewal
    expenses, a contingency margin, and a target profit margin.

    Inputs:
      - age (int): Entry age of policyholder (e.g. 40)
      - term (int): Policy term in years (e.g. 10)
      - sum_assured (float): The total claim payout value (e.g. 1000000)
      - interest_rate (float): The discount rate in percentage (e.g. 4.0 for 4%)
      - improvement_rate (float): Annual compound mortality improvement (e.g. 0.01 for 1% improvement). Default 0.0.
      - initial_expense_pct (float): Initial expense as a decimal fraction of Sum Assured (e.g. 0.02 for 2%). Default 0.02.
      - renewal_expense (float): Flat renewal expense per policy per year in rupees (e.g. 500). Default 500.
      - contingency_pct (float): Contingency margin as a decimal fraction of Gross Premium (e.g. 0.02 for 2%). Default 0.02.
      - profit_margin_pct (float): Target profit margin as a decimal fraction of Gross Premium (e.g. 0.08 for 8%). Default 0.08.

    Returns:
      A formatted text summary of the Net Premium, expense loadings, Gross Premium, and Profit Loading.
    """
    try:
        df_mort = load_raw_table()

        res = calculate_gross_premium(
            age=age,
            term=term,
            sum_assured=sum_assured,
            interest_rate_pct=interest_rate,
            improvement_rate=improvement_rate,
            df_mort=df_mort,
            initial_expense_pct=initial_expense_pct,
            renewal_expense=renewal_expense,
            contingency_pct=contingency_pct,
            profit_margin_pct=profit_margin_pct,
        )

        output = (
            f"--- Gross Premium & Profit Loading Results ---\n"
            f"Policyholder: Age {age}\n"
            f"Sum Assured: {format_currency(sum_assured)}\n"
            f"Policy Term: {term} years\n"
            f"Discount Rate: {interest_rate}%\n"
            f"Mortality Improvement: {improvement_rate*100:.1f}% per annum\n\n"
            f"Expense & Margin Assumptions:\n"
            f"   - Initial Expense: {initial_expense_pct*100:.1f}% of Sum Assured "
            f"({format_currency(res['initial_expense_amount'])})\n"
            f"   - Renewal Expense: {format_currency(renewal_expense)} per year\n"
            f"   - Contingency Margin: {contingency_pct*100:.1f}% of Gross Premium\n"
            f"   - Target Profit Margin: {profit_margin_pct*100:.1f}% of Gross Premium\n\n"
            f"Premium Build-Up:\n"
            f"   - Net Premium (NP): {format_currency(res['net_premium'])} per year\n"
            f"   - Initial Expense (spread per yr): {format_currency(res['initial_expense_per_year'])}\n"
            f"   - Renewal Expense (per yr): {format_currency(res['renewal_expense'])}\n"
            f"   - Loaded Premium (before margins): {format_currency(res['loaded_premium'])}\n\n"
            f"Final Results:\n"
            f"   - Gross Premium (GP): {format_currency(res['gross_premium'])} per year\n"
            f"   - Profit Loading: {format_currency(res['profit_loading'])} "
            f"({res['profit_loading_pct_of_np']:.2%} of Net Premium)\n"
            f"------------------------------------------------"
        )
        return output
    except Exception as e:
        return f"Error executing gross_premium_tool: {str(e)}"