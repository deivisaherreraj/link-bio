import reflex as rx
import website_frontend.constants.site_constants as const

from website_frontend.components.link_button import link_button
from website_frontend.components.title import title
from website_frontend.styles.styles import Color, Spacing


def courses_links() -> rx.Component:
    return rx.vstack(
        title("Tutoriales gratis"),
        link_button(
            "C# desde cero",
            "Tutorial de +37h: Fundamentos, backend, testing...",
            "/icons/csharp.svg",
            const.CSHARP_COURSE_URL,
            True,
            False,
            Color.SECONDARY.value,
        ),
        title("Mucho más en"),
        link_button(
            "Twitch",
            "Transmisiones sobre programación de lunes a viernes",
            "/icons/twitch.svg",
            const.TWITCH_URL,
            True,
        ),
        link_button(
            "YouTube",
            "Tutoriales sobre desarrollo de software semanales",
            "/icons/youtube.svg",
            const.YOUTUBE_URL,
            True,
        ),
        width="100%",
        spacing=Spacing.DEFAULT.value,
    )
