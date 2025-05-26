# pip install ambientagi
import os
from ambientagi.services.agent_service import AmbientAgentService

# 1. Initialize the AmbientAgentService with your OpenAI API key
service = AmbientAgentService(api_key=os.getenv("OPENAI_API_KEY"))

# 2. Create a new agent with a name and wallet
resp = service.create_agent(
    agent_name="Broswy",
    private_key="********",
    description="A browser agent for crypto enthusiasts to track market news and trends.",
)
agent_id = resp["agent_id"]
print("✅ Created agent:", agent_id)

# 3. Launch the WebUI for this agent
webui_agent = service.add_webui_agent(agent_id=agent_id)
webui_agent.launch()  # Launches Gradio UI on default IP/port unless args override
