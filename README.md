# MCP GitHub Learning Assistant

[![PyPI version](https://img.shields.io/pypi/v/mcp-github-learning-assistant.svg)](https://pypi.org/project/mcp-github-learning-assistant/)
[![CI](https://github.com/iyiook333/mcp-github-learning-assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/iyiook333/mcp-github-learning-assistant/actions/workflows/ci.yml)

An MCP (Model Context Protocol) server that helps developers discover and learn from open-source projects on GitHub, based on their skill level and goals.

## Features

8 tools to support every stage of open-source learning:

| Tool | Description |
|------|-------------|
| `analyze_repo_for_learning` | Score a repo: stars, doc quality, difficulty, prerequisites, suggested learning path |
| `recommend_learning_repos` | Curated recommendations per tech stack (Spring Boot, FastAPI, Vue, React, Electron, HarmonyOS) |
| `get_repo_roadmap` | Generate a step-by-step learning roadmap from a repo's directory structure |
| `find_similar_repos` | Find thematically similar repos (same language/topic) for comparison |
| `find_good_first_issues` | Find beginner-friendly open issues (good first issue / help wanted) |
| `compare_learning_repos` | Compare 2+ candidate repos and suggest which to learn first |
| `get_trending_repos_for_learning` | Find breakout repos created recently by language/topic |
| `get_server_info` | Verify the MCP server connection |

## Screenshots

| MCP Inspector - Tools list | MCP Inspector - analyze_repo_for_learning result |
|:---:|:---:|
| ![Inspector Tools](https://raw.githubusercontent.com/iyiook333/mcp-github-learning-assistant/master/docs/screenshots/inspector-tools.jpg) | ![Inspector Analyze](https://raw.githubusercontent.com/iyiook333/mcp-github-learning-assistant/master/docs/screenshots/inspector-analyze.jpg) |

Screenshots use dark-mode crops under 500KB each.

## Installation

```bash
pip install mcp-github-learning-assistant
```

Requires Python 3.10+ and `mcp>=2.3.0`.

## Configuration

Set your GitHub Personal Access Token:

```powershell
# Windows PowerShell
$env:GITHUB_TOKEN = "your_github_token"
```

```bash
# Linux / macOS
export GITHUB_TOKEN=your_github_token
```

Token scope: fine-grained PAT with no special permissions (public repo read-only) is enough.
## Entry Point

After `pip install mcp-github-learning-assistant`, the console command `mcp-github-learning` is available:

```bash
mcp-github-learning
```

This is equivalent to `python -m mcp_github_learning_assistant`.

## Usage in MCP Clients

### MCP Inspector (development)

```bash
npx @modelcontextprotocol/inspector mcp-github-learning
```

### Cherry Studio

1. Open Cherry Studio, go to Settings -> MCP
2. Add an MCP server with the command `mcp-github-learning`
3. Set the environment variable `GITHUB_TOKEN`

### Claude Desktop

Edit `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mcp-github-learning": {
      "command": "mcp-github-learning",
      "env": {
        "GITHUB_TOKEN": "your_github_token"
      }
    }
  }
}
```

> On Windows, if the command is not found, use the full path or fall back to `python -m mcp_github_learning_assistant`.

### DSH / Dify

Add an MCP server of type `stdio`:

```yaml
name: mcp-github-learning
transport: stdio
command: mcp-github-learning
env:
  GITHUB_TOKEN: your_github_token
```

If the client does not support custom `env`, set `GITHUB_TOKEN` at the system level before launching the client.

## Current limitations

These are known and intentional, not bugs. They are listed so the tool's output is not over-trusted.

- **No AI/LLM layer.** Scoring is deterministic: star thresholds, README byte length, and directory-name
  keyword matching. There are no embeddings and no model calls.
- **`recommend_learning_repos` uses a curated seed list**, currently covering Spring Boot, FastAPI, Vue,
  React, Electron and HarmonyOS. Any other stack returns an empty list rather than a bad guess.
- **Only `get_trending_repos_for_learning` derives its ranking from data** — it computes
  `stars / age_in_days` and re-sorts, since GitHub has no public trending API.
- **No HTTP caching, retry, backoff, or pagination.** Unauthenticated GitHub allows 60 requests/hour, and
  one `recommend_learning_repos` call can spend several of them. Always set `GITHUB_TOKEN`.
- **Some parameters are accepted but not yet used** (`depth` in `get_repo_roadmap`, `user_level`
  comparison weighting in `compare_learning_repos`). They are reserved for the next iteration.
- **Test coverage is partial.** 9 tests cover `analyze`, `roadmap`, `trending` and `info`; the
  `recommender`, `comparer`, `similar` and `issuefind` modules have none.

## Development

```bash
git clone https://github.com/iyiook333/mcp-github-learning-assistant.git
cd mcp-github-learning-assistant
pip install -e .[dev]
pytest
```

## License

MIT
