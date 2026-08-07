from agent.real_llm import chat as llm_chat
from agent.memory import Messages

def chat(messages:list[Messages],system:str =""):
    """Send conversation history to LLM, get one action (JSON string).

    Args:
        messages: full conversation history.
        system: system prompt.

    Returns:
        JSON string — either tool_call or final action.
    """
    return llm_chat(history=messages,system=system)