import reflex as rx
import website_frontend.utils as utils
import website_frontend.constants as const

from website_frontend.model.Live import Live
from website_frontend.model.Featured import Featured
from website_frontend.api.api import live, featured, schedule

class PageState(rx.State):
    live_status = Live(live=False, title="", category="", tags=[], viewer=0)
    featured_info: list[Featured]
    timezone = ""
    next_live = ""
    
    async def check_live(self):
        self.live_status = await live(const.USER)
        
    async def featured_links(self):
        self.featured_info = await featured()
        
    async def check_schedule(self):
        if self.timezone == "":
            return rx.call_script(
                utils.LOCAL_TIMEZONE_SCRIPT,
                PageState.update_timezone
            )
        else:
            await self.update_timezone(self.timezone)

    async def update_timezone(self, timezone: str):
        self.timezone = timezone
        self.next_live = utils.next_date(await schedule(), self.timezone)