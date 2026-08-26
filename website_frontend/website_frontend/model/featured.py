from typing import List, Optional

from pydantic import BaseModel, Field

from website_frontend.model.project_status import ProjectStatus


class Featured(BaseModel):
    href: Optional[str] = None
    image_url: Optional[str] = None
    title: str
    description: Optional[str] = None
    technologies: List[str] = Field(default_factory=list)
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    status: ProjectStatus
