from website_frontend.integrations.configcat import ConfigCatAPI
from website_frontend.shared.datetime_utils import next_date

CONFIGCAT_API = ConfigCatAPI()


def get_live_schedule() -> dict:
    return CONFIGCAT_API.schedule()


def get_next_live_date(timezone: str) -> str:
    return next_date(get_live_schedule(), timezone)
