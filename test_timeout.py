#!/usr/bin/env python3

import sys
import os
sys.path.append('/home/niko/workspace/adk-accommodation-search_agent')

from accomodation_search_single_agent.agent import root_agent

async def test_agent():
    try:
        print("Testing agent with a simple request...")
        print(f"Available methods on agent: {[m for m in dir(root_agent) if not m.startswith('_')]}")
        
        # Try the run_async method which should trigger the MCP tools
        print("Using run_async method...")
        responses = []
        async for response in root_agent.run_async("Navigate to google.com and tell me what you see"):
            print(f"Got response chunk: {response}")
            responses.append(response)
            
        print(f"Final responses: {responses}")
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()
        return False
    return True

if __name__ == "__main__":
    import asyncio
    success = asyncio.run(test_agent())
    print(f"Test {'PASSED' if success else 'FAILED'}")