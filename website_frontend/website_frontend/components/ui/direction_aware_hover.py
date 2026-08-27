import reflex as rx

from website_frontend.styles.styles import Color, Padding


def direction_aware_hover(
    image_url: str | None,
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
            rx.cond(
                image_url != None,
                rx.image(
                    src=image_url,
                    alt="",
                    position="absolute",
                    inset="0",
                    width="100%",
                    height="100%",
                    object_fit="cover",
                    z_index="0",
                ),
            ),
            # Contenido animado (overlay)
            rx.flex(
                rx.box(
                    children,
                    position="relative",
                    z_index="10",
                    width="100%",
                    height="100%",
                ),
                position="absolute",
                inset="0",
                bg_color=Color.BG_BLACK_TRANSPARENT_STRONG.value,
                align_items="stretch",
                justify_content="flex-end",
                padding_y=Padding.DEFAULT.value,
                padding_x=Padding.DEFAULT.value,
                z_index="20",
                class_name=(
                    "backdrop-blur-sm overlay-hidden translate-y-3 group-hover:translate-y-0 group-hover:opacity-100 transition-all duration-300"
                ),
            ),
            position="relative",
            height="100%",
            width="100%",
            background=(
                "linear-gradient(135deg, rgba(99, 102, 241, 0.28) 0%, rgba(15, 23, 42, 0.92) 100%)"
            ),
        ),
        position="relative",
        overflow="hidden",
        width="100%",
        height="288px",
        border_color=Color.TRANSPARENT.value,
        padding=Padding.ZERO.value,
        cursor="pointer",
        class_name="group",
    )
