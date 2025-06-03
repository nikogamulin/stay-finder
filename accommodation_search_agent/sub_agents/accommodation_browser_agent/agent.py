import os

from dotenv import load_dotenv
load_dotenv()

from google.adk.agents import LoopAgent, SequentialAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

from .sub_agents.search_term_process_agent import search_term_process_agent
from ..results_presenter_agent import results_presenter_agent

accomodation_browser_loop_agent = LoopAgent(
    name="accomodation_browser_loop_agent",
    description="""Iteratively processes search terms one at a time by:
    1. Selecting the next search term to process
    2. Browsing the web for the search term
    3. Saving the results
    """,
    sub_agents=[search_term_process_agent],
    max_iterations=10
)

accomodation_sequential_agent = SequentialAgent(
    name="accomodation_sequential_agent",
    description="""First, analyzes all search terms and then passes the results to the results presenter agent to prepare a neat list of all the results.
    """,
    sub_agents=[accomodation_browser_loop_agent, results_presenter_agent]
)