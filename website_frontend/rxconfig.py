import os
import reflex as rx

config = rx.Config(
    app_name="website_frontend", # Nombre de la aplicación Reflex
    api_url=os.getenv("API_URL", "http://localhost:8000"), # URL de la API backend
    plugins=[
        rx.plugins.SitemapPlugin() # Habilita la generación automática de sitemaps
    ],
    tailwind=None, # Deshabilita Tailwind CSS
    show_built_with_reflex=False # Oculta el banner "Built with Reflex"
)