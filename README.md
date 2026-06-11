# 📊 AI-Powered Mortality Improvement Pricing & Sensitivity Analyzer

An interactive actuarial pricing and sensitivity analysis engine utilizing centralized assumptions, compound mortality improvement scenarios, premium risk shock analysis, and an integrated LangChain Conversational AI Agent.

---

## 📁 Modular Directory Structure
```text
mortality-pricing-agent/
│
├── README.md                     # This documentation guide
├── requirements.txt              # Project library dependencies
├── .env.example                  # Environment key placeholders
├── .gitignore                    # Version control ignore rules
│
├── data/
│   ├── raw/
│   │   └── mortality_table.csv   # Baseline life table (qx rates)
│   │
│   └── sample_inputs/
│       └── pricing_scenarios.json # Saved scenario inputs
│
├── actuarial/
│   ├── mortality.py              # Life table loading & improvement projections
│   ├── pricing.py                # NSP, LAP and NPV claim cash flow calculators
│   ├── scenarios.py              # Multi-scenario premium comparisons
│   └── utils.py                  # Currency formatters & utilities
│
├── analytics/
│   ├── sensitivity_analysis.py   # Discount rate & multiplier shock simulations
│   ├── charts.py                 # Plotly curve visualizations
│   └── insights.py               # Data-driven text summary generators
│
├── tools/
│   ├── pricing_tool.py           # Tool wrapper for simple pricing calls
│   ├── scenario_tool.py          # Tool wrapper for scenario comparisons
│   ├── sensitivity_tool.py       # Tool wrapper for sensitivity curves
│   └── explanation_tool.py       # Tool wrapper for structured reports
│
├── agents/
│   ├── pricing_agent.py          # LangChain conversational tools agent config
│   ├── prompts.py                # System instructions & actuarial persona
│   └── router.py                 # Agent invocation entry point
│
├── app/
│   ├── main.py                   # Main landing page for Streamlit Dashboard
│   │
│   ├── components/
│   │   ├── charts.py             # Reusable streamlit plotting helpers
│   │   ├── inputs.py             # Sidebar parameter panels
│   │   └── tables.py             # Renderers for structured dataframes
│   │
│   └── pages/
│       ├── 1_Pricing_Calculator.py  # Page 1: Metric cards, survival curves, qx comparison
│       ├── 2_Scenario_Analysis.py   # Page 2: Scenario tables & sensitivity curves
│       └── 3_AI_Assistant.py        # Page 3: Conversational assistant with tool trace logging
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_pricing_engine.ipynb
│   ├── 03_sensitivity_analysis.ipynb
│   └── 04_agent_testing.ipynb
│
├── tests/
│   ├── test_pricing.py           # Unit tests for core actuarial models
│   ├── test_scenarios.py         # Unit tests for scenario comparisons
│   └── test_agent.py             # Unit tests for tool calling executions
│
└── deployment/
    ├── streamlit_config.toml     # Streamlit theme preferences
    └── deploy.md                 # Deployment & Hosting guide
```

---

## 🚀 Setup & Execution

### 1. Installation & Environment Configuration
Ensure you have the virtual environment configured and activated. Copy `.env.example` to `.env` and set your `GEMINI_API_KEY`:
```bash
# Clone/Open workspace
cd mortality-pricing-agent

# Create & configure .env
cp .env.example .env
# Open .env and write GEMINI_API_KEY="..."

# Install dependencies in the active virtual environment
.venv/bin/pip install -r requirements.txt
```

### 2. Run the Multi-Page Streamlit App
Launch the interactive dashboard locally:
```bash
.venv/bin/streamlit run app/main.py
```

### 3. Run Automated Tests
Execute the unit testing suite to verify premium calculations, sensitivities, and tool executions:
```bash
.venv/bin/pytest tests/
```

### 4. Interactive Notebooks
You can inspect or run the calculations step-by-step using Jupyter (registered under the `mortality-pricing-agent` kernel):
```bash
jupyter notebook notebooks/02_pricing_engine.ipynb
```
