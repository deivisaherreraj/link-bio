from website_frontend.model.social_link import SocialLink
from website_frontend.services import social_links_service


def test_get_social_links_uses_supabase_rows_when_available(monkeypatch):
    expected = [
        SocialLink(
            label="Discord",
            url="https://discord.gg/example",
            icon="fa-brands fa-discord",
            section="community",
            priority=1,
            is_active=True,
            is_external=True,
        )
    ]

    monkeypatch.setattr(
        social_links_service.SUPABASE_API,
        "social_links",
        lambda: expected,
    )

    assert social_links_service.get_social_links() == expected


def test_get_social_links_filters_inactive_rows_before_returning(monkeypatch):
    monkeypatch.setattr(
        social_links_service.SUPABASE_API,
        "social_links",
        lambda: [
            SocialLink(
                label="Visible",
                url="https://example.com/visible",
                icon="fa-solid fa-star",
                section="work",
                priority=1,
                is_active=True,
                is_external=True,
            ),
            SocialLink(
                label="Hidden",
                url="https://example.com/hidden",
                icon="fa-solid fa-eye-slash",
                section="work",
                priority=2,
                is_active=False,
                is_external=True,
            ),
        ],
    )

    result = social_links_service.get_social_links()

    assert [link.label for link in result] == ["Visible"]


def test_get_social_links_falls_back_to_default_links_when_supabase_is_empty(monkeypatch):
    monkeypatch.setattr(
        social_links_service.SUPABASE_API,
        "social_links",
        lambda: [],
    )

    result = social_links_service.get_social_links()

    assert result == social_links_service.get_default_social_links()
    assert any(link.label == "Workana" for link in result)


def test_get_social_links_by_section_groups_links_in_expected_buckets(monkeypatch):
    monkeypatch.setattr(
        social_links_service,
        "get_social_links",
        lambda: [
            SocialLink(
                label="Discord",
                url="https://discord.gg/example",
                icon="fa-brands fa-discord",
                section="community",
                priority=1,
                is_active=True,
                is_external=True,
            ),
            SocialLink(
                label="Email",
                url="mailto:test@example.com",
                icon="fa-solid fa-envelope",
                section="contact",
                priority=2,
                is_active=True,
                is_external=False,
            ),
        ],
    )

    result = social_links_service.get_social_links_by_section()

    assert [link.label for link in result["community"]] == ["Discord"]
    assert [link.label for link in result["contact"]] == ["Email"]
    assert result["work"] == []
    assert result["resources"] == []
