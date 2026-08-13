import reflex as rx

from website_frontend.shared.urls import is_actionable_external_url
from website_frontend.styles.styles import Size


def link_icon(image: str, url: str, alt: str) -> rx.Component:
    is_actionable = is_actionable_external_url(url)
    href = url if is_actionable else "#"

    return rx.link(
        rx.image(src=image, width=Size.LARGE.value, height=Size.LARGE.value, alt=alt),
        href=href,
        is_external=is_actionable,
        pointer_events="auto" if is_actionable else "none",
        opacity="1" if is_actionable else "0.6",
    )
