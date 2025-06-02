import os

from dotenv import load_dotenv
load_dotenv()

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters, SseServerParams

# Comprehensive monkey patch to override ALL potential 5-second timeouts
print("Applying comprehensive timeout patches to main agent...")

# Patch 1: ClientSession
try:
    from datetime import timedelta
    from mcp.client.session import ClientSession
    
    original_client_init = ClientSession.__init__
    def patched_client_init(self, read_transport, write_transport, read_timeout_seconds=None):
        if read_timeout_seconds is None or read_timeout_seconds == timedelta(seconds=5):
            read_timeout_seconds = timedelta(seconds=60)
        return original_client_init(self, read_transport, write_transport, read_timeout_seconds)
    
    ClientSession.__init__ = patched_client_init
    print("✓ Patched ClientSession timeout in main agent")
except Exception as e:
    print(f"✗ ClientSession patch failed in main agent: {e}")

# Patch 2: Global timedelta replacement
try:
    import datetime
    original_timedelta = datetime.timedelta
    
    def patched_timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        if seconds == 5 and days == 0 and microseconds == 0 and milliseconds == 0 and minutes == 0 and hours == 0 and weeks == 0:
            seconds = 60  # Replace 5-second timeouts with 60 seconds
        return original_timedelta(days, seconds, microseconds, milliseconds, minutes, hours, weeks)
    
    datetime.timedelta = patched_timedelta
    print("✓ Patched global timedelta in main agent")
except Exception as e:
    print(f"✗ Global timedelta patch failed in main agent: {e}")

# Note: Session manager patch removed to avoid signature conflicts
print("✓ Skipped session manager patch in main agent (not needed with other patches)")

print("Main agent timeout patches applied, continuing with agent setup...")

from .prompt import WEB_SEARCH_PROMPT, AIRBNB_SEARCH_PROMPT
from accommodation_search_agent.shared_lib.callbacks import before_search_term_browser_agent_callback

# ---- MCP Library ----
# https://github.com/modelcontextprotocol/servers
# https://smithery.ai/

# Microsoft Playwright MCP server
args_playwrightmcp = [
    "-y",
    "playwright-mcp@latest"
]

# simple browser MCP
args_browsermcp = [
    "-y",
    "@browsermcp/mcp@latest"
]

args_airbnbmcp = [
    "-y",
    "@openbnb/mcp-server-airbnb",
    "--ignore-robots-txt"
  ]

# Determine the search mode from environment variables
SEARCH_MODE = os.getenv("SEARCH_MODE", "AIRBNB") # Default to AIRBNB if not set

# Conditionally set arguments and prompt based on SEARCH_MODE
if SEARCH_MODE == "BROWSER":
    agent_args = args_browsermcp
    agent_instruction = WEB_SEARCH_PROMPT
    toolset_command = 'npx'
    print("✓ Using BROWSER mode for search_term_browser_agent")
elif SEARCH_MODE == "AIRBNB":
    agent_args = args_airbnbmcp
    agent_instruction = AIRBNB_SEARCH_PROMPT
    toolset_command = 'npx' # npx is also used for airbnb mcp
    print("✓ Using AIRBNB mode for search_term_browser_agent")
else:
    # Default to AIRBNB if an invalid mode is specified
    agent_args = args_airbnbmcp
    agent_instruction = AIRBNB_SEARCH_PROMPT
    toolset_command = 'npx'
    print(f"✗ Invalid SEARCH_MODE: {SEARCH_MODE}. Defaulting to AIRBNB mode.")

search_term_browser_agent = LlmAgent(
    # model='gemini-2.0-flash',
    model=LiteLlm(model="openai/gpt-4o"),
    name='search_term_browser_agent',
    instruction=agent_instruction, # Use the dynamically set instruction
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command=toolset_command, # Use the dynamically set command
                args=agent_args # Use the dynamically set arguments
            )
        )
    ],
    output_key="search_results",
    
    before_agent_callback=before_search_term_browser_agent_callback,
)
