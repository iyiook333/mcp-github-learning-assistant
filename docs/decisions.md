# 决策记录

## 2026-10-10：项目方向

决定不做通用 GitHub MCP Server，因为 GitHub 官方已经做了很全的版本。
我们选择「开源学习助手」这一细分方向，聚焦学习决策。

## 2026-10-10：技术选型

- 语言：Python 3.10+
- 原因：MCP 官方 Python SDK 最成熟，上手快，适合快速验证
- 分发方式：pip install（主要），Docker 后续可选
- 依赖管理：pyproject.toml + pip
- 测试客户端：Cherry Studio（国产开源，MCP 支持好）
- 备选客户端：Cline（VS Code 插件）、LobeHub

## 2026-10-10：GitHub API 选择

使用 GitHub REST API v3，因为：
- 文档完善
- 无需复杂 GraphQL 查询
- 覆盖我们需要的所有功能

## 2026-10-10：部署策略

优先 pip install，原因：
- Python 项目安装最自然
- 用户已有 Python 环境
- 比 Docker 轻量
- 开发和调试更方便

Docker 作为第二阶段的可选方案。

## 2026-10-10：测试客户端

没有 Claude Desktop，选择国产客户端 Cherry Studio 进行测试。
Cherry Studio 开源、支持 MCP、中文界面友好。
