import reflex as rx

from typing import Callable

from website_frontend.model.Featured import Featured


def _animation_style(direction: str, speed: str) -> dict:
    animation_direction = "forwards" if direction == "left" else "reverse"

    if speed == "fast":
        duration = "20s"
    elif speed == "normal":
        duration = "40s"
    else:
        duration = "80s"

    return {
        "--animation-direction": animation_direction,
        "--animation-duration": duration,
    }


def auto_scrolling_carousel(
    reactive_list: list[Featured],
    render_function: Callable[[Featured], rx.Component],
    direction: str = "left",
    speed: str = "normal",
) -> rx.Component:
    """
    Versión Reflex de InfiniteMovingCards:
    - Recibe una lista reactiva (p.ej. PageState.featured_info).
    - render_function: función que recibe un elemento y devuelve un componente.
    - Duplica la lista para lograr efecto de scroll infinito.
    - Usa clases CSS `scroller` y `animate-scroll` como en Magic Patterns.
    """
    return rx.box(
        # Lista desplazable
        rx.list(
            # Primera copia de la lista
            rx.foreach(
                reactive_list, lambda featured: rx.list.item(render_function(featured))
            ),
            # Segunda copia de la lista (para loop infinito)
            rx.foreach(
                reactive_list, lambda featured: rx.list.item(render_function(featured))
            ),
            display="flex",
            min_width="100%",
            width="max-content",
            flex_wrap="nowrap",
            flex_shrink="0",
            gap="1rem",
            class_name="animate-scroll",
        ),
        position="relative",
        z_index="20",
        width="100%",
        overflow="hidden",
        class_name="scroller",
        style=_animation_style(direction, speed),
    )
