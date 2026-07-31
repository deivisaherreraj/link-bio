from website_frontend.model.live import Live
from website_frontend.services import live_service


class StubTwitchAPI:
    def __init__(self, live_status: Live) -> None:
        self.live_status = live_status
        self.users: list[str] = []

    def live(self, user: str) -> Live:
        self.users.append(user)
        return self.live_status


def test_get_live_status_uses_requested_user(monkeypatch):
    live_status = Live(
        live=True,
        title="Live coding",
        category="Software and Game Development",
        tags=["python", "reflex"],
        viewer=42,
    )
    twitch_api = StubTwitchAPI(live_status)
    monkeypatch.setattr(live_service, "TWITCH_API", twitch_api)

    result = live_service.get_live_status("dherrerajdev")

    assert result == live_status
    assert twitch_api.users == ["dherrerajdev"]


def test_get_live_status_returns_offline_payload(monkeypatch):
    live_status = Live(
        live=False,
        title="",
        category="",
        tags=[],
        viewer=0,
    )
    twitch_api = StubTwitchAPI(live_status)
    monkeypatch.setattr(live_service, "TWITCH_API", twitch_api)

    result = live_service.get_live_status("dherrerajdev")

    assert result.live is False
    assert result.viewer == 0
    assert twitch_api.users == ["dherrerajdev"]
