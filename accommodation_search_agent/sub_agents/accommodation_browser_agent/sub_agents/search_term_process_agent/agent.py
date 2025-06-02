from google.adk.agents import SequentialAgent

from ..search_term_selection_agent import search_term_selection_agent # Commented out due to missing file
from ..search_term_browser_agent import search_term_browser_agent # Commented out due to missing file
from ..browsing_results_agent import browsing_results_agent # Commented out due to missing file

search_term_process_agent = SequentialAgent(
    sub_agents=[search_term_selection_agent, search_term_browser_agent, browsing_results_agent], # Commented out due to missing agents
    name="search_term_process_agent",
    description="""Processes the search term one at a time by:
    1. Selecting the next search term to process
    2. Browsing the web for the search term
    3. Saving the results
    """
)