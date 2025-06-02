from google.adk.agents import Agent
from ...shared_lib.callbacks import before_model_callback, after_model_callback, before_agent_callback, after_agent_callback
from .prompt import REQUEST_PARSER_PROMPT

request_parser_agent = Agent(
    name="request_parser_and_preference_extractor",
    description="Extracts key travel parameters and preferences from user requests.",
    model="gemini-2.5-flash-preview-05-20",
    instruction=REQUEST_PARSER_PROMPT,
    output_key="parsed_request",
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
    before_agent_callback=before_agent_callback,
    after_agent_callback=after_agent_callback
)

# TODO: check https://google.github.io/adk-docs/agents/multi-agents/#coordinatordispatcher-pattern