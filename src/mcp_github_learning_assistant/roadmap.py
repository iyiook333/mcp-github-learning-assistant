"""Learning-roadmap logic based on repo top-level structure."""

from .github_client import github_client
from .models.outputs import RepoRoadmap

# Ordered learning hints by directory-name keywords
_HINTS = [
    ("docs", "Read documentation first for concepts and setup"),
    ("examples", "Run sample examples to see usage"),
    ("tests", "Read tests to learn expected behavior"),
    ("core", "Study core implementation module"),
    ("src", "Study main source code"),
    ("lib", "Review library internals"),
    ("app", "Understand application entry points"),
    ("web", "Front-end integration details"),
    ("tools", "Look at build/dev tooling"),
]


def _hint_for(name: str) -> str:
    """Attach a learning hint based on folder name keywords."""
    for kw, hint in _HINTS:
        if kw in name.lower():
            return hint
    return "Explore module to understand its purpose"


async def build_roadmap(owner: str, repo: str, depth: int) -> RepoRoadmap:
    """Fetch top-level content and produce a step-by-step roadmap."""
    async with await github_client() as client:
        resp = await client.get(f"/repos/{owner}/{repo}/contents")
        resp.raise_for_status()
        items = resp.json()

    modules = []
    for i, item in enumerate(items, start=1):
        if item.get("type") == "dir":
            modules.append(
                {
                    "name": item.get("name"),
                    "hint": _hint_for(item.get("name", "")),
                    "learning_order": i,
                    "path": item.get("path"),
                }
            )

    # Limit to 10 modules for readability
    modules = modules[:10]

    summary = (
        f"Generated a learning sequence with {len(modules)} modules "
        f"from {owner}/{repo} top-level structure."
    )
    return RepoRoadmap(repo=f"{owner}/{repo}", modules=modules, summary=summary)