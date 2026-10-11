# 决策记录

## 2026-10-10：项目方向

决定不做通用 GitHub MCP Server，因为 GitHub 官方已经做了很全的版本。
我们选择「开源学习助手」这一细分方向，聚焦学习决策。

## 2026-10-10：技术选型

- 语言：Python 3.10+
- 原因：MCP 官方 Python SDK 最成熟，上手快，适合快速验证
- 分发方式：pip install（主要），Docker 后续可选
- 依赖管理：pyproject.toml + pip
- 用户实际环境：Python 3.12.10（Windows）
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

---

## 2026-10-11：MCP SDK API 版本适配

mcp 2.3.0 的 Server 类没有 list_tools / call_tool 装饰器。
改用高层 MCPServer，使用 @app.tool() 装饰器注册工具。
决策：跟随已安装的 mcp 2.3.0 API，不回退旧版本。

## 2026-10-11：添加 python -m 运行入口

为了支持 `python -m mcp_github_learning_assistant`，
新增 src/mcp_github_learning_assistant/__main__.py 作为包执行入口。

## 2026-10-11：项目分层

参考 Spring Boot 分层结构：
- models/outputs.py  → DTO（数据结构）
- analyzer.py        → Service（核心业务逻辑）
- tools/analyze.py   → Controller（MCP 工具接入口）
- server.py          → 启动类

好处：逻辑独立、便于测试、面试讲得清楚。

## 2026-10-11：GitHub Token 策略

申请 fine-grained PAT：
- Repository access: Public Repositories (read-only)
- Permissions: 无
- 目的：只提高 60 -> 5000 次每小时的请求额度
- 传递方式：环境变量 GITHUB_TOKEN，不入库（.gitignore 排除 .env）

## 2026-10-11：评分算法调整

发现 learning_score 可能超过 10（stars 加分后再 + 文档分）。
修复：min(10.0, ...) 挪到所有加减法之后统一封顶。
评分函数是纯启发式，后续可以替换成更复杂的启发式或模型打分。

## 2026-10-11：首次 Git 提交

commit: d2ab733
提交内容：项目骨架 + 2 个工具（get_server_info、analyze_repo_for_learning）+ 文档。
其中 analyze_repo_for_learning 已实测成功（spring-projects/spring-boot）。

## 2026-10-11：确认项目不含 FastAPI

MCP 走 stdio 时不需要 HTTP 服务。
后续若支持远程部署（SSE / streamable HTTP）再考虑引入 FastAPI。


---

## 2026-10-11：MCP Inspector 调试通过

使用 MCP 官方 Inspector（npx @modelcontextprotocol/inspector）验证：
- Server 进程启动正常（stdio 待命）
- Connect 握手成功
- Tools 标签列出 get_server_info 和 analyze_repo_for_learning
- get_server_info Run 后正确返回

结论：MCP 协议层、工具注册层全链路可用，可以进入新工具开发和真实客户端（Cherry Studio）集成阶段。

## 2026-10-11：README 乱码修复

原因：PowerShell 5.1 Set-Content -Encoding UTF8 带 BOM，且代码块语言标注被写入坏字节。
修复：用 .NET [System.IO.File]::WriteAllText 配合 UTF8Encoding($false) 重写为 UTF-8 无 BOM。
README 改为英文为主，后续考虑增加 README.zh-CN.md 双语版。


---

## 2026-10-11：MVP 全部工具实数据验证通过

所有 7 个工具在真实 GitHub 数据下验证成功：
- spring-boot analysis 评分/难度/路径
- Spring Boot 仓库推荐（3 条）
- vscode good-first-issues（10 条）
- fastapi similar repos（aiohttp/starlette，语义正确）
- spring-boot vs quarkus vs micronaut 排序
- spring-boot roadmap（documentation → core → tests 顺序合理）

### Issues 空列表诊断（spring-boot）

连续三次为空，通过 debug_issues.py 三路交叉验证：
- 无 label 基线 → 有数据（排除连通性）
- labels=good first issue → []
- Search API 同条件 → total_count: 0

结论：spring-boot 确实当前 0 条 open good-first-issue（大数据项目常见），
不是 bug。测试目标切到 microsoft/vscode 后正常返回 10 条。
产品改进点（下一步）：空结果时返回引导文案而非空 JSON。

### Roadmap 优化史

第一版：按 API 返回顺序取前 10 个目录，充斥 .idea/antora/buildSrc 等噪音。
第二版：加 _SKIP_PATTERNS 跳过工程目录，按关键词赋学习优先级。
第三版：修复 "src in buildSrc" 子串误匹配（buildSrc 加入黑名单），
documentation 通过 "doc" 关键词正确识别为高优先级。
经验：目录名关键词匹配必须用词边界或黑名单双保险。

### Similar 优化史

第一版按 topic/language 搜索，fastapi 混入 public-apis（只是同为 Python）。
第二版增加策略：优先非通用 topic，其次从 repo 名/描述提关键词，
兜底 language-only + stars:>10000。fastapi 现在返回 aiohttp/starlette，语义正确。
