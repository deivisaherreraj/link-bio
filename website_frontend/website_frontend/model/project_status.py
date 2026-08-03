from pydantic import BaseModel


class ProjectStatus(BaseModel):
    """
    Modelo para representar el estado visual de un proyecto destacado.
    Sirve como “API” de configuración que en el futuro podrá venir de Supabase
    u otro origen.
    """

    key: str
    label: str
    color: str
    bg_color: str
    icon: str
    animation_class: str
