import asyncio
import os

from ambientagi.services.agent_service import AmbientAgentService



async def main():
    # Initialize your extended Ambient service with your OpenAI API key
    
    service = AmbientAgentService(api_key=os.getenv("OPENAI_API_KEY"))
    create_resp = service.create_agent(
        agent_name="language_triage_agent",
        wallet_address="0x456DEF",
        description="Language Triage Agent",
    )
    agent_id = create_resp["agent_id"]

    # Create our Spanish and English agents
    service.create_openai_agent(
        name="SpanishAgent", instructions="You only speak Spanish."
    )
    service.create_openai_agent(
        name="EnglishAgent", instructions="You only speak English."
    )

    # Create the Triage agent
    service.create_openai_agent(
        name="TriageAgent",
        instructions="Handoff to the appropriate agent based on the language of the request.",
    )

    #  Assign the handoffs property on Triage agent to point to the Spanish & English agents
    #    Each call to create_openai_agent returns an Agent, but we also have them stored
    #    internally in service.openai_wrapper.agents. Let's retrieve them by name:
    triage_agent_obj = service.openai_wrapper.agents["TriageAgent"]
    spanish_agent_obj = service.openai_wrapper.agents["SpanishAgent"]
    english_agent_obj = service.openai_wrapper.agents["EnglishAgent"]

    # Now set the triage agent's handoffs
    triage_agent_obj.handoffs = [spanish_agent_obj, english_agent_obj]

    # Test by running the Triage agent asynchronously
    #    We'll give it a Spanish input so it hands off to the Spanish agent:
    user_input = "hello good ebvnenig"
    result_obj = await service.run_openai_agent_async("TriageAgent", user_input, agent_id=agent_id)
    print("Final agent output:", result_obj)


if __name__ == "__main__":
    asyncio.run(main())
