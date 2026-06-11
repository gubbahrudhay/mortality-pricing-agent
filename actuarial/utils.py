"""
Actuarial Utilities Module

This module provides common utilities such as currency and percentage formatting helpers,
and batch loading pricing scenarios from JSON files.
"""

import os
import json
import sys

# Add parent directory to path to support config imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

def format_currency(val, symbol="₹"):
    """
    Formats a numeric value as currency (Indian Rupee style formatting by default).
    """
    if val is None:
        return ""
    # Standard format: 1,000,000.00 (We can also implement custom Indian comma grouping if desired,
    # but standard comma grouping with Rupee symbol is typical in corporate systems).
    return f"{symbol}{val:,.2f}"

def format_percentage(val):
    """
    Formats a decimal fraction as percentage (e.g. 0.05 -> 5.00%).
    """
    if val is None:
        return ""
    return f"{val * 100:.2f}%"

def load_pricing_scenarios_from_json(json_path="data/sample_inputs/pricing_scenarios.json"):
    """
    Loads sample pricing scenarios from a JSON file.
    If the file does not exist, it creates a default one.
    """
    if not os.path.exists(json_path):
        resolved_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', json_path))
        if os.path.exists(resolved_path):
            json_path = resolved_path
        else:
            # Create a default configuration structure
            default_scenarios = {
                "default_male_35": {
                    "age": 35,
                    "gender": "Male",
                    "term": 20,
                    "sum_assured": 1000000,
                    "interest_rate": 6.0,
                    "improvement_rate": 0.01
                },
                "default_female_35": {
                    "age": 35,
                    "gender": "Female",
                    "term": 20,
                    "sum_assured": 1000000,
                    "interest_rate": 6.0,
                    "improvement_rate": 0.01
                },
                "senior_male_60": {
                    "age": 60,
                    "gender": "Male",
                    "term": 15,
                    "sum_assured": 500000,
                    "interest_rate": 5.5,
                    "improvement_rate": 0.005
                }
            }
            os.makedirs(os.path.dirname(json_path), exist_ok=True)
            with open(json_path, 'w') as f:
                json.dump(default_scenarios, f, indent=4)
            return default_scenarios
            
    with open(json_path, 'r') as f:
        return json.load(f)
