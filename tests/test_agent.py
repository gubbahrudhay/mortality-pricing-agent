"""
Unit Tests: Agent Tools

This module executes pytest tests validating direct local invocation of custom LangChain tools.
"""

import os
import sys
import pytest

# Add parent directory to path to support config/pricing imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.pricing_tool import pricing_tool
from tools.scenario_tool import scenario_tool
from tools.sensitivity_tool import sensitivity_tool
from tools.explanation_tool import explanation_tool

def test_pricing_tool():
    res = pricing_tool.invoke({
        "age": 35,
        "gender": "Male",
        "term": 20,
        "sum_assured": 1000000.0,
        "interest_rate": 6.0,
        "improvement_rate": 0.01
    })
    
    assert "Actuarial Pricing Results" in res
    assert "Term Life Insurance" in res
    assert "Whole Life Insurance" in res
    assert "₹" in res

def test_scenario_tool():
    res = scenario_tool.invoke({
        "age": 35,
        "gender": "Male",
        "term": 20,
        "sum_assured": 1000000.0,
        "interest_rate": 6.0
    })
    
    assert "Improvement Scenario Comparison" in res
    assert "0% (Base)" in res
    assert "2.0%" in res

def test_sensitivity_tool():
    # Interest sensitivity
    res_int = sensitivity_tool.invoke({
        "age": 35,
        "gender": "Male",
        "term": 20,
        "sum_assured": 1000000.0,
        "interest_rate": 6.0,
        "improvement_rate": 0.01,
        "sensitivity_type": "interest"
    })
    assert "Interest Rate Sensitivity Analysis" in res_int
    assert "1.00%" in res_int
    assert "12.00%" in res_int
    
    # Shock sensitivity
    res_shock = sensitivity_tool.invoke({
        "age": 35,
        "gender": "Male",
        "term": 20,
        "sum_assured": 1000000.0,
        "interest_rate": 6.0,
        "improvement_rate": 0.01,
        "sensitivity_type": "shock"
    })
    assert "Mortality Shock" in res_shock
    assert "0.80x" in res_shock
    assert "1.50x" in res_shock

def test_explanation_tool():
    res = explanation_tool.invoke({
        "age": 35,
        "gender": "Male",
        "term": 20,
        "sum_assured": 1000000.0,
        "interest_rate": 6.0,
        "improvement_rate": 0.01
    })
    
    assert "ACTUARIAL PRICING & RISK ANALYSIS REPORT" in res
    assert "Premium Summary Table" in res
    assert "Expected Claim Distribution" in res
