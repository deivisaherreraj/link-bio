import os
from collections.abc import Mapping

import dotenv
from supabase import Client, create_client

import website_frontend.constants.featured_constants as featured_const
from website_frontend.model.featured import Featured


class SupabaseAPI:
    dotenv.load_dotenv()

    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

    def __init__(self) -> None:
        if self.SUPABASE_URL is not None and self.SUPABASE_KEY is not None:
            self.supabase: Client = create_client(self.SUPABASE_URL, self.SUPABASE_KEY)

    def _normalize_technologies(self, raw_value: object) -> list[str]:
        """
        Normaliza el campo 'technologies' desde Supabase a List[str].

        Casos posibles:
        - Array/text[] de Supabase -> list
        - Cadena separada por comas -> se hace split
        - None u otro tipo -> []
        """
        if raw_value is None:
            return []

        if isinstance(raw_value, list):
            # Ya viene como lista de strings
            return [str(t).strip() for t in raw_value if str(t).strip()]

        if isinstance(raw_value, str):
            # Cadena "React, Node.js, MongoDB"
            return [t.strip() for t in raw_value.split(",") if t.strip()]

        # Cualquier otro tipo, se ignora
        return []

    def _get_string(self, payload: Mapping[str, object], key: str) -> str:
        value = payload.get(key)
        return value if isinstance(value, str) else ""

    def _get_optional_string(
        self, payload: Mapping[str, object], key: str
    ) -> str | None:
        value = payload.get(key)
        return value if isinstance(value, str) else None

    def featured(self) -> list[Featured]:
        if not hasattr(self, "supabase"):
            return []

        response = (
            self.supabase.table("featured")
            .select("*")
            .order("init_date", desc=True)
            .limit(4)
            .execute()
        )

        featured_data: list[Featured] = []

        if len(response.data) > 0:
            for featured_item in response.data:
                if not isinstance(featured_item, Mapping):
                    continue

                featured_item = dict(featured_item)
                technologies = self._normalize_technologies(
                    featured_item.get("technologies")
                )

                status_key = (
                    str(
                        featured_item.get(
                            "status", featured_const.DEFAULT_PROJECT_STATUS_KEY
                        )
                    )
                    .strip()
                    .lower()
                )
                status_config = featured_const.PROJECT_STATUS_CONFIG.get(
                    status_key,
                    featured_const.PROJECT_STATUS_CONFIG[
                        featured_const.DEFAULT_PROJECT_STATUS_KEY
                    ],
                )

                featured_data.append(
                    Featured(
                        href=self._get_string(featured_item, "href"),
                        image_url=self._get_string(featured_item, "image_url"),
                        title=self._get_string(featured_item, "title"),
                        description=self._get_optional_string(
                            featured_item, "description"
                        ),
                        technologies=technologies,
                        github_url=self._get_string(featured_item, "github_url"),
                        live_url=self._get_string(featured_item, "live_url"),
                        status=status_config,
                    )
                )

        return featured_data
