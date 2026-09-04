from collections.abc import Mapping
from typing import Any

import website_frontend.constants.featured_constants as featured_const
from website_frontend.integrations.supabase import SupabaseAPI
from website_frontend.model.featured import Featured
from website_frontend.model.profile import Profile
from website_frontend.model.social_link import SocialLink


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


def test_normalize_technologies_drops_non_string_list_items():
    api = SupabaseAPI()

    assert api._normalize_technologies(
        [" Python ", None, True, 42, {"name": "Reflex"}, "   ", "Reflex"]
    ) == ["Python", "Reflex"]


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


def test_featured_queries_latest_four_items():
    api = SupabaseAPI()
    api.supabase = StubSupabaseClient([])  # type: ignore[assignment]

    result = api.featured()

    assert result == []
    assert api.supabase.tables == ["featured"]
    assert api.supabase.query.calls == [
        ("select", "*"),
        ("order", ("init_date", True)),
        ("limit", 4),
        ("execute", None),
    ]


def test_normalize_featured_item_returns_featured_for_accepted_row():
    api = SupabaseAPI()

    result = api._normalize_featured_item(
        {
            "href": "/blog/example-project",
            "image_url": None,
            "title": "Example Project",
            "description": "Example description",
            "technologies": ["Python", "Reflex"],
            "github_url": "https://github.com/example/project",
            "live_url": None,
            "status": "production",
        }
    )

    assert result == Featured(
        href="/blog/example-project",
        image_url=None,
        title="Example Project",
        description="Example description",
        technologies=["Python", "Reflex"],
        github_url="https://github.com/example/project",
        live_url=None,
        status=featured_const.PROJECT_STATUS_CONFIG["production"],
    )


def test_normalize_featured_item_returns_none_for_rejected_row():
    api = SupabaseAPI()

    result = api._normalize_featured_item(
        {
            "href": "#",
            "image_url": "https://example.com/project.png",
            "title": "Rejected Project",
            "github_url": "/",
            "live_url": None,
            "status": "production",
        }
    )

    assert result is None


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


def test_featured_drops_non_string_technologies_from_list_payload():
    rows: list[Mapping[str, Any]] = [
        {
            "href": "https://example.com/project",
            "image_url": "https://example.com/project.png",
            "title": "Example Project",
            "technologies": [" Python ", False, None, 3.14, "", "Reflex"],
            "status": "production",
        }
    ]
    api = SupabaseAPI()
    api.supabase = StubSupabaseClient(rows)  # type: ignore[assignment]

    result = api.featured()

    assert len(result) == 1
    assert result[0].technologies == ["Python", "Reflex"]


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


def test_featured_accepts_internal_href_and_missing_image_when_another_action_exists():
    rows: list[Mapping[str, Any]] = [
        {
            "href": "/blog/example-project",
            "image_url": None,
            "title": "Example Project",
            "description": "Example description",
            "technologies": ["Python", "Reflex"],
            "github_url": "https://github.com/example/project",
            "live_url": None,
            "status": "production",
        }
    ]
    api = SupabaseAPI()
    api.supabase = StubSupabaseClient(rows)  # type: ignore[assignment]

    result = api.featured()

    assert len(result) == 1
    assert result[0].href == "/blog/example-project"
    assert result[0].image_url is None
    assert result[0].github_url == "https://github.com/example/project"


def test_featured_keeps_valid_row_when_href_is_missing_but_live_url_exists():
    rows: list[Mapping[str, Any]] = [
        {
            "href": None,
            "image_url": "https://example.com/project.png",
            "title": "Example Project",
            "description": "Example description",
            "technologies": ["Python", "Reflex"],
            "github_url": None,
            "live_url": "https://example.com/live",
            "status": "production",
        }
    ]
    api = SupabaseAPI()
    api.supabase = StubSupabaseClient(rows)  # type: ignore[assignment]

    result = api.featured()

    assert len(result) == 1
    assert result[0].href is None
    assert result[0].live_url == "https://example.com/live"


def test_featured_drops_non_actionable_placeholder_values_before_validation():
    rows: list[Mapping[str, Any]] = [
        {
            "href": "/",
            "image_url": None,
            "title": "Invalid Placeholder Project",
            "description": "Example description",
            "technologies": ["Python"],
            "github_url": "#",
            "live_url": "https://example.com/live",
            "status": "production",
        }
    ]
    api = SupabaseAPI()
    api.supabase = StubSupabaseClient(rows)  # type: ignore[assignment]

    result = api.featured()

    assert len(result) == 1
    assert result[0].href is None
    assert result[0].github_url is None
    assert result[0].live_url == "https://example.com/live"


