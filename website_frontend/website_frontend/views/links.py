import reflex as rx
import website_frontend.constants.site_constants as const

from website_frontend.styles.styles import Color, Spacing

from website_frontend.components.link_featured import link_featured
from website_frontend.components.link_button import link_button
from website_frontend.components.section import section

from website_frontend.components.ui.auto_scrolling_carousel import (
    auto_scrolling_carousel,
)
from website_frontend.components.ui.direction_aware_hover import (
    direction_aware_hover,
)

from website_frontend.routes import Route

from website_frontend.state.page_state import PageState


def links() -> rx.Component:
    return rx.vstack(
        rx.cond(
            PageState.featured_info,
            section(
                "Proyectos Destacados",
                auto_scrolling_carousel(
                    reactive_list=PageState.featured_info,
                    render_function=lambda featured: rx.flex(
                        direction_aware_hover(
                            image_url=featured.image_url,
                            children=link_featured(featured),
                        ),
                        width="350px",
                        height="280px",
                        align_items="center",
                        justify_content="center",
                    ),
                    direction="right",
                    speed="slow",
                ),
            ),
        ),
        section(
            "Plataformas de trabajo",
            link_button(
                href=const.WORKANA_URL,
                title="Workana",
                description="Perfil donde ofrezco mis servicios profesionales de desarrollo.",
                icon="fa-solid fa-briefcase",
                icon_color=Color.WHITE.value,
                badge="Freelance",
                badge_color=Color.PRIMARY.value,
            ),
            link_button(
                href=const.GUMROAD_URL,
                title="Gumroad",
                description="Tienda de recursos, plantillas y cursos sobre desarrollo Full-Stack.",
                icon="fa-solid fa-store",
                icon_color=Color.WHITE.value,
                badge="Productos digitales",
                badge_color=Color.PINK.value,
            ),
        ),
        section(
            "Comunidad",
            link_button(
                href=const.DISCORD_URL,
                title="Discord",
                description="Únete al chat para discutir tecnologías y proyectos.",
                icon="fa-brands fa-discord",
                icon_color=Color.DISCORD.value,
                badge="Comunidad",
                badge_color=Color.DISCORD.value,
            ),
            link_button(
                href=const.YOUTUBE_URL,
                title="YouTube",
                description="Tutoriales de .NET, Angular y arquitectura de software.",
                icon="fa-brands fa-youtube",
                icon_color=Color.RED.value,
            ),
            link_button(
                href=const.TWITCH_URL,
                title="Twitch",
                description="Live coding y sesiones de preguntas y respuestas.",
                icon="fa-brands fa-twitch",
                icon_color=Color.PURPLE.value,
            ),
        ),
        section(
            "Recursos y más",
            link_button(
                href=Route.BLOG.value,
                title="Mi Blog (Artículos Técnicos)",
                description="Publicaciones sobre arquitectura, patrones de diseño y Full-Stack.",
                icon="fa-solid fa-newspaper",
                icon_color=Color.WHITE.value,
                badge="Featured",
                badge_color=Color.PRIMARY.value,
                border_color=Color.PRIMARY.value,
            ),
            link_button(
                href=const.DEIVISAHERRERAJ_URL,
                title="Mi Portafolio Web",
                description="Explora proyectos a profundidad y experiencia detallada.",
                icon="fa-solid fa-briefcase",
                icon_color=Color.WHITE.value,
                border_color=Color.PRIMARY.value,
            ),
            link_button(
                href=const.SETUP_URL,
                title="Mi setup",
                description="Listado de hardware y software que utilizo diariamente.",
                icon="fa-solid fa-desktop",
                icon_color=Color.WHITE.value,
                badge="Setup",
                badge_color=Color.GRAY_DARK.value,
            ),
            link_button(
                href=const.COFFEE_URL,
                title="Invítame a un café",
                description="Apoya mi contenido y desarrollo con una pequeña contribución.",
                icon="fa-solid fa-mug-hot",
                icon_color=Color.WHITE.value,
                badge="Apoyo",
                badge_color=Color.ORANGE.value,
            ),
        ),
        section(
            "Contacto",
            link_button(
                href=const.MYPUBLICINBOX_URL,
                title="My Public Inbox",
                description="Para consultas rápidas y profesionales con prioridad de respuesta.",
                icon="fa-solid fa-inbox",
                icon_color=Color.WHITE.value,
                badge="Directo",
                badge_color=Color.PRIMARY.value,
            ),
            link_button(
                href=f"mailto:{const.EMAIL}",
                title="Email",
                description="Envíame un correo electrónico para consultas directas.",
                icon="fa-solid fa-envelope",
                icon_color=Color.WHITE.value,
                badge="Correo",
                badge_color=Color.GRAY_DARK.value,
                is_external=False,
            ),
        ),
        width="100%",
        spacing=Spacing.DEFAULT.value,
        on_mount=PageState.featured_links,
    )
