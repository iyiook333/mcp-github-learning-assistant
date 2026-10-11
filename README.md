# MCP GitHub Learning Assistant

一个基于 MCP 协议的开源学习助手，帮助开发者根据自身水平和目标，发现适合学习的 GitHub 开源项目。

## 功能

- 根据用户定位推荐学习项目
- 深度分析项目是否适合学习
- 根据项目结构生成学习路线
- 查找相似项目做对比
- 对比多个候选项目
- 发现适合新手的 good first issues
- 获取近期热门学习项目

## 安装

`ash
pip install mcp-github-learning-assistant
`

## 配置

需要设置 GitHub Personal Access Token：

`ash
# Windows PowerShell
 = "your_github_token"

# Linux/macOS
export GITHUB_TOKEN=your_github_token
`

## 在 Cherry Studio 中使用

1. 打开 Cherry Studio，进入设置 → MCP
2. 添加 MCP Server，命令为：
   `ash
   python -m mcp_github_learning_assistant
   `
3. 配置环境变量 GITHUB_TOKEN

## 开发

`ash
git clone https://github.com/yourusername/mcp-github-learning-assistant.git
cd mcp-github-learning-assistant
pip install -e .[dev]
pytest
`

## License

MIT
