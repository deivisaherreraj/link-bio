import reflex as rx

from website_frontend.styles.styles import Margin

from website_frontend.components.title import title


def section(head: str, *children: rx.Component) -> rx.Component:
    return rx.el.Section.create(
        title(head),
        *children,
        width="100%",
        margin_bottom=Margin.VERY_BIG.value,
    )
