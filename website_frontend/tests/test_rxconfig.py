import importlib

import pytest

import rxconfig


def _load_api_url(monkeypatch: pytest.MonkeyPatch, value: str | None) -> str:
    if value is None:
        monkeypatch.delenv("API_URL", raising=False)
    else:
        monkeypatch.setenv("API_URL", value)

    module = importlib.reload(rxconfig)
    return module.config.api_url


def test_api_url_defaults_when_env_is_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    assert _load_api_url(monkeypatch, None) == rxconfig.DEFAULT_API_URL


def test_api_url_defaults_when_env_is_blank(monkeypatch: pytest.MonkeyPatch) -> None:
    assert _load_api_url(monkeypatch, "   ") == rxconfig.DEFAULT_API_URL


@pytest.mark.parametrize(
    "value",
    [
        "not-a-url",
        "javascript:alert('xss')",
        "https:///missing-host",
    ],
)
def test_api_url_defaults_when_env_is_malformed(
    monkeypatch: pytest.MonkeyPatch, value: str
) -> None:
    assert _load_api_url(monkeypatch, value) == rxconfig.DEFAULT_API_URL


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("https://api.example.com", "https://api.example.com"),
        (" http://localhost:9000/api ", "http://localhost:9000/api"),
    ],
)
def test_api_url_keeps_valid_http_urls(
    monkeypatch: pytest.MonkeyPatch, value: str, expected: str
) -> None:
    assert _load_api_url(monkeypatch, value) == expected
