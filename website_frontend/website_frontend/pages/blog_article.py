import reflex as rx
import website_frontend.utils as utils

from website_frontend.routes import Route
from website_frontend.styles.colors import TextColor


@rx.page(
    route=Route.BLOG_ARTICLE.value,
    title=utils.blog_article_title,
    description=utils.blog_article_description,
    image=utils.preview,
    meta=utils.blog_article_meta,
)
def blog_article() -> rx.Component:
    return rx.box(
        utils.lang(),
        rx.text(
            f"Artículo del blog - Próximamente: {rx.State.slug}",
            color=TextColor.BODY.value,
        ),
    )
