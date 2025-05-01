import os
import time
import asyncio
from dotenv import load_dotenv
from ambientagi.services.agent_service import AmbientAgentService
from ambientagi.services.scheduler import AgentScheduler

load_dotenv()

# Function tool
def fetch_market_stats():
    import requests
    try:
        data = requests.get("https://api.coingecko.com/api/v3/global").json()
        btc = data["data"]["market_cap_percentage"]["btc"]
        eth = data["data"]["market_cap_percentage"]["eth"]
        active = data["data"]["active_cryptocurrencies"]
        return (
            f"BTC Dominance: {btc:.2f}%\n"
            f"ETH Dominance: {eth:.2f}%\n"
            f"Active Coins: {active}"
        )
    except Exception as e:
        return f"Error fetching stats: {str(e)}"

# Async agent logic
def run_hourly_summary(agent_id: str):
    """
    Schedules this function to run hourly.
    It uses browser + OpenAI to generate a crypto summary.
    """
    async def _run():
        service = AmbientAgentService(api_key=os.getenv("OPENAI_API_KEY"))

        # 1. Run stats summary
        stats = await service.run_openai_agent_async("MarketSentinel", "Get market stats", agent_id)

        # 2. Scrape headline
        browser = service.create_browser_agent(agent_id)
        headline = await browser.run_task("Go to https://coindesk.com and return the top headline.")

        # 3. Merge & generate final summary
        prompt = f"[Stats]\n{stats}\n\n[Headline]\n{headline}\n\nWrite a 3-line crypto update."
        final = await service.run_openai_agent_async("MarketSentinel", prompt, agent_id)

        print("🧠 Hourly Market Summary:\n", final)

    asyncio.run(_run())


def main():
    # Setup service with scheduler
    scheduler = AgentScheduler()
    service = AmbientAgentService(api_key=os.getenv("OPENAI_API_KEY"), scheduler=scheduler)

    # Create agent
    agent = service.create_agent(
        agent_name="MarketSentinel",
        wallet_address="0xMARKET1H",
        description="Hourly crypto market summary bot.",
    )
    agent_id = agent["agent_id"]
    print("✅ Created agent:", agent_id)

    # Create LLM logic + tool
    service.create_openai_agent("MarketSentinel", instructions="""
You are a crypto summarizer. Use 'fetch_market_stats' and browser headlines to create a 3-line update.
""")
    service.openai_wrapper.add_function_tool("MarketSentinel", fetch_market_stats)

    # Schedule the task every hour
    service.schedule_agent(
        agent_id=agent_id,
        func=lambda: run_hourly_summary(agent_id),
        interval=3600  # seconds = 1 hour
    )

    print("⏱️ MarketSentinel scheduled to run every hour. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)  # Keep the scheduler alive
    except KeyboardInterrupt:
        print("🛑 Scheduler stopped.")
        scheduler.shutdown()


if __name__ == "__main__":
    main()
