"""
AI Pricing Agent Configuration

This module configures the ChatGoogleGenerativeAI (Gemini) LLM agent, binding custom actuarial tools
and setting up conversational prompts and memory structures.
"""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path to support config/pricing imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

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
    Initializes and returns the LangChain AgentExecutor bound with actuarial tools.
    """
    api_key = gemini_api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError(
            "Gemini API key not found. Please set GEMINI_API_KEY or GOOGLE_API_KEY "
            "in your .env file or environment variables."
        )
        
    # Set model to gemini-1.5-flash
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=api_key,
        temperature=temperature
    )
    
    # Collect tools
    tools = [pricing_tool, scenario_tool, sensitivity_tool, explanation_tool]
    
    # Define prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # Create the agent using native tool calling
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    # Create the agent executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        return_intermediate_steps=True # Useful for rendering execution logs in Streamlit!
    )
    
    return agent_executor
