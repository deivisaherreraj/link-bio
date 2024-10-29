import reflex as rx

config = rx.Config(
    app_name="website_frontend",
    cors_allowed_origins=[
        "http://localhost:3000",
        "https://dherrerajdev.vercel.app"
    ]
)