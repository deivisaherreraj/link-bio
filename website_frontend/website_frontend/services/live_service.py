from website_frontend.integrations.twitch import TwitchAPI
from website_frontend.model.live import Live

TWITCH_API = TwitchAPI()


def get_live_status(user: str) -> Live:
    return TWITCH_API.live(user)
