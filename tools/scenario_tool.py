import os
import sys
from langchain_core.tools import tool

# Add parent directory to path to support config/pricing imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from actuarial.mortality import load_raw_table
from actuarial.scenarios import compare_scenarios
from actuarial.utils import format_currency

@tool
def scenario_tool(age: int, gender: str, term: int, sum_assured: float, interest_rate: float) -> str:
    """
    Compares premiums across various mortality improvement scenarios (0%, 0.5%, 1.0%, and 2.0%).
    Useful when asked to compare premium rates under different mortality assumptions.
    
    Inputs:
      - age (int): Entry age of policyholder
      - gender (str): 'Male' or 'Female'
      - term (int): Policy term in years
      - sum_assured (float): The total claim payout value
      - interest_rate (float): The discount rate in percentage
      
    Returns:
      A formatted comparison table of premiums and savings across scenarios.
    """
    try:
        df_mort = load_raw_table()
        comparison = compare_scenarios(
            age=age,
            gender=gender,
            term=term,
            sum_assured=sum_assured,
            interest_rate_pct=interest_rate,
            df_mort=df_mort
        )
        
        output = (
            f"--- Mortality Improvement Scenario Comparison ---\n"
            f"Client: Age {age}, {gender} | Sum Assured: {format_currency(sum_assured)}\n"
            f"Policy Term: {term} years | Discount Rate: {interest_rate}%\n\n"
            f"{'Scenario':<12} | {'Term LAP':<12} | {'Term Savings':<15} | {'Whole LAP':<12} | {'Whole Savings':<15}\n"
            f"-" * 78 + "\n"
        )
        
        for res in comparison:
            scenario = res['Scenario']
            t_lap = format_currency(res['Term_LAP'])
            t_sav = f"{format_currency(res['Term_Savings_Abs'])} ({res['Term_Savings_Pct']:.1f}%)"
            w_lap = format_currency(res['Whole_LAP'])
            w_sav = f"{format_currency(res['Whole_Savings_Abs'])} ({res['Whole_Savings_Pct']:.1f}%)"
            
            output += f"{scenario:<12} | {t_lap:<12} | {t_sav:<15} | {w_lap:<12} | {w_sav:<15}\n"
            
        output += f"-" * 78 + "\n"
        output += "Note: Percent savings are calculated relative to the 0% (Base) scenario."
        return output
    except Exception as e:
        return f"Error executing scenario_tool: {str(e)}"
