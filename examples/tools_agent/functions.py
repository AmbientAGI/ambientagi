import asyncio
import os
from ambientagi.services.agent_service import AmbientAgentService
from ambientagi.services.scheduler import AgentScheduler


def get_weather(city: str) -> str:
    """
    Returns a hardcoded weather string for the specified city.
    In production, replace this with a real weather API call.
    """
    return f"The weather in {city} is sunny with a light breeze."


async def main():
    # 1. Load your OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")

    # 2. Optional: set up scheduler (needed only for recurring tasks)
    scheduler = AgentScheduler()

    # 3. Create AmbientAgentService with scheduler
    service = AmbientAgentService(api_key=api_key, scheduler=scheduler)

    # 4. Create the agent in your database
    agent = service.create_agent(
        agent_name="WeatherAgent",
        private_key="********",
        description="Answers weather questions using a custom tool.",
    )
    agent_id = agent["agent_id"]
    print(f"✅ Created agent: {agent_id}")

    # 5. Define local OpenAI agent logic
    service.create_openai_agent(
        local_agent_name="WeatherAgent",
        instructions=(
            "You are a weather-savvy assistant. "
            "When asked about the weather, call the `get_weather` function with a city name, "
            "then use the result in your answer."
        ),
    )

    # 6. Register the function tool
    service.openai_wrapper.add_function_tool("WeatherAgent", get_weather)

    # 7. Run the agent with a prompt
    prompt = "What's the weather in London?"
    result = await service.run_openai_agent_async("WeatherAgent", prompt, agent_id=agent_id)
    print("\n🌤️ Agent Response:", result)

    # 8. (Optional) Shut down the scheduler if not needed further
    scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
