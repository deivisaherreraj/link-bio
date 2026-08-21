import reflex as rx

import website_frontend.shared.browser as browser
import website_frontend.shared.meta as meta
from website_frontend.routes import Route
from website_frontend.views.status_page import status_page


@rx.page(
    route=Route.MAINTENANCE.value,
    title=meta.maintenance_title,
    description=meta.maintenance_description,
    image=meta.preview,
    meta=meta.maintenance_meta,
)
def maintenance() -> rx.Component:
    return rx.box(
        browser.lang(),
        status_page(
            title="Mantenimiento en curso",
            message=(
                "El sitio está temporalmente no disponible mientras termino de "
                "publicar algunas mejoras."
            ),
            icon="fa-solid fa-screwdriver-wrench",
        ),
    )
