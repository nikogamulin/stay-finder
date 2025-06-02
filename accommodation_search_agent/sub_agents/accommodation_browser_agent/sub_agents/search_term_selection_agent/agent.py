from google.adk.agents import Agent
import os
from dotenv import load_dotenv
load_dotenv()

from accommodation_search_agent.shared_lib.callbacks import before_search_term_selection_agent_callback

from .tools.select_search_term import select_search_term
# Import save_search_results if it's also intended for this agent's toolkit later
# from .tools.save_search_results import save_search_results

instructions = """
You are a Search Term Selection Orchestrator.
Your primary responsibility is to manage the queue of search terms that need to be processed for web searches.

# CURRENT STATE OVERVIEW
- `state['search_process']`: A dictionary where each key is a search term. The value for each term is another dictionary with:
    - `'processed' (bool)`: True if this term has been used for a search and results are saved, False otherwise.
    - `'results' (list)`: A list of results obtained for this search term.

# YOUR TASK
Your first and primary task is to invoke the `select_search_term` tool ONCE. This tool will automatically:
1. Examine `state['search_process']`.
2. If it finds a search term with `processed: False`:
   - It will select the first such term.
   - It will update `state['selected_search_term']` with this chosen term.
   - It will return a status indicating success and the selected term.
3. If all search terms in `state['search_process']` have `processed: True`:
   - The tool will automatically trigger an escalation, signaling that all search terms have been exhausted.
   - It will return a status indicating that all terms are processed.

After the `select_search_term` tool has been successfully invoked and `state['selected_search_term']` is updated (or escalation has occurred), your task for this step is complete. The system will use the updated `state` or the escalation signal to determine the next action.

# INSTRUCTIONS
- You are provided with the current `state['search_process']` below for context.
- Your first action is to call the `select_search_term` tool. You do not need to pass any arguments to it. This tool must only be called once.
- The tool internally handles the selection logic and the escalation if all terms have been processed.
- After the tool runs, `state['selected_search_term']` will either hold the next term to be searched, or the process will have been escalated by the tool.
- After `select_search_term` has run, you should output a concise message confirming the action taken by the tool (either a term was selected or escalation occurred), and then your execution for this turn will end.

# IMPORTANT
- Call the `select_search_term` tool exactly once.
- Do not try to manually pick a term or decide to escalate yourself; the `select_search_term` tool encapsulates this logic.
- Keep your responses concise - just confirm which search term you've selected or that you're exiting the loop.

Here is the current state of the search process:
{search_process}
"""

search_term_selection_agent = Agent(
    model=os.getenv("GEMINI_MODEL"),
    name="search_term_selection_agent",
    description="Selects the next search term to process or escalates if all terms are done.",
    instruction=instructions,
    tools=[select_search_term], # Add save_search_results here if needed by this agent
    before_agent_callback=before_search_term_selection_agent_callback,
)