#!/usr/bin/env python3

# Simple script to trigger MCP timeout
import sys
import os
sys.path.append('/home/niko/workspace/adk-accommodation-search_agent')

# Import the agent setup only
from accomodation_search_single_agent.agent import search_term_browser_agent

print("Agent loaded successfully")
print(f"Agent tools: {search_term_browser_agent.tools}")

# Try to trigger the MCP connection which should cause timeout
try:
    print("Attempting to initialize MCP tools...")
    for tool in search_term_browser_agent.tools:
        print(f"Tool: {tool}")
        # This should trigger MCP connection and potentially the timeout
        
    print("MCP tools initialized successfully - no timeout occurred!")
    
except Exception as e:
    print(f"Error during MCP initialization: {e}")
    import traceback
    traceback.print_exc()