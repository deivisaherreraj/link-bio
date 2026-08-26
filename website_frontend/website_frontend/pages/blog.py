import reflex as rx

import website_frontend.shared.browser as browser
import website_frontend.shared.meta as meta
from website_frontend.routes import Route
from website_frontend.views.blog import blog_index_view


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
        blog_index_view(),
    )
