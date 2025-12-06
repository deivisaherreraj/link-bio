import reflex as rx
import website_frontend.constants.site_constants as const

from website_frontend.styles.styles import Color, Spacing, Margin

from website_frontend.components.link_featured import link_featured
from website_frontend.components.link_button import link_button
from website_frontend.components.title import title
from website_frontend.components.ui.auto_scrolling_carousel import (
    auto_scrolling_carousel,
)
from website_frontend.components.ui.direction_aware_hover import (
    direction_aware_hover,
)

from website_frontend.routes import Route

from website_frontend.state.PageState import PageState


def links() -> rx.Component:
    return rx.vstack(
        rx.cond(
            PageState.featured_info,
            rx.el.Section.create(
                title("Proyectos Destacados"),
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
                width="100%",
                margin_bottom=Margin.VERY_BIG.value,
            ),
        ),
        title("Comunidad"),
        link_button(
            "Discord",
            "Únete al chat para discutir tecnologías y proyectos.",
            "/icons/discord.svg",
            const.DISCORD_URL,
            True,
        ),
        link_button(
            "YouTube",
            "Tutoriales de .NET, Angular y arquitectura de software.",
            "/icons/youtube.svg",
            const.YOUTUBE_URL,
            True,
        ),
        link_button(
            "Twitch",
            "Live coding y sesiones de preguntas y respuestas.",
            "/icons/twitch.svg",
            const.TWITCH_URL,
            True,
        ),
        title("Plataformas de trabajo"),
        link_button(
            "Workana",
            "Perfil de Workana donde ofrezco mis servicios como freelance",
            "/icons/freelancer.svg",
            const.WORKANA_URL,
        ),
        link_button(
            "Gumroad",
            "Mi tienda en Gumroad donde vendo recursos, cursos, o productos digitales",
            "/icons/gumroad.svg",
            const.GUMROAD_URL,
        ),
        title("Recursos y más"),
        link_button(
            "Mi setup",
            "Listado con todos los elementos que uso en mi trabajo",
            "/icons/setup.svg",
            Route.INDEX.value,
            True,
            False,
        ),
        link_button(
            "DeivisAHerreraJ",
            "Mi porfolio web",
            "/icons/portfolio.svg",
            const.DEIVISAHERRERAJ_URL,
            False,
            True,
            Color.SECONDARY.value,
        ),
        link_button(
            "Invítame a un café",
            "¿Quieres ayudarme a que siga creando contenido?",
            "/icons/coffee.svg",
            const.COFFEE_URL,
            False,
            True,
        ),
        title("Contacto"),
        link_button(
            "My Public Inbox",
            "Respuesta rápida y con preferencia",
            "/icons/checkemail.svg",
            Route.INDEX.value,
            True,
            True,
        ),
        link_button("Email", const.EMAIL, "/icons/email.svg", f"mailto:{const.EMAIL}"),
        width="100%",
        spacing=Spacing.DEFAULT.value,
        on_mount=PageState.featured_links,
    )
