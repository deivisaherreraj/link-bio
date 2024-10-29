import reflex as rx
import website_frontend.utils as utils
import website_frontend.styles.styles as styles

from website_frontend.routes import Route
from website_frontend.views.navbar import navbar
from website_frontend.views.header import header
from website_frontend.views.courses_links import courses_links
from website_frontend.views.sponsors import sponsors
from website_frontend.views.footer import footer
from website_frontend.styles.styles import Size

@rx.page(
    route=Route.COURSES.value,
    title=utils.courses_title,
    description=utils.courses_description,
    image=utils.preview,
    meta=utils.courses_meta
)
def courses() -> rx.Component:
    return rx.box(
        utils.lang(),
        navbar(),
        rx.center(
            rx.vstack(
                header(
                    details=False
                ),
                courses_links(),
                # TODO Habilitar función solo cuando se tenga lo necesario
                # sponsors(),
                max_width=styles.MAX_WIDTH,
                width="100%",
                margin_y=Size.BIG.value,
                padding=Size.BIG.value
            )
        ),
        footer()
    )