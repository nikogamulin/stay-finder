import os
import asyncio

from dotenv import load_dotenv
load_dotenv()

# Try to override asyncio timeout defaults
# This might help with the hardcoded 5-second timeout issue
os.environ['ASYNCIO_DEFAULT_TIMEOUT'] = '60'
os.environ['MCP_TIMEOUT'] = '60'
os.environ['MCP_READ_TIMEOUT'] = '60'

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters, SseServerParams

# Comprehensive monkey patch to override ALL potential 5-second timeouts
print("Applying comprehensive timeout patches...")

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
    print("✓ Patched ClientSession timeout")
except Exception as e:
    print(f"✗ ClientSession patch failed: {e}")

# Patch 2: Global timedelta replacement
try:
    import datetime
    original_timedelta = datetime.timedelta
    
    def patched_timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        if seconds == 5 and days == 0 and microseconds == 0 and milliseconds == 0 and minutes == 0 and hours == 0 and weeks == 0:
            seconds = 60  # Replace 5-second timeouts with 60 seconds
        return original_timedelta(days, seconds, microseconds, milliseconds, minutes, hours, weeks)
    
    datetime.timedelta = patched_timedelta
    print("✓ Patched global timedelta")
except Exception as e:
    print(f"✗ Global timedelta patch failed: {e}")

# Patch 3: Session manager level - REMOVED due to signature issues
# The session manager patch was causing errors because it changed the method signature
# The ClientSession and timedelta patches should be sufficient
print("✓ Skipped session manager patch (not needed with other patches)")

print("Timeout patches applied, continuing with agent setup...")


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
                args=args_browsermcp
            )
        )
    ]
)

root_agent = search_term_browser_agent
