from website_frontend.model.featured import Featured
from website_frontend.model.project_status import ProjectStatus
from website_frontend.services import featured_service


class StubSupabaseAPI:
    def __init__(self, featured_projects: list[Featured]) -> None:
        self.featured_projects = featured_projects

    def featured(self) -> list[Featured]:
        return self.featured_projects


def test_get_featured_projects_returns_adapter_result(monkeypatch):
    featured_projects = [
        Featured(
            href="https://example.com/project",
            image_url="https://example.com/project.png",
            title="Example Project",
            description="Example description",
            technologies=["Python", "Reflex"],
            github_url="https://github.com/example/project",
            live_url="https://example.com/live",
            status=ProjectStatus(
                key="production",
                label="En Produccion",
                color="#10B981",
                bg_color="rgba(16, 185, 129, 0.15)",
                icon="globe",
                animation_class="",
            ),
        )
    ]
    monkeypatch.setattr(
        featured_service,
        "SUPABASE_API",
        StubSupabaseAPI(featured_projects),
    )

    result = featured_service.get_featured_projects()

    assert result == featured_projects


def test_get_featured_projects_returns_empty_list(monkeypatch):
    monkeypatch.setattr(
        featured_service,
        "SUPABASE_API",
        StubSupabaseAPI([]),
    )

    result = featured_service.get_featured_projects()

    assert result == []
