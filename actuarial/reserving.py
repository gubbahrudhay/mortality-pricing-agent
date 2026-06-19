"""
Actuarial Reserving Module

Computes the Prospective Gross Premium Reserve for a Term Life policy at
every policy duration t, following the methodology in the
Gross_Premium_Reserve_Age40_Term30.xlsx illustration:

    tV = SA x A^1(x+t : n-t)  +  PV(Future Expenses)_t  -  P x ä(x+t : n-t)

Where:
    A^1(x+t : n-t)   = term assurance EPV factor at duration t (remaining term)
    ä(x+t : n-t)     = annuity-due EPV factor at duration t (remaining term)
    PV(Future Expenses)_t = EPV, as of duration t, of all future renewal
                             expenses (e1 x P) and fixed policy fees (F),
                             for durations t, t+1, ..., n-1
    P                = Gross Annual Premium (solved once at issue via the
                        equivalence principle, in actuarial.gross_premium)

This reuses the existing IALM 2012-14 mortality engine (actuarial.mortality)
and the existing Gross Premium calculation (actuarial.gross_premium) so the
premium P and the reserve are always internally consistent.

Reserve sanity checks (matching the Excel):
    tV at t=0       = 0   (premium is solved by the equivalence principle)
    tV at t=n (mat.) = 0   (term assurance pays no maturity benefit)
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
from actuarial.mortality import get_improved_mortality_rates, get_survival_probabilities
from actuarial.pricing import calculate_discount_factor, calculate_annuity_due_factor


def _calculate_nsp_term_eoy(age, term, sum_assured, interest_rate_pct, improved_rates, tpx):
    """
    Term assurance EPV using END-OF-YEAR death benefit discounting (v^(t+1)),
    matching the convention used in the Gross_Premium_Reserve illustration.

    This intentionally does NOT reuse actuarial.pricing.calculate_nsp_term,
    which uses mid-year discounting (v^(t+0.5)) for the Pricing Calculator
    pages — a different, equally valid actuarial convention. Keeping this
    separate ensures the Reserving module reconciles exactly to the
    Gross_Premium_Reserve_Age40_Term30.xlsx illustration.
    """
    v = calculate_discount_factor(interest_rate_pct)
    max_periods = len(improved_rates) - age
    n = min(term, max_periods - 1)

    nsp_factor = 0.0
    for t in range(n):
        nsp_factor += (v ** (t + 1)) * tpx[t] * improved_rates[age + t]

    return nsp_factor * sum_assured


def calculate_reserve_schedule(
    age,
    term,
    sum_assured,
    interest_rate_pct,
    improvement_rate,
    df_mort,
    initial_expense_pct=0.5,
    renewal_expense_pct=0.05,
    fixed_fee=500,
    gross_premium=None,
):
    """
    Computes the Gross Premium Reserve at every duration t = 0, 1, ..., term
    for a Term Life policy.

    Note on expense convention: this reserving illustration uses
    PERCENTAGE-of-premium expense rates (e0 = initial expense % of premium,
    e1 = renewal expense % of premium) plus a flat fixed fee F per year,
    which differs from the Gross Premium Pricing page's convention
    (initial expense as % of Sum Assured, flat renewal expense in Rs.).
    Both are legitimate actuarial conventions; this module follows the
    convention used in the Gross_Premium_Reserve illustration so the
    reserve reconciles to it exactly.

    age, term, sum_assured, interest_rate_pct, improvement_rate, df_mort:
        same meaning as elsewhere in the codebase.
    initial_expense_pct: e0, initial expense as a fraction of Year-1 premium (e.g. 0.5 for 50%).
    renewal_expense_pct: e1, renewal expense as a fraction of premium in years 2..n (e.g. 0.05 for 5%).
    fixed_fee: F, flat policy maintenance fee charged every year (e.g. 500).
    gross_premium: if provided, use this premium instead of solving it via
        the equivalence principle (useful for consistency with the
        Gross Premium Pricing page's existing per-Sum-Assured expense
        convention). If None, P is solved using this module's own
        equivalence-principle formula matching the Excel exactly.

    Returns a list of dicts, one per duration t = 0..term, each containing:
        t, age_t, annuity_due, term_assurance_factor,
        pv_future_benefits, pv_future_expenses, pv_future_premiums,
        gross_premium_reserve
    """
    improved_rates = get_improved_mortality_rates(df_mort, improvement_rate, entry_age=age)
    tpx_full = get_survival_probabilities(improved_rates, age, term)

    v = calculate_discount_factor(interest_rate_pct)

    # --- Step 1: Solve Gross Premium P via the equivalence principle ---
    # P x ä(x:n) = SA x A^1(x:n) + e0 x P + F x ä(x:n) + e1 x P x (ä(x:n) - 1)
    # => P = [SA x A^1(x:n) + F x ä(x:n)] / [ä(x:n) x (1 - e1) - (e0 - e1)]
    if gross_premium is None:
        a_due_0 = calculate_annuity_due_factor(tpx_full, interest_rate_pct)
        nsp_0 = _calculate_nsp_term_eoy(age, term, sum_assured, interest_rate_pct, improved_rates, tpx_full)
        numerator = nsp_0 + fixed_fee * a_due_0
        denominator = a_due_0 * (1 - renewal_expense_pct) - (initial_expense_pct - renewal_expense_pct)
        gross_premium = numerator / denominator if denominator != 0 else 0.0

    P = gross_premium

    # --- Step 2: For each duration t, compute ä(x+t:n-t), A^1(x+t:n-t),
    #             PV future benefits, PV future expenses, PV future premiums,
    #             and the resulting reserve. ---
    schedule = []

    for t in range(term + 1):
        remaining_term = term - t

        if remaining_term <= 0:
            # Maturity: no future benefits, expenses, or premiums remain.
            schedule.append({
                't': t,
                'age_t': age + t,
                'annuity_due': 0.0,
                'term_assurance_factor': 0.0,
                'pv_future_benefits': 0.0,
                'pv_future_expenses': 0.0,
                'pv_future_premiums': 0.0,
                'gross_premium_reserve': 0.0,
            })
            continue

        # Survival probabilities re-based at duration t (k=0 means "alive at age+t")
        tpx_t = get_survival_probabilities(improved_rates, age + t, remaining_term)

        a_due_t = calculate_annuity_due_factor(tpx_t, interest_rate_pct)
        nsp_t = _calculate_nsp_term_eoy(age + t, remaining_term, sum_assured, interest_rate_pct, improved_rates, tpx_t)
        a1_factor_t = nsp_t / sum_assured if sum_assured else 0.0

        pv_future_benefits = nsp_t

        # PV of future expenses from duration t onward:
        #   - renewal expense (e1 x P) at every future renewal year (t=0 itself
        #     uses e0 x P only if t==0; for t>=1, use e1 x P throughout)
        #   - fixed fee F every year, including the current duration
        # Following the Excel's "cost(t) = e0*P + F at t=0, else e1*P + F" pattern,
        # but re-based here at duration t (so for t>0, all remaining years use e1).
        pv_future_expenses = 0.0
        for k in range(remaining_term):
            if t == 0 and k == 0:
                cost_k = initial_expense_pct * P + fixed_fee
            else:
                cost_k = renewal_expense_pct * P + fixed_fee
            pv_future_expenses += (v ** k) * tpx_t[k] * cost_k

        pv_future_premiums = P * a_due_t

        reserve = pv_future_benefits + pv_future_expenses - pv_future_premiums

        schedule.append({
            't': t,
            'age_t': age + t,
            'annuity_due': a_due_t,
            'term_assurance_factor': a1_factor_t,
            'pv_future_benefits': pv_future_benefits,
            'pv_future_expenses': pv_future_expenses,
            'pv_future_premiums': pv_future_premiums,
            'gross_premium_reserve': reserve,
        })

    return {
        'gross_premium': P,
        'schedule': schedule,
    }


def get_reserve_at_duration(
    age,
    term,
    sum_assured,
    interest_rate_pct,
    improvement_rate,
    df_mort,
    duration,
    initial_expense_pct=0.5,
    renewal_expense_pct=0.05,
    fixed_fee=500,
    gross_premium=None,
):
    """
    Convenience function: returns the Gross Premium Reserve at a single
    specified duration t, along with the supporting figures.
    """
    result = calculate_reserve_schedule(
        age, term, sum_assured, interest_rate_pct, improvement_rate, df_mort,
        initial_expense_pct, renewal_expense_pct, fixed_fee, gross_premium,
    )
    for row in result['schedule']:
        if row['t'] == duration:
            return {
                'gross_premium': result['gross_premium'],
                **row,
            }
    raise ValueError(f"Duration {duration} is out of range for a {term}-year policy.")


if __name__ == "__main__":
    from actuarial.mortality import load_raw_table
    df_mort = load_raw_table()

    result = calculate_reserve_schedule(
        age=40,
        term=30,
        sum_assured=1_000_000,
        interest_rate_pct=6.0,
        improvement_rate=0.0,
        df_mort=df_mort,
        initial_expense_pct=0.5,
        renewal_expense_pct=0.05,
        fixed_fee=500,
    )

    print(f"Gross Premium (P): {result['gross_premium']:.2f}")
    print(f"{'t':<4}{'Age':<6}{'Reserve':>14}")
    for row in result['schedule']:
        print(f"{row['t']:<4}{row['age_t']:<6}{row['gross_premium_reserve']:>14.2f}")