import reflex as rx
import datetime
import website_frontend.constants.site_constants as const

from website_frontend.styles.styles import Size, Spacing, Logo
from website_frontend.styles.colors import Color, TextColor


def footer() -> rx.Component:
    return rx.vstack(
        rx.image(
            src="/logo.png",
            height=Logo.HEIGHT.value,
            width=Logo.WIDTH.value,
            alt="Logotipo de DHerreraJDev. Una doble > &quot;de&quot; _.",
        ),
        rx.link(
            rx.box(
                f"Copyright © 2023-{datetime.date.today().year} ",
                rx.text(
                    "DherrerajDev by Deivis Andres Herrera Julio",
                    as_="span",
                    color=Color.PRIMARY.value,
                ),
                padding_top=Size.DEFAULT.value,
                color=TextColor.BODY.value,
            ),
            href=const.DHERRERAJDEV_URL,
            is_external=True,
            font_size=Size.MEDIUM.value,
        ),
        rx.link(
            rx.hstack(
                rx.image(
                    src="/icons/github.svg",
                    height=Size.LARGE.value,
                    width=Size.LARGE.value,
                    alt="Logo GitHub",
                ),
                rx.text(
                    "INNOVACIÓN Y PASIÓN ♥ EN CADA LÍNEA DE CÓDIGO",
                    font_size=Size.MEDIUM.value,
                    margin_top=Size.ZERO.value,
                    color=TextColor.BODY.value,
                ),
            ),
            href=const.REPO_URL,
            is_external=True,
        ),
        align="center",
        margin_bottom=Size.BIG.value,
        padding_bottom=Size.VERY_BIG.value,
        padding_x=Size.BIG.value,
        spacing=Spacing.ZERO.value,
        color=TextColor.FOOTER.value,
    )
