"""MCP tool: find similar repositories by language & topic."""

from mcp.types import TextContent

from ..similar import find_similar


async def similar_tool(arguments: dict) -> list[TextContent]:
    """Entry point: expects owner, repo, count(optional)."""
    try:
        owner = arguments["owner"]
        repo = arguments["repo"]
    except KeyError as e:
        return [TextContent(type="text", text=f"Missing required argument: {e}")]
    count = int(arguments.get("count", 3))
    count = max(1, min(count, 10))

    try:
        result = await find_similar(owner, repo, count)
    except Exception as e:
        return [TextContent(type="text", text=f"Similar-repos failed: {e}")]
    return [TextContent(type="text", text=result.model_dump_json(indent=2))]
