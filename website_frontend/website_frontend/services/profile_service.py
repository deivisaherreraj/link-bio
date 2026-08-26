import website_frontend.constants.profile_constants as profile_const
import website_frontend.constants.site_constants as site_const
from website_frontend.integrations.configcat import ConfigCatAPI
from website_frontend.integrations.supabase import SupabaseAPI
from website_frontend.model.avatar_status import AvatarStatus
from website_frontend.model.primary_social import PrimarySocial
from website_frontend.model.profile import Profile
from website_frontend.model.tech_badge import TechBadge

CONFIGCAT_API = ConfigCatAPI()
SUPABASE_API = SupabaseAPI()


def _default_profile() -> Profile:
    return Profile(
        full_name="Herrera, Deivis",
        handle="@dherrerajdev",
        headline="Full-Stack Developer & Tech Enthusiast",
        bio_short=(
            "Desarrollador Full-Stack con experiencia creando soluciones de alto "
            "impacto y software confiable, tanto del lado del Back-End como del "
            "Front-End. Acá vas a encontrar mis trabajos, contacto y perfiles "
            "profesionales."
        ),
        avatar_url="/avatar.jpeg",
        email=site_const.EMAIL,
        availability_status_key=site_const.AVAILABILITY_STATUS_DEFAULT,
        tech_stack_summary=(
            "Especializado en desarrollo web moderno y arquitecturas escalables"
        ),
        primary_socials=[
            PrimarySocial(
                label="GitHub",
                url=site_const.GITHUB_URL,
                icon="fa-brands fa-github",
                is_active=True,
                priority=1,
            ),
            PrimarySocial(
                label="LinkedIn",
                url=site_const.LINKEDIN_URL,
                icon="fa-brands fa-linkedin",
                is_active=True,
                priority=2,
            ),
        ],
    )


def _resolve_avatar_state(key: str) -> tuple[str, dict[str, str]]:
    default_key = site_const.AVAILABILITY_STATUS_DEFAULT
    default_state = profile_const.AVAILABILITY_STATES[default_key]

    candidate = profile_const.AVAILABILITY_STATES.get(key)
    if not isinstance(candidate, dict):
        return default_key, default_state

    text = candidate.get("text")
    class_name = candidate.get("class_name")
    icon = candidate.get("icon")

    if not isinstance(text, str) or not text.strip():
        return default_key, default_state

    if not isinstance(class_name, str) or not class_name.strip():
        return default_key, default_state

    if not isinstance(icon, str) or not icon.strip():
        return default_key, default_state

    return key, {
        "text": text.strip(),
        "class_name": class_name.strip(),
        "icon": icon.strip(),
    }


def get_default_avatar_status() -> AvatarStatus:
    return build_avatar_status(site_const.AVAILABILITY_STATUS_DEFAULT)


def get_avatar_status_key() -> str:
    return CONFIGCAT_API.avatar_status()


def build_avatar_status(raw_key: object) -> AvatarStatus:
    if not isinstance(raw_key, str):
        return get_default_avatar_status()

    normalized_key = raw_key.strip().strip('"').strip("'").lower()

    if not normalized_key:
        return get_default_avatar_status()

    resolved_key, state = _resolve_avatar_state(normalized_key)
    return AvatarStatus(
        key=resolved_key,
        text=state["text"],
        class_name=state["class_name"],
        icon=state["icon"],
    )


def get_profile_technologies() -> list[TechBadge]:
    badges: list[TechBadge] = []

    for item in profile_const.TECHNOLOGIES:
        if not isinstance(item, dict):
            continue

        name = item.get("name")
        color = item.get("color")
        icon_class = item.get("icon_class")

        if not isinstance(name, str) or not name.strip():
            continue

        if not isinstance(color, str) or not color.strip():
            continue

        if not isinstance(icon_class, str) or not icon_class.strip():
            continue

        badges.append(
            TechBadge(
                name=name.strip(),
                color=color.strip(),
                icon_class=icon_class.strip(),
            )
        )

    return badges


def get_default_profile() -> Profile:
    return _default_profile()


def get_profile() -> Profile:
    profile = SUPABASE_API.profile()
    if profile is None:
        return get_default_profile()

    return profile


def get_primary_social_url(profile: Profile, label: str) -> str | None:
    normalized_label = label.strip().lower()
    if not normalized_label:
        return None

    for social in profile.primary_socials:
        if not social.is_active:
            continue

        if social.label.strip().lower() != normalized_label:
            continue

        return social.url

    return None
