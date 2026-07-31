import reflex as rx

import website_frontend.shared.browser as browser
import website_frontend.shared.meta as meta
import website_frontend.styles.styles as styles
from website_frontend.routes import Route
from website_frontend.styles.styles import Margin
from website_frontend.views.footer import footer
from website_frontend.views.header import header
from website_frontend.views.links import links
from website_frontend.views.navbar import navbar


@rx.page(
    route=Route.INDEX.value,
    title=meta.index_title,
    description=meta.index_description,
    image=meta.preview,
    meta=meta.index_meta,
)
def index() -> rx.Component:
    return rx.box(
        browser.lang(),
        navbar(),
        rx.center(
            rx.vstack(
                header(),
                links(),
                max_width=styles.MAX_WIDTH,
                width="100%",
                margin_y=Margin.BIG.value,
            )
        ),
        footer(),
    )
