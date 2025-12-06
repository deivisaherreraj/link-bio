import reflex as rx
import pytz

from datetime import datetime, timedelta


# Común
def lang() -> rx.Component:
    return rx.script("document.documentElement.lang='es'")


preview = "https://dherrerajdev.vercel.app/preview.png"

_meta = [
    {"name": "og:type", "content": "website"},
    {"name": "og:image", "content": preview},
    {"name": "twitter:card", "content": "summary_large_image"},
    {"name": "twitter:site", "content": "@dherrerajdev"},
]

# Index
index_title = "DHerreraJDev | Desarrollo de software Full-Stack"
index_description = "Hola, mi nombre es Deivis Andres Herrera Julio. Soy ingeniero de software, desarrollador Full-Stack."

index_meta = [
    {"name": "og:title", "content": index_title},
    {"name": "og:description", "content": index_description},
]
index_meta.extend(_meta)

# Guías/Tutoriales
courses_title = "DHerreraJDev | Guías/Tutoriales gratis de programación"
courses_description = "Este es un listado con algunas guías y tutoriales para aprender programación y desarrollo de software."

courses_meta = [
    {"name": "og:title", "content": courses_title},
    {"name": "og:description", "content": courses_description},
]
courses_meta.extend(_meta)

# Blog (listado)
blog_title = "DHerreraJDev | Blog de desarrollo de software"
blog_description = (
    "Artículos, reflexiones y experiencias sobre desarrollo de software, "
    "arquitectura, buenas prácticas y más."
)

blog_meta = [
    {"name": "og:title", "content": blog_title},
    {"name": "og:description", "content": blog_description},
]
blog_meta.extend(_meta)

# Blog (artículo)
blog_article_title = "DHerreraJDev | Artículo del blog"
blog_article_description = "Detalle de un artículo del blog de desarrollo de software."

blog_article_meta = [
    {"name": "og:title", "content": blog_article_title},
    {"name": "og:description", "content": blog_article_description},
]
blog_article_meta.extend(_meta)

# Mantenimiento
maintenance_title = "DHerreraJDev | Mantenimiento"
maintenance_description = (
    "El sitio se encuentra temporalmente en mantenimiento. "
    "Estoy trabajando para mejorar la experiencia."
)

maintenance_meta = [
    {"name": "og:title", "content": maintenance_title},
    {"name": "og:description", "content": maintenance_description},
]
maintenance_meta.extend(_meta)

# Error genérico
error_generic_title = "DHerreraJDev | Error inesperado"
error_generic_description = (
    "Ha ocurrido un error inesperado. Por favor intenta de nuevo más tarde."
)

error_generic_meta = [
    {"name": "og:title", "content": error_generic_title},
    {"name": "og:description", "content": error_generic_description},
]
error_generic_meta.extend(_meta)

# Página no encontrada (404)
not_found_title = "DHerreraJDev | Página no encontrada"
not_found_description = "La página que buscas no existe o ha sido movida."

not_found_meta = [
    {"name": "og:title", "content": not_found_title},
    {"name": "og:description", "content": not_found_description},
]
not_found_meta.extend(_meta)

# Date
LOCAL_TIMEZONE_SCRIPT = "Intl.DateTimeFormat().resolvedOptions().timeZone"

WEEKDAYS = {
    0: "Lunes",
    1: "Martes",
    2: "Miércoles",
    3: "Jueves",
    4: "Viernes",
    5: "Sábado",
    6: "Domingo",
}

MONTHS = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre",
}


def next_date(dates: dict, timezone: str) -> str:
    if len(dates) == 0:
        return ""

    tz = pytz.timezone(timezone)
    now = datetime.now(tz)
    current_time = now.timetz()

    for weekday in range(7):
        current_weekday = str((now.weekday() + weekday) % 7)

        if current_weekday not in dates or dates[current_weekday] == "":
            continue

        time_utc = (
            datetime.strptime(dates[current_weekday], "%H:%M")
            .replace(tzinfo=pytz.UTC)
            .timetz()
        )
        next_time = datetime.combine(now.date(), time_utc).astimezone(tz).timetz()

        if current_time < next_time or weekday > 0:
            next_date = now + timedelta(days=weekday)

            local_date = datetime(
                next_date.year,
                next_date.month,
                next_date.day,
                time_utc.hour,
                time_utc.minute,
                tzinfo=pytz.UTC,
            ).astimezone(tz)

            day = "Hoy" if weekday == 0 else WEEKDAYS[local_date.weekday()]
            zones = timezone.replace("_", " ").split("/")

            return local_date.strftime(
                f"{day}, %d de {MONTHS[local_date.month]} a las %H:%M | Zona horaria: {zones[len(zones) - 1]}"
            )

    return ""
