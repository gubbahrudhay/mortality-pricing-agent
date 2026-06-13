# config.py

# Actuarial assumptions
INTEREST_RATE = 0.06           # 6% annual discount rate
SUM_ASSURED   = 1_000_000      # ₹10,00,000 default

# Mortality improvement scenarios to test
IMPROVEMENT_SCENARIOS = {
    "0% (Base)":  0.00,
    "0.5%":       0.005,
    "1.0%":       0.01,
    "2.0%":       0.02,
}

# Actuarial adjustment factors
GENDER_FACTORS = {
    "Male": 1.00,
    "Female": 0.85
}

# Default policy parameters
DEFAULT_AGE  = 35
DEFAULT_TERM = 20

# Age range covered by your mortality table
MIN_AGE = 0
MAX_AGE = 100
