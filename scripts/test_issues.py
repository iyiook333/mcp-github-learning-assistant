import asyncio
from mcp_github_learning_assistant.issuefind import find_first_issues

async def main():
    r = await find_first_issues("spring-projects", "spring-boot", ["good first issue"])
    print(r.model_dump_json(indent=2))

asyncio.run(main())