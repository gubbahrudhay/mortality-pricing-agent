"""
AI Pricing Agent Configuration
This module configures the ChatGoogleGenerativeAI (Gemini) LLM agent, binding custom actuarial tools
and setting up conversational prompts and memory structures.

Rewritten for LangChain 1.x using the unified create_agent API.
"""
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

from agents.prompts import SYSTEM_PROMPT
from tools.pricing_tool import pricing_tool
from tools.scenario_tool import scenario_tool
from tools.sensitivity_tool import sensitivity_tool
from tools.explanation_tool import explanation_tool
from tools.gross_premium_tool import gross_premium_tool
from tools.reserving_tool import reserving_tool

load_dotenv()

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

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=temperature
    )

    tools = [
        pricing_tool,
        scenario_tool,
        sensitivity_tool,
        explanation_tool,
        gross_premium_tool,
        reserving_tool,
    ]

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=SYSTEM_PROMPT,
    )

    return agent