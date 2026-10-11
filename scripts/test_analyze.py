"""Direct test for the analyzer logic (no MCP involved)."""

import asyncio

from mcp_github_learning_assistant.analyzer import analyze_repo


async def main():
    """Analyze spring-projects/spring-boot and print JSON."""
    result = await analyze_repo("spring-projects", "spring-boot")
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
