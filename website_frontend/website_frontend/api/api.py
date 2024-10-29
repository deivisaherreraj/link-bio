from website_frontend.model.Live import Live
from website_frontend.model.Featured import Featured
from .TwitchAPI import TwitchAPI
from .SupabaseAPI import SupabaseAPI
from .ConfigCatAPI import ConfigCatAPI

TWITCH_API = TwitchAPI()
SUPABASE_API = SupabaseAPI()
CONFIGCAT_API = ConfigCatAPI()

async def live(user: str) -> Live:    
    return TWITCH_API.live(user)

async def featured() -> list[Featured]:
    return SUPABASE_API.featured()

async def schedule() -> dict:
    return CONFIGCAT_API.schedule()