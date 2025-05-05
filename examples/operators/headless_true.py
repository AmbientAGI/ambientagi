# headless_true.py

import asyncio
import os
from dotenv import load_dotenv
 # Load environment variables from .env file
from ambientagi.services.agent_service import AmbientAgentService

load_dotenv() 

async def main():
    service = AmbientAgentService(api_key=os.getenv("OPENAI_API_KEY"))  # your OpenAI key

    agent = service.create_agent(
        agent_name="HeadlessBot",
        wallet_address="0xBOT",
        description="Get latest news headline from CNN",
    )

    # ✅ Consistent usage of create_browser_agent with overrides
    browser_agent = service.create_browser_agent(
        agent_id=agent["agent_id"],
        browser_config={
            "headless": True,
            "new_context_config": {
                "window_width": 1280,
                "window_height": 900,
            },
        },
    )

    result = await browser_agent.run_task(
        model="gpt-4o",
        task="Go to cnn.com and return the top headline on the homepage.",
    )

    print("\n[HEADLESS RESULT]:", result.final_result())


if __name__ == "__main__":
    asyncio.run(main())
