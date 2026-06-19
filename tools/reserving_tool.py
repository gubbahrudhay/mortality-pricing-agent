"""
Agent Tool: Reserving Tool

This module defines a LangChain tool wrapper around the Gross Premium
Reserve calculation, returning a formatted reserve schedule summary for a
given Term Life policy.
"""

import os
import sys
from langchain_core.tools import tool

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from actuarial.mortality import load_raw_table
from actuarial.reserving import calculate_reserve_schedule
from actuarial.utils import format_currency


@tool
def reserving_tool(
    age: int,
    term: int,
    sum_assured: float,
    interest_rate: float,
    improvement_rate: float = 0.0,
    initial_expense_pct: float = 0.5,
    renewal_expense_pct: float = 0.05,
    fixed_fee: float = 500,
    duration: int = None,
) -> str:
    """
    Computes the Prospective Gross Premium Reserve for a Term Life policy,
    either as a full year-by-year schedule (if duration is not specified)
    or at one specific policy duration.

    The reserve at duration t represents the amount the insurer must hold
    on its balance sheet at that point: it equals the present value of
    future benefits and future expenses, minus the present value of
    future premiums still to be collected.

    Inputs:
      - age (int): Entry age of policyholder (e.g. 40)
      - term (int): Policy term in years (e.g. 30)
      - sum_assured (float): The total claim payout value (e.g. 1000000)
      - interest_rate (float): The discount rate in percentage (e.g. 6.0 for 6%)
      - improvement_rate (float): Annual compound mortality improvement (e.g. 0.01 for 1% improvement). Default 0.0.
      - initial_expense_pct (float): Initial expense as a decimal fraction of the FIRST YEAR premium (e.g. 0.5 for 50%). Default 0.5.
      - renewal_expense_pct (float): Renewal expense as a decimal fraction of premium in renewal years (e.g. 0.05 for 5%). Default 0.05.
      - fixed_fee (float): Flat policy maintenance fee per year in rupees (e.g. 500). Default 500.
      - duration (int, optional): If specified, return the reserve at this single duration only (e.g. 10 for the reserve at the end of policy year 10). If not specified, return key points from the full schedule (start, every 5 years, and maturity).

    Returns:
      A formatted text summary of the Gross Premium used and the reserve(s) requested.
    """
    try:
        df_mort = load_raw_table()

        result = calculate_reserve_schedule(
            age=age,
            term=term,
            sum_assured=sum_assured,
            interest_rate_pct=interest_rate,
            improvement_rate=improvement_rate,
            df_mort=df_mort,
            initial_expense_pct=initial_expense_pct,
            renewal_expense_pct=renewal_expense_pct,
            fixed_fee=fixed_fee,
        )

        gross_premium = result['gross_premium']
        schedule = result['schedule']

        header = (
            f"--- Gross Premium Reserve Results ---\n"
            f"Policyholder: Age {age}\n"
            f"Sum Assured: {format_currency(sum_assured)}\n"
            f"Policy Term: {term} years\n"
            f"Discount Rate: {interest_rate}%\n"
            f"Mortality Improvement: {improvement_rate*100:.1f}% per annum\n"
            f"Gross Annual Premium (P): {format_currency(gross_premium)}\n\n"
        )

        if duration is not None:
            row = next((r for r in schedule if r['t'] == duration), None)
            if row is None:
                return f"Error: duration {duration} is out of range for a {term}-year policy (valid range 0-{term})."

            body = (
                f"Reserve at Duration t={duration} (Age {row['age_t']}):\n"
                f"   - Annuity-Due Factor: {row['annuity_due']:.4f}\n"
                f"   - Term Assurance Factor (A^1): {row['term_assurance_factor']:.6f}\n"
                f"   - PV Future Benefits: {format_currency(row['pv_future_benefits'])}\n"
                f"   - PV Future Expenses: {format_currency(row['pv_future_expenses'])}\n"
                f"   - PV Future Premiums: {format_currency(row['pv_future_premiums'])}\n\n"
                f"   GROSS PREMIUM RESERVE at t={duration}: {format_currency(row['gross_premium_reserve'])}\n"
            )
        else:
            # Show key points: t=0, every 5 years, and maturity
            key_durations = sorted(set([0] + list(range(5, term, 5)) + [term]))
            lines = ["Reserve Schedule (key durations):\n", "Duration (t) | Age | Gross Premium Reserve", "-" * 45]
            for t in key_durations:
                row = next((r for r in schedule if r['t'] == t), None)
                if row:
                    lines.append(f"   t={row['t']:<3}      | {row['age_t']:<3} | {format_currency(row['gross_premium_reserve'])}")
            body = "\n".join(lines) + "\n"

        footer = (
            "\nNote: The reserve at t=0 is 0 by construction (the premium is "
            "solved via the equivalence principle so assets equal liabilities "
            "at issue), and the reserve at t=term (maturity) is also 0 since "
            "a term assurance pays no maturity benefit."
        )

        return header + body + footer

    except Exception as e:
        return f"Error executing reserving_tool: {str(e)}"