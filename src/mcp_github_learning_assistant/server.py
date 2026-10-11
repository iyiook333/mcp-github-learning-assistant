"""MCP server entry point."""

import asyncio
import sys

from dotenv import load_dotenv
from mcp.server import MCPServer

from .tools import analyze, compare, issues, recommend, roadmap, similar, trending

app = MCPServer("mcp-github-learning-assistant")


@app.tool()
async def get_server_info() -> str:
    """Return basic server info to verify the MCP connection works."""
    return "MCP GitHub Learning Assistant v0.1.0 - discover open-source projects worth learning"


@app.tool()
async def analyze_repo_for_learning(owner: str, repo: str) -> str:
    """Analyze a GitHub repo to see if it is worth learning.

    Returns score, difficulty, prerequisites, pros/cons and a suggested
    learning path as a JSON string.

    Args:
        owner: GitHub user or org name, e.g. spring-projects
        repo: Repository name, e.g. spring-boot
    """
    results = await analyze.analyze_repo_tool({"owner": owner, "repo": repo})
    return results[0].text


@app.tool()
async def recommend_learning_repos(
    role: str,
    target_tech: str,
    experience_level: str,
    goal: str,
    count: int = 5,
) -> str:
    """Recommend GitHub repos to learn, based on the user's profile.

    Args:
        role: user role, e.g. student, backend_dev, frontend_dev, mobile_dev
        target_tech: tech to learn, e.g. Spring Boot, FastAPI, Vue
        experience_level: beginner, intermediate, or advanced
        goal: interview_prep, skill_upgrade, open_source, project_practice
        count: max recommendation count (default 5)
    """
    arguments = {
        "role": role,
        "target_tech": target_tech,
        "experience_level": experience_level,
        "goal": goal,
        "count": count,
    }
    results = await recommend.recommend_repos_tool(arguments)
    return results[0].text


@app.tool()
async def get_repo_roadmap(owner: str, repo: str, depth: int = 2) -> str:
    """Generate a learning roadmap from a repo's top-level structure.

    Args:
        owner: GitHub user or org name
        repo: Repository name
        depth: how deep to explore (reserved; currently uses top level)
    """
    results = await roadmap.roadmap_tool({"owner": owner, "repo": repo, "depth": depth})
    return results[0].text


@app.tool()
async def find_similar_repos(owner: str, repo: str, count: int = 3) -> str:
    """Find similar repositories (same language/topic) for comparison.

    Args:
        owner: GitHub user or org name
        repo: Repository name
        count: max similar repos to return
    """
    results = await similar.similar_tool({"owner": owner, "repo": repo, "count": count})
    return results[0].text


@app.tool()
async def find_good_first_issues(owner: str, repo: str) -> str:
    """Find beginner-friendly (good first issue / help wanted) open issues.

    Args:
        owner: GitHub user or org name
        repo: Repository name
    """
    results = await issues.issues_tool({"owner": owner, "repo": repo})
    return results[0].text


@app.tool()
async def compare_learning_repos(repos: list[str], user_level: str = "intermediate") -> str:
    """Compare 2+ repos and suggest which to learn first.

    Args:
        repos: list of full repo names like ["spring-projects/spring-boot", "quarkusio/quarkus"]
        user_level: beginner / intermediate / advanced
    """
    results = await compare.compare_tool({"repos": repos, "user_level": user_level})
    return results[0].text


@app.tool()
async def get_trending_repos_for_learning(
    language: str = "",
    topic: str = "",
    count: int = 5,
    min_stars: int = 100,
    period_days: int = 90,
) -> str:
    """Find recently popular repositories suitable for learning.

    Args:
        language: programming language filter, e.g. Python
        topic: GitHub topic filter, e.g. fastapi
        count: maximum repos to return (1-10)
        min_stars: minimum lifetime stars (default 100)
        period_days: look-back window in days (1-365)
    """
    results = await trending.trending_tool(
        {
            "language": language,
            "topic": topic,
            "count": count,
            "min_stars": min_stars,
            "period_days": period_days,
        }
    )
    return results[0].text


async def main():
    """Run the MCP server."""
    load_dotenv()  # auto-load .env file if present
    print("MCP Server starting...", file=sys.stderr, flush=True)
    await app.run_stdio_async()


if __name__ == "__main__":
    asyncio.run(main())
