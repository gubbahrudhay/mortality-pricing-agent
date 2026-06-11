import numpy as np

def calculate_pricing(age, gender, term, sum_assured, interest_rate, improvement_rate, df_mort, gender_factors):
    """
    Computes Net Single Premiums (NSP) and Net Level Annual Premiums (LAP)
    for Term Life and Whole Life insurance products.
    """
    i = interest_rate / 100.0
    v = 1 / (1 + i)
    
    # Extract baseline qx rates
    base_rates = df_mort['qx'].values
    
    # Get gender factor
    gender_factor = gender_factors[gender]
    
    # Apply gender factor and mortality improvement scenario
    improved_rates = np.clip(base_rates * gender_factor * (1.0 - improvement_rate), 0.0, 1.0)
    
    max_periods = len(df_mort) - age
    
    # Compute survival probabilities tpx
    tpx = np.zeros(max_periods)
    tpx[0] = 1.0
    for t in range(1, max_periods):
        tpx[t] = tpx[t-1] * (1.0 - improved_rates[age + t - 1])
        
    # Term Life NSP
    n = min(term, max_periods - 1)
    nsp_term = 0.0
    for t in range(n):
        nsp_term += (v ** (t + 1)) * tpx[t] * improved_rates[age + t]
    nsp_term_val = nsp_term * sum_assured
    
    # Whole Life NSP
    nsp_whole = 0.0
    for t in range(max_periods - 1):
        nsp_whole += (v ** (t + 1)) * tpx[t] * improved_rates[age + t]
    nsp_whole_val = nsp_whole * sum_assured
    
    # Annuity due factors (to convert NSP to Level Annual Premiums)
    a_due_term = 0.0
    for t in range(n):
        a_due_term += (v ** t) * tpx[t]
    lap_term_val = nsp_term_val / a_due_term if a_due_term > 0 else nsp_term_val
    
    a_due_whole = 0.0
    for t in range(max_periods - 1):
        a_due_whole += (v ** t) * tpx[t]
    lap_whole_val = nsp_whole_val / a_due_whole if a_due_whole > 0 else nsp_whole_val
    
    return {
        'nsp_term': nsp_term_val,
        'lap_term': lap_term_val,
        'nsp_whole': nsp_whole_val,
        'lap_whole': lap_whole_val,
        'tpx': tpx[:n+1],
        'ages_axis': list(range(age, age + n + 1)),
        'improved_rates': improved_rates[age:age+n],
        'base_rates': base_rates[age:age+n]
    }
