"""MCP tool: analyze repo for learning."""

from mcp.types import TextContent

from ..analyzer import analyze_repo


async def analyze_repo_tool(arguments: dict) -> list[TextContent]:
    """Entry point called by AI.

    Args:
        arguments: dict with keys `owner` and `repo`.
    """
    try:
        owner = arguments["owner"]
        repo = arguments["repo"]
    except KeyError as e:
        return [TextContent(type="text", text=f"Missing required argument: {e}")]

    try:
        result = await analyze_repo(owner, repo)
    except Exception as e:
        return [TextContent(type="text", text=f"Analysis failed: {e}")]

    return [TextContent(type="text", text=result.model_dump_json(indent=2))]
