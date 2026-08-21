preview = "https://dherrerajdev.vercel.app/preview.png"

_meta = [
    {"name": "og:type", "content": "website"},
    {"name": "og:image", "content": preview},
    {"name": "twitter:card", "content": "summary_large_image"},
    {"name": "twitter:site", "content": "@dherrerajdev"},
]

index_title = "DHerreraJDev | Desarrollo de software Full-Stack"
index_description = (
    "Hola, mi nombre es Deivis Andres Herrera Julio. Soy ingeniero de "
    "software, desarrollador Full-Stack."
)
index_meta = [
    {"name": "og:title", "content": index_title},
    {"name": "og:description", "content": index_description},
    *_meta,
]

blog_title = "DHerreraJDev | Blog de desarrollo de software"
blog_description = (
    "Artículos, reflexiones y experiencias sobre desarrollo de software, "
    "arquitectura, buenas prácticas y más."
)
blog_meta = [
    {"name": "og:title", "content": blog_title},
    {"name": "og:description", "content": blog_description},
    *_meta,
]

blog_article_title = "DHerreraJDev | Artículo del blog"
blog_article_description = "Detalle de un artículo del blog de desarrollo de software."
blog_article_meta = [
    {"name": "og:title", "content": blog_article_title},
    {"name": "og:description", "content": blog_article_description},
    *_meta,
]

maintenance_title = "DHerreraJDev | Mantenimiento"
maintenance_description = (
    "El sitio se encuentra temporalmente en mantenimiento. "
    "Estoy trabajando para mejorar la experiencia."
)
maintenance_meta = [
    {"name": "og:title", "content": maintenance_title},
    {"name": "og:description", "content": maintenance_description},
    *_meta,
]

error_generic_title = "DHerreraJDev | Error inesperado"
error_generic_description = (
    "Ha ocurrido un error inesperado. Por favor intenta de nuevo más tarde."
)
error_generic_meta = [
    {"name": "og:title", "content": error_generic_title},
    {"name": "og:description", "content": error_generic_description},
    *_meta,
]

not_found_title = "DHerreraJDev | Página no encontrada"
not_found_description = "La página que buscas no existe o ha sido movida."
not_found_meta = [
    {"name": "og:title", "content": not_found_title},
    {"name": "og:description", "content": not_found_description},
    *_meta,
]
