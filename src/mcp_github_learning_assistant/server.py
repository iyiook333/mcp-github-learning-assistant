"""MCP server entry point."""

import asyncio
import sys

from dotenv import load_dotenv
from mcp.server import MCPServer

from .tools import analyze, recommend

app = MCPServer("mcp-github-learning-assistant")


@app.tool()
async def get_server_info() -> str:
    """获取 MCP Server 的基本信息，用于测试连接是否成功。"""
    return "MCP GitHub Learning Assistant v0.1.0 - 帮助开发者发现适合学习的开源项目"


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


async def main():
    """Run the MCP server."""
    load_dotenv()  # auto-load .env file if present
    print("MCP Server starting...", file=sys.stderr, flush=True)
    await app.run_stdio_async()


if __name__ == "__main__":
    asyncio.run(main())