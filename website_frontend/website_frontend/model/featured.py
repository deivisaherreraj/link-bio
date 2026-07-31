from pydantic import BaseModel
from typing import List, Optional

from website_frontend.model.project_status import ProjectStatus


class Featured(BaseModel):
    href: str
    image_url: str
    title: str
    description: Optional[str] = None
    technologies: List[str] = []
    github_url: str
    live_url: str
    status: ProjectStatus
