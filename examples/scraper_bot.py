import os
import asyncio
from dotenv import load_dotenv
from ambientagi.services.agent_service import AmbientAgentService

load_dotenv()  # Load OPENAI_API_KEY

async def main():
    # 1. Initialize the service
    service = AmbientAgentService(api_key=os.getenv("OPENAI_API_KEY"))

    # 2. Create an agent record
    agent = service.create_agent(
        agent_name="BrowserScraper",
        wallet_address="0xFAKE123",
        description="A browser agent that scrapes and summarizes pages.",
    )
    agent_id = agent["agent_id"]
    print(f"✅ Created agent: {agent_id}")

    # 3. Create a BrowserAgent
    browser_agent = service.create_browser_agent(agent_id)

    # 4. Define the browser task
    task = "Go to openai.com/research and summarize the most recent article title."

    # 5. Run the browser task
    result = await browser_agent.run_task(task)
    print("🧠 Scraped Browser Result:\n", result)


if __name__ == "__main__":
    asyncio.run(main())
