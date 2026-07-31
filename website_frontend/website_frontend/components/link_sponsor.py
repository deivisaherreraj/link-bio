import reflex as rx

from website_frontend.styles.styles import Size


def link_sponsor(imagen: str, url: str, alt: str) -> rx.Component:
    return rx.link(
        rx.image(
            src=imagen, height=Size.VERY_LARGE.value, aspect_ratio="5 / 2", alt=alt
        ),
        href=url,
        is_external=True,
    )
