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


def _extract_text(content):
    """
    Normalizes AIMessage.content into a plain string.

    Gemini (and some other providers) can return content as a list of
    content blocks, e.g.:
        [{'type': 'text', 'text': '...'}, {'type': 'thinking', ...}]
    instead of a plain string. This extracts and joins only the actual
    text blocks, ignoring 'thinking'/'extras'/signature metadata blocks.
    """
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict):
                # Only take actual text content; skip thinking/signature/other metadata blocks
                if block.get("type") == "text" and "text" in block:
                    parts.append(block["text"])
        return "\n".join(parts).strip()

    # Fallback for any other unexpected type
    return str(content)


def invoke_pricing_agent(query: str, chat_history=None, gemini_api_key=None):
    """
    Invokes the pricing agent with the given query and chat history.

    chat_history: list of ("human"/"ai", text) tuples (same format the
    Streamlit page already saves).

    Returns:
      dict: Contains:
        - 'output': The final agent response string (always a clean plain string).
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

        # Extract the final AI response (last AIMessage with non-empty text content)
        final_output = "No response generated."
        for msg in reversed(result_messages):
            if isinstance(msg, AIMessage):
                text = _extract_text(msg.content)
                if text:
                    final_output = text
                    break

        # Extract intermediate tool calls + their results for the UI trace
        intermediate_steps = []
        tool_results = {}
        for msg in result_messages:
            if isinstance(msg, ToolMessage):
                tool_results[msg.tool_call_id] = _extract_text(msg.content)

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
        error_str = str(e)

        # Friendly message for Gemini free-tier quota exhaustion (429 RESOURCE_EXHAUSTED)
        if "RESOURCE_EXHAUSTED" in error_str or "429" in error_str or "quota" in error_str.lower():
            return {
                'output': (
                    "⏳ **Daily AI quota reached**\n\n"
                    "The free Gemini API tier allows a limited number of requests per day. "
                    "That limit has been reached for now.\n\n"
                    "Please try again in a few minutes, or come back tomorrow once the daily quota resets. "
                    "This is a usage limit on the underlying AI model, not an error in the application itself — "
                    "the Pricing Calculator, Scenario Analysis, and Gross Premium Pricing pages are unaffected "
                    "and remain fully usable without the AI Assistant."
                ),
                'intermediate_steps': []
            }

        return {
            'output': f"An error occurred while invoking the AI Assistant:\n\n`{error_str}`"
                      f"\n\n*Please ensure your GEMINI_API_KEY is correctly configured in your .env file.*",
            'intermediate_steps': []
        }