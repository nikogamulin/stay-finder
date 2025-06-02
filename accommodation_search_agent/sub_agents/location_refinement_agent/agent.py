import os
from typing import List
from pydantic import BaseModel, Field
from google.adk.agents import Agent
from ...shared_lib.callbacks import after_agent_callback
from .prompt import LOCATION_REFINEMENT_PROMPT

class RefinedLocations(BaseModel):
    candidate_locations: List[str] = Field(description="A list of refined candidate locations")

location_refinement_agent = Agent(
    name="location_refinement_agent",
    description="Refines general locations into specific, suitable areas based on preferences.",
    model=os.getenv("GEMINI_MODEL"),
    # This agent might ideally have access to a knowledge base or real-time search capabilities
    # for location attributes (e.g., what areas in Dalmatia are known for being kid-friendly).
    instruction=LOCATION_REFINEMENT_PROMPT,
    output_key="refined_location",
    output_schema=RefinedLocations,
    after_agent_callback=after_agent_callback
)