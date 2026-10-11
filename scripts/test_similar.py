import asyncio

from mcp_github_learning_assistant.similar import find_similar


async def main():
    r = await find_similar("fastapi", "fastapi", 3)
    print(r.model_dump_json(indent=2))

asyncio.run(main())
