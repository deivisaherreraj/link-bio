import reflex as rx

import website_frontend.constants.site_constants as const
from website_frontend.components.link_sponsor import link_sponsor
from website_frontend.components.title import title
from website_frontend.styles.styles import Spacing


def sponsors() -> rx.Component:
    return rx.vstack(
        title("Colaboran"),
        rx.flex(
            link_sponsor("/elgato.png", const.ELGATO_URL, "Logotipo de Elgato"),
            link_sponsor("/mvp.png", const.MVP_URL, "Logotipo de Microsoft MVP"),
            link_sponsor(
                "/githubstar.png", const.GITHUB_STAR_URL, "Logotipo de GitHub Star"
            ),
            spacing=Spacing.BIG.value,
            flex_direction=["column", "row"],
        ),
        width="100%",
        align_items="start",
        spacing=Spacing.DEFAULT.value,
    )
