import reflex as rx

import website_frontend.styles.styles as styles
from website_frontend.routes import Route
from website_frontend.styles.colors import (
    BackgroundColor,
    BorderColor,
    Color,
    TextColor,
)
from website_frontend.styles.fonts import FontSize
from website_frontend.styles.styles import Margin, Padding, Radius, Size, Spacing
from website_frontend.views.footer import footer
from website_frontend.views.navbar import navbar


def status_page(
    title: str,
    message: str,
    icon: str = "fa-solid fa-clock",
) -> rx.Component:
    return rx.box(
        navbar(),
        rx.center(
            rx.vstack(
                rx.box(
                    rx.el.I.create(class_name=icon),
                    font_size=Size.VERY_LARGE.value,
                    color=Color.PRIMARY.value,
                    width="72px",
                    height="72px",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    border_radius=Radius.FULL.value,
                    background_color=BackgroundColor.LIGHT.value,
                    border=f"1px solid {BorderColor.WHITE_TRANSPARENT_LIGHT.value}",
                ),
                rx.vstack(
                    rx.heading(title, as_="h1", font_size=FontSize.TITLE.value),
                    rx.text(
                        message,
                        color=TextColor.BODY.value,
                        font_size=FontSize.DEFAULT.value,
                        text_align="center",
                    ),
                    spacing=Spacing.SMALL.value,
                    align="center",
                    width="100%",
                ),
                rx.link(
                    rx.button(
                        "Volver al inicio",
                        width="auto",
                        justify_content="center",
                        padding_x=Padding.BIG.value,
                    ),
                    href=Route.INDEX.value,
                ),
                width="100%",
                max_width=styles.MAX_WIDTH,
                min_height="calc(100vh - 220px)",
                justify="center",
                align="center",
                spacing=Spacing.BIG.value,
                padding=Size.BIG.value,
                margin_y=Margin.BIG.value,
            )
        ),
        footer(),
    )
