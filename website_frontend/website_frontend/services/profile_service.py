import website_frontend.constants.profile_constants as profile_const
import website_frontend.constants.site_constants as site_const
from website_frontend.integrations.supabase import SupabaseAPI
from website_frontend.model.avatar_status import AvatarStatus
from website_frontend.model.primary_social import PrimarySocial
from website_frontend.model.profile import Profile
from website_frontend.model.tech_badge import TechBadge

SUPABASE_API = SupabaseAPI()


def _default_profile() -> Profile:
    return Profile(
        full_name="Deivis Herrera",
        handle="@dherrerajdev",
        headline="Software Developer",
        bio_short="Profile details are temporarily unavailable.",
        bio_short_highlights=[],
        avatar_url="/avatar.jpeg",
        email=site_const.EMAIL,
        availability_status_key=site_const.AVAILABILITY_STATUS_DEFAULT,
        tech_stack_summary="Tech stack details are temporarily unavailable.",
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


def get_avatar_status_key() -> str:
    return get_profile().availability_status_key


def build_avatar_status(raw_key: object) -> AvatarStatus:
    return profile_const.resolve_availability_status(
        raw_key,
        default_key=site_const.AVAILABILITY_STATUS_DEFAULT,
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
    fallback_profile = get_default_profile()
    profile = SUPABASE_API.profile(fallback=fallback_profile)
    if profile is None:
        return fallback_profile

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
