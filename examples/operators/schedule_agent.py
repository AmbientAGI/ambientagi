# pip install ambientagi
import os
import time
import asyncio
from ambientagi.services.agent_service import AmbientAgentService


def run_browser_task(agent_id: str, task: str):
    """
    Run an async browser task from a synchronous context.
    """
    service = AmbientAgentService(api_key=os.getenv("OPENAI_API_KEY"))
    browser_agent = service.create_browser_agent(agent_id)

    async def _run():
        result = await browser_agent.run_task(task)
        print("🧠 Browser Task Result:", result)

    asyncio.run(_run())


def main():
    # 1. Initialize the agent service
    service = AmbientAgentService(api_key=os.getenv("OPENAI_API_KEY"))

    # 2. Create a browser agent
    resp = service.create_agent(
        agent_name="BrowserAssistant",
        private_key="********",
        description="An agent that uses a browser to find trending AI news.",
    )
    agent_id = resp["agent_id"]
    print(f"✅ Created agent: {agent_id}")

    # 3. Define a browser automation task
    task = "Go to Reddit, search for 'AI news', and return the first post title."

    # 4. Schedule the task to run every 60 seconds
    service.schedule_agent(
        agent_id=agent_id,
        func=lambda: run_browser_task(agent_id, task),
        interval=60,
    )
    print("📅 Task scheduled every 60 seconds. Press Ctrl+C to stop.")

    # 5. Keep the scheduler alive
    try:
        while True:
            time.sleep(1)  # Correct: not asyncio.sleep
    except KeyboardInterrupt:
        print("🛑 Shutting down...")


if __name__ == "__main__":
    main()
