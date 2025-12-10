import reflex as rx
import website_frontend.styles.styles as styles

from website_frontend.styles.styles import Margin, Size, Padding
from website_frontend.styles.colors import Color, BackgroundColor
from website_frontend.styles.fonts import FontSize, FontWeight


def link_button(
    href: str,
    title: str,
    description: str,
    image: str | None = None,
    icon: str | None = None,
    icon_color: str | None = None,
    badge: str | None = None,
    badge_color: str = Color.PRIMARY.value,
    border_color: str | None = None,
    is_disabled=False,
    is_external=True,
    animated=False,
) -> rx.Component:
    class_name = ""

    # Animación opcional (animate.css)
    if animated:
        class_name = f"{class_name} {styles.BOUNCEIN_ANIMATION}"

    # Estilos inline (disabled, border, shadow)
    style: dict[str, str] = {}

    if is_disabled:
        style.update(
            {
                "pointerEvents": "none",
                "opacity": "0.6",
            }
        )

    # Estilo de borde y sombra cuando se fuerza un color
    if border_color is not None:
        style.update(
            {
                "borderColor": border_color,
                "border": f"2px solid {border_color}",
                "boxShadow": f"0 0 15px {Color.WHITE_TRANSPARENT.value}",
            }
        )

    return rx.button(
        rx.hstack(
            # Icon wrapper
            rx.box(
                rx.cond(
                    icon,
                    rx.el.I.create(
                        class_name=icon,
                        style={"color": icon_color} if icon_color else None,
                    ),
                    rx.image(
                        src=image,
                        width=Size.LARGE.value,
                        height=Size.LARGE.value,
                        margin=Size.MEDIUM.value,
                        alt=title,
                    ),
                ),
                font_size=FontSize.DEFAULT.value,
                color=Color.WHITE.value,
                width="32px",
                height="32px",
                min_width="32px",
                display="flex",
                align_items="center",
                justify_content="center",
                flex_shrink=0,
                margin_right=Margin.LARGE.value,
                border_radius="8px",
                background_color=BackgroundColor.LIGHT.value,
            ),
            # Texto
            rx.box(
                rx.hstack(
                    # Título
                    rx.text(
                        title,
                        color=Color.WHITE.value,
                        font_weight=FontWeight.MEDIUM.value,
                        font_size=FontSize.MEDIUM.value,
                        as_="span",
                    ),
                    # Badge (si aplica)
                    rx.cond(
                        badge,
                        rx.text(
                            badge,
                            font_size=FontSize.TINY.value,
                            font_weight=FontWeight.MEDIUM.value,
                            color=Color.WHITE.value,
                            padding=f"{Padding.VERY_SMALL.value} {Padding.MEDIUM.value}",
                            border_radius="6px",
                            line_height="1",
                            style={"backgroundColor": badge_color}
                            if badge_color
                            else None,
                            as_="span",
                        ),
                    ),
                    display="flex",
                    align_items="center",
                    gap="8px",
                    margin_bottom=Margin.SMALL.value,
                ),
                rx.text(
                    description,
                    font_size=FontSize.TINY.value,
                    color=Color.GRAY.value,
                    as_="span",
                ),
                flex_grow=1,
                flex_shrink=1,
                flex_basis="0%",
                display="flex",
                flex_direction="column",
                text_align="left",
            ),
            align="center",
            width="100%",
        ),
        disabled=is_disabled,
        class_name=class_name,
        style=style,
        on_click=rx.redirect(path=href, is_external=is_external),
    )
