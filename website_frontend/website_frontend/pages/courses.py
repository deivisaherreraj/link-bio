import reflex as rx

import website_frontend.shared.browser as browser
import website_frontend.shared.meta as meta
import website_frontend.styles.styles as styles
from website_frontend.routes import Route
from website_frontend.styles.styles import Size
from website_frontend.views.courses_links import courses_links
from website_frontend.views.footer import footer
from website_frontend.views.header import header
from website_frontend.views.navbar import navbar


@rx.page(
    route=Route.COURSES.value,
    title=meta.courses_title,
    description=meta.courses_description,
    image=meta.preview,
    meta=meta.courses_meta,
)
def courses() -> rx.Component:
    return rx.box(
        browser.lang(),
        navbar(),
        rx.center(
            rx.vstack(
                header(details=False),
                courses_links(),
                # TODO Habilitar función solo cuando se tenga lo necesario
                # sponsors(),
                max_width=styles.MAX_WIDTH,
                width="100%",
                margin_y=Size.BIG.value,
                padding=Size.BIG.value,
            )
        ),
        footer(),
    )
