import reflex as rx

from website_frontend.components.title import title
from website_frontend.styles.styles import Margin, Spacing


def section(head: str, *children: rx.Component) -> rx.Component:
    return rx.el.Section.create(
        rx.vstack(
            title(head),
            *children,
            width="100%",
            spacing=Spacing.EXTRA_SMALL.value,
            align="stretch",
        ),
        width="100%",
        margin_bottom=Margin.ZERO.value,
    )