def test_featured_skips_rows_without_any_actionable_targets():
    rows: list[Mapping[str, Any]] = [
        {
            "href": "#",
            "image_url": "https://example.com/project.png",
            "title": "No Actions Project",
            "description": "Example description",
            "technologies": ["Python"],
            "github_url": "/",
            "live_url": None,
            "status": "production",
        }
    ]
    api = SupabaseAPI()
    api.supabase = StubSupabaseClient(rows)  # type: ignore[assignment]

    result = api.featured()

    assert result == []


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


def test_featured_normalizes_typed_string_status_values():
    rows: list[Mapping[str, Any]] = [
        {
            "href": "https://example.com/project",
            "image_url": "https://example.com/project.png",
            "title": "Example Project",
            "status": "  PRODUCTION  ",
        }
    ]
    api = SupabaseAPI()
    api.supabase = StubSupabaseClient(rows)  # type: ignore[assignment]

    result = api.featured()

    assert len(result) == 1
    assert result[0].status == featured_const.PROJECT_STATUS_CONFIG["production"]


def test_featured_uses_default_status_for_missing_status_field():
    rows: list[Mapping[str, Any]] = [
        {
            "href": "https://example.com/project",
            "image_url": "https://example.com/project.png",
            "title": "Example Project",
        }
    ]
    api = SupabaseAPI()
    api.supabase = StubSupabaseClient(rows)  # type: ignore[assignment]

    result = api.featured()

    assert len(result) == 1
    assert (
        result[0].status
        == featured_const.PROJECT_STATUS_CONFIG[
            featured_const.DEFAULT_PROJECT_STATUS_KEY
        ]
    )


def test_featured_uses_default_status_for_non_string_status_values():
    rows: list[Mapping[str, Any]] = [
        {
            "href": "https://example.com/project-bool",
            "image_url": "https://example.com/project-bool.png",
            "title": "Boolean Status Project",
            "status": True,
        },
        {
            "href": "https://example.com/project-int",
            "image_url": "https://example.com/project-int.png",
            "title": "Integer Status Project",
            "status": 1,
        },
    ]
    api = SupabaseAPI()
    api.supabase = StubSupabaseClient(rows)  # type: ignore[assignment]

    result = api.featured()

    assert len(result) == 2
    default_status = featured_const.PROJECT_STATUS_CONFIG[
        featured_const.DEFAULT_PROJECT_STATUS_KEY
    ]
    assert [item.status for item in result] == [default_status, default_status]
    assert result[0].status != featured_const.PROJECT_STATUS_CONFIG["production"]


