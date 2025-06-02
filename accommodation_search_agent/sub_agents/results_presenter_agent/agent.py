from google.adk.agents import Agent
import os
from dotenv import load_dotenv
load_dotenv()

from .prompt import RESULTS_PRESENTER_PROMPT

results_presenter_agent = Agent(
    name="results_presenter_agent",
    description="Formats and presents the accommodation search results neatly.",
    model=os.getenv("GEMINI_MODEL"),
    instruction=RESULTS_PRESENTER_PROMPT
)
