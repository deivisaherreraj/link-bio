from website_frontend.components.link_button import link_button


def test_link_button_without_icon_or_image_skips_empty_visual_wrapper() -> None:
    component = link_button(
        href="https://example.com",
        title="Example",
        description="Example description",
        icon=None,
        image=None,
    )

    rendered = str(component)

    assert 'false?(jsx(Fragment,{},jsx(RadixThemesBox' in rendered
    assert "Example description" in rendered


def test_link_button_with_image_renders_image_fallback() -> None:
    component = link_button(
        href="https://example.com",
        title="Example",
        description="Example description",
        image="/icons/example.svg",
        icon=None,
    )

    rendered = str(component)

    assert 'src:"/icons/example.svg"' in rendered
