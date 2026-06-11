# 📊 Mortality Pricing Agent & Actuarial Dashboard

An interactive actuarial pricing and sensitivity analysis engine utilizing centralized assumptions in `config.py` and the life table in `data/morality_table.csv`.

## 📁 Repository Structure
```
mortality-pricing-agent/
│
├── data/
│   └── morality_table.csv        # Baseline life table (qx rates)
│
├── notebooks/
│   ├── pricing_engine.ipynb      # Actuarial math, NSP, and LAP validation
│   ├── sensitivity_analysis.ipynb# Interest rate & mortality shock simulations
│   └── chatbot.ipynb             # AI agent / LLM integration workspace
│
├── app/
│   └── streamlit_app.py          # Interactive Streamlit pricing dashboard
│
├── docs/
│   └── final_report.docx         # Actuarial summary report
│
├── config.py                     # Centralized assumptions (rates, scenarios, ages)
└── README.md                     # Setup and documentation guide
```

---

## 🛠️ Features Completed
1. **Centralized Configuration (`config.py`)**: All defaults (6% base interest rate, ₹10,00,000 sum assured, entry age, term limits) and mortality improvement scenarios (0%, 0.5%, 1.0%, 2.0%) are configured in one file.
2. **Interactive Streamlit Dashboard**: 
    *   Computes **Net Single Premiums (NSP)** and **Net Level Annual Premiums (LAP)** for both **Term Life** and **Whole Life** products dynamically.
    *   Imports and adjusts calculations based on configuration parameters.
    *   Embeds interactive Plotly charts showing survival probabilities ($tpx$) and comparisons of baseline vs. improved mortality rates ($qx$).
3. **Actuarial Notebooks**: Fully implemented and updated to pull inputs from `config.py` and evaluate premium sensitivity mathematically.

---

## 🚀 Setup & Execution

### 1. Installation
Install the required dependencies using pip3:
```bash
pip3 install streamlit pandas numpy plotly python-docx matplotlib
```

### 2. Run the Streamlit App
Launch the actuarial dashboard locally:
```bash
python3 -m streamlit run app/streamlit_app.py
```

### 3. Run Notebooks
You can inspect or run the calculations step-by-step using Jupyter:
```bash
jupyter notebook notebooks/pricing_engine.ipynb
```

---

## 📅 Build Plan Status & Next Steps
*   **[x] Day 1-2**: Project setup, loading `morality_table.csv`, and writing `config.py` (Complete).
*   **[x] Day 3-9**: Pricing calculations, mortality improvement scenarios, and sensitivity plots (Complete).
*   **[x] Day 10-11**: Core interactive dashboard and Plotly chart embedding (Complete).
*   **[ ] Day 12-13**: Developing the LangChain/Gemini AI Agent tool and integrating the Chatbot tab back into the Streamlit UI (Next).
