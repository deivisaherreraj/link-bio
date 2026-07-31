from typing import List, Optional

from pydantic import BaseModel

from website_frontend.model.project_status import ProjectStatus


class Featured(BaseModel):
    href: str
    image_url: str
    title: str
    description: Optional[str] = None
    technologies: List[str] = []
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    status: ProjectStatus
