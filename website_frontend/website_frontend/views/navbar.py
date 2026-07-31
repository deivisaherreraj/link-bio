import reflex as rx

import website_frontend.styles.styles as styles
from website_frontend.routes import Route
from website_frontend.styles.colors import Color, TextColor
from website_frontend.styles.styles import Size


def navbar() -> rx.Component:
    return rx.hstack(
        rx.link(
            rx.box(
                rx.text("<", as_="span", color=TextColor.BODY.value),
                rx.text("deivisaherreraj.dev", as_="span", color=Color.PRIMARY.value),
                rx.text("/>", as_="span", color=TextColor.BODY.value),
                style=styles.navbar_title_style,
            ),
            href=Route.INDEX.value,
        ),
        position="sticky",
        bg=Color.CONTENT.value,
        padding_x=Size.BIG.value,
        padding_y=Size.DEFAULT.value,
        z_index="999",
        top="0",
    )
