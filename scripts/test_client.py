"""Simple MCP client to test the server locally."""

import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    """Connect to the MCP server and call get_server_info."""
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_github_learning_assistant"],
        env=None,
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Available tools:", [tool.name for tool in tools.tools])

            result = await session.call_tool("get_server_info", {})
            print("Tool result:")
            for content in result.content:
                print(content.text)


if __name__ == "__main__":
    asyncio.run(main())
