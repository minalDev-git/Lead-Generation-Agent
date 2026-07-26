from app.config import GROQ_API_KEY,GROQ_MODEL
from app.models import LeadQuery
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


SYSTEM_PROMPT = """You are a precise information extraction assistant for a lead-generation tool.

Your job is to read a user's natural-language request describing what kind of
business leads they want to find, and extract exactly two fields:

1. "business_type": the category/industry/type of business the user is looking for
   (e.g., "coffee shops", "dentists", "law firms", "auto repair shops").
2. "location": the geographic area the user wants to search in
   (e.g., a city, state, country, region, or neighborhood).

Rules:
- Extract the business type in a clean, normalized noun phrase. Do not include
  filler words like "find", "search for", "looking for".
- Extract the location as it appears, normalized to a proper noun (fix casing,
  e.g. "america" -> "America", "nyc" -> "New York City" only if unambiguous).
- If multiple business types are mentioned, join them with a comma in a single string.
- If the location is missing or cannot be determined, set "location" to null.
- If the business type cannot be identified, return:
"business_type": null

- If the location cannot be identified, return:
"location": null

- If both are missing, return:
{
  "business_type": null,
  "location": null
}

- Do not infer information that is not present or reasonably implied in the text.
- Do not add explanations, commentary, or extra fields — return only the requested structure.
- Return only the structured response.
"""


def prompt_parser(user_prompt: str)-> dict:
    """Builds and returns the LangChain runnable chain for parsing prompts."""
    """
    Extracts business_type and location from a natural-language lead-gen prompt.
    
    Args:
        user_prompt: e.g. "coffee shops in America"
    
    Returns:
        dict with keys "business_type" and "location"
    """
    
    llm = ChatGroq(
        model=GROQ_MODEL,  # any Groq-hosted model works # type: ignore
        temperature=0,
        api_key=GROQ_API_KEY, # type: ignore
    )

    structured_llm = llm.with_structured_output(LeadQuery)

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{user_prompt}"),
    ])

    chain = prompt | structured_llm
    result = chain.invoke({"user_prompt": user_prompt})

    # result is a LeadQuery instance (or dict, depending on LangChain version)
    if isinstance(result, dict):
        return result
    else:
        return result.model_dump()
    
    
