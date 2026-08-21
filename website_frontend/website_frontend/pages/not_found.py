import reflex as rx

import website_frontend.shared.browser as browser
import website_frontend.shared.meta as meta
from website_frontend.routes import Route
from website_frontend.views.status_page import status_page


@rx.page(
    route=Route.NOT_FOUND.value,
    title=meta.not_found_title,
    description=meta.not_found_description,
    image=meta.preview,
    meta=meta.not_found_meta,
)
def not_found() -> rx.Component:
    return rx.box(
        browser.lang(),
        status_page(
            title="Página no encontrada",
            message="La página que buscas no existe o puede haber sido movida.",
            icon="fa-solid fa-compass-drafting",
        ),
    )
