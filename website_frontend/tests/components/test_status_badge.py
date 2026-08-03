from website_frontend.components.status_badge import status_badge
from website_frontend.model.project_status import ProjectStatus


def test_status_badge_renders_required_status_fields() -> None:
    component = status_badge(
        ProjectStatus(
            key="production",
            label="En Producción",
            color="#10B981",
            bg_color="rgba(16, 185, 129, 0.15)",
            icon="globe",
            animation_class="",
        )
    )

    rendered = str(component)

    assert "En Producci\\u00f3n" in rendered
    assert "LucideGlobe" in rendered
    assert "#10B981" in rendered
    assert "rgba(16, 185, 129, 0.15)" in rendered
