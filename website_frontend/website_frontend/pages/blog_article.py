import reflex as rx
import website_frontend.shared.browser as browser
import website_frontend.shared.meta as meta

from website_frontend.routes import Route
from website_frontend.styles.colors import TextColor


@rx.page(
    route=Route.BLOG_ARTICLE.value,
    title=meta.blog_article_title,
    description=meta.blog_article_description,
    image=meta.preview,
    meta=meta.blog_article_meta,
)
def blog_article() -> rx.Component:
    return rx.box(
        browser.lang(),
        rx.text(
            f"Artículo del blog - Próximamente: {rx.State.slug}",
            color=TextColor.BODY.value,
        ),
    )
