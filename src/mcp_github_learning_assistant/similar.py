"""Find similar repos using GitHub search.

Strategy (in order of specificity):
1. Search by the source repo's primary topic + language
2. If no topics, use descriptive keywords from repo name/description + language
3. Fall back to language-only query with framework-ish qualifier
"""

from .github_client import github_client
from .models.outputs import SimilarRepoList

# Very generic topics that give bad results if used alone
_GENERIC_TOPICS = {
    "python", "javascript", "typescript", "java", "go", "rust",
    "api", "library", "framework", "http", "server", "cli", "json",
    "hacktoberfest",
}


def _pick_topic(topics: list) -> str | None:
    """Pick the most topic-meaningful label."""
    for t in topics:
        if t.lower() not in _GENERIC_TOPICS:
            return t
    return None


def _keywords_from_name_desc(repo_name: str, desc: str) -> str:
    """Extract a short query from repo name or description."""
    # Try name first, take main word
    base = repo_name.split("/")[-1].lower()
    if len(base) > 3:
        return base
    # Fall back to first few words of description
    words = (desc or "").split()
    return " ".join(words[:3]) if words else ""


async def find_similar(owner: str, repo: str, count: int) -> SimilarRepoList:
    """Search GitHub for thematically similar repos (not merely same language)."""
    async with await github_client() as client:
        base_resp = await client.get(f"/repos/{owner}/{repo}")
        base_resp.raise_for_status()
        base = base_resp.json()

        language = base.get("language") or "Unknown"
        topics = base.get("topics") or []
        description = base.get("description") or ""

        topic = _pick_topic(topics) if topics else None
        if topic:
            q = f"topic:{topic} language:{language}"
        else:
            kw = _keywords_from_name_desc(repo, description)
            # Exclude generic keyword to avoid joining unrelated top-repos
            if kw and len(kw) > 3:
                q = f"{kw} language:{language} stars:>1000"
            else:
                q = f"language:{language} stars:>10000"  # last resort

        search_resp = await client.get(
            "/search/repositories",
            params={"q": q, "sort": "stars", "order": "desc", "per_page": 20},
        )
        search_resp.raise_for_status()
        items = search_resp.json().get("items", [])

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
