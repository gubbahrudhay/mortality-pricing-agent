"""
Gross Premium Sensitivity Analysis

Analyzes the impact of mortality improvement rates on Gross Premium
and Profit Loading: "look at the impact of mortality improvement on
gross premium and profit loadings at different mortality improvement rates."
"""

import os
import sys
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from actuarial.gross_premium import calculate_gross_premium


def analyze_gross_premium_mortality_sensitivity(
    age,
    term,
    sum_assured,
    interest_rate_pct,
    df_mort,
    improvement_rates=(0.0, 0.01, 0.02, 0.03),
    initial_expense_pct=0.02,
    renewal_expense=500,
    contingency_pct=0.02,
    profit_margin_pct=0.08,
):
    """
    Runs calculate_gross_premium across a list of mortality improvement rates
    and returns a DataFrame comparing Net Premium, Gross Premium, and
    Profit Loading at each rate, plus % change vs the 0% baseline.
    """
    rows = []
    for rate in improvement_rates:
        result = calculate_gross_premium(
            age=age,
            term=term,
            sum_assured=sum_assured,
            interest_rate_pct=interest_rate_pct,
            improvement_rate=rate,
            df_mort=df_mort,
            initial_expense_pct=initial_expense_pct,
            renewal_expense=renewal_expense,
            contingency_pct=contingency_pct,
            profit_margin_pct=profit_margin_pct,
        )
        rows.append({
            "Improvement Rate": f"{rate:.1%}",
            "Net Premium": round(result["net_premium"], 2),
            "Loaded Premium": round(result["loaded_premium"], 2),
            "Gross Premium": round(result["gross_premium"], 2),
            "Profit Loading ($)": round(result["profit_loading"], 2),
            "Profit Loading (% of NP)": f"{result['profit_loading_pct_of_np']:.2%}",
        })

    df = pd.DataFrame(rows)

    base_gp = df.loc[df["Improvement Rate"] == "0.0%", "Gross Premium"].values[0]
    base_pl = df.loc[df["Improvement Rate"] == "0.0%", "Profit Loading ($)"].values[0]
    df["Gross Premium Δ vs Base"] = df["Gross Premium"].apply(lambda x: f"{(x - base_gp) / base_gp:+.2%}")
    df["Profit Loading Δ vs Base"] = df["Profit Loading ($)"].apply(lambda x: f"{(x - base_pl) / base_pl:+.2%}")

    return df


if __name__ == "__main__":
    from actuarial.mortality import load_raw_table
    df_mort = load_raw_table()
    df = analyze_gross_premium_mortality_sensitivity(
        age=40,
        term=10,
        sum_assured=1_000_000,
        interest_rate_pct=4.0,
        df_mort=df_mort,
    )
    print(df.to_string(index=False))