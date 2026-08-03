from website_frontend.components.tech_badge import tech_badge
from website_frontend.model.tech_badge import TechBadge


def test_tech_badge_renders_name_icon_and_color() -> None:
    component = tech_badge(
        TechBadge(
            name="Python",
            color="#3776AB",
            icon_class="fa-brands fa-python",
        )
    )

    rendered = str(component)

    assert "Python" in rendered
    assert "fa-brands fa-python" in rendered
    assert "#3776AB" in rendered
