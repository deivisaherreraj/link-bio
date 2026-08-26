from pydantic import BaseModel


class PrimarySocial(BaseModel):
    label: str
    url: str
    icon: str
    is_active: bool
    priority: int
