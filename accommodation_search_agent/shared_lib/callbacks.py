from typing import Optional
import logging

from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest, LlmResponse
import google.genai.types as types

def before_model_callback(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """
    Callback that executes before the model is called.
    Detects and saves inline images from user messages to assets folder
    for use by the generate_image_agent.

    Args:
        callback_context: The callback context
        llm_request: The LLM request

    Returns:
        Optional[LlmResponse]: None to allow normal processing
    """
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    logging.info("Before model callback for %s with invocation ID %s", agent_name, invocation_id)
    return None

def after_model_callback(
    callback_context: CallbackContext, llm_response: LlmResponse
) -> None:
    """
    Callback that executes after the model is called.
    """
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    logging.info("After model callback for %s with invocation ID %s", agent_name, invocation_id)
    return None

def before_agent_callback(
    callback_context: CallbackContext) -> Optional[types.Content]:
    """
    Callback that executes before the agent is called.
    """
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    logging.info("Before agent callback for %s with invocation ID %s", agent_name, invocation_id)
    return None

def after_agent_callback(
    callback_context: CallbackContext) -> Optional[types.Content]:
    """
    Callback that executes after the agent is called.
    """
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    logging.info("After agent callback for %s with invocation ID %s", agent_name, invocation_id)
    return None

def before_search_term_selection_agent_callback(
    callback_context: CallbackContext) -> Optional[types.Content]:
    """
    Callback that executes before the search term selection agent is called.
    """
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    logging.info("Before search term selection agent callback for %s with invocation ID %s", agent_name, invocation_id)
    if 'search_process_status' not in callback_context.state:
        callback_context.state['search_process'] = {}
        for search_string in callback_context.state['search_strings']['search_strings']:
            callback_context.state['search_process'][search_string] = {
                'processed': False,
                'results': []
            }
    
    return None

def before_search_term_browser_agent_callback(
    callback_context: CallbackContext) -> Optional[types.Content]:
    """
    Callback that executes before the search term browser agent is called.
    """
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    logging.info("Before search term browser agent callback for %s with invocation ID %s", agent_name, invocation_id)
    return None