import asyncio
import os
from dotenv import load_dotenv
from ambientagi.services.agent_service import AmbientAgentService

load_dotenv()  # load OPENAI_API_KEY from .env

# Step 1: Initialize the AmbientAGI service with your OpenAI API key
service = AmbientAgentService(api_key=os.getenv("OPENAI_API_KEY"))

# Step 2: Define your agent with instructions
instructions = """
You are IdeaBot. You generate quirky but potentially profitable startup ideas based on user input.
Always include a funny name, a one-liner pitch, and a niche target audience.
"""

# Step 3: Register the agent locally
service.create_openai_agent("IdeaBot", instructions)

# Step 4: Run the agent with a prompt
async def main():
    prompt = "Give me an idea for a startup in the pet tech space"
    result = await service.run_openai_agent_async("IdeaBot", prompt, agent_id="demo-123")
    print("💡 Startup Idea:", result)

if __name__ == "__main__":
    asyncio.run(main())
