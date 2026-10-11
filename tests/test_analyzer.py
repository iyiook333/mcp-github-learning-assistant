"""Tests for repo analysis logic."""

import base64

from mcp_github_learning_assistant import analyzer


def _response(payload):
    class FakeResponse:
        status_code = 200

        def raise_for_status(self):
            return None

        def json(self):
            return payload

    return FakeResponse()


class FakeClient:
    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        return False

    async def get(self, path, params=None):
        if path.endswith('/readme'):
            return _response(README_DATA)
        if path.endswith('/languages'):
            return _response({'Python': 100})
        if path.endswith('/commits'):
            return _response([{'sha': 'abc'}])
        return _response(REPO_DATA)


async def fake_github_client():
    return FakeClient()


REPO_DATA = {
    'full_name': 'example/project',
    'language': 'Python',
    'stargazers_count': 60000,
}
README_DATA = {
    'content': base64.b64encode(b'# Example Project\n' * 300).decode('ascii')
}


async def test_analyze_repo_scores_and_quality(monkeypatch):
    monkeypatch.setattr(analyzer, 'github_client', fake_github_client)
    result = await analyzer.analyze_repo('example', 'project')
    assert result.repo_name == 'example/project'
    assert result.stars == 60000
    assert result.language == 'Python'
    assert result.difficulty == 'intermediate'
    assert result.doc_quality == 'good'
    assert result.learning_score == 10.0
    assert 'Well documented' in result.pros


def test_score_doc_length_boundaries():
    assert analyzer._score_doc_length(10001) == 'excellent'
    assert analyzer._score_doc_length(10000) == 'good'
    assert analyzer._score_doc_length(3000) == 'fair'
    assert analyzer._score_doc_length(0) == 'poor'


def test_judge_difficulty():
    assert analyzer._judge_difficulty(50001) == 'intermediate'
    assert analyzer._judge_difficulty(50000) == 'beginner'
