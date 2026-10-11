# 项目规划

## 产品定位

帮助开发者（尤其是初学者和转行者）根据自身水平和目标，发现适合学习的 GitHub 开源项目。

区别于 GitHub 官方 MCP Server（侧重仓库操作），我们聚焦「学习决策」。

## 目标用户

- 编程初学者
- 转行开发者
- 面试准备者
- 想参与开源的人
- 进阶学习者

## 核心功能

### Tools
1. recommend_learning_repos：根据定位推荐项目
2. analyze_repo_for_learning：深度分析项目学习价值
3. get_repo_roadmap：生成学习路线
4. find_similar_repos：查找相似项目
5. compare_learning_repos：对比多个项目
6. find_good_first_issues：找适合新手的 issue
7. get_trending_repos_for_learning：发现热门学习项目

## 技术栈

- Python 3.10+
- MCP 官方 SDK
- httpx
- pydantic
- pytest
- ruff
- pip / uv

## 开发阶段

### Week 1：项目骨架 + recommend tool
- 搭建项目结构
- 封装 GitHub API 客户端
- 实现第一个 Tool：recommend_learning_repos
- 在 Cherry Studio 中测试

### Week 2：核心分析工具
- analyze_repo_for_learning
- get_repo_roadmap
- find_similar_repos

### Week 3：高级工具 + Prompts
- compare_learning_repos
- find_good_first_issues
- get_trending_repos_for_learning
- 添加 MCP Prompts

### Week 4：测试 + 发布 + 文档
- 补充 pytest 测试
- GitHub Actions CI
- 发布到 PyPI
- 完善 README 和使用教程
