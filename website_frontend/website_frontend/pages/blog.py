import reflex as rx

import website_frontend.shared.browser as browser
import website_frontend.shared.meta as meta
from website_frontend.routes import Route
from website_frontend.views.status_page import status_page


@rx.page(
    route=Route.BLOG.value,
    title=meta.blog_title,
    description=meta.blog_description,
    image=meta.preview,
    meta=meta.blog_meta,
)
def blog() -> rx.Component:
    return rx.box(
        browser.lang(),
        status_page(
            title="Blog próximamente",
            message=(
                "Estoy preparando artículos sobre desarrollo de software, "
                "arquitectura y lecciones prácticas de proyectos reales."
            ),
            icon="fa-solid fa-pen-ruler",
        ),
    )
