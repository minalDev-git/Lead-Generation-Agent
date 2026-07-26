from pydantic import BaseModel, Field
from typing import Optional

class PromptRequest(BaseModel):
    prompt: str


# ---- 1. Define the expected structured output ----
class LeadQuery(BaseModel):
    business_type: Optional[str] = Field(
        default=None,
        description="The type/category of business the user wants leads for, e.g. 'coffee shops'"
    )
    location: Optional[str] = Field(
        default=None,
        description="The geographic location the user wants to search in, e.g. 'America'"
    )