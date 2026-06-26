"""
Streamlit Page: AI Assistant

This page integrates the LangChain conversational agent, displaying chat history and dynamic tool execution logs.
"""

import streamlit as st
import os
import sys

# Add parent directory to path to support agent/pricing imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.router import invoke_pricing_agent
from app.theme import inject_theme


# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Actuarial Assistant",
    page_icon="💬",
    layout="wide"
)

inject_theme()

# -----------------------------------------------------------------------------
# HEADER
# -----------------------------------------------------------------------------
st.markdown("""
<div class="hero-dark" style="padding: 40px 50px;">
    <div class="hero-dark-content">
        <div class="hero-dark-title" style="font-size: 1.7rem;">💬 AI Actuarial Assistant</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    "<p style='color:#6b7280; font-size:0.95rem; margin-top:18px;'>"
    "Engage with an intelligent agent that leverages custom actuarial tools to run pricing calculations, "
    "compare scenarios, evaluate sensitivity curves, and generate comprehensive actuarial reports.</p>",
    unsafe_allow_html=True
)

st.markdown('<hr class="glass-divider">', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# API KEY MANAGEMENT (SIDEBAR)
# -----------------------------------------------------------------------------
st.sidebar.title("🔑 Credentials")

user_api_key = st.sidebar.text_input(
    "Enter your Gemini API Key:",
    type="password",
    placeholder="AIza...",
    help="Get a free key at https://aistudio.google.com/app/apikey"
)
if user_api_key:
    api_key_to_use = user_api_key
    st.sidebar.success("✅ API Key configured.")
else:
    st.sidebar.info(
        "Enter your Gemini API Key above to activate the assistant.\n\n"
        "Get a free key at [aistudio.google.com](https://aistudio.google.com/app/apikey)"
    )
    api_key_to_use = None

# Sample prompts helper
st.sidebar.markdown("### 💡 Try Asking:")
sample_prompts = [
    "Compare premiums under 0%, 1%, and 2% mortality improvement.",
    "Calculate term life premium for age 40 male, 20 year term, sum assured 10 lakhs at 6% interest.",
    "What happens to Whole Life premiums for a female age 30 if we apply a 1.2x mortality shock?",
    "Generate pricing report for a 45-year-old female, 15-year term, 20,00,000 sum assured.",
    "What is the gross premium and profit loading for a 40-year-old, 10-year term, sum assured 10 lakhs, at 4% interest rate?",
    "How does 1% mortality improvement affect profit loading for a 35-year-old, 20-year term policy?",
    "Calculate gross premium with 3% initial expense and 10% profit margin for age 50, 15-year term, sum assured 15 lakhs."
]

for prompt in sample_prompts:
    if st.sidebar.button(prompt, use_container_width=True):
        st.session_state.prompt_query = prompt

# -----------------------------------------------------------------------------
# CONVERSATION SESSION STATE
# -----------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I am your AI Actuarial Consultant. I can help you compute life premiums, "
                   "model scenario adjustments, perform sensitivity studies, and draft professional reports. How can I assist you today?"
    })

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------------------------------------------------------
# CHAT INPUT — ALWAYS CALLED UNCONDITIONALLY (fixes disappearing input bug)
# -----------------------------------------------------------------------------
chat_input = st.chat_input("Type your question here...")

# Determine query: a sidebar sample-prompt click takes priority over a
# fresh chat_input value, but chat_input is still always rendered above.
user_query = None
if "prompt_query" in st.session_state and st.session_state.prompt_query:
    user_query = st.session_state.prompt_query
    st.session_state.prompt_query = None
elif chat_input:
    user_query = chat_input

# -----------------------------------------------------------------------------
# EXECUTION
# -----------------------------------------------------------------------------
if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    if not api_key_to_use:
        with st.chat_message("assistant"):
            err_msg = "Please enter a valid **Gemini API Key** in the sidebar or save it in your `.env` file to activate the AI assistant."
            st.error(err_msg)
            st.session_state.messages.append({"role": "assistant", "content": err_msg})
    else:
        with st.chat_message("assistant"):
            with st.spinner("AI Consulting Agent is thinking and executing tools..."):
                response = invoke_pricing_agent(
                    query=user_query,
                    chat_history=st.session_state.chat_history,
                    gemini_api_key=api_key_to_use
                )

                steps = response.get('intermediate_steps', [])
                if steps:
                    with st.expander("🛠️ Tool Executions & Actuarial reasoning trace", expanded=True):
                        for tool_name, tool_args, observation in steps:
                            st.markdown(f"**Action Called:** `{tool_name}`")
                            st.markdown(f"**Arguments:** `{tool_args}`")
                            st.text_area("Result:", value=str(observation), height=150)
                            st.markdown("---")

                final_output = response.get('output', 'No response.')
                st.markdown(final_output)

                st.session_state.messages.append({"role": "assistant", "content": final_output})
                st.session_state.chat_history.append(("human", user_query))
                st.session_state.chat_history.append(("ai", final_output))

    # Rerun so the new messages render in the normal history loop above
    # the chat_input, keeping the input box anchored at the bottom.
    st.rerun()