from pydantic import BaseModel, Field

from website_frontend.model.primary_social import PrimarySocial


class Profile(BaseModel):
    full_name: str
    handle: str
    headline: str
    bio_short: str
    avatar_url: str
    email: str
    availability_status_key: str
    tech_stack_summary: str
    primary_socials: list[PrimarySocial] = Field(default_factory=list)
