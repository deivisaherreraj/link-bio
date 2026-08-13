from website_frontend.components.link_featured import link_featured
from website_frontend.model.featured import Featured
from website_frontend.model.project_status import ProjectStatus


def _build_featured(**overrides: object) -> Featured:
    base = {
        "href": "https://example.com/project",
        "image_url": "https://example.com/project.png",
        "title": "Example Project",
        "description": "Example description",
        "technologies": ["Python", "Reflex"],
        "github_url": "https://github.com/example/project",
        "live_url": "https://example.com/live",
        "status": ProjectStatus(
            key="production",
            label="En Producción",
            color="#10B981",
            bg_color="rgba(16, 185, 129, 0.15)",
            icon="globe",
            animation_class="",
        ),
    }
    base.update(overrides)
    return Featured(**base)


def test_link_featured_renders_optional_actions_when_present() -> None:
    component = link_featured(_build_featured())

    rendered = str(component)

    assert "Example Project" in rendered
    assert "Example description" in rendered
    assert "Python" in rendered
    assert "Reflex" in rendered
    assert "https://github.com/example/project" in rendered
    assert "https://example.com/live" in rendered
    assert "Ver proyecto en vivo" in rendered
    assert "En Producci\\u00f3n" in rendered
    assert '"padingY"' not in rendered
    assert '"paddingTop"' in rendered


def test_link_featured_hides_optional_actions_when_links_are_missing() -> None:
    component = link_featured(
        _build_featured(
            description=None,
            technologies=[],
            github_url=None,
            live_url=None,
        )
    )

    rendered = str(component)

    assert "Example Project" in rendered
    assert 'to:"https://example.com/project"' in rendered
    assert 'aria-label={"Ver c\u00f3digo en GitHub"}' not in rendered
    assert 'aria-label={"Ver proyecto en vivo"}' not in rendered


def test_link_featured_disables_invalid_detail_link_and_hides_invalid_actions() -> None:
    component = link_featured(
        _build_featured(
            href="javascript:alert('xss')",
            github_url="#",
            live_url="not-a-url",
        )
    )

    rendered = str(component)

    assert "to:\"javascript:alert('xss')\"" not in rendered
    assert 'to:"#"' in rendered
    assert 'target:(false ? "_blank" : "")' in rendered
    assert (
        '"pointerEvents" : "none"' in rendered
        or '["pointerEvents"] : "none"' in rendered
    )
    assert 'aria-label={"Ver c\u00f3digo en GitHub"}' not in rendered
    assert 'aria-label={"Ver proyecto en vivo"}' not in rendered
