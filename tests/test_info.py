"""Tests for info tool."""

from mcp_github_learning_assistant.tools.info import get_server_info


async def test_get_server_info():
    """Test get_server_info returns expected content."""
    result = await get_server_info()
    assert len(result) == 1
    assert "MCP GitHub Learning Assistant" in result[0].text
