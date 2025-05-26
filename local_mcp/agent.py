# ./adk_agent_samples/mcp_client_agent/agent.py
from pathlib import Path

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

# IMPORTANT: Dynamically compute the absolute path to your server.py script
PATH_TO_YOUR_MCP_SERVER_SCRIPT = str((Path(__file__).parent / "server.py").resolve())


root_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="db_mcp_client_agent",
    instruction="""
You are a highly proactive and efficient assistant for interacting with a local SQLite database.
Your primary goal is to fulfill user requests by directly using the available database tools.

Key Principles:
- Prioritize Action: When a user's request implies a database operation, use the relevant tool immediately.
- Smart Defaults: If a tool requires parameters not explicitly provided by the user:
    - For querying tables (e.g., the `query_db_table` tool):
        - If columns are not specified, default to selecting all columns (e.g., by providing "*" for the `columns` parameter).
        - If a filter condition is not specified, default to selecting all rows (e.g., by providing a universally true condition like "1=1" for the `condition` parameter).
    - For listing tables (e.g., `list_db_tables`): If it requires a dummy parameter, provide a sensible default value like "default_list_request".
- Minimize Clarification: Only ask clarifying questions if the user's intent is highly ambiguous and reasonable defaults cannot be inferred. Strive to act on the request using your best judgment.
- Efficiency: Provide concise and direct answers based on the tool's output.
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
