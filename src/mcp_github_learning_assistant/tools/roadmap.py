"""MCP tool: generate learning roadmap from repo structure."""

from mcp.types import TextContent

from ..roadmap import build_roadmap


async def roadmap_tool(arguments: dict) -> list[TextContent]:
    """Entry point: expects owner, repo, depth(optional)."""
    try:
        owner = arguments["owner"]
        repo = arguments["repo"]
    except KeyError as e:
        return [TextContent(type="text", text=f"Missing required argument: {e}")]
    depth = int(arguments.get("depth", 2))
    depth = max(1, min(depth, 3))

    try:
        result = await build_roadmap(owner, repo, depth)
    except Exception as e:
        return [TextContent(type="text", text=f"Roadmap failed: {e}")]
    return [TextContent(type="text", text=result.model_dump_json(indent=2))]
