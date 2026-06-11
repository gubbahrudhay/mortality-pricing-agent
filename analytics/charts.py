"""
Analytics Charts Module

This module generates reusable Plotly figure objects for survival curves, mortality comparisons,
interest rate sensitivities, mortality shocks, and scenario comparisons.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def build_survival_curve_chart(ages, tpx, term, theme="plotly_dark"):
    """
    Plots survival probability (tpx) over the policy term.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ages,
        y=tpx,
        mode='lines+markers',
        name='Survival Probability (tpx)',
        line=dict(color='#0ea5e9', width=3),
        marker=dict(size=6)
    ))
    fig.update_layout(
        title=f"Survival Probability Curve over the Policy Term ({term} Years)",
        xaxis_title="Age",
        yaxis_title="Survival Probability (tpx)",
        template=theme,
        height=380,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    return fig

def build_mortality_rate_chart(ages, base_rates, improved_rates, gender, theme="plotly_dark"):
    """
    Plots baseline vs improved mortality rate comparison (qx).
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ages,
        y=base_rates,
        mode='lines',
        name='Baseline Mortality (qx)',
        line=dict(color='#64748b', width=2, dash='dash')
    ))
    fig.add_trace(go.Scatter(
        x=ages,
        y=improved_rates,
        mode='lines+markers',
        name='Scenario Mortality (qx)',
        line=dict(color='#f43f5e', width=3),
        marker=dict(size=6)
    ))
    fig.update_layout(
        title=f"Mortality Probability Comparison (qx) - {gender}",
        xaxis_title="Age",
        yaxis_title="Mortality Probability (qx)",
        template=theme,
        height=380,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    return fig

def build_interest_rate_sensitivity_chart(sensitivity_data, theme="plotly_dark"):
    """
    Plots premiums (Term & Whole Life) as a function of interest rate.
    """
    df = pd.DataFrame(sensitivity_data)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Interest_Rate'],
        y=df['Term_LAP'],
        mode='lines+markers',
        name='Term Life Premium (LAP)',
        line=dict(color='#818cf8', width=3),
        marker=dict(size=6)
    ))
    fig.add_trace(go.Scatter(
        x=df['Interest_Rate'],
        y=df['Whole_LAP'],
        mode='lines+markers',
        name='Whole Life Premium (LAP)',
        line=dict(color='#34d399', width=2),
        marker=dict(size=6)
    ))
    fig.update_layout(
        title="Premium Sensitivity to Discount / Interest Rates",
        xaxis_title="Interest Rate (%)",
        yaxis_title="Level Annual Premium (LAP)",
        template=theme,
        height=380,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    return fig

def build_mortality_shock_chart(sensitivity_data, theme="plotly_dark"):
    """
    Plots premiums (Term & Whole Life) as a function of mortality shock multiplier.
    """
    df = pd.DataFrame(sensitivity_data)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Mortality_Multiplier'],
        y=df['Term_LAP'],
        mode='lines+markers',
        name='Term Life Premium (LAP)',
        line=dict(color='#f43f5e', width=3),
        marker=dict(size=6)
    ))
    fig.add_trace(go.Scatter(
        x=df['Mortality_Multiplier'],
        y=df['Whole_LAP'],
        mode='lines+markers',
        name='Whole Life Premium (LAP)',
        line=dict(color='#fbbf24', width=2),
        marker=dict(size=6)
    ))
    fig.update_layout(
        title="Premium Sensitivity to Mortality Shocks (Multiplier)",
        xaxis_title="Mortality Multiplier (1.0x = Base)",
        yaxis_title="Level Annual Premium (LAP)",
        template=theme,
        height=380,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    return fig

def build_scenario_comparison_chart(comparison_data, theme="plotly_dark"):
    """
    Bar chart comparing LAP premiums across improvement scenarios.
    """
    df = pd.DataFrame(comparison_data)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['Scenario'],
        y=df['Term_LAP'],
        name='Term Life LAP',
        marker_color='#6366f1'
    ))
    fig.add_trace(go.Bar(
        x=df['Scenario'],
        y=df['Whole_LAP'],
        name='Whole Life LAP',
        marker_color='#10b981'
    ))
    fig.update_layout(
        title="Level Annual Premiums across Mortality Improvement Scenarios",
        xaxis_title="Scenario",
        yaxis_title="Annual Premium (LAP)",
        barmode='group',
        template=theme,
        height=380,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    return fig
