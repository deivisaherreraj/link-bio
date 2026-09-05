import json
import logging
import os
from datetime import datetime
from typing import Any, TypeGuard

import configcatclient
import dotenv

from website_frontend.integrations.observability import log_fail_closed_event
from website_frontend.shared.schedule_types import LiveSchedule, WeekdayKey

logger = logging.getLogger(__name__)


def _is_weekday_key(value: object) -> TypeGuard[WeekdayKey]:
    return isinstance(value, str) and value in {"0", "1", "2", "3", "4", "5", "6"}


class ConfigCatAPI:
    dotenv.load_dotenv()

    CONFIGCAT_SDK_KEY = os.environ.get("CONFIGCAT_SDK_KEY")

    def __init__(self) -> None:
        if self.CONFIGCAT_SDK_KEY is not None:
            self.configcat = configcatclient.get(self.CONFIGCAT_SDK_KEY)

    def _get_config_value(self, key: str, default: str) -> str:
        if not hasattr(self, "configcat"):
            return default

        try:
            response: Any = self.configcat.get_value(key, default)
        except Exception as exc:
            log_fail_closed_event(
                logger,
                event="configcat_get_value_failed_closed",
                integration="configcat",
                operation="get_value",
                context={"key": key, "error_type": type(exc).__name__},
            )
            return default

        if not isinstance(response, str):
            return default

        return response

    def _normalize_schedule(self, payload: object) -> LiveSchedule:
        if not isinstance(payload, dict):
            return {}

        normalized: LiveSchedule = {}

        for key, value in payload.items():
            if not _is_weekday_key(key):
                continue

            if not isinstance(value, str):
                continue

            schedule_time = value.strip()
            if not schedule_time:
                continue

            try:
                datetime.strptime(schedule_time, "%H:%M")
            except ValueError:
                continue

            normalized[key] = schedule_time

        return normalized

    def schedule(self) -> LiveSchedule:
        response = self._get_config_value("live_schedule", "")

        try:
            parsed = json.loads(response)
        except json.JSONDecodeError:
            return {}

        return self._normalize_schedule(parsed)
