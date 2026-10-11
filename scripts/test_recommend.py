"""Direct test for the recommendation logic (no MCP involved)."""

import asyncio

from mcp_github_learning_assistant.recommender import recommend_repos


async def main():
    """Recommend Spring Boot repos for a beginner preparing for interviews."""
    result = await recommend_repos(
        role="student",
        target_tech="Spring Boot",
        level="beginner",
        goal="interview_prep",
        count=3,
    )
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())