# Deployment Guide

This guide describes how to run the application locally or deploy it to a staging/production server.

## 1. Local Execution

To run the multi-page Streamlit pricing dashboard locally:

1. Ensure the virtual environment is active:
   ```bash
   source .venv/bin/activate
   ```
2. Configure your API key in a `.env` file in the root:
   ```bash
   cp .env.example .env
   # Open .env and set GEMINI_API_KEY
   ```
3. Run the Streamlit application:
   ```bash
   streamlit run app/main.py
   ```
4. Access the dashboard in your web browser at `http://localhost:8501`.

---

## 2. Deploying to Streamlit Community Cloud

Streamlit Community Cloud is the easiest way to share and deploy the app:

1. Push your repository to GitHub.
2. Log in to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click "New App", select your repository, branch, and set the main file path to `app/main.py`.
4. In the "Advanced Settings", add your environment secrets:
   ```toml
   GEMINI_API_KEY = "your_actual_gemini_api_key"
   ```
5. Click "Deploy". The app will build, install the dependencies listed in `requirements.txt`, and deploy online.
