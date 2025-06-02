import os

from dotenv import load_dotenv
load_dotenv()

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

from .prompt import WEB_PROMPT
from accommodation_search_agent.shared_lib.callbacks import before_search_term_browser_agent_callback

# ---- MCP Library ----
# https://github.com/modelcontextprotocol/servers
# https://smithery.ai/

args_playwright = [
    "-y",  # Argument for npx to auto-confirm install
    "@playwright/mcp@latest",
    # "--port", "8931",
    "--image-responses", "omit"
]

args_browsermcp = [
    "-y",  # Argument for npx to auto-confirm install
    "@browsermcp/mcp@latest"
]

search_term_browser_agent = LlmAgent(
    model='gemini-2.0-flash',
    # model=LiteLlm(model="openai/gpt-4o"),
    name='search_term_browser_agent',
    instruction=WEB_PROMPT,
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command='npx',
                args=args_browsermcp,
            ),
        )
    ],
    output_key="search_results",
    
    before_agent_callback=before_search_term_browser_agent_callback,
)
