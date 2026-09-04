import asyncio
import inspect
from collections.abc import Callable
from typing import Any, cast

from website_frontend.model.avatar_status import AvatarStatus
from website_frontend.model.featured import Featured
from website_frontend.model.live import Live
from website_frontend.model.primary_social import PrimarySocial
from website_frontend.model.profile import Profile
from website_frontend.model.project_status import ProjectStatus
from website_frontend.model.social_link import SocialLink
from website_frontend.model.tech_badge import TechBadge
from website_frontend.state import page_state
from website_frontend.state.page_state import PageState


def _event_fn(event: object) -> Callable[..., Any]:
    return cast(Callable[..., Any], getattr(event, "fn"))


def _state() -> PageState:
    state = object.__new__(PageState)
    object.__setattr__(state, "dirty_vars", set())
    object.__setattr__(state, "dirty_substates", set())
    object.__setattr__(state, "router_data", {})
    object.__setattr__(state, "substates", {})
    object.__setattr__(state, "parent_state", None)
    object.__setattr__(state, "live_status", Live.offline())
    object.__setattr__(state, "featured_info", [])
    object.__setattr__(state, "work_social_links", [])
    object.__setattr__(state, "community_social_links", [])
    object.__setattr__(state, "resources_social_links", [])
    object.__setattr__(state, "contact_social_links", [])
    object.__setattr__(state, "timezone", "")
    object.__setattr__(state, "next_live", "")
    object.__setattr__(state, "profile_info", page_state.get_default_profile())
    object.__setattr__(
        state,
        "avatar_status",
        AvatarStatus(
            key="activo",
            text="Disponible",
            class_name="is-active",
            icon="fa-bolt",
        ),
    )
    object.__setattr__(state, "github_url", "https://github.com/deivisaherreraj")
    object.__setattr__(state, "linkedin_url", "https://linkedin.com/in/deivisaherreraj")
    object.__setattr__(state, "technologies", [])
    return state


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


def test_check_live_sets_live_status_from_site_user(monkeypatch):
    state = _state()
    calls: list[str] = []
    expected = Live.online(
        title="Live coding",
        category="Software and Game Development",
        tags=["python", "reflex"],
        viewer=42,
    )

    def fake_get_live_status(user: str) -> Live:
        calls.append(user)
        return expected

    monkeypatch.setattr(page_state, "get_live_status", fake_get_live_status)

    asyncio.run(_event_fn(PageState.check_live)(state))

    assert state.live_status == expected
    assert calls == [page_state.site_const.USER]


def test_featured_links_sets_featured_projects(monkeypatch):
    state = _state()
    expected = [_featured_project()]

    monkeypatch.setattr(page_state, "get_featured_projects", lambda: expected)

    asyncio.run(_event_fn(PageState.featured_links)(state))

    assert state.featured_info == expected


def test_has_multiple_featured_projects_is_false_for_zero_or_one_item() -> None:
    state = _state()

    assert state.has_multiple_featured_projects is False

    state.featured_info = [_featured_project()]

    assert state.has_multiple_featured_projects is False


def test_has_multiple_featured_projects_is_true_for_multiple_items() -> None:
    state = _state()
    state.featured_info = [_featured_project(), _featured_project()]

    assert state.has_multiple_featured_projects is True


def test_load_social_links_sets_section_lists(monkeypatch):
    state = _state()
    expected = {
        "work": [
            SocialLink(
                label="Workana",
                url="https://example.com/workana",
                icon="fa-solid fa-briefcase",
                section="work",
                priority=1,
                is_active=True,
                is_external=True,
            )
        ],
        "community": [
            SocialLink(
                label="Discord",
                url="https://discord.gg/example",
                icon="fa-brands fa-discord",
                section="community",
                priority=2,
                is_active=True,
                is_external=True,
            )
        ],
        "resources": [],
        "contact": [
            SocialLink(
                label="Email",
                url="mailto:test@example.com",
                icon="fa-solid fa-envelope",
                section="contact",
                priority=3,
                is_active=True,
                is_external=False,
            )
        ],
    }

    monkeypatch.setattr(page_state, "get_social_links_by_section", lambda: expected)

    asyncio.run(_event_fn(PageState.load_social_links)(state))

    assert state.work_social_links == expected["work"]
    assert state.community_social_links == expected["community"]
    assert state.resources_social_links == expected["resources"]
    assert state.contact_social_links == expected["contact"]


def test_page_state_defaults_do_not_load_social_links_at_import_time(monkeypatch):
    rendered = inspect.getsource(page_state)

    assert "DEFAULT_SOCIAL_LINKS = get_social_links_by_section()" not in rendered
    assert "work_social_links: list[SocialLink] = []" in rendered
    assert "community_social_links: list[SocialLink] = []" in rendered
    assert "resources_social_links: list[SocialLink] = []" in rendered
    assert "contact_social_links: list[SocialLink] = []" in rendered


