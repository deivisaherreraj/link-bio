import json
import os
from datetime import datetime
from typing import Any, TypeGuard

import configcatclient
import dotenv

import website_frontend.constants.profile_constants as profile_const
import website_frontend.constants.site_constants as site_const
from website_frontend.shared.schedule_types import LiveSchedule, WeekdayKey


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

        response: Any = self.configcat.get_value(key, default)
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

    def avatar_status(self) -> str:
        """
        Devuelve el estado de disponibilidad del avatar desde ConfigCat.
        Flag sugerido: 'profile_availability_status'.

        Normaliza el valor:
        - trim de espacios
        - remove comillas sobrantes
        - lower
        """
        # Si no hay SDK o flag, devolvemos 'activo' por defecto.
        response = self._get_config_value(
            "profile_availability_status",
            site_const.AVAILABILITY_STATUS_DEFAULT,
        )

        # Aseguramos string y normalizamos lo básico
        value = response.strip().strip('"').strip("'").lower()

        if value in profile_const.AVAILABILITY_STATES:
            return value

        return site_const.AVAILABILITY_STATUS_DEFAULT
