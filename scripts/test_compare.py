import asyncio

from mcp_github_learning_assistant.comparer import compare_repos


async def main():
    r = await compare_repos(
        repos=[
            "spring-projects/spring-boot",
            "quarkusio/quarkus",
            "micronaut-projects/micronaut-core",
        ],
        user_level="beginner",
    )
    print(r.model_dump_json(indent=2))

asyncio.run(main())
