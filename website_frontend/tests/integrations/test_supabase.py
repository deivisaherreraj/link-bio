from collections.abc import Mapping
from typing import Any

import website_frontend.constants.featured_constants as featured_const
from website_frontend.integrations.supabase import SupabaseAPI
from website_frontend.model.featured import Featured


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


class FailingTableQuery(StubTableQuery):
    def execute(self) -> StubExecuteResult:
        raise RuntimeError("supabase unavailable")


class FailingSupabaseClient(StubSupabaseClient):
    def __init__(self) -> None:
        self.tables: list[str] = []
        self.query = FailingTableQuery([])


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


def test_featured_maps_blank_optional_fields_to_none():
    rows: list[Mapping[str, Any]] = [
        {
            "href": "https://example.com/project",
            "image_url": "https://example.com/project.png",
            "title": "Example Project",
            "description": "   ",
            "technologies": ["Python"],
            "github_url": " ",
            "live_url": None,
            "status": "production",
        }
    ]
    api = SupabaseAPI()
    api.supabase = StubSupabaseClient(rows)  # type: ignore[assignment]

    result = api.featured()

    assert len(result) == 1
    assert result[0].description is None
    assert result[0].github_url is None
    assert result[0].live_url is None


def test_featured_drops_invalid_optional_external_urls():
    rows: list[Mapping[str, Any]] = [
        {
            "href": "https://example.com/project",
            "image_url": "https://example.com/project.png",
            "title": "Example Project",
            "github_url": "github.com/example/project",
            "live_url": "javascript:alert('xss')",
            "status": "production",
        }
    ]
    api = SupabaseAPI()
    api.supabase = StubSupabaseClient(rows)  # type: ignore[assignment]

    result = api.featured()

    assert len(result) == 1
    assert result[0].github_url is None
    assert result[0].live_url is None


def test_featured_maps_known_status_with_full_contract():
    rows: list[Mapping[str, Any]] = [
        {
            "href": "https://example.com/project",
            "image_url": "https://example.com/project.png",
            "title": "Example Project",
            "description": "Example description",
            "technologies": ["Python"],
            "github_url": "https://github.com/example/project",
            "live_url": "https://example.com/live",
            "status": "production",
        }
    ]
    api = SupabaseAPI()
    api.supabase = StubSupabaseClient(rows)  # type: ignore[assignment]

    result = api.featured()

    assert len(result) == 1
    assert result[0].status.label == "En Producción"
    assert result[0].status.color == "#10B981"
    assert result[0].status.bg_color == "rgba(16, 185, 129, 0.15)"
    assert result[0].status.icon == "globe"
    assert result[0].status.animation_class == ""


def test_featured_skips_rows_missing_required_contract_fields():
    rows: list[Mapping[str, Any]] = [
        {
            "href": " ",
            "image_url": "https://example.com/project.png",
            "title": "Example Project",
            "status": "production",
        },
        {
            "href": "https://example.com/project",
            "image_url": "",
            "title": "Example Project",
            "status": "production",
        },
        {
            "href": "https://example.com/project",
            "image_url": "https://example.com/project.png",
            "title": "  ",
            "status": "production",
        },
        {
            "href": "example.com/project",
            "image_url": "https://example.com/project.png",
            "title": "Example Project",
            "status": "production",
        },
        {
            "href": "javascript:alert('xss')",
            "image_url": "https://example.com/project.png",
            "title": "Example Project",
            "status": "production",
        },
        {
            "href": "https://example.com/valid-project",
            "image_url": "https://example.com/valid-project.png",
            "title": "Valid Project",
            "status": "production",
        },
    ]
    api = SupabaseAPI()
    api.supabase = StubSupabaseClient(rows)  # type: ignore[assignment]

    result = api.featured()

    assert len(result) == 1
    assert result[0].href == "https://example.com/valid-project"
    assert result[0].image_url == "https://example.com/valid-project.png"
    assert result[0].title == "Valid Project"


def test_featured_technologies_default_list_is_not_shared():
    featured_a = Featured(
        href="https://example.com/a",
        image_url="https://example.com/a.png",
        title="A",
        status=featured_const.PROJECT_STATUS_CONFIG[
            featured_const.DEFAULT_PROJECT_STATUS_KEY
        ],
    )
    featured_b = Featured(
        href="https://example.com/b",
        image_url="https://example.com/b.png",
        title="B",
        status=featured_const.PROJECT_STATUS_CONFIG[
            featured_const.DEFAULT_PROJECT_STATUS_KEY
        ],
    )

    featured_a.technologies.append("Python")

    assert featured_a.technologies == ["Python"]
    assert featured_b.technologies == []


def test_featured_returns_empty_list_when_execute_raises_runtime_error():
    api = SupabaseAPI()
    api.supabase = FailingSupabaseClient()  # type: ignore[assignment]

    result = api.featured()

    assert result == []


def test_featured_logs_fail_closed_warning_when_execute_raises(caplog):
    api = SupabaseAPI()
    api.supabase = FailingSupabaseClient()  # type: ignore[assignment]

    with caplog.at_level("WARNING"):
        result = api.featured()

    assert result == []
    assert caplog.records[-1].message == "supabase_featured_fetch_failed_closed"
    assert caplog.records[-1].event == "supabase_featured_fetch_failed_closed"
    assert caplog.records[-1].error_type == "RuntimeError"
