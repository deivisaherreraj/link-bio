# ===============================
# Estados del Avatar / Disponibilidad
# ===============================
AVAILABILITY_STATES: dict[str, dict[str, str]] = {
    "activo": {
        "text": "Disponible para proyectos freelance — Respuesta rápida",
        "class_name": "is-active",
        "icon": "fa-bolt",
    },
    "pausado": {
        "text": "En proyectos activos — Disponibilidad limitada",
        "class_name": "is-paused",
        "icon": "fa-pause",
    },
    "no-disponible": {
        "text": "No aceptando nuevos proyectos por ahora",
        "class_name": "is-unavailable",
        "icon": "fa-ban",
    },
    "empleo": {
        "text": "Buscando oportunidades Full-Time — Disponible para entrevistas",
        "class_name": "is-hiring",
        "icon": "fa-magnifying-glass",
    },
    "consultoria": {
        "text": "Disponible para consultoría especializada — Corto plazo",
        "class_name": "is-consulting",
        "icon": "fa-laptop-code",
    },
    "tiempo-completo": {
        "text": "Trabajo en jornada completa — Disponibilidad mínima",
        "class_name": "is-fulltime",
        "icon": "fa-briefcase",
    },
    "aprendizaje": {
        "text": "En actualización — Aprendiendo nuevas tecnologías",
        "class_name": "is-learning",
        "icon": "fa-graduation-cap",
    },
    "viajando": {
        "text": "Fuera de oficina — Respuesta lenta",
        "class_name": "is-traveling",
        "icon": "fa-plane",
    },
    "mantenimiento": {
        "text": "En mantenimiento programado — Consultas por prioridad",
        "class_name": "is-maintenance",
        "icon": "fa-wrench",
    },
    "transmisión": {
        "text": "Creando contenido — Disponible luego",
        "class_name": "is-streaming",
        "icon": "fa-video",
    },
    "enfoque": {
        "text": "En modo enfoque — Notificaciones limitadas",
        "class_name": "is-focus",
        "icon": "fa-eye",
    },
}

# ===============================
# Tecnologías del Perfil
# ===============================
TECHNOLOGIES = [
    {"name": "Angular", "color": "#DD0031", "icon_class": "fa-brands fa-angular"},
    {"name": ".NET", "color": "#5C2D91", "icon_class": "fa-solid fa-code"},
    {"name": "Node.js", "color": "#339933", "icon_class": "fa-brands fa-node-js"},
    {"name": "PHP", "color": "#777BB4", "icon_class": "fa-brands fa-php"},
    {"name": "Azure", "color": "#0078D4", "icon_class": "fa-brands fa-microsoft"},
]
