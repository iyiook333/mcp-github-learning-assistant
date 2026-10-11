"""Recommendation logic: match user profile to suitable GitHub repos."""

import base64

from .github_client import github_client
from .models.outputs import RecommendationList, RepoRecommendation

# Seed repos per tech (curated starting set; can be expanded or replaced by search later)
_TECH_SEEDS = {
    "spring boot": [
        ("spring-projects/spring-boot", "Official Spring Boot repo"),
        ("alibaba/fastjson2", "Popular Java JSON library with clean code"),
        ("iluwatar/java-design-patterns", "Java design patterns, beginner-friendly docs"),
    ],
    "fastapi": [
        ("fastapi/fastapi", "Official FastAPI repo"),
        ("tiangolo/full-stack-fastapi-template", "Full-stack FastAPI template"),
    ],
    "vue": [
        ("vuejs/core", "Vue 3 core"),
        ("vuejs/pinia", "Official state management"),
        ("vitejs/vite", "Build tool for Vue ecosystem"),
    ],
    "electron": [
        ("electron/electron", "Electron framework"),
    ],
    "react": [
        ("facebook/react", "React core"),
    ],
    "harmonyos": [
        ("openharmony/docs", "OpenHarmony docs"),
    ],
}


def _guess_seed_key(target_tech: str) -> str | None:
    """Find a matching seed list key for the given target tech."""
    tech_lower = (target_tech or "").lower()
    for key in _TECH_SEEDS:
        if key in tech_lower:
            return key
    return None


def _score_for_level(stars: int, level: str) -> float:
    """Quick heuristic: beginner-friendly repos should have good docs and not be gigantic."""
    if level == "beginner":
        return min(10.0, 5.0 + min(stars, 50000) / 10000)
    return min(10.0, 4.0 + min(stars, 80000) / 10000)


async def recommend_repos(role, target_tech, level, goal, count):
    """Fetch repo data from GitHub and assemble recommendations."""
    tech = _guess_seed_key(target_tech)
    if not tech:
        return RecommendationList(
            recommendations=[],
            message=(
                f"No curated seeds for '{target_tech}'. Suggested: try Spring boot, "
                "FastAPI, Vue, React, Electron, HarmonyOS."
            ),
        )

    async with await github_client() as client:
        recommendations: list[RepoRecommendation] = []
        for full_name, note in _TECH_SEEDS[tech]:
            try:
                resp = await client.get(f"/repos/{full_name}")
                resp.raise_for_status()
                data = resp.json()
            except Exception:
                continue  # skip repos we can't fetch right now

            stars = data.get("stargazers_count", 0)
            difficulty = "beginner" if stars < 50000 else "intermediate"
            recs_score = _score_for_level(stars, level)

            # Fetch README length as doc-quality proxy
            doc = "fair"
            try:
                rm = await client.get(f"/repos/{full_name}/readme")
                rm.raise_for_status()
                content = rm.json().get("content", "")
                readme_len = len(base64.b64decode(content).decode("utf-8", errors="ignore"))
                if readme_len > 10000:
                    doc = "excellent"
                elif readme_len > 3000:
                    doc = "good"
                elif readme_len > 500:
                    doc = "fair"
                else:
                    doc = "poor"
            except Exception:
                doc = "fair"

            why = f"{note}. Main language: {data.get('language')}, doc quality: {doc}."
            if goal == "interview_prep":
                why += " Useful for building a resume project."
            elif goal == "open_source":
                why += " Look at 'good first issue' labels to start contributing."

            recommendations.append(
                RepoRecommendation(
                    repo=full_name,
                    stars=stars,
                    language=data.get("language") or "Unknown",
                    difficulty=difficulty if level == "intermediate" else level,
                    match_score=round(recs_score, 1),
                    why_recommended=why,
                    estimated_time="2-3 months" if difficulty == "intermediate" else "1-2 months",
                )
            )
            if len(recommendations) >= count:
                break

    return RecommendationList(
        recommendations=recommendations,
        message=f"Found {len(recommendations)} repos for '{target_tech}'.",
    )
