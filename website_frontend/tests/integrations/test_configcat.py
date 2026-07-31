import json

import website_frontend.constants.site_constants as site_const
from website_frontend.integrations.configcat import ConfigCatAPI


class StubConfigCatClient:
    def __init__(self, values: dict[str, str]) -> None:
        self.values = values
        self.calls: list[tuple[str, str]] = []

    def get_value(self, key: str, default: str) -> str:
        self.calls.append((key, default))
        return self.values.get(key, default)


def test_avatar_status_returns_default_when_client_is_missing():
    configcat_api = ConfigCatAPI()
    if hasattr(configcat_api, "configcat"):
        delattr(configcat_api, "configcat")

    result = configcat_api.avatar_status()

    assert result == site_const.AVAILABILITY_STATUS_DEFAULT


def test_avatar_status_normalizes_client_value():
    configcat_api = ConfigCatAPI()
    configcat_api.configcat = StubConfigCatClient(
        {"profile_availability_status": ' "CONSULTORIA" '}
    )

    result = configcat_api.avatar_status()

    assert result == "consultoria"
    assert configcat_api.configcat.calls == [
        ("profile_availability_status", site_const.AVAILABILITY_STATUS_DEFAULT)
    ]


def test_schedule_parses_json_payload():
    schedule_payload = {"0": "18:00", "2": "20:30"}
    configcat_api = ConfigCatAPI()
    configcat_api.configcat = StubConfigCatClient(
        {"live_schedule": json.dumps(schedule_payload)}
    )

    result = configcat_api.schedule()

    assert result == schedule_payload
    assert configcat_api.configcat.calls == [("live_schedule", "")]


def test_schedule_returns_empty_dict_when_client_is_missing():
    configcat_api = ConfigCatAPI()
    if hasattr(configcat_api, "configcat"):
        delattr(configcat_api, "configcat")

    result = configcat_api.schedule()

    assert result == {}


def test_schedule_returns_empty_dict_for_invalid_json_payload():
    configcat_api = ConfigCatAPI()
    configcat_api.configcat = StubConfigCatClient({"live_schedule": "not-json"})

    result = configcat_api.schedule()

    assert result == {}
    assert configcat_api.configcat.calls == [("live_schedule", "")]
