from collections.abc import Mapping
from typing import Any

import website_frontend.constants.featured_constants as featured_const
from website_frontend.integrations.supabase import SupabaseAPI


class StubExecuteResult:
    def __init__(self, data: list[Mapping[str, Any]]) -> None:
        self.data = data


class StubTableQuery:
    def __init__(self, data: list[Mapping[str, Any]]) -> None:
        self.data = data
        self.calls: list[tuple[str, object]] = []

    def select(self, value: str) -> "StubTableQuery":
        self.calls.append(("select", value))
        return self

    def order(self, column: str, desc: bool = False) -> "StubTableQuery":
        self.calls.append(("order", (column, desc)))
        return self

    def limit(self, value: int) -> "StubTableQuery":
        self.calls.append(("limit", value))
        return self

    def execute(self) -> StubExecuteResult:
        self.calls.append(("execute", None))
        return StubExecuteResult(self.data)


class StubSupabaseClient:
    def __init__(self, data: list[Mapping[str, Any]]) -> None:
        self.tables: list[str] = []
        self.query = StubTableQuery(data)

    def table(self, name: str) -> StubTableQuery:
        self.tables.append(name)
        return self.query


def test_normalize_technologies_handles_supported_shapes():
    api = SupabaseAPI()

    assert api._normalize_technologies(None) == []
    assert api._normalize_technologies(["Python", "  Reflex  ", ""]) == [
        "Python",
        "Reflex",
    ]
    assert api._normalize_technologies("Python, Reflex,  ") == [
        "Python",
        "Reflex",
    ]
    assert api._normalize_technologies(123) == []


def test_featured_returns_empty_list_when_client_is_missing():
    api = SupabaseAPI()
    if hasattr(api, "supabase"):
        delattr(api, "supabase")

    result = api.featured()

    assert result == []


def test_featured_maps_rows_and_uses_default_status_for_unknown_values():
    rows: list[Mapping[str, Any]] = [
        {
            "href": "https://example.com/project",
            "image_url": "https://example.com/project.png",
            "title": "Example Project",
            "description": "Example description",
            "technologies": "Python, Reflex",
            "github_url": "https://github.com/example/project",
            "live_url": "https://example.com/live",
            "status": "unknown-status",
        }
    ]
    api = SupabaseAPI()
    api.supabase = StubSupabaseClient(rows)  # type: ignore[assignment]

    result = api.featured()

    assert len(result) == 1
    assert result[0].title == "Example Project"
    assert result[0].technologies == ["Python", "Reflex"]
    assert (
        result[0].status
        == featured_const.PROJECT_STATUS_CONFIG[
            featured_const.DEFAULT_PROJECT_STATUS_KEY
        ]
    )
    assert api.supabase.tables == ["featured"]
    assert api.supabase.query.calls == [
        ("select", "*"),
        ("order", ("init_date", True)),
        ("limit", 4),
        ("execute", None),
    ]
