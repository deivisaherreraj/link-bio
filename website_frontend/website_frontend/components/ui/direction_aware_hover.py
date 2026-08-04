import reflex as rx

from website_frontend.styles.styles import Color, Padding


def direction_aware_hover(
    image_url: str,
    children: rx.Component,
) -> rx.Component:
    """
    Versión simplificada de DirectionAwareHover:
    - Mantiene overlay oscuro + blur.
    - Aplica transición suave en hover.
    - NO calcula la dirección exacta de entrada del mouse (limitación sin JS).
    """
    return rx.card(
        # Contenedor principal
        rx.box(
            # Overlay de fondo que aparece en hover
            rx.box(
                display="none",
                position="absolute",
                inset="0",
                width="100%",
                height="100%",
                z_index="10",
                bg_color=Color.BG_BLACK_TRANSPARENT.value,
                class_name="group-hover:block transition duration-500",
            ),
            # Imagen de fondo
            rx.image(
                src=image_url,
                alt="",
                position="absolute",
                inset="0",
                width="100%",
                height="100%",
                object_fit="cover",
            ),
            # Contenido animado (overlay)
            rx.flex(
                rx.box(
                    children,
                    position="relative",
                    z_index="10",
                ),
                position="absolute",
                inset="0",
                bg_color=Color.BG_BLACK_TRANSPARENT_STRONG.value,
                align_items="flex-end",
                justify_content="flex-start",
                padding_y=Padding.DEFAULT.value,
                padding_x=Padding.DEFAULT.value,
                class_name=("backdrop-blur-sm overlay-hidden hover-flip-in-y"),
            ),
            position="relative",
            height="100%",
            width="100%",
        ),
        position="relative",
        overflow="hidden",
        width="100%",
        height="270px",
        border_color=Color.TRANSPARENT.value,
        padding=Padding.ZERO.value,
        cursor="pointer",
        class_name="group",
    )
