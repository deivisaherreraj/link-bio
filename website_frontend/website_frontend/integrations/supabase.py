import logging
import os
from collections.abc import Mapping

import dotenv
from supabase import Client, create_client

import website_frontend.constants.featured_constants as featured_const
from website_frontend.integrations.observability import fail_closed_event
from website_frontend.model.featured import Featured
from website_frontend.shared.urls import is_actionable_external_url

logger = logging.getLogger(__name__)


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
            normalized: list[str] = []
            for technology in raw_value:
                if not isinstance(technology, str):
                    continue

                value = technology.strip()
                if value:
                    normalized.append(value)

            return normalized

        if isinstance(raw_value, str):
            # Cadena "React, Node.js, MongoDB"
            return [t.strip() for t in raw_value.split(",") if t.strip()]

        # Cualquier otro tipo, se ignora
        return []

    def _get_string(self, payload: Mapping[str, object], key: str) -> str:
        value = payload.get(key)
        if not isinstance(value, str):
            return ""

        return value.strip()

    def _get_optional_string(
        self, payload: Mapping[str, object], key: str
    ) -> str | None:
        value = payload.get(key)
        if not isinstance(value, str):
            return None

        normalized = value.strip()
        return normalized if normalized else None

    def _get_optional_external_url(
        self, payload: Mapping[str, object], key: str
    ) -> str | None:
        value = self._get_optional_string(payload, key)
        if not is_actionable_external_url(value):
            return None

        return value

    def _get_status_config(self, raw_value: object) -> featured_const.ProjectStatus:
        default_key = featured_const.DEFAULT_PROJECT_STATUS_KEY

        if not isinstance(raw_value, str):
            return featured_const.PROJECT_STATUS_CONFIG[default_key]

        normalized_key = raw_value.strip().lower()
        if normalized_key not in featured_const.PROJECT_STATUS_CONFIG:
            return featured_const.PROJECT_STATUS_CONFIG[default_key]

        return featured_const.PROJECT_STATUS_CONFIG[normalized_key]

    def featured(self) -> list[Featured]:
        if not hasattr(self, "supabase"):
            return []

        try:
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
                    href = self._get_string(featured_item, "href")
                    image_url = self._get_string(featured_item, "image_url")
                    title = self._get_string(featured_item, "title")

                    if (
                        not href
                        or not is_actionable_external_url(href)
                        or not image_url
                        or not title
                    ):
                        continue

                    technologies = self._normalize_technologies(
                        featured_item.get("technologies")
                    )
                    status_config = self._get_status_config(
                        featured_item.get("status")
                    )

                    featured_data.append(
                        Featured(
                            href=href,
                            image_url=image_url,
                            title=title,
                            description=self._get_optional_string(
                                featured_item, "description"
                            ),
                            technologies=technologies,
                            github_url=self._get_optional_external_url(
                                featured_item, "github_url"
                            ),
                            live_url=self._get_optional_external_url(
                                featured_item, "live_url"
                            ),
                            status=status_config,
                        )
                    )

            return featured_data
        except Exception as exc:
            logger.warning(
                "supabase_featured_fetch_failed_closed",
                extra=fail_closed_event(
                    event="supabase_featured_fetch_failed_closed",
                    integration="supabase",
                    operation="featured",
                    context={"error_type": type(exc).__name__},
                ),
            )
            return []
