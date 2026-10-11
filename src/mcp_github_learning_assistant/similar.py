"""Find similar repos using GitHub search by language & topic."""

from .github_client import github_client
from .models.outputs import SimilarRepoList


async def find_similar(owner: str, repo: str, count: int) -> SimilarRepoList:
    """Search GitHub for repos with same language/topic, high stars."""
    async with await github_client() as client:
        # Get base repo info
        base_resp = await client.get(f"/repos/{owner}/{repo}")
        base_resp.raise_for_status()
        base = base_resp.json()
        language = base.get("language") or "Unknown"
        topics = base.get("topics", [])

        # Prefer topic-based query if available, else by language
        if topics:
            topic = topics[0]
            q = f"topic:{topic} language:{language}"
        else:
            q = f"language:{language}"

        search_resp = await client.get(
            "/search/repositories",
            params={
                "q": q,
                "sort": "stars",
                "order": "desc",
                "per_page": 20,
            },
        )
        search_resp.raise_for_status()
        items = search_resp.json().get("items", [])

    # Exclude the source repo itself
    full = f"{owner}/{repo}"
    results = []
    for item in items:
        name = item.get("full_name")
        if name == full:
            continue
        results.append(
            {
                "repo": name,
                "stars": item.get("stargazers_count", 0),
                "language": item.get("language") or "Unknown",
                "description": item.get("description") or "",
                "url": item.get("html_url") or "",
            }
        )
        if len(results) >= count:
            break

    return SimilarRepoList(source_repo=full, similar=results)