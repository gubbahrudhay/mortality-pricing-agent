"""
Agent Tool: Sensitivity Tool

This module defines a LangChain tool wrapper that evaluates premium sensitivity to changes in
either interest/discount rates or mortality multiplier shocks.
"""

import os
import sys
from langchain_core.tools import tool

# Add parent directory to path to support config/pricing imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from actuarial.mortality import load_raw_table
from analytics.sensitivity_analysis import analyze_interest_rate_sensitivity, analyze_mortality_shock_sensitivity
from actuarial.utils import format_currency

@tool
def sensitivity_tool(age: int, gender: str, term: int, sum_assured: float, interest_rate: float, improvement_rate: float, sensitivity_type: str) -> str:
    """
    Evaluates premium sensitivity to changes in either the interest rate or mortality multiplier shocks.
    Useful when answering sensitivity questions like 'What happens if interest rates change?' or 'How do mortality shocks affect premiums?'.
    
    Inputs:
      - age (int): Entry age of policyholder
      - gender (str): 'Male' or 'Female'
      - term (int): Policy term in years
      - sum_assured (float): The total claim payout value
      - interest_rate (float): The base discount rate in percentage (e.g. 6.0)
      - improvement_rate (float): Base annual compound mortality improvement (e.g. 0.01)
      - sensitivity_type (str): Either 'interest' (interest rate sensitivity) or 'shock' (mortality shock sensitivity)
      
    Returns:
      A formatted summary of premium sensitivity.
    """
    try:
        df_mort = load_raw_table()
        
        if sensitivity_type.lower() == 'interest':
            res = analyze_interest_rate_sensitivity(
                age=age,
                gender=gender,
                term=term,
                sum_assured=sum_assured,
                improvement_rate=improvement_rate,
                df_mort=df_mort
            )
            output = (
                f"--- Interest Rate Sensitivity Analysis ---\n"
                f"Client: Age {age}, {gender} | Term: {term} years\n"
                f"Sum Assured: {format_currency(sum_assured)} | Mortality Improvement: {improvement_rate*100:.1f}%\n\n"
                f"{'Interest Rate':<15} | {'Term LAP':<15} | {'Whole LAP':<15}\n"
                f"-" * 51 + "\n"
            )
            for item in res:
                rate_str = f"{item['Interest_Rate']:.2f}%"
                t_lap = format_currency(item['Term_LAP'])
                w_lap = format_currency(item['Whole_LAP'])
                output += f"{rate_str:<15} | {t_lap:<15} | {w_lap:<15}\n"
            output += f"-" * 51 + "\n"
            
        elif sensitivity_type.lower() == 'shock':
            res = analyze_mortality_shock_sensitivity(
                age=age,
                gender=gender,
                term=term,
                sum_assured=sum_assured,
                interest_rate_pct=interest_rate,
                df_mort=df_mort
            )
            output = (
                f"--- Mortality Shock (Multiplier) Sensitivity Analysis ---\n"
                f"Client: Age {age}, {gender} | Term: {term} years\n"
                f"Sum Assured: {format_currency(sum_assured)} | Discount Rate: {interest_rate}%\n\n"
                f"{'Mortality Multiplier':<20} | {'Term LAP':<15} | {'Whole LAP':<15}\n"
                f"-" * 56 + "\n"
            )
            for item in res:
                mult_str = f"{item['Mortality_Multiplier']:.2f}x"
                t_lap = format_currency(item['Term_LAP'])
                w_lap = format_currency(item['Whole_LAP'])
                output += f"{mult_str:<20} | {t_lap:<15} | {w_lap:<15}\n"
            output += f"-" * 56 + "\n"
            output += "Note: Multipliers > 1.0 indicate elevated mortality risk; < 1.0 indicate favorable mortality improvement."
            
        else:
            return "Error: sensitivity_type must be either 'interest' or 'shock'."
            
        return output
    except Exception as e:
        return f"Error executing sensitivity_tool: {str(e)}"
