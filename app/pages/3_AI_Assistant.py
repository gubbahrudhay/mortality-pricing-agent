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
from dotenv import load_dotenv
from app.theme import inject_theme


# Load env variables
load_dotenv()


# -------------------------------------------------------------------------
# PAGE CONFIGURATION & STYLING
# -------------------------------------------------------------------------

st.set_page_config(
    page_title="AI Actuarial Assistant",
    page_icon="💬",
    layout="wide"
)

inject_theme()



# -------------------------------------------------------------------------
# HEADER
# -------------------------------------------------------------------------

st.markdown("""
<div class="hero-dark" style="padding: 40px 50px;">
    <div class="hero-dark-content">
        <div class="hero-dark-title" style="font-size: 1.7rem;">
            💬 AI Actuarial Assistant
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


st.markdown(
    "<p style='color:#6b7280; font-size:0.95rem; margin-top:18px;'>"
    "Engage with an intelligent agent that leverages custom actuarial tools "
    "to run pricing calculations, compare scenarios, evaluate sensitivity "
    "curves, and generate comprehensive actuarial reports."
    "</p>",
    unsafe_allow_html=True
)


st.markdown(
    '<hr class="glass-divider">',
    unsafe_allow_html=True
)



# -------------------------------------------------------------------------
# SESSION STATE
# -------------------------------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content":
            "Hello! I am your AI Actuarial Consultant. "
            "I can help you compute life premiums, model scenario adjustments, "
            "perform sensitivity studies, and draft professional reports. "
            "How can I assist you today?"
        }
    ]


if "chat_history" not in st.session_state:

    st.session_state.chat_history = []


if "prompt_query" not in st.session_state:

    st.session_state.prompt_query = None



# -------------------------------------------------------------------------
# SIDEBAR API KEY
# -------------------------------------------------------------------------

st.sidebar.title("🔑 Credentials")


env_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")


if env_key:

    st.sidebar.success(
        "✅ Gemini API Key detected in `.env` / environment."
    )

    api_key_to_use = env_key


else:

    user_api_key = st.sidebar.text_input(
        "Enter GEMINI_API_KEY:",
        type="password"
    )


    if user_api_key:

        api_key_to_use = user_api_key

        st.sidebar.success(
            "✅ Temporary API Key configured."
        )

    else:

        api_key_to_use = None

        st.sidebar.warning(
            "⚠️ Please configure GEMINI_API_KEY in `.env` "
            "or input it here to enable the agent."
        )



# -------------------------------------------------------------------------
# SAMPLE PROMPTS
# -------------------------------------------------------------------------

st.sidebar.markdown("### 💡 Try Asking:")


sample_prompts = [

    "Compare premiums under 0%, 1%, and 2% mortality improvement.",

    "Calculate term life premium for age 40 male, 20 year term, "
    "sum assured 10 lakhs at 6% interest.",

    "What happens to Whole Life premiums for a female age 30 "
    "if we apply a 1.2x mortality shock?",

    "Generate pricing report for a 45-year-old female, "
    "15-year term, 20,00,000 sum assured."

]


for i, prompt in enumerate(sample_prompts):

    if st.sidebar.button(
        prompt,
        key=f"prompt_{i}",
        width="stretch"
    ):

        st.session_state.prompt_query = prompt

        st.rerun()



# -------------------------------------------------------------------------
# CHAT HISTORY DISPLAY
# -------------------------------------------------------------------------

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])



# -------------------------------------------------------------------------
# USER INPUT
# -------------------------------------------------------------------------

user_query = None


if st.session_state.prompt_query:

    user_query = st.session_state.prompt_query
    st.session_state.prompt_query = None


# Always keep chat box available
chat_input = st.chat_input(
    "Type your question here..."
)


if chat_input:

    user_query = chat_input



# -------------------------------------------------------------------------
# AGENT EXECUTION
# -------------------------------------------------------------------------

if user_query:


    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query
        }
    )


    with st.chat_message("user"):

        st.markdown(user_query)



    if not api_key_to_use:


        error_message = (
            "Please enter a valid **Gemini API Key** "
            "in the sidebar or save it in your `.env` file."
        )


        with st.chat_message("assistant"):

            st.error(error_message)


        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": error_message
            }
        )



    else:


        with st.chat_message("assistant"):


            with st.spinner(
                "AI Consulting Agent is thinking and executing tools..."
            ):


                response = invoke_pricing_agent(

                    query=user_query,

                    chat_history=st.session_state.chat_history,

                    gemini_api_key=api_key_to_use

                )



                # ---------------------------------------------------------
                # TOOL EXECUTION LOGS
                # ---------------------------------------------------------

                steps = response.get(
                    "intermediate_steps",
                    []
                )


                if steps:


                    with st.expander(
                        "🛠️ Tool Executions & Actuarial reasoning trace",
                        expanded=True
                    ):


                        for tool_name, tool_args, observation in steps:


                            st.markdown(
                                f"**Action Called:** `{tool_name}`"
                            )


                            st.markdown(
                                f"**Arguments:** `{tool_args}`"
                            )


                            st.text_area(
                                "Result:",
                                value=str(observation),
                                height=150
                            )


                            st.markdown("---")



                # ---------------------------------------------------------
                # FIX GEMINI RESPONSE FORMAT
                # ---------------------------------------------------------

                raw_output = response.get(
                    "output",
                    "No response."
                )


                if isinstance(raw_output, list):

                    final_output = ""

                    for item in raw_output:

                        if isinstance(item, dict):

                            if "text" in item:

                                final_output += item["text"]

                        else:

                            final_output += str(item)


                else:

                    final_output = str(raw_output)



                # Display clean markdown response

                st.markdown(final_output)



                # Save clean response

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": final_output
                    }
                )



                # Update memory

                st.session_state.chat_history.append(
                    (
                        "human",
                        user_query
                    )
                )


                st.session_state.chat_history.append(
                    (
                        "ai",
                        final_output
                    )
                )
