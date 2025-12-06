from pydantic import BaseModel


class TechBadge(BaseModel):
    name: str
    color: str
    icon_class: str
