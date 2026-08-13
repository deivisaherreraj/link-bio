import re

from website_frontend.integrations.twitch import TwitchAPI
from website_frontend.model.live import Live

TWITCH_API = TwitchAPI()
TWITCH_USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_]{4,25}$")


def is_valid_twitch_username(user: str) -> bool:
    return bool(TWITCH_USERNAME_PATTERN.fullmatch(user))


def get_live_status(user: str) -> Live:
    if not is_valid_twitch_username(user):
        return Live.offline()

    return TWITCH_API.live(user)
