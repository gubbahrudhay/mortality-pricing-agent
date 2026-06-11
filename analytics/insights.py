import pandas as pd
import numpy as np

def generate_pricing_insights(pricing_results):
    """
    Generates natural language insights from single pricing calculation results.
    """
    lap_term = pricing_results['lap_term']
    nsp_term = pricing_results['nsp_term']
    lap_whole = pricing_results['lap_whole']
    nsp_whole = pricing_results['nsp_whole']
    age = pricing_results['age']
    term = pricing_results['term']
    gender = pricing_results['gender']
    sum_assured = pricing_results['sum_assured']
    interest_rate = pricing_results['interest_rate']
    improvement_rate = pricing_results['improvement_rate']
    
    insights = []
    
    # Insight 1: Premium structures comparison
    ratio = (lap_term / sum_assured) * 1000.0
    insights.append(
        f"For a **{age}-year-old {gender}**, the Term Life annual premium rate is **{ratio:.2f} per 1,000** of sum assured, "
        f"resulting in an annual level premium of **₹{lap_term:,.2f}** for **{term} years** of coverage."
    )
    
    # Insight 2: NSP vs LAP explanation
    total_lap_term = lap_term * term
    saving_nsp = total_lap_term - nsp_term
    insights.append(
        f"Opting for a **Net Single Premium (lump sum)** of **₹{nsp_term:,.2f}** instead of paying level annual premiums saves "
        f"a nominal total of **₹{saving_nsp:,.2f}** over the {term}-year term, reflecting a **{(nsp_term/total_lap_term * 100):.1f}%** "
        f"discount due to the time value of money and survival probability adjustments."
    )
    
    # Insight 3: Whole Life comparison
    whole_vs_term = lap_whole / lap_term if lap_term > 0 else 1.0
    insights.append(
        f"Whole Life coverage requires an annual level premium of **₹{lap_whole:,.2f}**, which is **{whole_vs_term:.2f}x** higher "
        f"than Term Life. This premium multiplier accounts for the certainty of a claim payout under Whole Life and its extended protection duration."
    )
    
    # Insight 4: Mortality improvement impact
    if improvement_rate > 0:
        insights.append(
            f"The **{improvement_rate*100:.1f}% annual mortality improvement** compound reduction has been successfully applied, "
            f"meaning mortality rates ($q_x$) are lowered each year, leading to higher survival rates and lower premiums."
        )
        
    return insights

def generate_sensitivity_insights(interest_sensitivity, shock_sensitivity):
    """
    Analyzes sensitivity arrays to produce premium elasticity insights.
    """
    df_interest = pd.DataFrame(interest_sensitivity)
    df_shock = pd.DataFrame(shock_sensitivity)
    
    insights = []
    
    # Interest rate elasticity
    if len(df_interest) >= 2:
        rates = df_interest['Interest_Rate'].values
        term_laps = df_interest['Term_LAP'].values
        
        # Calculate premium reduction per 1% increase in interest rate (from base/lowest to highest)
        pct_drops = []
        for i in range(len(rates) - 1):
            change_rate = rates[i+1] - rates[i]
            change_lap = (term_laps[i] - term_laps[i+1]) / term_laps[i]
            pct_drops.append((change_lap * 100) / change_rate)
            
        avg_elasticity = np.mean(pct_drops)
        insights.append(
            f"**Interest Rate Elasticity**: On average, a **1.0% increase** in the discount rate decreases the Term Life level annual premium "
            f"by approximately **{avg_elasticity:.2f}%**. Actuarial discounting has a highly compounding effect over longer policy terms."
        )
        
    # Mortality shock elasticity
    if len(df_shock) >= 2:
        multipliers = df_shock['Mortality_Multiplier'].values
        term_laps = df_shock['Term_LAP'].values
        
        # Calculate percentage premium increase per 10% increase in mortality multiplier
        pct_rises = []
        for i in range(len(multipliers) - 1):
            change_mult = (multipliers[i+1] - multipliers[i]) * 10 # 10% unit
            change_lap = (term_laps[i+1] - term_laps[i]) / term_laps[i]
            pct_rises.append((change_lap * 100) / change_mult)
            
        avg_shock_impact = np.mean(pct_rises)
        insights.append(
            f"**Mortality Risk Sensitivity**: A **10% increase** in baseline mortality rates (shock multiplier) leads to an estimated "
            f"**{avg_shock_impact:.2f}% increase** in level annual premiums. Underwriting shocks directly alter expected claims costs."
        )
        
    return insights
