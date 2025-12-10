import reflex as rx
import datetime

import website_frontend.constants.site_constants as site_const

from website_frontend.styles.styles import Spacing, Padding, Margin
from website_frontend.styles.colors import Color
from website_frontend.styles.fonts import FontSize

from website_frontend.components.info_text import info_text
from website_frontend.components.link_button import link_button

from website_frontend.views.profile import profile

from website_frontend.state.PageState import PageState


def header(details=True) -> rx.Component:
    return rx.vstack(
        # ProfileHeader
        profile(
            name="Herrera, Deivis",
            handle="@dherrerajdev",
            tagline="Full-Stack Developer & Tech Enthusiast",
            tech_stack="Especializado en desarrollo web moderno y arquitecturas escalables",
            avatar_url="/avatar.jpeg",
            avatar_status=PageState.avatar_status,
            github_url=site_const.GITHUB_URL,
            linkedin_url=site_const.LINKEDIN_URL,
            email_url="mailto:deivisaherreraj@gmail.com",
        ),
        rx.cond(
            details,
            rx.vstack(
                rx.flex(
                    rx.spacer(),
                    rx.spacer(),
                    info_text(f"{experience()}+", "años de experiencia"),
                    rx.spacer(),
                    info_text("100+", "aplicaciones creadas"),
                    rx.spacer(),
                    rx.spacer(),
                    width="100%",
                    text_align="center",
                ),
                rx.cond(
                    PageState.live_status.live,
                    link_button(
                        href=site_const.TWITCH_URL,
                        title="En directo",
                        description=PageState.live_status.title,
                        icon="fa-brands fa-twitch",
                        icon_color=Color.PURPLE.value,
                        border_color=Color.PURPLE.value,
                        animated=True,
                    ),
                    rx.box(
                        rx.cond(
                            PageState.next_live,
                            link_button(
                                href=site_const.TWITCH_URL,
                                title="Próximo directo",
                                description=PageState.next_live,
                                icon="fa-brands fa-twitch",
                                icon_color=Color.PURPLE.value,
                                border_color=Color.PURPLE.value,
                                animated=True,
                            ),
                        ),
                        width="100%",
                        on_mount=PageState.check_schedule,
                    ),
                ),
                # Introduction a mi Bio
                rx.el.Section.create(
                    rx.text(
                        """
                        ¡Hola! 👋, Soy Deivis Herrera, Desarrollador Full-Stack con experiencia en crear
                        soluciones de altos impacto, ofreciendo un desarrollo de software confiable y
                        eficiente, tanto del lado del
                        """,
                        rx.text.strong("Back-End 💻", color=Color.WHITE.value),
                        " como del ",
                        rx.text.strong("Front-End 🌐", color=Color.WHITE.value),
                        """
                        . Estoy siempre listo para explorar nuevas ideas y hacer realidad proyectos emocionantes. Aquí
                        encontrarás mis trabajos, contacto y perfiles profesionales 🔗. 🚀¡Gracias por tu
                        visita y bienvenido a mi mundo digital!
                        """,
                        as_="p",
                        font_size=FontSize.MEDIUM.value,
                        color=Color.GRAY.value,
                    ),
                    padding_top=Padding.ZERO.value,
                    padding_bottom=Padding.ZERO.value,
                ),
                width="100%",
                margin_bottom=Margin.VERY_BIG.value,
            ),
        ),
        width="100%",
        spacing=Spacing.BIG.value,
        align_items="start",
        on_mount=[PageState.check_live, PageState.check_avatar_status],
    )


def experience() -> int:
    return datetime.date.today().year - 2013
