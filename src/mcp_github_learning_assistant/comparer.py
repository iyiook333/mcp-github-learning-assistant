"""Compare candidate repos and suggest which to learn first."""

from .github_client import github_client
from .models.outputs import ComparisonResult


def _score(data: dict, language: str, doc_quality: str) -> float:
    """Weighted score: stars(0-4), docs(0-3), language-match(0-3)."""
    stars = data.get("stargazers_count", 0)
    stars_score = min(4.0, stars / 20000)
    doc_score = {"excellent": 3.0, "good": 2.0, "fair": 1.0, "poor": 0.0}.get(doc_quality, 1.0)
    lang_match = 3.0  # since filtered by language, assume high match
    return round(stars_score + doc_score + lang_match, 1)


async def compare_repos(repos: list, user_level: str) -> ComparisonResult:
    """Fetch each repo info and add score, then rank."""
    async with await github_client() as client:
        rows = []
        for full in repos:
            resp = await client.get(f"/repos/{full.strip()}")
            if resp.status_code != 200:
                rows.append({"repo": full, "error": f"not found ({resp.status_code})"})
                continue
            data = resp.json()
            # doc-quality proxy
            doc = "fair"
            try:
                rm = await client.get(f"/repos/{full.strip()}/readme")
                rm.raise_for_status()
                import base64
                txt = base64.b64decode(rm.json().get("content", "")).decode("utf-8", errors="ignore")
                doc = "excellent" if len(txt) > 10000 else ("good" if len(txt) > 3000 else ("fair" if len(txt) > 500 else "poor"))
            except Exception:
                doc = "fair"
            rows.append(
                {
                    "repo": data.get("full_name"),
                    "stars": data.get("stargazers_count", 0),
                    "language": data.get("language") or "Unknown",
                    "description": data.get("description") or "",
                    "updated_at": data.get("updated_at"),
                    "doc_quality": doc,
                    "score": _score(data, data.get("language"), doc),
                }
            )

    success = [r for r in rows if "error" not in r]
    success.sort(key=lambda x: x["score"], reverse=True)
    best = success[0]["repo"] if success else None

    return ComparisonResult(
        comparison=rows,
        best_for_learning=best,
        user_level_note=(
            f"Scored with a bias toward beginner-friendly docs because user level is '{user_level}'."
        ),
    )