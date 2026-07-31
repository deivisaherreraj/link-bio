import os
import dotenv
import configcatclient
import json

import website_frontend.constants.site_constants as site_const


class ConfigCatAPI:
    dotenv.load_dotenv()

    CONFIGCAT_SDK_KEY = os.environ.get("CONFIGCAT_SDK_KEY")

    def __init__(self) -> None:
        if self.CONFIGCAT_SDK_KEY is not None:
            self.configcat = configcatclient.get(self.CONFIGCAT_SDK_KEY)

    def schedule(self) -> dict:
        if not hasattr(self, "configcat"):
            return {}

        response = self.configcat.get_value("live_schedule", "")

        try:
            return json.loads(str(response))
        except json.JSONDecodeError:
            return {}

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
        if not hasattr(self, "configcat"):
            return site_const.AVAILABILITY_STATUS_DEFAULT

        response = self.configcat.get_value(
            "profile_availability_status",
            site_const.AVAILABILITY_STATUS_DEFAULT,
        )

        # Aseguramos string y normalizamos lo básico
        value = str(response).strip().strip('"').strip("'").lower()

        return value
