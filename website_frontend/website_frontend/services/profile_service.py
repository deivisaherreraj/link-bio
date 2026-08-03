import website_frontend.constants.profile_constants as profile_const
import website_frontend.constants.site_constants as site_const
from website_frontend.integrations.configcat import ConfigCatAPI
from website_frontend.model.avatar_status import AvatarStatus
from website_frontend.model.tech_badge import TechBadge

CONFIGCAT_API = ConfigCatAPI()


def _resolve_avatar_state(key: str) -> tuple[str, dict[str, str]]:
    if key in profile_const.AVAILABILITY_STATES:
        return key, profile_const.AVAILABILITY_STATES[key]

    default_key = site_const.AVAILABILITY_STATUS_DEFAULT
    return default_key, profile_const.AVAILABILITY_STATES[default_key]


def get_default_avatar_status() -> AvatarStatus:
    return build_avatar_status(site_const.AVAILABILITY_STATUS_DEFAULT)


def get_avatar_status_key() -> str:
    return CONFIGCAT_API.avatar_status()


def build_avatar_status(raw_key: str) -> AvatarStatus:
    normalized_key = str(raw_key).strip().strip('"').strip("'").lower()
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
