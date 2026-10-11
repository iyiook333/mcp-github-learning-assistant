"""Pydantic models for tool outputs."""

from pydantic import BaseModel


class RepoAnalysis(BaseModel):
    """Learning value analysis result."""

    repo_name: str
    stars: int
    language: str
    difficulty: str          # beginner / intermediate / advanced
    learning_score: float    # 0-10
    prerequisites: list[str]
    pros: list[str]
    cons: list[str]
    suggested_path: list[str]
    doc_quality: str         # poor / fair / good / excellent
    active: bool
    summary: str


class RepoRecommendation(BaseModel):
    """A single recommended repo."""

    repo: str
    stars: int
    language: str
    difficulty: str
    match_score: float
    why_recommended: str
    estimated_time: str


class RecommendationList(BaseModel):
    """List of recommendations from recommend_learning_repos tool."""

    recommendations: list[RepoRecommendation]
    message: str