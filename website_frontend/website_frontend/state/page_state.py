import reflex as rx

import website_frontend.constants.site_constants as site_const
from website_frontend.model.avatar_status import AvatarStatus
from website_frontend.model.featured import Featured
from website_frontend.model.live import Live
from website_frontend.model.profile import Profile
from website_frontend.model.social_link import SocialLink
from website_frontend.model.tech_badge import TechBadge
from website_frontend.services.featured_service import get_featured_projects
from website_frontend.services.live_service import get_live_status
from website_frontend.services.profile_service import (
    build_avatar_status,
    get_default_profile,
    get_primary_social_url,
    get_profile,
    get_profile_technologies,
)
from website_frontend.services.schedule_service import get_next_live_date
from website_frontend.services.social_links_service import get_social_links_by_section
from website_frontend.shared.browser import LOCAL_TIMEZONE_SCRIPT
from website_frontend.shared.datetime_utils import normalize_timezone

DEFAULT_PROFILE = get_default_profile()
DEFAULT_SOCIAL_LINKS = get_social_links_by_section()


class PageState(rx.State):
    live_status = Live.offline()
    featured_info: list[Featured] = []
    work_social_links: list[SocialLink] = DEFAULT_SOCIAL_LINKS["work"]
    community_social_links: list[SocialLink] = DEFAULT_SOCIAL_LINKS["community"]
    resources_social_links: list[SocialLink] = DEFAULT_SOCIAL_LINKS["resources"]
    contact_social_links: list[SocialLink] = DEFAULT_SOCIAL_LINKS["contact"]
    timezone: str = ""
    next_live: str = ""
    profile_info: Profile = DEFAULT_PROFILE
    avatar_status: AvatarStatus = build_avatar_status(
        DEFAULT_PROFILE.availability_status_key
    )
    github_url: str | None = get_primary_social_url(DEFAULT_PROFILE, "GitHub")
    linkedin_url: str | None = get_primary_social_url(DEFAULT_PROFILE, "LinkedIn")
    technologies: list[TechBadge] = []

    @rx.var
    def has_multiple_featured_projects(self) -> bool:
        return len(self.featured_info) > 1

    @rx.event
    async def check_live(self):
        self.live_status = get_live_status(site_const.USER)

    @rx.event
    async def featured_links(self):
        self.featured_info = get_featured_projects()

    @rx.event
    async def load_social_links(self):
        social_links_by_section = get_social_links_by_section()
        self.work_social_links = social_links_by_section["work"]
        self.community_social_links = social_links_by_section["community"]
        self.resources_social_links = social_links_by_section["resources"]
        self.contact_social_links = social_links_by_section["contact"]

    @rx.event
    async def check_avatar_status(self):
        self.avatar_status = build_avatar_status(
            self.profile_info.availability_status_key
        )

    @rx.event
    async def load_profile(self):
        profile = get_profile()
        self.profile_info = profile
        self.avatar_status = build_avatar_status(profile.availability_status_key)
        self.github_url = get_primary_social_url(profile, "GitHub")
        self.linkedin_url = get_primary_social_url(profile, "LinkedIn")

    @rx.event
    async def check_schedule(self):
        if self.timezone == "":
            return rx.call_script(
                LOCAL_TIMEZONE_SCRIPT,
                PageState.update_timezone,  # type: ignore[operator]
            )
        else:
            await self.update_timezone(self.timezone)  # type: ignore[operator]

    @rx.event
    async def update_timezone(self, timezone: str):
        normalized_timezone = normalize_timezone(timezone)
        if normalized_timezone == "":
            return

        self.timezone = normalized_timezone
        self.next_live = get_next_live_date(self.timezone)

    @rx.event
    def init_technologies(self):
        self.technologies = get_profile_technologies()
