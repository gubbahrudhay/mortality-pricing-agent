import numpy as np
import pandas as pd

# Load mortality table
df = pd.read_csv("IALM2012_14_Page2.csv")
base_qx = dict(zip(df["Age"], df["qx"]))

def compute_term_premium(age, term, base_qx, improvement_rate, interest_rate=0.07):
    APV_claims  = 0.0
    APV_annuity = 0.0
    survival_prob = 1.0
    v = 1 / (1 + interest_rate)

    for t in range(term):
        improved_qx = base_qx[age + t] * ((1 - improvement_rate) ** t)
        APV_claims  += (v ** (t + 1)) * survival_prob * improved_qx
        APV_annuity += (v ** t)       * survival_prob
        survival_prob *= (1 - improved_qx)

    return APV_claims / APV_annuity

if __name__ == "__main__":
    premium = compute_term_premium(age=35, term=20, base_qx=base_qx, improvement_rate=0.01)
    print(f"Annual premium for ₹10 lakh policy: ₹{premium * 1_000_000:,.0f}")