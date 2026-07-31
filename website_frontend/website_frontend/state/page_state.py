import reflex as rx

import website_frontend.constants.site_constants as site_const

from website_frontend.model.live import Live
from website_frontend.model.featured import Featured
from website_frontend.model.tech_badge import TechBadge
from website_frontend.model.avatar_status import AvatarStatus

from website_frontend.services.featured_service import get_featured_projects
from website_frontend.services.live_service import get_live_status
from website_frontend.services.profile_service import (
    get_avatar_status_key,
    get_default_avatar_status,
    get_profile_technologies,
    build_avatar_status,
)
from website_frontend.services.schedule_service import get_next_live_date
from website_frontend.shared.browser import LOCAL_TIMEZONE_SCRIPT


class PageState(rx.State):
    live_status = Live(live=False, title="", category="", tags=[], viewer=0)
    featured_info: list[Featured] = []
    timezone: str = ""
    next_live: str = ""
    avatar_status: AvatarStatus = get_default_avatar_status()
    technologies: list[TechBadge] = []

    @rx.event
    async def check_live(self):
        self.live_status = get_live_status(site_const.USER)

    @rx.event
    async def featured_links(self):
        self.featured_info = get_featured_projects()

    @rx.event
    async def check_avatar_status(self):
        self.avatar_status = build_avatar_status(get_avatar_status_key())

    @rx.event
    async def check_schedule(self):
        if self.timezone == "":
            return rx.call_script(
                LOCAL_TIMEZONE_SCRIPT,
                PageState.update_timezone,
            )
        else:
            await self.update_timezone(self.timezone)

    @rx.event
    async def update_timezone(self, timezone: str):
        self.timezone = timezone
        self.next_live = get_next_live_date(self.timezone)

    @rx.event
    def init_technologies(self):
        self.technologies = get_profile_technologies()
