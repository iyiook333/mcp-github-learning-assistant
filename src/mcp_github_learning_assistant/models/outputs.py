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
