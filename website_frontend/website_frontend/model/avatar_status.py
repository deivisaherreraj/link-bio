from pydantic import BaseModel


class AvatarStatus(BaseModel):
    """
    Modelo que encapsula toda la información de estado del avatar.
    - key: clave lógica (activo, pausado, empleo, etc.)
    - text: texto que se muestra en el tooltip
    - class_name: clase CSS (is-active, is-paused, etc.)
    - icon: clase Font Awesome (fa-bolt, fa-pause, etc.)
    """

    key: str
    text: str
    class_name: str
    icon: str