def test_featured_skips_rows_missing_required_contract_fields():
    rows: list[Mapping[str, Any]] = [
        {
            "href": " ",
            "image_url": "https://example.com/project.png",
            "title": "Example Project",
            "status": "production",
        },
        {
            "href": None,
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
            "href": None,
            "image_url": None,
            "title": "No Action Project",
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
    assert caplog.records[-1].integration == "supabase"
    assert caplog.records[-1].operation == "featured"
    assert caplog.records[-1].fail_closed is True
    assert caplog.records[-1].error_type == "RuntimeError"


def test_profile_returns_none_when_client_is_missing():
    api = SupabaseAPI()
    if hasattr(api, "supabase"):
        delattr(api, "supabase")

    result = api.profile()

    assert result is None


def test_profile_maps_backfilled_profile_contract_and_sorts_socials():
    rows: list[Mapping[str, Any]] = [
        {
            "full_name": "Deivis Herrera",
            "handle": "@dherrerajdev",
            "headline": "Full-Stack Developer",
            "bio_short": "Short bio",
            "bio_short_highlights": ["Short"],
            "avatar_url": "https://example.com/avatar.png",
            "email": "deivis@example.com",
            "availability_status_key": "empleo",
            "tech_stack_summary": "Python, Reflex",
            "primary_socials": [
                {
                    "label": "GitHub",
                    "url": "https://github.com/example",
                    "icon": "fa-brands fa-github",
                    "is_active": True,
                    "priority": 2,
                },
                {
                    "label": "LinkedIn",
                    "url": "https://linkedin.com/in/example",
                    "icon": "fa-brands fa-linkedin",
                    "is_active": True,
                    "priority": 1,
                },
            ],
        }
    ]
    api = SupabaseAPI()
    api.supabase = StubSupabaseClient(rows)  # type: ignore[assignment]

    result = api.profile()

    assert isinstance(result, Profile)
    assert result.full_name == "Deivis Herrera"
    assert result.bio_short_highlights == ["Short"]
    assert [segment.text for segment in result.bio_short_segments] == ["Short", " bio"]
    assert result.bio_short_segments[0].is_highlighted is True
    assert [social.label for social in result.primary_socials] == ["LinkedIn", "GitHub"]
    assert api.supabase.tables == ["profile"]
    assert api.supabase.query.calls == [
        ("select", "*"),
        ("limit", 1),
        ("execute", None),
    ]


def test_profile_returns_none_for_incomplete_required_contract():
    rows: list[Mapping[str, Any]] = [
        {
            "full_name": "Deivis Herrera",
            "handle": "@dherrerajdev",
            "headline": "Full-Stack Developer",
            "bio_short": "Short bio",
            "avatar_url": "https://example.com/avatar.png",
            "email": "invalid-email",
            "availability_status_key": "empleo",
            "tech_stack_summary": "Python, Reflex",
            "primary_socials": [],
        }
    ]
    api = SupabaseAPI()
    api.supabase = StubSupabaseClient(rows)  # type: ignore[assignment]

    result = api.profile()

    assert result is None


def test_profile_skips_invalid_primary_social_items_without_failing_row():
    rows: list[Mapping[str, Any]] = [
        {
            "full_name": "Deivis Herrera",
            "handle": "@dherrerajdev",
            "headline": "Full-Stack Developer",
            "bio_short": "Short bio",
            "avatar_url": "/avatar.jpeg",
            "email": "deivis@example.com",
            "availability_status_key": "empleo",
            "tech_stack_summary": "Python, Reflex",
            "primary_socials": [
                {
                    "label": "GitHub",
                    "url": "https://github.com/example",
                    "icon": "fa-brands fa-github",
                    "is_active": True,
                    "priority": 1,
                },
                {
                    "label": "Broken",
                    "url": "javascript:alert('xss')",
                    "icon": "fa-brands fa-x-twitter",
                    "is_active": True,
                    "priority": 2,
                },
            ],
        }
    ]
    api = SupabaseAPI()
    api.supabase = StubSupabaseClient(rows)  # type: ignore[assignment]

    result = api.profile()

    assert isinstance(result, Profile)
    assert len(result.primary_socials) == 1
    assert result.primary_socials[0].label == "GitHub"


def test_profile_logs_fail_closed_warning_when_execute_raises(caplog):
    api = SupabaseAPI()
    api.supabase = FailingSupabaseClient()  # type: ignore[assignment]

    with caplog.at_level("WARNING"):
        result = api.profile()

    assert result is None
    assert caplog.records[-1].message == "supabase_profile_fetch_failed_closed"
    assert caplog.records[-1].event == "supabase_profile_fetch_failed_closed"
    assert caplog.records[-1].integration == "supabase"
    assert caplog.records[-1].operation == "profile"
    assert caplog.records[-1].fail_closed is True
    assert caplog.records[-1].error_type == "RuntimeError"


def test_social_links_returns_empty_list_when_client_is_missing():
    api = SupabaseAPI()
    if hasattr(api, "supabase"):
        delattr(api, "supabase")

    result = api.social_links()

    assert result == []


def test_social_links_maps_rows_with_optional_contract_fields():
    rows: list[Mapping[str, Any]] = [
        {
            "label": "Discord",
            "url": "https://discord.gg/example",
            "icon": "fa-brands fa-discord",
            "section": "community",
            "priority": 2,
            "is_active": True,
            "is_external": True,
            "description": "Join the server",
            "badge": "Comunidad",
            "badge_color": "#5865F2",
            "border_color": "#5865F2",
        },
        {
            "label": "Blog",
            "url": "/blog",
            "icon": "fa-solid fa-newspaper",
            "section": "resources",
            "priority": 1,
            "is_active": True,
            "is_external": False,
        },
    ]
    api = SupabaseAPI()
    api.supabase = StubSupabaseClient(rows)  # type: ignore[assignment]

    result = api.social_links()

    assert result == [
        SocialLink(
            label="Blog",
            url="/blog",
            icon="fa-solid fa-newspaper",
            section="resources",
            priority=1,
            is_active=True,
            is_external=False,
        ),
        SocialLink(
            label="Discord",
            url="https://discord.gg/example",
            icon="fa-brands fa-discord",
            section="community",
            priority=2,
            is_active=True,
            is_external=True,
            description="Join the server",
            badge="Comunidad",
            badge_color="#5865F2",
            border_color="#5865F2",
        ),
    ]
    assert api.supabase.tables == ["social_links"]
    assert api.supabase.query.calls == [
        ("select", "*"),
        ("execute", None),
    ]


def test_social_links_preserves_safe_placeholder_urls_for_disabled_rendering():
    rows: list[Mapping[str, Any]] = [
        {
            "label": "Setup",
            "url": "/",
            "icon": "fa-solid fa-desktop",
            "section": "resources",
            "priority": 1,
            "is_active": True,
            "is_external": True,
        },
        {
            "label": "Public Inbox",
            "url": "#",
            "icon": "fa-solid fa-inbox",
            "section": "contact",
            "priority": 2,
            "is_active": True,
            "is_external": True,
        },
    ]
    api = SupabaseAPI()
    api.supabase = StubSupabaseClient(rows)  # type: ignore[assignment]

    result = api.social_links()

    assert [link.url for link in result] == ["/", "#"]


def test_social_links_sanitizes_unsafe_urls_to_disabled_placeholders():
    rows: list[Mapping[str, Any]] = [
        {
            "label": "Unsafe External",
            "url": "javascript:alert('xss')",
            "icon": "fa-solid fa-triangle-exclamation",
            "section": "work",
            "priority": 2,
            "is_active": True,
            "is_external": True,
        },
        {
            "label": "Unsafe Internal",
            "url": "data:text/html,boom",
            "icon": "fa-solid fa-bomb",
            "section": "contact",
            "priority": 1,
            "is_active": True,
            "is_external": False,
        },
    ]
    api = SupabaseAPI()
    api.supabase = StubSupabaseClient(rows)  # type: ignore[assignment]

    result = api.social_links()

    assert [link.url for link in result] == ["#", "#"]


def test_social_links_accepts_mailto_when_row_is_marked_internal():
    rows: list[Mapping[str, Any]] = [
        {
            "label": "Email",
            "url": "mailto:test@example.com",
            "icon": "fa-solid fa-envelope",
            "section": "contact",
            "priority": 1,
            "is_active": True,
            "is_external": False,
        }
    ]
    api = SupabaseAPI()
    api.supabase = StubSupabaseClient(rows)  # type: ignore[assignment]

    result = api.social_links()

    assert result == [
        SocialLink(
            label="Email",
            url="mailto:test@example.com",
            icon="fa-solid fa-envelope",
            section="contact",
            priority=1,
            is_active=True,
            is_external=False,
        )
    ]


def test_social_links_skips_rows_missing_required_contract_fields():
    rows: list[Mapping[str, Any]] = [
        {
            "label": " ",
            "url": "https://example.com/a",
            "icon": "fa-solid fa-star",
            "section": "work",
            "priority": 1,
            "is_active": True,
            "is_external": True,
        },
        {
            "label": "Missing Url",
            "url": " ",
            "icon": "fa-solid fa-star",
            "section": "work",
            "priority": 2,
            "is_active": True,
            "is_external": True,
        },
        {
            "label": "Missing Icon",
            "url": "https://example.com/c",
            "icon": " ",
            "section": "work",
            "priority": 3,
            "is_active": True,
            "is_external": True,
        },
        {
            "label": "Bad Section",
            "url": "https://example.com/d",
            "icon": "fa-solid fa-star",
            "section": "unknown",
            "priority": 4,
            "is_active": True,
            "is_external": True,
        },
        {
            "label": "Bad Active",
            "url": "https://example.com/e",
            "icon": "fa-solid fa-star",
            "section": "work",
            "priority": 5,
            "is_active": "yes",
            "is_external": True,
        },
        {
            "label": "Bad External",
            "url": "https://example.com/f",
            "icon": "fa-solid fa-star",
            "section": "work",
            "priority": 6,
            "is_active": True,
            "is_external": "no",
        },
        {
            "label": "Bad Priority",
            "url": "https://example.com/g",
            "icon": "fa-solid fa-star",
            "section": "work",
            "priority": True,
            "is_active": True,
            "is_external": True,
        },
        {
            "label": "Valid",
            "url": "https://example.com/h",
            "icon": "fa-solid fa-star",
            "section": "work",
            "priority": 7,
            "is_active": True,
            "is_external": True,
        },
    ]
    api = SupabaseAPI()
    api.supabase = StubSupabaseClient(rows)  # type: ignore[assignment]

    result = api.social_links()

    assert len(result) == 1
    assert result[0].label == "Valid"


def test_social_links_logs_fail_closed_warning_when_execute_raises(caplog):
    api = SupabaseAPI()
    api.supabase = FailingSupabaseClient()  # type: ignore[assignment]

    with caplog.at_level("WARNING"):
        result = api.social_links()

    assert result == []
    assert caplog.records[-1].message == "supabase_social_links_fetch_failed_closed"
    assert caplog.records[-1].event == "supabase_social_links_fetch_failed_closed"
    assert caplog.records[-1].integration == "supabase"
    assert caplog.records[-1].operation == "social_links"
    assert caplog.records[-1].fail_closed is True
    assert caplog.records[-1].error_type == "RuntimeError"
