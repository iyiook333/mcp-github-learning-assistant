"""Direct test for find_first_issues (no MCP involved)."""

import asyncio

from mcp_github_learning_assistant.issuefind import find_first_issues


async def main():
    """vscode reliably has many good first issues."""
    r = await find_first_issues("microsoft", "vscode", ["good first issue"])
    print(r.model_dump_json(indent=2))


asyncio.run(main())