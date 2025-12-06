import reflex as rx
import website_frontend.styles.styles as styles

from website_frontend.styles.styles import Size, Spacing


def link_button(
    title: str,
    subTitle: str,
    image: str,
    url: str,
    is_disabled=False,
    is_external=True,
    highlight_color=None,
    animated=False,
) -> rx.Component:
    return rx.button(
        rx.hstack(
            rx.image(
                src=image,
                width=Size.LARGE.value,
                height=Size.LARGE.value,
                margin=Size.MEDIUM.value,
                alt=title,
            ),
            rx.vstack(
                rx.text(
                    title, size=Spacing.SMALL.value, style=styles.button_title_style
                ),
                rx.text(
                    subTitle,
                    size=Spacing.VERY_SMALL.value,
                    style=styles.button_body_style,
                ),
                align_items="start",
                spacing=Spacing.VERY_SMALL.value,
                padding_y=Size.SMALL.value,
                padding_right=Size.SMALL.value,
            ),
            align="center",
            width="100%",
        ),
        disabled=is_disabled,
        border=f"{'2px' if highlight_color is not None else '0px'} solid {highlight_color}",
        class_name=styles.BOUNCEIN_ANIMATION if animated else None,
        on_click=rx.redirect(path=url, is_external=is_external),
    )
