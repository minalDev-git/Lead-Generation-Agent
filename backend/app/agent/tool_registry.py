from typing import Callable

from services.parser import prompt_parser
from services.browser import scrape_leads
from services.exporter import save_to_excel

_TOOLS: list[dict] = []

# ------------------------------------------------------------------
# Tool 1: Prompt Parser
# ------------------------------------------------------------------

_TOOLS.append({
    "name": "prompt_parser",
    "description": (
        "Extract the business category and geographic location from a user's "
        "natural language request. Use this whenever the user provides a lead "
        "generation prompt in plain English."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "user_prompt": {
                "type": "string",
                "description": (
                    "The user's natural language request describing the type "
                    "of businesses and location."
                ),
            }
        },
        "required": ["user_prompt"],
    },
    "handler": prompt_parser,
})

# ------------------------------------------------------------------
# Tool 2: Google Maps Scraper
# ------------------------------------------------------------------

_TOOLS.append({
    "name": "scrape_leads",
    "description": (
        "Search Google Maps for businesses matching a business category and "
        "location. Returns business name, website, phone number, address, "
        "and email if available."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "business_type": {
                "type": "string",
                "description": "Business category to search for.",
            },
            "location": {
                "type": "string",
                "description": "City, state, country or region to search in.",
            },
        },
        "required": ["business_type", "location"],
    },
    "handler": scrape_leads,
})

# ------------------------------------------------------------------
# Tool 3: Excel Export
# ------------------------------------------------------------------

_TOOLS.append({
    "name": "excel_export",
    "description": (
        "Save the collected business leads into an Excel (.xlsx) file and "
        "return the generated file path."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "businesses": {
                "type": "array",
                "description": "List of business lead dictionaries.",
                "items": {
                    "type": "object"
                }
            },
            "business_type": {
                "type": "string",
                "description": "Business category used in the search.",
            },
            "location": {
                "type": "string",
                "description": "Location used in the search.",
            },
        },
        "required": [
            "businesses",
            "business_type",
            "location",
        ],
    },
    "handler": save_to_excel,
})

# ─────────────────────────────────────────────────────────
# Public API — the only thing the loop should import.
# ─────────────────────────────────────────────────────────

def get_schemas() -> list[dict]:
    """Return tool schemas for LLM (without handlers)."""
    return [
        {"name": t["name"], "description": t["description"], "parameters": t["parameters"]}
        for t in _TOOLS
    ]


def get_handler(name: str) -> Callable[..., str] | None:
    """Return the handler for a tool name, or None if not found."""
    for t in _TOOLS:
        if t["name"] == name:
            return t["handler"]
    return None


def list_names() -> list[str]:
    return [t["name"] for t in _TOOLS]