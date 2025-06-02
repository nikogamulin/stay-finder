from google.adk.agents import Agent
import os
from dotenv import load_dotenv

from google.adk.tools.agent_tool import AgentTool

# Load environment variables early
load_dotenv()

from .sub_agents.request_parser_agent import request_parser_agent
from .sub_agents.location_refinement_agent import location_refinement_agent
from .sub_agents.search_string_generator_agent import search_string_generator_agent
from .sub_agents.accommodation_browser_agent.agent import accomodation_sequential_agent

from .prompt import TRAVEL_PLANNER_PROMPT_TOOLS_AND_SUB_AGENTS

# --- Create the Main Travel Planner Agent ---
accommodation_manager_agent = Agent(
    name="accommodation_manager_agent",
    description="A manager agent that orchestrates the vacation planning process.",
    model=os.getenv("GEMINI_MODEL"), # Master orchestrator model
    tools=[
        AgentTool(agent=request_parser_agent),
        AgentTool(agent=location_refinement_agent),
        AgentTool(agent=search_string_generator_agent)
    ],
    sub_agents=[accomodation_sequential_agent],
    instruction=TRAVEL_PLANNER_PROMPT_TOOLS_AND_SUB_AGENTS
)

root_agent = accommodation_manager_agent