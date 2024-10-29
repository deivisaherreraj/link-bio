import reflex as rx
import datetime
import website_frontend.constants as const

from website_frontend.styles.styles import Size, Spacing, Logo
from website_frontend.styles.colors import Color, TextColor
from website_frontend.components.float_button import float_button

def footer() -> rx.Component:
    return rx.vstack(
        rx.image(
            src="/logo.png",
            height=Logo.HEIGHT.value,
            width=Logo.WIDTH.value,
            alt="Logotipo de DHerreraJDev. Una doble > &quot;de&quot; _."
        ),
        rx.link(
            rx.box(
                f"Copyright © 2023-{datetime.date.today().year} ",
                rx.text(
                    "DHerreraJDev by Deivis Andres Herrera Julio", 
                    as_="span", 
                    color=Color.PRIMARY.value
                ),
                " v1.",
                padding_top=Size.DEFAULT.value,
                color=TextColor.BODY.value
            ),
            href=const.DHERRERAJDEV_URL,
            is_external=True,
            font_size=Size.MEDIUM.value
        ),
        rx.link(
            rx.hstack(
                rx.image(
                    src="/icons/github.svg",
                    height=Size.LARGE.value,
                    width=Size.LARGE.value,
                    alt="Logo GitHub"
                ),
                rx.text(
                    "CONSTRUYENDO SOFTWARE CON ♥ DESDE COLOMBIA PARA EL MUNDO.",
                    font_size=Size.MEDIUM.value,
                    margin_top=Size.ZERO.value,
                    color=TextColor.BODY.value
                ),
            ),
            href=const.REPO_URL,
            is_external=True
        ),
        float_button(
            # icon=rx.image(src="/icons/donate.svg"),            
            href=const.COFFEE_URL,
            tooltip="Invítame a un café"
        ),
        align="center",
        margin_bottom=Size.BIG.value,
        padding_bottom=Size.VERY_BIG.value,
        padding_x=Size.BIG.value,
        spacing=Spacing.ZERO.value,
        color=TextColor.FOOTER.value
    )