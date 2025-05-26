import os
from ambientagi.services.agent_service import AmbientAgentService

# 1️⃣ Initialize the core agent service
service = AmbientAgentService(api_key=os.getenv("OPENAI_API_KEY"))

# 2️⃣ Create and register a new crawler agent
agent_info = service.create_agent(
    agent_name="CrawlerAgent",
    private_key="********",
    description="Autonomous agent that crawls websites and summarizes key insights.",
)
agent_id = agent_info["agent_id"]
print(f"✅ Created agent: {agent_id}")

# 3️⃣ Create Firecrawl wrapper bound to this agent
crawler = service.create_firecrawl_agent(agent_id)

# 🔍 Target domain to crawl
target_url = "https://news.ycombinator.com"

# 4️⃣ Crawl the website (limit to 5 pages)
crawl_result = crawler.crawl_website(target_url, limit=5)
pages = crawl_result.get("pages", [])
print(f"🔎 Crawled {len(pages)} pages from {target_url}")

# 5️⃣ Generate AI summaries for each page
summaries = []
for page in pages:
    markdown = page.get("markdown", "")[:4000]  # Token safety
    if markdown:
        summary = service.run_openai_agent("CrawlerAgent", markdown, agent_id=agent_id)
        summaries.append(summary)

# 🧠 Output results
print("\n🧠 Summarized Content:")
for s in summaries:
    print("-", s)
