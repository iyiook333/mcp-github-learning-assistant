import asyncio
from mcp_github_learning_assistant.roadmap import build_roadmap

async def main():
    r = await build_roadmap("spring-projects", "spring-boot", 2)
    print(r.model_dump_json(indent=2))

asyncio.run(main())