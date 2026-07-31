import reflex as rx

from website_frontend.styles.colors import Color
from website_frontend.styles.fonts import FontSize, FontWeight


def info_text(title: str, subTitle: str) -> rx.Component:
    return rx.box(
        rx.text(
            title,
            as_="span",
            font_weight=FontWeight.BOLD.value,
            color=Color.PRIMARY.value,
        ),
        f" {subTitle}",
        font_size=FontSize.SMALL.value,
        color=Color.GRAY.value,
    )
