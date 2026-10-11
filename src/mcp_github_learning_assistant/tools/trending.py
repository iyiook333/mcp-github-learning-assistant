"""MCP tool: find recent popular repositories."""

from mcp.types import TextContent

from ..trending import get_trending_repos


async def trending_tool(arguments: dict) -> list[TextContent]:
    """Entry point: expects language and/or topic with search options."""
    language = str(arguments.get("language", "")).strip()
    topic = str(arguments.get("topic", "")).strip()
    if not language and not topic:
        return [TextContent(type="text", text="Provide a language and/or topic.")]

    try:
        count = max(1, min(int(arguments.get("count", 5)), 10))
        min_stars = max(0, int(arguments.get("min_stars", 100)))
        period_days = max(1, min(int(arguments.get("period_days", 90)), 365))
    except (TypeError, ValueError):
        count = 5
        min_stars = 100
        period_days = 90

    try:
        result = await get_trending_repos(
            language=language.lower(),
            topic=topic.lower(),
            count=count,
            min_stars=min_stars,
            period_days=period_days,
        )
    except Exception as error:
        return [TextContent(type="text", text=f"Trending lookup failed: {error}")]

    return [TextContent(type="text", text=result.model_dump_json(indent=2))]
