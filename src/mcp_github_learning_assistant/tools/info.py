"""Simple info tool for testing."""

from mcp.types import TextContent


async def get_server_info() -> list[TextContent]:
    """Return server information."""
    return [
        TextContent(
            type="text",
            text="MCP GitHub Learning Assistant v0.1.0 - 帮助开发者发现适合学习的开源项目",
        )
    ]
