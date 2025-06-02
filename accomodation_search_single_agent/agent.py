import os

from dotenv import load_dotenv
load_dotenv()

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters, SseServerParams


# ---- MCP Library ----
# https://github.com/modelcontextprotocol/servers
# https://smithery.ai/

# Microsoft Playwright MCP server
args_playwrightmcp = [
    "-y",
    "playwright-mcp@latest"
]

# Backup: simple browser MCP
args_browsermcp = [
    "-y",
    "@browsermcp/mcp@latest"
]

search_term_browser_agent = LlmAgent(
    model='gemini-2.0-flash',
    # model=LiteLlm(model="openai/gpt-4o"),
    name='search_term_browser_agent',
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command='npx',
                args=args_browsermcp,
                env={
                    # Fast operation settings
                    "PLAYWRIGHT_TIMEOUT": "4000",
                    "PLAYWRIGHT_NAVIGATION_TIMEOUT": "3000",
                }
            )
        )
    ]
)

root_agent = search_term_browser_agent
