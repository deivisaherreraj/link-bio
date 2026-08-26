import reflex as rx

import website_frontend.shared.browser as browser
import website_frontend.shared.meta as meta
from website_frontend.routes import Route
from website_frontend.views.system_page import system_page


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
        system_page(
            status_label="404 · Lost route",
            title="Página no encontrada",
            message=(
                "La ruta que buscás no existe, cambió de lugar o el enlace llegó "
                "incompleto."
            ),
            icon="fa-solid fa-compass-drafting",
            primary_label="Ir al inicio",
            primary_href=Route.INDEX.value,
            secondary_label="Explorar el blog",
            secondary_href=Route.BLOG.value,
            detail_title="Cómo volver a ubicarse",
            detail_body=(
                "Podés retomar desde la portada, explorar el blog o revisar si el "
                "enlace original tenía un error de copia."
            ),
            checklist_title="Atajos útiles",
            checklist_items=[
                "Abrir la portada",
                "Entrar al blog",
                "Comprobar la URL manualmente",
            ],
            note=(
                "Si llegaste desde un enlace interno, seguramente estoy reorganizando "
                "contenido y esa dirección quedó desactualizada."
            ),
        ),
    )
