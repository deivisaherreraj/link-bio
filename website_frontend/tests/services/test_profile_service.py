import pytest

from website_frontend.model.avatar_status import AvatarStatus
from website_frontend.model.profile import Profile
from website_frontend.services import profile_service


class StubSupabaseAPI:
    def __init__(self, profile: Profile | None) -> None:
        self.profile_value = profile

    def profile(self) -> Profile | None:
        return self.profile_value


def test_build_avatar_status_normalizes_input():
    result = profile_service.build_avatar_status(' "CONSULTORIA" ')

    assert isinstance(result, AvatarStatus)
    assert result.key == "consultoria"
    assert result.class_name == "is-consulting"


def test_build_avatar_status_falls_back_for_unknown_key():
    result = profile_service.build_avatar_status("desconocido")

    assert result.key == "activo"
    assert result.class_name == "is-active"


def test_build_avatar_status_falls_back_for_blank_key():
    result = profile_service.build_avatar_status(' "  " ')

    assert result.key == "activo"
    assert result.class_name == "is-active"


@pytest.mark.parametrize(
    ("raw_key", "coerced_key"),
    [
        (None, "none"),
        (True, "true"),
        (123, "123"),
    ],
)
def test_build_avatar_status_rejects_non_string_keys_even_if_coercion_would_match(
    monkeypatch, raw_key, coerced_key
):
    monkeypatch.setitem(
        profile_service.profile_const.AVAILABILITY_STATES,
        coerced_key,
        {
            "text": "Coerced Match",
            "class_name": "is-coerced-match",
            "icon": "fa-mask",
        },
    )

    result = profile_service.build_avatar_status(raw_key)

    assert result.key == "activo"
    assert result.class_name == "is-active"


def test_get_default_avatar_status_uses_project_default():
    result = profile_service.get_default_avatar_status()

    assert result.key == "activo"
    assert result.class_name == "is-active"


def test_get_avatar_status_key_reads_from_profile(monkeypatch):
    monkeypatch.setattr(
        profile_service,
        "SUPABASE_API",
        StubSupabaseAPI(
            Profile(
                full_name="Deivis Herrera",
                handle="@dherrerajdev",
                headline="Headline",
                bio_short="Short bio",
                avatar_url="https://example.com/avatar.png",
                email="deivis@example.com",
                availability_status_key="empleo",
                tech_stack_summary="Python, Reflex",
                primary_socials=[],
            )
        ),
    )

    result = profile_service.get_avatar_status_key()

    assert result == "empleo"


def test_get_profile_technologies_returns_badges():
    result = profile_service.get_profile_technologies()

    assert result
    assert result[0].name == "Angular"
    assert result[0].icon_class == "fa-brands fa-angular"


def test_get_profile_technologies_returns_empty_list_when_config_is_empty(monkeypatch):
    monkeypatch.setattr(profile_service.profile_const, "TECHNOLOGIES", [])

    result = profile_service.get_profile_technologies()

    assert result == []


def test_get_profile_technologies_skips_invalid_entries(monkeypatch):
    monkeypatch.setattr(
        profile_service.profile_const,
        "TECHNOLOGIES",
        [
            {"name": "Angular", "color": "#DD0031", "icon_class": "fa-angular"},
            {"name": "", "color": "#000000", "icon_class": "fa-empty"},
            {"name": "Node.js", "color": " ", "icon_class": "fa-node-js"},
            {"name": "Python", "color": "#3776AB", "icon_class": None},
            "not-a-dict",
        ],
    )

    result = profile_service.get_profile_technologies()

    assert len(result) == 1
    assert result[0].name == "Angular"
    assert result[0].color == "#DD0031"
    assert result[0].icon_class == "fa-angular"


def test_build_avatar_status_falls_back_for_incomplete_catalog_entry(monkeypatch):
    monkeypatch.setitem(
        profile_service.profile_const.AVAILABILITY_STATES,
        "consultoria",
        {
            "text": "",
            "class_name": "is-consulting",
            "icon": "fa-laptop-code",
        },
    )

    result = profile_service.build_avatar_status("consultoria")

    assert result.key == "activo"
    assert result.class_name == "is-active"


def test_get_profile_returns_supabase_profile(monkeypatch):
    expected = Profile(
        full_name="Deivis Herrera",
        handle="@dherrerajdev",
        headline="Headline",
        bio_short="Short bio",
        avatar_url="https://example.com/avatar.png",
        email="deivis@example.com",
        availability_status_key="empleo",
        tech_stack_summary="Python, Reflex",
        primary_socials=[],
    )
    monkeypatch.setattr(
        profile_service,
        "SUPABASE_API",
        StubSupabaseAPI(expected),
    )

    result = profile_service.get_profile()

    assert result == expected


def test_get_profile_falls_back_to_default_profile(monkeypatch):
    monkeypatch.setattr(
        profile_service,
        "SUPABASE_API",
        StubSupabaseAPI(None),
    )

    result = profile_service.get_profile()

    assert result == profile_service.get_default_profile()


def test_get_default_profile_restores_published_fallback_copy() -> None:
    profile = profile_service.get_default_profile()

    assert profile.bio_short == (
        "¡Hola! 👋 Soy Deivis Herrera, desarrollador Full-Stack enfocado en "
        "construir software confiable, escalable y de alto impacto. Trabajo "
        "tanto del lado del Back-End 💻 como del Front-End 🌐, y siempre estoy "
        "explorando nuevas ideas para convertirlas en productos reales. Acá vas "
        "a encontrar mis proyectos, contenido, formas de contacto y perfiles "
        "profesionales 🔗🚀 ¡Gracias por tu visita y bienvenido a mi mundo digital!"
    )
    assert profile.bio_short_highlights == [
        "Deivis Herrera",
        "desarrollador Full-Stack",
        "software confiable, escalable y de alto impacto",
        "Back-End 💻",
        "Front-End 🌐",
    ]
    assert [segment.text for segment in profile.bio_short_segments if segment.is_highlighted] == [
        "Deivis Herrera",
        "desarrollador Full-Stack",
        "software confiable, escalable y de alto impacto",
        "Back-End 💻",
        "Front-End 🌐",
    ]
    assert (
        profile.tech_stack_summary
        == "Especializado en desarrollo web moderno y arquitecturas escalables"
    )


def test_get_primary_social_url_returns_active_social_match():
    profile = profile_service.get_default_profile()

    result = profile_service.get_primary_social_url(profile, " github ")

    assert result == "https://github.com/deivisaherreraj"


def test_get_primary_social_url_skips_inactive_social():
    profile = profile_service.get_default_profile()
    profile.primary_socials[0].is_active = False

    result = profile_service.get_primary_social_url(profile, "GitHub")

    assert result is None
