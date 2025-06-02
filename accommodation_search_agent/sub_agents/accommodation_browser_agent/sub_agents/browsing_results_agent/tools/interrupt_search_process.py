from typing import Dict

from google.adk.tools.tool_context import ToolContext


def interrupt_search_process(
    tool_context: ToolContext,
) -> Dict:
    """
    Interrupt the search process.

    Args:
        tool_context: ADK tool context

    Returns:
        Dictionary with exit status
    """
    tool_context.actions.escalate = True

    return {
        "status": "success",
        "message": "Search process interrupted due to error.",
    }