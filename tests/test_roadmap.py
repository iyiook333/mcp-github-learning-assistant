"""Tests for roadmap generation logic."""

from mcp_github_learning_assistant import roadmap


def test_priority_prefers_documentation():
    assert roadmap._priority_for('documentation')[0] == 1
    assert roadmap._priority_for('docs')[0] == 1
    assert roadmap._priority_for('core')[0] == 3
    assert roadmap._priority_for('unknown-dir')[0] == 5


def test_skip_ignores_non_source_directories():
    assert roadmap._skip('.github')
    assert roadmap._skip('buildSrc')
    assert roadmap._skip('eclipse')
    assert not roadmap._skip('core')


class FakeResponse:
    status_code = 200

    def raise_for_status(self):
        return None

    def json(self):
        return CONTENTS


class FakeClient:
    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        return False

    async def get(self, path):
        return FakeResponse()


async def fake_github_client():
    return FakeClient()


CONTENTS = [
    {'name': '.github', 'type': 'dir', 'path': '.github'},
    {'name': 'buildSrc', 'type': 'dir', 'path': 'buildSrc'},
    {'name': 'documentation', 'type': 'dir', 'path': 'documentation'},
    {'name': 'core', 'type': 'dir', 'path': 'core'},
    {'name': 'README.md', 'type': 'file', 'path': 'README.md'},
]


async def test_build_roadmap_orders_and_skips(monkeypatch):
    monkeypatch.setattr(roadmap, 'github_client', fake_github_client)
    result = await roadmap.build_roadmap('example', 'project', depth=1)
    assert [module.name for module in result.modules] == ['documentation', 'core']
    assert result.modules[0].learning_order == 1
    assert result.summary.startswith('Generated learning sequence with 2 relevant modules')
