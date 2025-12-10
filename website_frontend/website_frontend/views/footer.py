import reflex as rx
import datetime

from website_frontend.styles.styles import Margin
from website_frontend.styles.colors import Color
from website_frontend.styles.fonts import FontSize, FontWeight


def footer() -> rx.Component:
    current_year = datetime.date.today().year

    return rx.el.Footer.create(
        rx.vstack(
            rx.box(
                rx.el.I.create(
                    class_name="fa-solid fa-code",
                ),
                font_size=FontSize.LARGE.value,
                color=Color.WHITE.value,
                margin_bottom=Margin.MEDIUM.value,
            ),
            rx.text(
                f"Copyright © 2023-{current_year} Deivis Andres Herrera Julio",
                color=Color.GRAY.value,
                font_size=FontSize.TINY.value,
                margin_bottom=Margin.SMALL.value,
                as_="p",
            ),
            # Slogan in Spanish
            rx.text(
                "INNOVACIÓN Y PASIÓN ♥ EN CADA LÍNEA DE CÓDIGO",
                color=Color.PRIMARY.value,
                font_weight=FontWeight.MEDIUM.value,
                font_size=FontSize.SMALL.value,
                as_="p",
            ),
            align="center",
        ),
        margin_top=Margin.BIG.value,
        margin_bottom=Margin.VERY_BIG.value,
        width="100%",
    )
