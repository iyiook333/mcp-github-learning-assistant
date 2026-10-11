"""GitHub API client."""

import os

import httpx

GITHUB_API_BASE = "https://api.github.com"


def get_github_token() -> str | None:
    """Get GitHub token from environment."""
    return os.environ.get("GITHUB_TOKEN")


async def github_client() -> httpx.AsyncClient:
    """Create an authenticated GitHub API client."""
    token = get_github_token()
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "mcp-github-learning-assistant",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return httpx.AsyncClient(base_url=GITHUB_API_BASE, headers=headers, timeout=30.0)
