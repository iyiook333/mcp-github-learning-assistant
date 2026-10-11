"""MCP tool: find good first issues."""

from mcp.types import TextContent

from ..issuefind import find_first_issues


async def issues_tool(arguments: dict) -> list[TextContent]:
    """Entry point: expects owner, repo(optional labels)."""
    try:
        owner = arguments["owner"]
        repo = arguments["repo"]
    except KeyError as e:
        return [TextContent(type="text", text=f"Missing required argument: {e}")]
    labels = arguments.get("labels", "good first issue,help wanted")

    try:
        result = await find_first_issues(owner, repo, [labels])
    except Exception as e:
        return [TextContent(type="text", text=f"Issue-finding failed: {e}")]
    return [TextContent(type="text", text=result.model_dump_json(indent=2))]
