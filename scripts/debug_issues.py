"""Debug why issue queries return empty."""

import asyncio
import os

from dotenv import load_dotenv
from mcp_github_learning_assistant.github_client import github_client


async def main():
    """Print raw responses for label queries."""
    load_dotenv()
    owner, repo = "spring-projects", "spring-boot"

    async with await github_client() as client:
        # No-label baseline
        r0 = await client.get(
            f"/repos/{owner}/{repo}/issues",
            params={"state": "open", "per_page": 3},
        )
        print("no-label status:", r0.status_code)
        if r0.status_code == 200:
            items = r0.json()
            print("  got", len(items), "issues (any labels)")
            for it in items:
                print("   -", it.get("number"), it.get("title"))

        # Label query
        r1 = await client.get(
            f"/repos/{owner}/{repo}/issues",
            params={"labels": "good first issue", "state": "open", "per_page": 3},
        )
        print("good-first-issue status:", r1.status_code)
        print("  body[:300]:", r1.text[:300])

        # Search API alternative (OR across labels)
        q = f"repo:{owner}/{repo} is:issue is:open label:'good first issue',label:'help wanted'"
        r2 = await client.get("/search/issues", params={"q": q, "per_page": 5})
        print("search-api status:", r2.status_code)
        if r2.status_code == 200:
            data = r2.json()
            print("  total_count:", data.get("total_count"))
            for it in data.get("items", [])[:5]:
                print("   -", it.get("number"), it.get("title"))


asyncio.run(main())