"""
AI Agent Router

This module serves as the primary entry point to invoke the Conversational Actuarial Agent,
parsing queries, managing chat history, and returning execution outputs and traces.
"""

import os
import sys

# Add parent directory to path to support config/pricing imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.pricing_agent import get_pricing_agent

def invoke_pricing_agent(query: str, chat_history=None, gemini_api_key=None):
    """
    Invokes the pricing agent with the given query and chat history.
    
    Returns:
      dict: Contains:
        - 'output': The final agent response string.
        - 'intermediate_steps': List of tool calls and results.
    """
    if chat_history is None:
        chat_history = []
        
    try:
        agent_executor = get_pricing_agent(gemini_api_key=gemini_api_key)
        
        # Invoke the executor
        response = agent_executor.invoke({
            "input": query,
            "chat_history": chat_history
        })
        
        return {
            'output': response.get('output', 'No response generated.'),
            'intermediate_steps': response.get('intermediate_steps', [])
        }
        
    except Exception as e:
        return {
            'output': f"An error occurred while invoking the AI Assistant:\n\n`{str(e)}`"
                      f"\n\n*Please ensure your GEMINI_API_KEY is correctly configured in your .env file.*",
            'intermediate_steps': []
        }
