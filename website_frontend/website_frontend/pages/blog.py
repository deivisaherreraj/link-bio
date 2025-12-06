import reflex as rx
import website_frontend.utils as utils

from website_frontend.routes import Route
from website_frontend.styles.colors import TextColor


@rx.page(
    route=Route.BLOG.value,
    title=utils.blog_title,
    description=utils.blog_description,
    image=utils.preview,
    meta=utils.blog_meta,
)
def blog() -> rx.Component:
    return rx.box(
        utils.lang(),
        rx.text(
            "Página del blog - Próximamente",
            color=TextColor.BODY.value,
        ),
    )
