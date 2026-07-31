import json
import os
from typing import Any

import configcatclient
import dotenv

import website_frontend.constants.site_constants as site_const


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
        return str(response)

    def schedule(self) -> dict:
        response = self._get_config_value("live_schedule", "")

        try:
            parsed = json.loads(response)
        except json.JSONDecodeError:
            return {}

        return parsed if isinstance(parsed, dict) else {}

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

        return value
