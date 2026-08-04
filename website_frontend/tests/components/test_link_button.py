from website_frontend.components.link_button import link_button


def test_link_button_disabled_state_removes_redirect() -> None:
    component = link_button(
        href="https://example.com",
        title="Example",
        description="Example description",
        icon="fa-solid fa-star",
        is_disabled=True,
    )

    rendered = str(component)

    assert 'disabled:true' in rendered
    assert '"pointerEvents"' in rendered
    assert 'ReflexEvent("_redirect"' not in rendered


def test_link_button_enabled_state_keeps_redirect() -> None:
    component = link_button(
        href="https://example.com",
        title="Example",
        description="Example description",
        icon="fa-solid fa-star",
    )

    rendered = str(component)

    assert 'ReflexEvent("_redirect"' in rendered
    assert 'https://example.com' in rendered


def test_link_button_placeholder_href_disables_navigation() -> None:
    component = link_button(
        href="#",
        title="Example",
        description="Example description",
        icon="fa-solid fa-star",
    )

    rendered = str(component)

    assert 'disabled:true' in rendered
    assert 'ReflexEvent("_redirect"' not in rendered
    assert (
        '"pointerEvents" : "none"' in rendered
        or '["pointerEvents"] : "none"' in rendered
    )
