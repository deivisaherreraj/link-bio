import reflex as rx

from website_frontend.styles.styles import Size, Spacing
from website_frontend.styles.colors import Color, TextColor
from website_frontend.styles.fonts import FontSize, FontWeight

from website_frontend.components.avatar_with_status import avatar_with_status
from website_frontend.components.tech_badge import tech_badge

from website_frontend.model.AvatarStatus import AvatarStatus

from website_frontend.state.PageState import PageState


def profile(
    name: str,
    handle: str,
    tagline: str,
    tech_stack: str,
    avatar_url: str,
    avatar_status: AvatarStatus,
    github_url: str | None = None,
    linkedin_url: str | None = None,
    email_url: str | None = None,
) -> rx.Component:
    return rx.vstack(
        # Avatar con badge de disponibilidad
        avatar_with_status(
            avatar_url=avatar_url,
            name=name,
            status=avatar_status,
        ),
        # Nombre con posibilidad de gradiente (via CSS)
        rx.heading(
            name,
            color=Color.TRANSPARENT.value,
            font_weight=FontWeight.BOLD.value,
            font_size=FontSize.EXTRA_LARGE.value,
            margin_bottom=Size.VERY_SMALL.value,
            class_name="profile-name-gradient",
            as_="h1",
        ),
        # Handle
        rx.text(
            handle,
            color=Color.PRIMARY.value,
            font_weight=FontWeight.MEDIUM.value,
            margin_bottom=Size.SMALL.value,
        ),
        # Tagline
        rx.text(
            tagline,
            color=Color.WHITE.value,
            font_size=FontSize.MEDIUM.value,
            font_weight=FontWeight.MEDIUM.value,
            margin_bottom=Size.VERY_SMALL.value,
        ),
        # Tech stack description
        rx.text(
            tech_stack,
            color=Color.GRAY.value,
            font_size=FontSize.SMALL.value,
            margin_bottom=Size.DEFAULT.value,
            as_="p",
        ),
        # Tecnologías (badges)
        rx.flex(
            rx.foreach(PageState.technologies, tech_badge),
            gap="0.75rem",
            wrap="wrap",
            justify_content="center",
            spacing=Spacing.SMALL.value,
            margin_bottom=Size.DEFAULT.value,
        ),
        # Iconos sociales
        rx.hstack(
            rx.cond(
                github_url is not None,
                # Ajustar el componente generico para que pueda usarse aqui
                # link_icon("/icons/github.svg", const.GITHUB_URL, "GitHub"),
                rx.link(
                    rx.el.I.create(
                        class_name="fa-brands fa-github",
                        font_size=FontSize.EXTRA_LARGE.value,
                    ),
                    href=github_url,
                    is_external=True,
                    aria_label="GitHub",
                    color=TextColor.BODY.value,
                    _hover={"color": Color.PRIMARY.value},
                ),
            ),
            rx.cond(
                linkedin_url is not None,
                # Ajustar el componente generico para que pueda usarse aqui
                # link_icon("/icons/linkedin.svg", const.LINKEDIN_URL, "LinkedIn"),
                rx.link(
                    rx.el.I.create(
                        class_name="fa-brands fa-linkedin",
                        font_size=FontSize.EXTRA_LARGE.value,
                    ),
                    href=linkedin_url,
                    is_external=True,
                    aria_label="LinkedIn",
                    color=TextColor.BODY.value,
                    _hover={"color": Color.PRIMARY.value},
                ),
            ),
            rx.cond(
                email_url is not None,
                # Ajustar el componente generico para que pueda usarse aqui
                # link_icon("/icons/email.svg", const.EMAIL, "Email"),
                rx.link(
                    rx.el.I.create(
                        class_name="fa-regular fa-envelope",
                        font_size=FontSize.EXTRA_LARGE.value,
                    ),
                    href=email_url,
                    is_external=True,
                    aria_label="Email",
                    color=TextColor.BODY.value,
                    _hover={"color": Color.PRIMARY.value},
                ),
            ),
            justify="center",
            spacing=Spacing.LARGE.value,
        ),
        align_items="center",
        text_align="center",
        flex_direction="column",
        display="flex",
        width="100%",
        spacing=Spacing.ZERO.value,
        on_mount=PageState.init_technologies,
    )
