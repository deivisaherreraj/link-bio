import reflex as rx

import website_frontend.shared.browser as browser
import website_frontend.shared.meta as meta
from website_frontend.routes import Route
from website_frontend.views.system_page import error_page


@rx.page(
    route=Route.ERROR_GENERIC.value,
    title=meta.error_generic_title,
    description=meta.error_generic_description,
    image=meta.preview,
    meta=meta.error_generic_meta,
)
def error_generic() -> rx.Component:
    return rx.box(
        browser.lang(),
        error_page(
            status_label="Unexpected issue",
            title="Algo salió mal",
            message=(
                "Esta vista encontró un problema inesperado mientras cargaba. "
                "Probá una recuperación rápida o seguí navegando desde una ruta "
                "estable."
            ),
            primary_label="Intentar de nuevo",
            primary_href=Route.ERROR_GENERIC.value,
            secondary_label="Volver al inicio",
            secondary_href=Route.INDEX.value,
            recovery_title="Recuperación inmediata",
            recovery_body=(
                "Empezá por volver a intentar esta página. Si el error sigue, usá la "
                "portada para retomar la navegación sin fricción."
            ),
            note=(
                "Si el problema persiste, seguramente estoy corrigiendo una "
                "integración o desplegando un ajuste puntual."
            ),
        ),
    )
