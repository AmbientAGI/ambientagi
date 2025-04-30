from dotenv import load_dotenv
import os
from ambientagi.services.agent_service import AmbientAgentService

load_dotenv()  # Load FIRECRAWL_API_KEY from .env

# 1. Initialize the service (OpenAI key required, even if not used)
service = AmbientAgentService(api_key=os.getenv("OPENAI_API_KEY"))

# 2. Create a dummy agent record (so we can tie tools to it)
agent = service.create_agent(
    agent_name="ScraperBot",
    wallet_address="0xFAKE123",  # Just a placeholder
    description="A bot that scrapes content from web pages.",
)

# 3. Create a Firecrawl wrapper agent
scraper = service.create_firecrawl_agent(agent_id=agent["agent_id"])

# 4. Scrape a page (as Markdown + HTML)
result = scraper.scrape_website("https://openai.com/research")
print("📄 Markdown Content:\n", result["markdown"][:500])  # Show first 500 chars
