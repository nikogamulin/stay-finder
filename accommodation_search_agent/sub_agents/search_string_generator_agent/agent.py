import os
from typing import List
from pydantic import BaseModel, Field

from google.adk.agents import Agent

from ...shared_lib.callbacks import after_agent_callback
from .prompt import SEARCH_STRINGS_GENERATOR_PROMPT

class SearchStrings(BaseModel):
    search_strings: List[str] = Field(description="A list of search strings")

search_string_generator_agent = Agent(
    name="search_string_generator_agent",
    description="Generates sets of search strings for accommodation search.",
    model=os.getenv("GEMINI_MODEL"),
    instruction=SEARCH_STRINGS_GENERATOR_PROMPT,
    output_key="search_strings",
    output_schema=SearchStrings,
    after_agent_callback=after_agent_callback
)