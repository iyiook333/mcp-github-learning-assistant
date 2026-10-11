"""Analysis logic: turn GitHub raw data into learning advice."""

import base64

from .github_client import github_client
from .models.outputs import RepoAnalysis

_PREREQ_MAP = {
    "Java": ["Java basics", "Maven/Gradle", "IDE usage"],
    "Python": ["Python basics", "pip/venv", "Data structures"],
    "TypeScript": ["TypeScript basics", "npm/pnpm", "Node.js"],
    "JavaScript": ["JavaScript basics", "npm", "DOM"],
    "Go": ["Go basics", "go mod"],
    "Rust": ["Rust basics", "cargo"],
}


def _score_doc_length(readme_len: int) -> str:
    """Judge doc quality roughly by README length."""
    if readme_len > 10000:
        return "excellent"
    elif readme_len > 3000:
        return "good"
    elif readme_len > 500:
        return "fair"
    return "poor"


def _judge_difficulty(stars: int) -> str:
    """Rough difficulty by repo size; can be refined later."""
    if stars > 50000:
        return "intermediate"
    return "beginner"


def _build_prerequisites(language: str) -> list[str]:
    """Recommend prerequisites by main language."""
    return _PREREQ_MAP.get(language, ["Basic programming"])


def _build_path(doc_quality: str) -> list[str]:
    """Build a suggested learning path."""
    path = ["Read README to understand positioning"]
    if doc_quality in ("good", "excellent"):
        path.append("Follow official docs / quickstart with a minimal example")
    path.extend([
        "Browse repo structure, find core modules",
        "Start reading code via a small issue or feature",
    ])
    return path


async def analyze_repo(owner: str, repo: str) -> RepoAnalysis:
    """Fetch data from GitHub API and produce analysis."""
    async with await github_client() as client:
        # 1. Basic repo info
        repo_resp = await client.get(f"/repos/{owner}/{repo}")
        repo_resp.raise_for_status()
        repo_data = repo_resp.json()

        # 2. Language breakdown
        lang_resp = await client.get(f"/repos/{owner}/{repo}/languages")
        lang_data = lang_resp.json()
        main_language = next(iter(lang_data), repo_data.get("language") or "Unknown")

        # 3. Recent commit activity
        commit_resp = await client.get(
            f"/repos/{owner}/{repo}/commits", params={"per_page": 1}
        )
        has_commits = commit_resp.status_code == 200 and len(commit_resp.json()) > 0

        # 4. README quality
        readme_resp = await client.get(f"/repos/{owner}/{repo}/readme")
        readme_bytes = readme_resp.json().get("content", "")
        readme_text = base64.b64decode(readme_bytes).decode("utf-8", errors="ignore")
        doc_quality = _score_doc_length(len(readme_text))

    stars = repo_data["stargazers_count"]
    difficulty = _judge_difficulty(stars)
    prerequisites = _build_prerequisites(main_language)
    path = _build_path(doc_quality)

    pros: list[str] = []
    if stars > 10000:
        pros.append(f"Large community ({stars} stars)")
    if doc_quality in ("good", "excellent"):
        pros.append("Well documented")
    if has_commits:
        pros.append("Actively maintained")

    cons: list[str] = []
    if stars > 50000:
        cons.append("Large codebase, takes time to read")
    if doc_quality == "poor":
        cons.append("Weak docs, will rely on source code")

    score = stars / 10000 + 3.0
    if doc_quality in ("good", "excellent"):
        score += 1.0
    if not has_commits:
        score -= 2.0
    score = max(0.0, min(10.0, round(score, 1)))

    active_text = "still maintained" if has_commits else "possibly unmaintained"
    summary = (
        f"{repo_data['full_name']} has {stars} stars, main language {main_language}. "
        f"Doc quality is {doc_quality}, project is {active_text}. "
        f"Overall difficulty: {difficulty}."
    )

    return RepoAnalysis(
        repo_name=repo_data["full_name"],
        stars=stars,
        language=main_language,
        difficulty=difficulty,
        learning_score=score,
        prerequisites=prerequisites,
        pros=pros,
        cons=cons,
        suggested_path=path,
        doc_quality=doc_quality,
        active=has_commits,
        summary=summary,
    )

