"""
AI Pricing Agent Configuration
This module configures the ChatGoogleGenerativeAI (Gemini) LLM agent, binding custom actuarial tools
and setting up conversational prompts and memory structures.

Rewritten for LangChain 1.x using the unified create_agent API.
"""
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path to support config/pricing imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent

from agents.prompts import SYSTEM_PROMPT
from tools.pricing_tool import pricing_tool
from tools.scenario_tool import scenario_tool
from tools.sensitivity_tool import sensitivity_tool
from tools.explanation_tool import explanation_tool

# Load environment variables
load_dotenv()

# Make sure GOOGLE_API_KEY is mapped from GEMINI_API_KEY if needed
if "GEMINI_API_KEY" in os.environ and "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]


def get_pricing_agent(temperature=0.2, gemini_api_key=None):
    """
    Initializes and returns a LangChain 1.x agent bound with actuarial tools.

    The returned agent is invoked with:
        agent.invoke({"messages": [...]})

    and returns a dict containing a "messages" list (LangGraph style).
    """
    api_key = gemini_api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "Gemini API key not found. Please set GEMINI_API_KEY or GOOGLE_API_KEY "
            "in your .env file or environment variables."
        )

    # Set model to gemini-2.5-flash
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=temperature
    )

    # Collect tools
    tools = [pricing_tool, scenario_tool, sensitivity_tool, explanation_tool]

    # Create the agent using the new unified API.
    # system_prompt replaces the old ChatPromptTemplate + MessagesPlaceholder setup.
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
    )

    return agent