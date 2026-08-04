import reflex as rx

from website_frontend.styles.styles import Size


def link_sponsor(imagen: str, url: str, alt: str) -> rx.Component:
    is_placeholder = url.strip() == "/"

    return rx.link(
        rx.image(
            src=imagen, height=Size.VERY_LARGE.value, aspect_ratio="5 / 2", alt=alt
        ),
        href=url,
        is_external=not is_placeholder,
        pointer_events="none" if is_placeholder else "auto",
        opacity="0.6" if is_placeholder else "1",
    )
