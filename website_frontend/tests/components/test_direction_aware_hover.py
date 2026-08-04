import reflex as rx

from website_frontend.components.ui.direction_aware_hover import direction_aware_hover


def test_direction_aware_hover_uses_decorative_background_alt() -> None:
    component = direction_aware_hover(
        image_url="/images/example.png",
        children=rx.text("Contenido"),
    )

    rendered = str(component)

    assert 'alt:""' in rendered
    assert 'alt:"Background"' not in rendered
    assert '/images/example.png' in rendered
