from typing import Optional

from pydantic import BaseModel


class ProjectStatus(BaseModel):
    """
    Modelo para representar el estado visual de un proyecto destacado.
    Sirve como “API” de configuración que en el futuro podrá venir de Supabase
    u otro origen.
    """

    key: str
    label: Optional[str]
    color: Optional[str]
    bg_color: Optional[str]
    icon: Optional[str]
    animation_class: Optional[str]
