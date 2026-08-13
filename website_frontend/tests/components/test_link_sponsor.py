from website_frontend.components.link_sponsor import link_sponsor


def test_link_sponsor_disables_placeholder_links() -> None:
    component = link_sponsor("/elgato.png", "/", "Logotipo de Elgato")

    rendered = str(component)

    assert 'to:"/"' not in rendered
    assert 'to:"#"' in rendered
    assert 'target:(false ? "_blank" : "")' in rendered
    assert '["pointerEvents"] : "none"' in rendered
    assert '["opacity"] : "0.6"' in rendered


def test_link_sponsor_disables_invalid_external_links() -> None:
    component = link_sponsor("/elgato.png", "not-a-url", "Logotipo de Elgato")

    rendered = str(component)

    assert 'to:"not-a-url"' not in rendered
    assert 'to:"#"' in rendered
    assert 'target:(false ? "_blank" : "")' in rendered
    assert '["pointerEvents"] : "none"' in rendered


def test_link_sponsor_keeps_external_behavior_for_real_urls() -> None:
    component = link_sponsor(
        "/elgato.png",
        "https://example.com",
        "Logotipo de Elgato",
    )

    rendered = str(component)

    assert 'to:"https://example.com"' in rendered
    assert 'target:(true ? "_blank" : "")' in rendered
    assert '"pointerEvents" : "none"' not in rendered
