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


class RoadmapModule(BaseModel):
    """One module in a learning roadmap."""

    name: str
    hint: str
    learning_order: int
    path: str


class RepoRoadmap(BaseModel):
    """Learning roadmap derived from repo structure."""

    repo: str
    modules: list[RoadmapModule]
    summary: str


class SimilarRepo(BaseModel):
    """One similar repo result."""

    repo: str
    stars: int
    language: str
    description: str
    url: str


class SimilarRepoList(BaseModel):
    """List of similar repos."""

    source_repo: str
    similar: list[SimilarRepo]


class FirstIssue(BaseModel):
    """One good-first-issue entry."""

    number: int
    title: str
    url: str
    labels: list[str]
    preview: str


class FirstIssueList(BaseModel):
    """List of good first issues."""

    repo: str
    issues: list[FirstIssue]


class ComparisonRow(BaseModel):
    """One row in a repo comparison."""

    repo: str
    stars: int
    language: str
    description: str
    updated_at: str | None = None
    doc_quality: str = "fair"
    score: float = 0.0


class ComparisonResult(BaseModel):
    """Comparison of multiple repos."""

    comparison: list[ComparisonRow]
    best_for_learning: str | None
    user_level_note: str
