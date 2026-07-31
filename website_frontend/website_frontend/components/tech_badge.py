import reflex as rx

from website_frontend.model.tech_badge import TechBadge
from website_frontend.styles.colors import Color
from website_frontend.styles.fonts import FontWeight
from website_frontend.styles.styles import Spacing


def tech_badge(technologie: TechBadge) -> rx.Component:
    """
    Componente de badge tecnológico.
    """
    return rx.hstack(
        rx.el.I.create(class_name=technologie.icon_class),
        rx.text(technologie.name),
        padding_x="0.75rem",
        padding_y="0.375rem",
        font_size="0.75rem",
        font_weight=FontWeight.MEDIUM.value,
        border_radius="0.375rem",
        border_width="2px",
        border_style="solid",
        style={
            "color": technologie.color,
            "borderColor": technologie.color,
            "backgroundColor": Color.TRANSPARENT.value,
        },
        align_items="center",
        spacing=Spacing.VERY_SMALL.value,
    )
