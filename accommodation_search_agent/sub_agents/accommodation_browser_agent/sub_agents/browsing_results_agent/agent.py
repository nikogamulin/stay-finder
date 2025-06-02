from google.adk.agents import Agent
import os
from dotenv import load_dotenv
load_dotenv()

from .prompt import BROWSING_RESULTS_PROMPT
from .tools.interrupt_search_process import interrupt_search_process

browsing_results_agent = Agent(
    name="browsing_results_agent",
    model=os.getenv("GEMINI_MODEL"),
    description="Browses the results of the search term",
    instruction=BROWSING_RESULTS_PROMPT,
    tools=[interrupt_search_process],
)