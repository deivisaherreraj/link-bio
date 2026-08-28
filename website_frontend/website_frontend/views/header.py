import datetime

import reflex as rx

import website_frontend.constants.site_constants as site_const
from website_frontend.components.info_text import info_text
from website_frontend.components.link_button import link_button
from website_frontend.state.page_state import PageState
from website_frontend.styles.colors import Color, TextColor
from website_frontend.styles.fonts import FontSize, FontWeight
from website_frontend.styles.styles import Margin, Spacing
from website_frontend.views.profile import profile


def _intro_paragraph() -> rx.Component:
    return rx.el.P.create(
        "¡Hola! 👋, Soy ",
        rx.el.Strong.create(PageState.profile_info.full_name, color=TextColor.HEADER.value),
        ", un ",
        rx.el.Strong.create("desarrollador Full-Stack", color=TextColor.HEADER.value),
        " enfocado en construir ",
        rx.el.Strong.create("software confiable, escalable y de alto impacto", color=TextColor.HEADER.value),
        ". Trabajo tanto del lado del ",
        rx.el.Strong.create("Back-End 💻", color=TextColor.HEADER.value),
        " como del ",
        rx.el.Strong.create("Front-End 🌐", color=TextColor.HEADER.value),
        ", y siempre estoy explorando nuevas ideas para convertirlas en productos reales. Acá vas a encontrar mis proyectos, contenido, formas de contacto y perfiles profesionales 🔗🚀 ¡Gracias por tu visita y bienvenido a mi mundo digital!",
        color=Color.GRAY.value,
        font_size=FontSize.MEDIUM.value,
        font_weight=FontWeight.NORMAL.value,
        line_height="1.8",
        text_align="justify",
        width="100%",
        max_width="760px",
    )


def header(details=True) -> rx.Component:
    return rx.vstack(
        # ProfileHeader
        profile(
            name=PageState.profile_info.full_name,
            handle=PageState.profile_info.handle,
            headline=PageState.profile_info.headline,
            tech_stack_summary=PageState.profile_info.tech_stack_summary,
            avatar_url=PageState.profile_info.avatar_url,
            avatar_status=PageState.avatar_status,
            github_url=PageState.github_url,
            linkedin_url=PageState.linkedin_url,
            email=PageState.profile_info.email,
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
                _intro_paragraph(),
                width="100%",
                margin_bottom=Margin.VERY_BIG.value,
                align="center",
            ),
        ),
        width="100%",
        spacing=Spacing.BIG.value,
        align_items="start",
        on_mount=[PageState.check_live, PageState.load_profile],
    )


def experience() -> int:
    return datetime.date.today().year - 2013
