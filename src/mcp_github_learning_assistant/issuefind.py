"""Find good first issues for newcomers."""

import re

from .github_client import github_client
from .models.outputs import FirstIssueList

_TAG_RE = re.compile(r"<[^>]+>")


async def find_first_issues(owner: str, repo: str, labels):
    """Fetch issues filtered by starter-friendly labels."""
    q_label = ",".join(x.strip() for x in labels[0].split(","))
    async with await github_client() as client:
        resp = await client.get(
            f"/repos/{owner}/{repo}/issues",
            params={"labels": q_label, "state": "open", "per_page": 10},
        )
        resp.raise_for_status()
        items = resp.json()

    issues = []
    for it in items:
        if "pull_request" in it:  # GitHub includes PRs, skip them
            continue
        body = re.sub(_TAG_RE, "", (it.get("body") or ""))[:200]
        issues.append(
            {
                "number": it.get("number"),
                "title": it.get("title"),
                "url": it.get("html_url"),
                "labels": [l.get("name") for l in it.get("labels", [])],
                "preview": body.strip(),
            }
        )

    return FirstIssueList(repo=f"{owner}/{repo}", issues=issues)