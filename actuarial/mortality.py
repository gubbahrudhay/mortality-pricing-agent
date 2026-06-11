import os
import pandas as pd
import numpy as np
import sys

# Add parent directory to path to support config imports when run as scripts
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

def load_raw_table(csv_path="data/raw/mortality_table.csv"):
    """
    Loads the baseline mortality table from the specified CSV path.
    """
    if not os.path.exists(csv_path):
        # Fallback to local import if called from subdirectories
        resolved_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', csv_path))
        if os.path.exists(resolved_path):
            csv_path = resolved_path
        else:
            raise FileNotFoundError(f"Mortality table file not found at {csv_path}")
    
    df = pd.read_csv(csv_path)
    
    # Ensure correct columns
    if 'Age' not in df.columns or 'qx' not in df.columns:
        raise ValueError("Mortality table must contain 'Age' and 'qx' columns.")
        
    return df

def get_improved_mortality_rates(df_mort, gender, improvement_rate, gender_factors=None):
    """
    Applies gender factor and annual compound mortality improvement to baseline qx rates.
    qx_improved = qx_base * gender_factor * (1 - improvement_rate)
    """
    if gender_factors is None:
        gender_factors = config.GENDER_FACTORS
        
    base_rates = df_mort['qx'].values
    gender_factor = gender_factors.get(gender, 1.0)
    
    # Apply improvement rate (compound reduction in mortality rates)
    improved_rates = np.clip(base_rates * gender_factor * (1.0 - improvement_rate), 0.0, 1.0)
    return improved_rates

def get_survival_probabilities(improved_rates, age, term):
    """
    Computes survival probability (tpx) for each policy year t.
    tpx = product_{s=0}^{t-1} (1 - q_{x+s})
    Returns a numpy array of length term + 1, where index t corresponds to survival prob at age + t.
    """
    max_periods = len(improved_rates) - age
    n = min(term, max_periods - 1)
    
    tpx = np.zeros(n + 1)
    tpx[0] = 1.0 # Probability of surviving 0 years is 1.0
    
    for t in range(1, n + 1):
        tpx[t] = tpx[t-1] * (1.0 - improved_rates[age + t - 1])
        
    return tpx

def export_improvement_table(df_mort, gender_factors=None, scenarios=None, output_path="data/processed/mortality_improvement_table.csv"):
    """
    Generates a consolidated table comparing qx rates for Males/Females across all configured scenarios.
    """
    if gender_factors is None:
        gender_factors = config.GENDER_FACTORS
    if scenarios is None:
        scenarios = config.IMPROVEMENT_SCENARIOS
        
    result_df = pd.DataFrame({'Age': df_mort['Age']})
    
    for gender in gender_factors.keys():
        for scenario_name, improvement_rate in scenarios.items():
            col_name = f"{gender}_{scenario_name.replace(' ', '_').replace('(', '').replace(')', '')}"
            improved_rates = get_improved_mortality_rates(df_mort, gender, improvement_rate, gender_factors)
            result_df[col_name] = improved_rates
            
    # Ensure parent directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    result_df.to_csv(output_path, index=False)
    return result_df

if __name__ == "__main__":
    # Test execution
    df = load_raw_table()
    print(f"Loaded {len(df)} rows from raw table.")
    processed_df = export_improvement_table(df)
    print(f"Exported processed improvement table to data/processed/mortality_improvement_table.csv")
