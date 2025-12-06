import reflex as rx

from website_frontend.styles.styles import Padding
from website_frontend.styles.fonts import FontSize, FontWeight

from website_frontend.model.ProjectStatus import ProjectStatus


def status_badge(status_info: ProjectStatus) -> rx.Component:
    """
    Badge compacto para mostrar el estado del proyecto.
    Si status_info es None, no renderiza nada.
    """
    return rx.text(
        rx.icon(
            status_info.icon,
            size=12,
        ),
        rx.text(
            status_info.label,
        ),
        padding_y=Padding.SMALL.value,
        padding_x=Padding.MEDIUM.value,
        font_size=FontSize.TINY.value,
        font_weight=FontWeight.SEMI_BOLD.value,
        border_radius="0.375rem",
        white_space="nowrap",
        gap="0.25rem",
        flex_shrink=0,
        display="flex",
        align_items="center",
        class_name=f"{status_info.animation_class}",
        style={
            "color": status_info.color,
            "backgroundColor": status_info.bg_color,
        },
        as_="span",
    )
