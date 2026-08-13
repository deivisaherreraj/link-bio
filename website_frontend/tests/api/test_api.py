from fastapi.testclient import TestClient

from website_frontend.api import api
from website_frontend.model.featured import Featured
from website_frontend.model.live import Live
from website_frontend.model.project_status import ProjectStatus


def _featured_project() -> Featured:
    return Featured(
        href="https://example.com/project",
        image_url="https://example.com/project.png",
        title="Example Project",
        description="Example description",
        technologies=["Python", "Reflex"],
        github_url="https://github.com/example/project",
        live_url="https://example.com/live",
        status=ProjectStatus(
            key="production",
            label="En Produccion",
            color="#10B981",
            bg_color="rgba(16, 185, 129, 0.15)",
            icon="globe",
            animation_class="",
        ),
    )


def test_live_endpoint_delegates_user_and_preserves_offline_payload(monkeypatch):
    client = TestClient(api.fastapi_app)
    calls: list[str] = []
    expected = Live.offline()

    def fake_get_live_status(user: str) -> Live:
        calls.append(user)
        return expected

    monkeypatch.setattr(api, "get_live_status", fake_get_live_status)

    response = client.get("/live/dherrerajdev")

    assert response.status_code == 200
    assert response.json() == expected.model_dump()
    assert calls == ["dherrerajdev"]


def test_live_endpoint_rejects_invalid_twitch_username(monkeypatch):
    client = TestClient(api.fastapi_app)
    calls: list[str] = []

    def fake_get_live_status(user: str) -> Live:
        calls.append(user)
        return Live.offline()

    monkeypatch.setattr(api, "get_live_status", fake_get_live_status)

    response = client.get("/live/bad-user")

    assert response.status_code == 422
    assert calls == []


def test_featured_endpoint_returns_service_projects(monkeypatch):
    client = TestClient(api.fastapi_app)
    expected = [_featured_project()]

    monkeypatch.setattr(api, "get_featured_projects", lambda: expected)

    response = client.get("/featured")

    assert response.status_code == 200
    assert response.json() == [item.model_dump() for item in expected]


def test_schedule_endpoint_preserves_empty_schedule_fallback(monkeypatch):
    client = TestClient(api.fastapi_app)

    monkeypatch.setattr(api, "get_live_schedule", lambda: {})

    response = client.get("/schedule")

    assert response.status_code == 200
    assert response.json() == {}


def test_avatar_status_endpoint_returns_service_key(monkeypatch):
    client = TestClient(api.fastapi_app)

    monkeypatch.setattr(api, "get_avatar_status_key", lambda: "empleo")

    response = client.get("/config-avatar-status")

    assert response.status_code == 200
    assert response.json() == "empleo"
