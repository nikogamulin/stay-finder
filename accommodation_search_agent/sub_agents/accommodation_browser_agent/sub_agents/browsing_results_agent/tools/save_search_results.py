from typing import Dict, List

from google.adk.tools.tool_context import ToolContext


def save_search_results(
    tool_context: ToolContext,
    search_results: str  # Assuming search_results is a string
) -> Dict:
    """
    Save the search results for the currently selected search term to state
    and mark it as processed.

    Args:
        tool_context: ADK tool context.
        search_results: A string representing the search results that are the candidate accommodation listings.

    Returns:
        Dictionary with save status.
    """
    try:
        if "selected_search_term" not in tool_context.state:
            return {
                "status": "error",
                "message": "No search term selected. Cannot save results."
            }
        
        selected_search_term = tool_context.state["selected_search_term"]

        if not selected_search_term:
            return {
                "status": "error",
                "message": "Selected search term is empty. Cannot save results."
            }

        if "search_process" not in tool_context.state:
            # This should ideally be initialized by a callback, but handle defensively
            tool_context.state["search_process"] = {}
            # return {
            #     "status": "error",
            #     "message": "search_process not found in state. Cannot save results."
            # }

        if not isinstance(tool_context.state["search_process"], dict):
            return {
                "status": "error",
                "message": "search_process in state is not a dictionary."
            }
            
        if selected_search_term not in tool_context.state["search_process"]:
            # Initialize if somehow missing, though select_search_term should ensure it exists
            tool_context.state["search_process"][selected_search_term] = {
                'processed': False,
                'results': []
            }
            # return {
            #     "status": "error",
            #     "message": f"Search term '{selected_search_term}' not found in search_process state."
            # }
        
        # Save the results and mark as processed
        # if the selected term already has results, append the new string to the existing results
        if tool_context.state["search_process"][selected_search_term]['results']:
            tool_context.state["search_process"][selected_search_term]['results'] += search_results
        else:
            tool_context.state["search_process"][selected_search_term]['results'] = search_results
        tool_context.state["search_process"][selected_search_term]['processed'] = True

        return {
            "status": "success",
            "message": f"Search results for '{selected_search_term}' saved successfully.",
            "search_term": selected_search_term
        }

    except Exception as e:
        error_message = f"Error saving search results: {str(e)}"
        print(error_message)
        return {"status": "error", "message": error_message}
