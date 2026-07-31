from website_frontend.integrations import twitch


class StubResponse:
    def __init__(self, status_code: int, payload: dict) -> None:
        self.status_code = status_code
        self.payload = payload

    def json(self) -> dict:
        return self.payload


def test_generate_token_saves_token_and_expiration(monkeypatch):
    api = twitch.TwitchAPI()

    monkeypatch.setattr(twitch.time, "time", lambda: 100)
    monkeypatch.setattr(
        twitch.requests,
        "post",
        lambda url, data: StubResponse(
            200,
            {"access_token": "token-123", "expires_in": 3600},
        ),
    )

    api.generate_token()

    assert api.token == "token-123"
    assert api.token_exp == 3700


def test_generate_token_clears_state_on_failure(monkeypatch):
    api = twitch.TwitchAPI()
    api.token = "old-token"
    api.token_exp = 999

    monkeypatch.setattr(
        twitch.requests,
        "post",
        lambda url, data: StubResponse(500, {}),
    )

    api.generate_token()

    assert api.token is None
    assert api.token_exp == 0


def test_token_valid_depends_on_current_time(monkeypatch):
    api = twitch.TwitchAPI()
    api.token_exp = 150

    monkeypatch.setattr(twitch.time, "time", lambda: 100)
    assert api.token_valid() is True

    monkeypatch.setattr(twitch.time, "time", lambda: 200)
    assert api.token_valid() is False


def test_live_generates_token_and_maps_online_payload(monkeypatch):
    api = twitch.TwitchAPI()
    generated = []

    def fake_generate_token():
        generated.append(True)
        api.token = "fresh-token"
        api.token_exp = 999

    monkeypatch.setattr(api, "token_valid", lambda: False)
    monkeypatch.setattr(api, "generate_token", fake_generate_token)
    monkeypatch.setattr(
        twitch.requests,
        "get",
        lambda url, headers: StubResponse(
            200,
            {
                "data": [
                    {
                        "title": "Live coding",
                        "game_name": "Software and Game Development",
                        "tags": ["python", "reflex"],
                        "viewer_count": 42,
                    }
                ]
            },
        ),
    )

    result = api.live("dherrerajdev")

    assert generated == [True]
    assert result.live is True
    assert result.title == "Live coding"
    assert result.category == "Software and Game Development"
    assert result.tags == ["python", "reflex"]
    assert result.viewer == 42


def test_live_returns_offline_payload_when_stream_is_missing(monkeypatch):
    api = twitch.TwitchAPI()
    api.token = "existing-token"
    api.token_exp = 999

    monkeypatch.setattr(api, "token_valid", lambda: True)
    monkeypatch.setattr(
        twitch.requests,
        "get",
        lambda url, headers: StubResponse(200, {"data": []}),
    )

    result = api.live("dherrerajdev")

    assert result.live is False
    assert result.title == ""
    assert result.category == ""
    assert result.tags == []
    assert result.viewer == 0
