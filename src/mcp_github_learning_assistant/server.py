"""MCP server entry point."""

import asyncio
import sys

from mcp.server import MCPServer

from .tools import analyze

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


async def main():
    """Run the MCP server."""
    print("MCP Server starting...", file=sys.stderr, flush=True)
    await app.run_stdio_async()


if __name__ == "__main__":
    asyncio.run(main())
