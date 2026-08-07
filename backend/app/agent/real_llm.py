from langchain_groq import ChatGroq
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
)
from agent.memory import Messages
from config import GROQ_API_KEY,GROQ_MODEL

llm = ChatGroq(
    model=GROQ_MODEL,  # type: ignore
    temperature=0,
    api_key=GROQ_API_KEY, # type: ignore
)

def chat(history:list[Messages],system):
    """
    Send the current conversation to the LLM.

    Returns:
        str
    """

    messages = []

    messages.append(SystemMessage(content=system))

    for m in history:

        if m["role"] == "user":
            messages.append(
                HumanMessage(content=m["content"])
            )

        elif m["role"] == "assistant":
            messages.append(
                AIMessage(content=m["content"])
            )
    response = llm.invoke(messages)

    return response.content
