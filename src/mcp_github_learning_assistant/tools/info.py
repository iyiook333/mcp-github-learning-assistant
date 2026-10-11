"""Simple info tool for testing."""

from mcp.types import TextContent


async def get_server_info() -> list[TextContent]:
    """Return server information."""
    return [
        TextContent(
            type="text",
            text=(
                "MCP GitHub Learning Assistant v0.1.0 - "
                "discover open-source projects worth learning"
            ),
        )
    ]
