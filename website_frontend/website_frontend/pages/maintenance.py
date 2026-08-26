import reflex as rx

import website_frontend.shared.browser as browser
import website_frontend.shared.meta as meta
from website_frontend.routes import Route
from website_frontend.views.system_page import maintenance_page


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
        maintenance_page(
            status_label="Maintenance mode",
            title="Mantenimiento en curso",
            message=(
                "Estoy ajustando contenido, cerrando detalles visuales y validando "
                "que cada cambio quede estable antes de volver a abrir el sitio "
                "completo."
            ),
            eta_title="Tiempo estimado",
            eta_value="15–30 minutos",
            eta_message=(
                "Si todo sigue como espero, esta ventana debería cerrarse pronto. "
                "Podés reintentar ahora o volver en un rato."
            ),
            primary_label="Reintentar ahora",
            primary_href=Route.MAINTENANCE.value,
            secondary_label="Volver al inicio",
            secondary_href=Route.INDEX.value,
            checklist_title="Mientras tanto podés",
            checklist_items=[
                "Revisar el blog disponible",
                "Esperar a que termine la publicación actual",
                "Volver más tarde para ver los cambios",
            ],
            note=(
                "La interrupción es temporal. Prefiero pausar esta parte del sitio un "
                "momento antes que publicar una experiencia a medias."
            ),
        ),
    )
