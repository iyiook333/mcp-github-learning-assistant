"""Tests for trending repository search."""

from datetime import datetime, timedelta, timezone

from mcp_github_learning_assistant import trending
from mcp_github_learning_assistant.tools.trending import trending_tool


class FakeResponse:
    status_code = 200

    def raise_for_status(self):
        return None

    def json(self):
        return {
            "items": [
                {
                    "full_name": "example/older",
                    "stargazers_count": 700,
                    "language": "Python",
                    "description": "Popular project",
                    "html_url": "https://github.com/example/older",
                    "created_at": (
                        datetime.now(timezone.utc) - timedelta(days=70)
                    ).isoformat().replace("+00:00", "Z"),
                },
                {
                    "full_name": "example/newer",
                    "stargazers_count": 500,
                    "language": "Python",
                    "description": "Fast rising project",
                    "html_url": "https://github.com/example/newer",
                    "created_at": (
                        datetime.now(timezone.utc) - timedelta(days=10)
                    ).isoformat().replace("+00:00", "Z"),
                    "archived": False,
                    "fork": False,
                },
            ]
        }


class FakeClient:
    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        return False

    async def get(self, path, params=None):
        assert path == "/search/repositories"
        assert "language:python" in params["q"]
        assert "created:>" in params["q"]
        assert params["sort"] == "stars"
        return FakeResponse()


async def fake_github_client():
    return FakeClient()


async def test_get_trending_repos_ranks_by_recent_stars(monkeypatch):
    monkeypatch.setattr(trending, "github_client", fake_github_client)
    result = await trending.get_trending_repos(
        language="Python",
        topic="",
        count=2,
        min_stars=100,
        period_days=90,
    )

    assert result.language == "python"
    assert [repo.repo for repo in result.repos] == ["example/newer", "example/older"]
    assert result.repos[0].stars_per_day > result.repos[1].stars_per_day


async def test_trending_tool_requires_language_or_topic():
    result = await trending_tool({})
    assert result[0].text == "Provide a language and/or topic."
