"""
memory.py — Conversation history (short-term memory).

Keeps an in-memory list of messages. We send whole history to the LLM. (this is the simplest form of "context window").
"""

from typing import TypedDict

class Messages(TypedDict):
    role: str # "system" | "user" | "assistant"
    content: str # message text

def init_history()-> list[Messages]:
    return []

def add_user(history:list[Messages], text:str)-> None:
    history.append({"role":"user","content":text})

def add_assistant(history:list[Messages], text:str)->None:
    history.append({"role":"assistant", "content":text})
