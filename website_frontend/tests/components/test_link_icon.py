from website_frontend.components.link_icon import link_icon


def test_link_icon_disables_invalid_external_urls() -> None:
    component = link_icon("/github.svg", "not-a-url", "GitHub")

    rendered = str(component)

    assert 'to:"not-a-url"' not in rendered
    assert 'to:"#"' in rendered
    assert 'target:(false ? "_blank" : "")' in rendered
    assert '["pointerEvents"] : "none"' in rendered


def test_link_icon_keeps_external_behavior_for_real_urls() -> None:
    component = link_icon("/github.svg", "https://github.com/example", "GitHub")

    rendered = str(component)

    assert 'to:"https://github.com/example"' in rendered
    assert 'target:(true ? "_blank" : "")' in rendered
    assert '"pointerEvents" : "none"' not in rendered
