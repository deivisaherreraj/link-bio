from website_frontend.constants.site_constants import (
    COFFEE_URL,
    DEIVISAHERRERAJ_URL,
    DISCORD_URL,
    EMAIL,
    GUMROAD_URL,
    MYPUBLICINBOX_URL,
    SETUP_URL,
    TWITCH_URL,
    WORKANA_URL,
    YOUTUBE_URL,
)
from website_frontend.integrations.supabase import SupabaseAPI
from website_frontend.model.social_link import SocialLink, SocialLinkSection
from website_frontend.routes import Route
from website_frontend.styles.styles import Color

SUPABASE_API = SupabaseAPI()

SOCIAL_LINK_SECTION_ORDER: tuple[SocialLinkSection, ...] = (
    "work",
    "community",
    "resources",
    "contact",
)


def get_default_social_links() -> list[SocialLink]:
    return [
        SocialLink(
            label="Workana",
            url=WORKANA_URL,
            icon="fa-solid fa-briefcase",
            section="work",
            priority=1,
            is_active=True,
            is_external=True,
            description="Perfil donde ofrezco mis servicios profesionales de desarrollo.",
            badge="Freelance",
            badge_color=Color.PRIMARY.value,
        ),
        SocialLink(
            label="Gumroad",
            url=GUMROAD_URL,
            icon="fa-solid fa-store",
            section="work",
            priority=2,
            is_active=True,
            is_external=True,
            description=(
                "Tienda de recursos, plantillas y cursos sobre desarrollo Full-Stack."
            ),
            badge="Productos digitales",
            badge_color=Color.PINK.value,
        ),
        SocialLink(
            label="Discord",
            url=DISCORD_URL,
            icon="fa-brands fa-discord",
            section="community",
            priority=1,
            is_active=True,
            is_external=True,
            description="Únete al chat para discutir tecnologías y proyectos.",
            badge="Comunidad",
            badge_color=Color.DISCORD.value,
        ),
        SocialLink(
            label="YouTube",
            url=YOUTUBE_URL,
            icon="fa-brands fa-youtube",
            section="community",
            priority=2,
            is_active=True,
            is_external=True,
            description="Tutoriales de .NET, Angular y arquitectura de software.",
            badge_color=Color.RED.value,
        ),
        SocialLink(
            label="Twitch",
            url=TWITCH_URL,
            icon="fa-brands fa-twitch",
            section="community",
            priority=3,
            is_active=True,
            is_external=True,
            description="Live coding y sesiones de preguntas y respuestas.",
            badge_color=Color.PURPLE.value,
        ),
        SocialLink(
            label="Mi Blog (Artículos Técnicos)",
            url=Route.BLOG.value,
            icon="fa-solid fa-newspaper",
            section="resources",
            priority=1,
            is_active=True,
            is_external=False,
            description="Publicaciones sobre arquitectura, patrones de diseño y Full-Stack.",
            badge="Featured",
            badge_color=Color.PRIMARY.value,
            border_color=Color.PRIMARY.value,
        ),
        SocialLink(
            label="Mi Portafolio Web",
            url=DEIVISAHERRERAJ_URL,
            icon="fa-solid fa-briefcase",
            section="resources",
            priority=2,
            is_active=True,
            is_external=True,
            description="Explora proyectos a profundidad y experiencia detallada.",
            border_color=Color.PRIMARY.value,
        ),
        SocialLink(
            label="Mi setup",
            url=SETUP_URL,
            icon="fa-solid fa-desktop",
            section="resources",
            priority=3,
            is_active=True,
            is_external=True,
            description="Listado de hardware y software que utilizo diariamente.",
            badge="Setup",
            badge_color=Color.GRAY_DARK.value,
        ),
        SocialLink(
            label="Invítame a un café",
            url=COFFEE_URL,
            icon="fa-solid fa-mug-hot",
            section="resources",
            priority=4,
            is_active=True,
            is_external=True,
            description="Apoya mi contenido y desarrollo con una pequeña contribución.",
            badge="Apoyo",
            badge_color=Color.ORANGE.value,
        ),
        SocialLink(
            label="My Public Inbox",
            url=MYPUBLICINBOX_URL,
            icon="fa-solid fa-inbox",
            section="contact",
            priority=1,
            is_active=True,
            is_external=True,
            description="Para consultas rápidas y profesionales con prioridad de respuesta.",
            badge="Directo",
            badge_color=Color.PRIMARY.value,
        ),
        SocialLink(
            label="Email",
            url=f"mailto:{EMAIL}",
            icon="fa-solid fa-envelope",
            section="contact",
            priority=2,
            is_active=True,
            is_external=False,
            description="Envíame un correo electrónico para consultas directas.",
            badge="Correo",
            badge_color=Color.GRAY_DARK.value,
        ),
    ]


def get_social_links() -> list[SocialLink]:
    social_links = [link for link in SUPABASE_API.social_links() if link.is_active]
    if social_links:
        return social_links

    return get_default_social_links()


def get_social_links_by_section() -> dict[SocialLinkSection, list[SocialLink]]:
    grouped: dict[SocialLinkSection, list[SocialLink]] = {
        section: [] for section in SOCIAL_LINK_SECTION_ORDER
    }

    for link in get_social_links():
        grouped[link.section].append(link)

    return grouped
