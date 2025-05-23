import random

from google.adk.agents.llm_agent import Agent


def random_number() -> dict:
    """
    Generate a random number between 1 and 100.
    """
    return {"number": random.randint(1, 100)}


root_agent = Agent(
    model="gemini-2.0-flash",
    name="Traditional_Agent",
    instruction="""
    You are a helpful assistant that can help with a variety of tasks.
    """,
    tools=[random_number],
)
