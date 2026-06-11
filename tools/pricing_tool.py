"""
Agent Tool: Pricing Tool

This module defines a LangChain tool wrapper around the core actuarial pricing calculations,
returning a formatted summary of Term and Whole Life premiums for a given client scenario.
"""

import os
import sys
from langchain_core.tools import tool

# Add parent directory to path to support config/pricing imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from actuarial.mortality import load_raw_table
from actuarial.pricing import calculate_all_pricing
from actuarial.utils import format_currency

@tool
def pricing_tool(age: int, gender: str, term: int, sum_assured: float, interest_rate: float, improvement_rate: float = 0.0) -> str:
    """
    Computes Term and Whole Life net premiums (Net Single Premium and Level Annual Premium) 
    for a specified client scenario.
    
    Inputs:
      - age (int): Entry age of policyholder (e.g. 35)
      - gender (str): 'Male' or 'Female'
      - term (int): Policy term in years (e.g. 20)
      - sum_assured (float): The total claim payout value (e.g. 1000000)
      - interest_rate (float): The discount rate in percentage (e.g. 6.0 for 6%)
      - improvement_rate (float): Annual compound mortality improvement (e.g. 0.01 for 1% improvement)
      
    Returns:
      A formatted text summary of Term Life and Whole Life premiums.
    """
    try:
        # Load raw mortality table
        df_mort = load_raw_table()
        
        # Calculate pricing
        res = calculate_all_pricing(
            age=age,
            gender=gender,
            term=term,
            sum_assured=sum_assured,
            interest_rate_pct=interest_rate,
            improvement_rate=improvement_rate,
            df_mort=df_mort
        )
        
        output = (
            f"--- Actuarial Pricing Results ---\n"
            f"Policyholder: Age {age}, {gender}\n"
            f"Sum Assured: {format_currency(sum_assured)}\n"
            f"Policy Term: {term} years\n"
            f"Discount Rate: {interest_rate}%\n"
            f"Mortality Improvement: {improvement_rate*100:.1f}% per annum\n\n"
            f"1. Term Life Insurance ({term}-Year Term):\n"
            f"   - Net Single Premium (NSP): {format_currency(res['nsp_term'])}\n"
            f"   - Level Annual Premium (LAP): {format_currency(res['lap_term'])} per year\n"
            f"   - Temporary Annuity Due Factor: {res['a_due_term']:.4f}\n\n"
            f"2. Whole Life Insurance:\n"
            f"   - Net Single Premium (NSP): {format_currency(res['nsp_whole'])}\n"
            f"   - Level Annual Premium (LAP): {format_currency(res['lap_whole'])} per year\n"
            f"   - Whole Life Annuity Due Factor: {res['a_due_whole']:.4f}\n"
            f"----------------------------------"
        )
        return output
    except Exception as e:
        return f"Error executing pricing_tool: {str(e)}"
