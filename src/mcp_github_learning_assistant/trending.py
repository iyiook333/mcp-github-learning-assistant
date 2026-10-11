"""Find recently popular repositories using GitHub search."""

from datetime import datetime, timedelta, timezone

from .github_client import github_client
from .models.outputs import TrendingRepo, TrendingRepoList


def _build_query(language: str, topic: str, min_stars: int, created_after: str) -> str:
    """Build a GitHub repository search query."""
    terms = [
        f"language:{language}" if language else "",
        f"topic:{topic}" if topic else "",
        f"stars:>={min_stars}",
        f"created:>{created_after}",
        "archived:false",
        "fork:false",
    ]
    return " ".join(term for term in terms if term)


def _parse_created_at(value: str) -> datetime | None:
    """Parse an ISO-8601 GitHub timestamp safely."""
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, TypeError, ValueError):
        return None


async def get_trending_repos(
    language: str,
    topic: str,
    count: int,
    min_stars: int,
    period_days: int,
) -> TrendingRepoList:
    """Find high-star repositories created within the requested period."""
    language = language.strip().lower()
    topic = topic.strip().lower()
    period_ended = datetime.now(timezone.utc)
    period_started = period_ended - timedelta(days=period_days)
    created_after = period_started.date().isoformat()
    search_query = _build_query(language, topic, min_stars, created_after)

    async with await github_client() as client:
        response = await client.get(
            "/search/repositories",
            params={
                "q": search_query,
                "sort": "stars",
                "order": "desc",
                "per_page": count,
            },
        )
        response.raise_for_status()
        items = response.json().get("items", [])

    repos: list[TrendingRepo] = []
    for item in items:
        created_at = _parse_created_at(item.get("created_at"))
        age_days = max(
            1, (period_ended - created_at).days if created_at else period_days
        )
        stars = item.get("stargazers_count", 0)
        repos.append(
            TrendingRepo(
                repo=item.get("full_name") or "",
                stars=stars,
                stars_per_day=round(stars / age_days, 1),
                language=item.get("language") or "Unknown",
                description=item.get("description") or "",
                url=item.get("html_url") or "",
            )
        )

    repos.sort(key=lambda repo: repo.stars_per_day, reverse=True)
    return TrendingRepoList(
        language=language or None,
        topic=topic or None,
        period_days=period_days,
        repos=repos,
    )
