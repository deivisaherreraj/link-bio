import reflex as rx

import website_frontend.utils as utils
import website_frontend.constants.site_constants as site_const
import website_frontend.constants.profile_constants as profile_const

from website_frontend.model.Live import Live
from website_frontend.model.Featured import Featured
from website_frontend.model.TechBadge import TechBadge
from website_frontend.model.AvatarStatus import AvatarStatus

from website_frontend.api.api import (
    live,
    featured,
    schedule,
    avatar_status,
)


class PageState(rx.State):
    live_status = Live(live=False, title="", category="", tags=[], viewer=0)
    featured_info: list[Featured] = []
    technologies: list[TechBadge] = []

    timezone: str = ""
    next_live: str = ""

    default_avatar_state = profile_const.AVAILABILITY_STATES[
        site_const.AVAILABILITY_STATUS_DEFAULT
    ]
    avatar_status: AvatarStatus = AvatarStatus(
        key=site_const.AVAILABILITY_STATUS_DEFAULT,
        text=default_avatar_state["text"],
        class_name=default_avatar_state["class_name"],
        icon=default_avatar_state["icon"],
    )

    @rx.event
    async def check_live(self):
        self.live_status = await live(site_const.USER)

    @rx.event
    async def featured_links(self):
        self.featured_info = await featured()

    @rx.event
    async def check_schedule(self):
        if self.timezone == "":
            return rx.call_script(
                utils.LOCAL_TIMEZONE_SCRIPT, PageState.update_timezone
            )
        else:
            await self.update_timezone(self.timezone)

    @rx.event
    async def update_timezone(self, timezone: str):
        self.timezone = timezone
        self.next_live = utils.next_date(await schedule(), self.timezone)

    @rx.event
    async def check_avatar_status(self):
        """
        Lee el estado del avatar desde ConfigCat y lo mapea a AvatarStatus.
        Toda la lógica de mapping se resuelve aquí (lado servidor).
        """
        # 1. Obtener clave “cruda” desde la API de ConfigCat
        raw_key = await avatar_status()
        key = str(raw_key).strip().strip('"').strip("'").lower()

        # 2. Resolver en el dict de estados, o usar el default si no existe
        state = profile_const.AVAILABILITY_STATES.get(
            key,
            profile_const.AVAILABILITY_STATES[site_const.AVAILABILITY_STATUS_DEFAULT],
        )

        # 3. Guardar todo empaquetado en AvatarStatus
        self.avatar_status = AvatarStatus(
            key=key,
            text=state["text"],
            class_name=state["class_name"],
            icon=state["icon"],
        )

    @rx.event
    def init_technologies(self):
        self.technologies = []

        if len(profile_const.TECHNOLOGIES) > 0:
            for technologies_item in profile_const.TECHNOLOGIES:
                self.technologies.append(
                    TechBadge(
                        name=technologies_item["name"],
                        color=technologies_item["color"],
                        icon_class=technologies_item["icon_class"],
                    )
                )