def test_load_profile_sets_profile_and_primary_social_urls(monkeypatch):
    state = _state()
    expected_profile = Profile(
        full_name="Deivis Herrera",
        handle="@dherrerajdev",
        headline="Headline",
        bio_short="Short bio",
        avatar_url="https://example.com/avatar.png",
        email="deivis@example.com",
        availability_status_key="consultoria",
        tech_stack_summary="Python, Reflex",
        primary_socials=[
            PrimarySocial(
                label="GitHub",
                url="https://github.com/example",
                icon="fa-brands fa-github",
                is_active=True,
                priority=2,
            ),
            PrimarySocial(
                label="LinkedIn",
                url="https://linkedin.com/in/example",
                icon="fa-brands fa-linkedin",
                is_active=True,
                priority=1,
            ),
        ],
    )
    expected_status = AvatarStatus(
        key="consultoria",
        text="Disponible para consultoría",
        class_name="is-consulting",
        icon="fa-laptop-code",
    )

    monkeypatch.setattr(page_state, "get_profile", lambda: expected_profile)
    monkeypatch.setattr(
        page_state,
        "build_avatar_status",
        lambda key: expected_status if key == "consultoria" else None,
    )

    asyncio.run(_event_fn(PageState.load_profile)(state))

    assert state.profile_info == expected_profile
    assert state.avatar_status == expected_status
    assert state.github_url == "https://github.com/example"
    assert state.linkedin_url == "https://linkedin.com/in/example"


def test_check_schedule_requests_browser_timezone_when_missing(monkeypatch):
    state = _state()
    calls: list[tuple[object, object]] = []
    expected = object()

    def fake_call_script(script: object, callback: object) -> object:
        calls.append((script, callback))
        return expected

    monkeypatch.setattr(page_state.rx, "call_script", fake_call_script)

    result = asyncio.run(_event_fn(PageState.check_schedule)(state))

    assert result is expected
    assert calls == [(page_state.LOCAL_TIMEZONE_SCRIPT, PageState.update_timezone)]


def test_check_schedule_updates_existing_timezone(monkeypatch):
    state = _state()
    state.timezone = "America/Bogota"
    calls: list[str] = []

    def fake_get_next_live_date(timezone: str) -> str:
        calls.append(timezone)
        return "Martes, 01 de Enero a las 15:30 | Zona horaria: Bogota"

    monkeypatch.setattr(page_state, "get_next_live_date", fake_get_next_live_date)

    result = asyncio.run(_event_fn(PageState.check_schedule)(state))

    assert result is None
    assert calls == ["America/Bogota"]
    assert state.next_live == "Martes, 01 de Enero a las 15:30 | Zona horaria: Bogota"


def test_update_timezone_sets_timezone_and_next_live(monkeypatch):
    state = _state()
    calls: list[str] = []

    def fake_get_next_live_date(timezone: str) -> str:
        calls.append(timezone)
        return "Martes, 01 de Enero a las 15:30 | Zona horaria: Bogota"

    monkeypatch.setattr(page_state, "get_next_live_date", fake_get_next_live_date)

    asyncio.run(_event_fn(PageState.update_timezone)(state, "America/Bogota"))

    assert state.timezone == "America/Bogota"
    assert state.next_live == "Martes, 01 de Enero a las 15:30 | Zona horaria: Bogota"
    assert calls == ["America/Bogota"]


def test_update_timezone_rejects_blank_timezone_before_assignment(monkeypatch):
    state = _state()

    monkeypatch.setattr(
        page_state,
        "get_next_live_date",
        lambda timezone: (_ for _ in ()).throw(AssertionError(timezone)),
    )

    asyncio.run(_event_fn(PageState.update_timezone)(state, "   "))

    assert state.timezone == ""
    assert state.next_live == ""


def test_update_timezone_rejects_invalid_timezone_before_assignment(monkeypatch):
    state = _state()
    state.timezone = "America/Bogota"
    state.next_live = "existing schedule"

    monkeypatch.setattr(
        page_state,
        "get_next_live_date",
        lambda timezone: (_ for _ in ()).throw(AssertionError(timezone)),
    )

    asyncio.run(_event_fn(PageState.update_timezone)(state, "Mars/Olympus_Mons"))

    assert state.timezone == "America/Bogota"
    assert state.next_live == "existing schedule"


def test_init_technologies_loads_profile_technologies(monkeypatch):
    state = _state()
    expected = [
        TechBadge(name="Python", color="#3776AB", icon_class="fa-brands fa-python")
    ]

    monkeypatch.setattr(page_state, "get_profile_technologies", lambda: expected)

    _event_fn(PageState.init_technologies)(state)

    assert state.technologies == expected
