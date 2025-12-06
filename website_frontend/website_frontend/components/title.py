import reflex as rx
import website_frontend.styles.styles as styles


def title(text: str) -> rx.Component:
    return rx.heading(text, as_="h2", style=styles.title_style)
