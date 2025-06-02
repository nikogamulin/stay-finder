from typing import Dict

from google.adk.tools.tool_context import ToolContext

def select_search_term(tool_context: ToolContext) -> Dict:
    """
    Selects a search term that has not yet been processed.

    Args:
        tool_context: ADK tool context.

    Returns:
        Dictionary with selection status and the selected search term or an error/warning message.
    """
    try:
        if "search_process" not in tool_context.state:
            return {
                "status": "error",
                "message": "search_process not found in state. Cannot select search term.",
            }

        search_process = tool_context.state["search_process"]
        if not isinstance(search_process, dict):
            return {
                "status": "error",
                "message": "search_process in state is not a dictionary.",
            }

        for search_term, status in search_process.items():
            if isinstance(status, dict) and not status.get('processed', True):
                tool_context.state['selected_search_term'] = search_term
                return {
                    "status": "success",
                    "message": f"Selected search term '{search_term}' for processing.",
                    "selected_search_term": search_term,
                }

        # If all search terms have been processed
        tool_context.actions.escalate = True
        return {
            "status": "all_processed",
            "message": "All search terms have been processed. Escalating.",
        }

    except Exception as e:
        error_message = f"Error selecting search term: {str(e)}"
        print(error_message) # It's good practice to log the error
        return {"status": "error", "message": error_message}