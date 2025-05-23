import json
import os

from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
if NOTION_API_KEY is None:
    raise ValueError("NOTION_API_KEY is not set")

NOTION_MCP_HEADERS = json.dumps(
    {"Authorization": f"Bearer {NOTION_API_KEY}", "Notion-Version": "2022-06-28"}
)


print(NOTION_MCP_HEADERS)
# https://developers.notion.com/docs/mcp
# https://github.com/makenotion/notion-mcp-server
# https://github.com/makenotion/notion-mcp-server/blob/main/scripts/notion-openapi.json
root_agent = Agent(
    model="gemini-2.0-flash",
    name="Notion_MCP_Agent",
    instruction="""
    You are a helpful assistant that can help with a variety of tasks using Notion.

    Rules:
    - Take initiative and be proactive.
    - If you already have information (such as a document's page ID) from a previous search or step, use it directly—do not ask the user for it again, and do not ask for confirmation.
    - Never ask the user to confirm information you already possess. If you have the page ID or any other required detail, proceed to use it without further user input.
    - Only ask the user for information if it is truly unavailable or ambiguous after all reasonable attempts to infer or recall it from previous context.
    - When a user requests a summary or action on a document you have already listed or found, use the page ID or details you already have, without asking for confirmation.
    - Minimize unnecessary questions and streamline the user's workflow.
    - If you are unsure, make a best effort guess based on available context before asking the user.
    """,
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command="npx",
                args=["-y", "@notionhq/notion-mcp-server"],
                env={"OPENAPI_MCP_HEADERS": NOTION_MCP_HEADERS},
            )
        )
    ],
)
