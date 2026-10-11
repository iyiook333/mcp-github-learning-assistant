"""MCP tool: compare candidate repos for learning."""

from mcp.types import TextContent

from ..comparer import compare_repos


async def compare_tool(arguments: dict) -> list[TextContent]:
    """Entry point: expects `repos` (list of full names) and optional user_level."""
    repos = arguments.get("repos") or []
    if not isinstance(repos, list) or len(repos) < 2:
        return [TextContent(type="text", text="Please provide at least 2 repos as list of 'owner/repo'.")]
    level = arguments.get("user_level", "intermediate")

    try:
        result = await compare_repos(repos, level)
    except Exception as e:
        return [TextContent(type="text", text=f"Comparison failed: {e}")]
    return [TextContent(type="text", text=result.model_dump_json(indent=2))]