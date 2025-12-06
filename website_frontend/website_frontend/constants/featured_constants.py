from typing import Dict
from website_frontend.model.ProjectStatus import ProjectStatus

# Mapeo de estados del proyecto (colores y animaciones)
PROJECT_STATUS_CONFIG: Dict[str, ProjectStatus] = {
    "dev": ProjectStatus(
        key="dev",
        label="En Desarrollo",
        color="#FBBF24",
        bg_color="rgba(251, 191, 36, 0.15)",
        icon="code",
        animation_class="animate-pulse-dev",
    ),
    "migration": ProjectStatus(
        key="migration",
        label="En Migración",
        color="#FB923C",
        bg_color="rgba(251, 146, 60, 0.15)",
        icon="move",
        animation_class="animate-fade-migration",
    ),
    "testing": ProjectStatus(
        key="testing",
        label="Pruebas Unitarias",
        color="#A78BFA",
        bg_color="rgba(167, 139, 250, 0.15)",
        icon="box",
        animation_class="animate-glow-testing",
    ),
    "deploying": ProjectStatus(
        key="deploying",
        label="En Despliegue",
        color="#0099FF",
        bg_color="rgba(0, 153, 255, 0.15)",
        icon="rocket",
        animation_class="animate-pulse-deploying",
    ),
    "production": ProjectStatus(
        key="production",
        label="En Producción",
        color="#10B981",
        bg_color="rgba(16, 185, 129, 0.15)",
        icon="globe",
        animation_class="",
    ),
    "finalized": ProjectStatus(
        key="finalized",
        label="Finalizado",
        color="#22D3EE",
        bg_color="rgba(34, 211, 238, 0.15)",
        icon="circle-check",
        animation_class="",
    ),
    "paused": ProjectStatus(
        key="paused",
        label="Pausado",
        color="#EF4444",
        bg_color="rgba(239, 68, 68, 0.15)",
        icon="circle-pause",
        animation_class="animate-fade-paused",
    ),
}

# Clave del estado por defecto
DEFAULT_PROJECT_STATUS_KEY = "dev"
