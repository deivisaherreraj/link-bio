import reflex as rx
import website_frontend.constants as const

from website_frontend.routes import Route
from website_frontend.components.link_featured import link_featured
from website_frontend.components.link_button import link_button
from website_frontend.components.title import title
from website_frontend.styles.styles import Color, Spacing
from website_frontend.state.PageState import PageState


def links() -> rx.Component:
    return rx.vstack(
        title("Comunidad"),
        # TODO Habilitar función solo cuando se tengo los tutorias o videos
        # link_button(
        #     "Guías y tutoriales",
        #     "Consulta mis tutoriales para aprender programación",
        #     "/icons/code.svg",
        #     Route.COURSES.value,
        #     True,
        #     False,
        #     Color.SECONDARY.value
        # ),
        link_button(
            "Discord",
            "El chat y los grupos de estudio de la comunidad",
            "/icons/discord.svg",
            const.DISCORD_URL,
            True
        ),
        
        title("Plataformas de trabajo"),
        link_button(
            "Workana",
            "Perfil de Workana donde ofrezco mis servicios como freelance",
            "/icons/freelancer.svg",
            const.WORKANA_URL
        ),
        link_button(
            "Gumroad",
            "Mi tienda en Gumroad donde vendo recursos, cursos, o productos digitales",
            "/icons/gumroad.svg",
            const.GUMROAD_URL
        ),
        
        rx.cond(
            PageState.featured_info,
            rx.vstack(
                title("Destacado"),
                rx.flex(
                    rx.foreach(
                        PageState.featured_info,
                        link_featured
                    ),
                    flex_direction=["column", "row"],
                    spacing=Spacing.DEFAULT.value
                ),
                spacing=Spacing.DEFAULT.value
            )
        ),
                
        title("Recursos y más"),
        link_button(
            "Mi setup",
            "Listado con todos los elementos que uso en mi trabajo",
            "/icons/setup.svg",
            Route.INDEX.value,
            True,
            False
        ),
        link_button(
            "DeivisAHerreraJ",
            "Mi porfolio web",
            "/icons/portfolio.svg",
            const.DEIVISAHERRERAJ_URL,
            False,
            True,            
            Color.SECONDARY.value
        ),
        # TODO Deshabilitar al tener la pagina
        # link_button(
        #     "DherrerajDev",
        #     "Mi sitio web",
        #     "/icons/challenges.svg",
        #     const.DHERRERAJDEV_URL,
        #     True,
        #     False,            
        #     Color.SECONDARY.value
        # ),
        link_button(
            "Invítame a un café",
            "¿Quieres ayudarme a que siga creando contenido?",
            "/icons/coffee.svg",
            const.COFFEE_URL,
            False,
            True
        ),

        title("Contacto"),
        link_button(
            "My Public Inbox",
            "Respuesta rápida y con preferencia",
            "/icons/checkemail.svg",
            Route.INDEX.value,
            True,
            True
        ),
        link_button(
            "Email",
            const.EMAIL,
            "/icons/email.svg",
            f"mailto:{const.EMAIL}"
        ),
        width="100%",
        spacing=Spacing.DEFAULT.value,
        on_mount=PageState.featured_links
    )