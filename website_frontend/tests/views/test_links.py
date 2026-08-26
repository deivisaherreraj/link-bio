import inspect

from website_frontend.model.social_link import SocialLink
from website_frontend.views.links import links, render_social_link


def test_render_social_link_uses_model_contract_fields() -> None:
    component = render_social_link(
        SocialLink(
            label="Email",
            url="mailto:test@example.com",
            icon="fa-solid fa-envelope",
            section="contact",
            priority=1,
            is_active=True,
            is_external=False,
            description="Direct contact",
            badge="Correo",
            border_color="#123456",
        )
    )

    rendered = str(component)

    assert 'mailto:test@example.com' in rendered
    assert 'Direct contact' in rendered
    assert 'fa-solid fa-envelope' in rendered
    assert '2px solid #123456' in rendered
    assert '"padding" : "12px"' in rendered or '["padding"] : "12px"' in rendered
    assert 'target:(false ? "_blank" : "")' in rendered


def test_render_social_link_visually_separates_disabled_cards() -> None:
    component = render_social_link(
        SocialLink(
            label="Próximamente",
            url="https://example.com/soon",
            icon="fa-solid fa-hourglass-half",
            section="resources",
            priority=99,
            is_active=False,
            is_external=True,
            description="Aún no disponible.",
        )
    )

    rendered = str(component)

    assert '(false ? "1" : "0.42")' in rendered
    assert 'saturate(0.65)' in rendered
    assert 'linear-gradient(180deg, #0b1016 0%, #090d12 100%)' in rendered


def test_links_view_loads_featured_and_social_link_state_on_mount() -> None:
    rendered = inspect.getsource(links)

    assert "featured_links" in rendered
    assert "load_social_links" in rendered
