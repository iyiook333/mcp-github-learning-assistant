"""Find good first issues for newcomers."""

import re

from .github_client import github_client
from .models.outputs import FirstIssueList

_TAG_RE = re.compile(r"<[^>]+>")


def _clean(text: str, limit: int = 200) -> str:
    """Strip HTML tags and truncate text."""
    return re.sub(_TAG_RE, "", text or "")[:limit].strip()


async def find_first_issues(owner: str, repo: str, labels) -> FirstIssueList:
    """Fetch open issues matching ANY of the starter-friendly labels (OR query).

    We split multiple labels into separate requests because GitHub API's
    `labels` param is AND semantics, which almost always yields no results
    when passing multiple labels together.
    """
    label_list = [x.strip() for x in (labels[0] if labels else "").split(",") if x.strip()]
    if not label_list:
        label_list = ["good first issue"]

    async with await github_client() as client:
        all_issues: dict[int, dict] = {}
        for label in label_list:
            resp = await client.get(
                f"/repos/{owner}/{repo}/issues",
                params={"labels": label, "state": "open", "per_page": 10},
            )
            if resp.status_code != 200:
                continue
            for it in resp.json():
                if "pull_request" in it:  # skip PRs
                    continue
                all_issues[it["number"]] = it  # dedupe by issue number

    ordered = sorted(all_issues.values(), key=lambda x: x.get("number", 0), reverse=True)

    issues = [
        {
            "number": it.get("number"),
            "title": it.get("title"),
            "url": it.get("html_url"),
            "labels": [label.get("name") for label in it.get("labels", [])],
            "preview": _clean(it.get("body") or ""),
        }
        for it in ordered[:10]
    ]

    return FirstIssueList(repo=f"{owner}/{repo}", issues=issues)
