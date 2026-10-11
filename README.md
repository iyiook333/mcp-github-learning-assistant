# MCP GitHub Learning Assistant

An MCP (Model Context Protocol) server that helps developers discover and learn from open-source projects on GitHub, based on their skill level and goals.

## Features

- Recommend learning repositories based on your profile
- Analyze whether a repository is worth learning
- Generate a learning roadmap from repo structure
- Find similar repositories for comparison
- Compare multiple candidate repos
- Find good first issues for newcomers
- Get trending repos for learning

## Installation

```bash
pip install mcp-github-learning-assistant
```

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

## Usage in Cherry Studio

1. Open Cherry Studio, go to Settings -> MCP
2. Add an MCP server with the command:

```bash
python -m mcp_github_learning_assistant
```

3. Set the environment variable `GITHUB_TOKEN`

## Development

```bash
git clone https://github.com/iyiook333/mcp-github-learning-assistant.git
cd mcp-github-learning-assistant
pip install -e .[dev]
pytest
```

## Tools

| Tool | Description |
|------|-------------|
| `get_server_info` | Get server version and description |
| `analyze_repo_for_learning` | Analyze a GitHub repo: score, difficulty, prerequisites, suggested learning path |

## License

MIT