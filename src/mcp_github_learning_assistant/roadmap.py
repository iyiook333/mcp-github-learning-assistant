"""Learning-roadmap logic based on repo top-level structure."""

from .github_client import github_client
from .models.outputs import RepoRoadmap

# Directories to skip: not helpful for learning
_SKIP_PATTERNS = {
    ".github", ".idea", ".vscode", ".git", ".circleci", ".devcontainer",
    "antora", "config", "buildpack", "gradle", "mvn", "scripts",
    "distribution", "buildsrc", "build", "eclipse", "git", "ci",
    "framework", "checkstyle", "etc",
}

# Ordered learning priority by directory-name keywords
_HINTS = [
    ("doc", "Read documentation first for concepts and setup", 1),
    ("example", "Run sample examples to see usage", 2),
    ("test", "Read tests to learn expected behavior", 5),
    ("core", "Study core implementation module", 3),
    ("src", "Study main source code", 3),
    ("lib", "Review library internals", 4),
    ("app", "Understand application entry points", 4),
    ("web", "Front-end integration details", 4),
    ("tools", "Look at build/dev tooling", 6),
]

# Lower `priority` = earlier in learning order
_PRIORITY_DEFAULT = 5  # for unmatched dirs


def _priority_for(name: str) -> tuple[int, str]:
    """Return (priority, hint). Lower priority learns first."""
    for kw, hint, prio in _HINTS:
        if kw in name.lower():
            return prio, hint
    return _PRIORITY_DEFAULT, "Explore module to understand its purpose"


def _skip(name: str) -> bool:
    """Return True if this directory should not appear in roadmap."""
    return name.lower() in _SKIP_PATTERNS or name.startswith(".")


async def build_roadmap(owner: str, repo: str, depth: int) -> RepoRoadmap:
    """Fetch top-level content and produce a clean, ordered learning roadmap."""
    async with await github_client() as client:
        resp = await client.get(f"/repos/{owner}/{repo}/contents")
        resp.raise_for_status()
        items = resp.json()

    dirs = [item for item in items if item.get("type") == "dir" and not _skip(item.get("name", ""))]

    # Sort by priority then name so ordering is deterministic
    scored = []
    for d in dirs:
        prio, hint = _priority_for(d.get("name", ""))
        scored.append((prio, d.get("name", ""), hint, d.get("path")))

    scored.sort(key=lambda x: (x[0], x[1]))

    modules = []
    for i, (prio, name, hint, path) in enumerate(scored[:10], start=1):
        modules.append(
            {
                "name": name,
                "hint": hint,
                "learning_order": i,
                "path": path,
            }
        )

    summary = (
        f"Generated learning sequence with {len(modules)} relevant modules "
        f"from {owner}/{repo} top level (skipped {len([i for i in items if i.get('type') == 'dir']) - len(dirs)} non-source directories)."
    )
    return RepoRoadmap(repo=f"{owner}/{repo}", modules=modules, summary=summary)