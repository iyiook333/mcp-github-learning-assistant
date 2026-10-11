"""MCP tool: recommend learning repositories based on user profile."""

from mcp.types import TextContent

from ..recommender import recommend_repos


async def recommend_repos_tool(arguments: dict) -> list[TextContent]:
    """Entry point called by AI.

    Expected argument keys:
        role: student / backend_dev / frontend_dev / mobile_dev / ai_dev
        target_tech: e.g. Spring Boot, FastAPI, Vue 3
        experience_level: beginner / intermediate / advanced
        goal: interview_prep / skill_upgrade / open_source / project_practice
        count: max recommendations to return
    """
    role = arguments.get("role", "student")
    tech = arguments.get("target_tech", "")
    level = arguments.get("experience_level", "beginner")
    goal = arguments.get("goal", "skill_upgrade")
    count = arguments.get("count", 5)
    try:
        count = max(1, min(int(count), 10))
    except (TypeError, ValueError):
        count = 5

    try:
        recs = await recommend_repos(role, tech, level, goal, count)
    except Exception as e:
        return [TextContent(type="text", text=f"Recommendation failed: {e}")]

    return [TextContent(type="text", text=recs.model_dump_json(indent=2))]
