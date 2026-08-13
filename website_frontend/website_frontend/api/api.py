from typing import Annotated

from fastapi import FastAPI, Path

from website_frontend.model.featured import Featured
from website_frontend.model.live import Live
from website_frontend.services.featured_service import get_featured_projects
from website_frontend.services.live_service import get_live_status
from website_frontend.services.profile_service import get_avatar_status_key
from website_frontend.services.schedule_service import get_live_schedule

TwitchUsername = Annotated[
    str,
    Path(
        min_length=4,
        max_length=25,
        pattern=r"^[A-Za-z0-9_]{4,25}$",
    ),
]

# Create a FastAPI app
fastapi_app = FastAPI(title="Website API")


@fastapi_app.get("/live/{user}")
async def live(user: TwitchUsername) -> Live:
    return get_live_status(user)


@fastapi_app.get("/featured")
async def featured() -> list[Featured]:
    return get_featured_projects()


@fastapi_app.get("/schedule")
async def schedule() -> dict:
    return get_live_schedule()


@fastapi_app.get("/config-avatar-status")
async def avatar_status() -> str:
    return get_avatar_status_key()
