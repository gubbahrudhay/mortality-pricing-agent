"""
AI Agent Router
This module serves as the primary entry point to invoke the Conversational Actuarial Agent,
parsing queries, managing chat history, and returning execution outputs and traces.

Rewritten for LangChain 1.x create_agent (LangGraph-style message interface).
"""
import os
import sys

# Add parent directory to path to support config/pricing imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from agents.pricing_agent import get_pricing_agent


def invoke_pricing_agent(query: str, chat_history=None, gemini_api_key=None):
    """
    Invokes the pricing agent with the given query and chat history.

    chat_history: list of ("human"/"ai", text) tuples (same format the
    Streamlit page already saves).

    Returns:
      dict: Contains:
        - 'output': The final agent response string.
        - 'intermediate_steps': List of (tool_name, tool_args, tool_result) tuples.
    """
    if chat_history is None:
        chat_history = []

    try:
        agent = get_pricing_agent(gemini_api_key=gemini_api_key)

        # Build the LangGraph-style messages list from chat_history + new query
        messages = []
        for role, text in chat_history:
            if role == "human":
                messages.append(HumanMessage(content=text))
            elif role == "ai":
                messages.append(AIMessage(content=text))

        messages.append(HumanMessage(content=query))

        # Invoke the agent
        result = agent.invoke({"messages": messages})

        result_messages = result.get("messages", [])

        # Extract the final AI response (last AIMessage with content)
        final_output = "No response generated."
        for msg in reversed(result_messages):
            if isinstance(msg, AIMessage) and msg.content:
                final_output = msg.content
                break

        # Extract intermediate tool calls + their results for the UI trace
        intermediate_steps = []
        tool_results = {}
        for msg in result_messages:
            if isinstance(msg, ToolMessage):
                tool_results[msg.tool_call_id] = msg.content

        for msg in result_messages:
            if isinstance(msg, AIMessage) and getattr(msg, "tool_calls", None):
                for tc in msg.tool_calls:
                    tool_name = tc.get("name")
                    tool_args = tc.get("args")
                    tool_id = tc.get("id")
                    observation = tool_results.get(tool_id, "")
                    intermediate_steps.append((tool_name, tool_args, observation))

        return {
            'output': final_output,
            'intermediate_steps': intermediate_steps
        }

    except Exception as e:
        return {
            'output': f"An error occurred while invoking the AI Assistant:\n\n`{str(e)}`"
                      f"\n\n*Please ensure your GEMINI_API_KEY is correctly configured in your .env file.*",
            'intermediate_steps': []
        }
