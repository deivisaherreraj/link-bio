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
    return [
        TechBadge(
            name=item["name"],
            color=item["color"],
            icon_class=item["icon_class"],
        )
        for item in profile_const.TECHNOLOGIES
    ]
