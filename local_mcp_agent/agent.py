# ./adk_agent_samples/mcp_client_agent/agent.py
from pathlib import Path

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

# IMPORTANT: Dynamically compute the absolute path to your server.py script
PATH_TO_YOUR_MCP_SERVER_SCRIPT = str(
    (Path(__file__).parent / "../local_mcp_server/server.py").resolve()
)


root_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="db_mcp_client_agent",
    instruction="""
        You are an assistant that can interact with a local SQLite database using a set of tools. 
        When a user asks about the database, use the available tools to answer their questions 
        or perform the requested actions. Be proactive and helpful, and always return clear, structured results.
    """,
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command="python3",  # Command to run your MCP server script
                args=[
                    PATH_TO_YOUR_MCP_SERVER_SCRIPT  # Argument is the path to the script
                ],
            )
            # tool_filter=['list_tables'] # Optional: ensure only specific tools are loaded
        )
    ],
)
