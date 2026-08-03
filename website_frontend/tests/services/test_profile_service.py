from website_frontend.model.avatar_status import AvatarStatus
from website_frontend.services import profile_service


class StubConfigCatAPI:
    def __init__(self, avatar_status_key: str) -> None:
        self.avatar_status_key = avatar_status_key

    def avatar_status(self) -> str:
        return self.avatar_status_key


def test_build_avatar_status_normalizes_input():
    result = profile_service.build_avatar_status(' "CONSULTORIA" ')

    assert isinstance(result, AvatarStatus)
    assert result.key == "consultoria"
    assert result.class_name == "is-consulting"


def test_build_avatar_status_falls_back_for_unknown_key():
    result = profile_service.build_avatar_status("desconocido")

    assert result.key == "activo"
    assert result.class_name == "is-active"


def test_get_default_avatar_status_uses_project_default():
    result = profile_service.get_default_avatar_status()

    assert result.key == "activo"
    assert result.class_name == "is-active"


def test_get_avatar_status_key_reads_from_adapter(monkeypatch):
    monkeypatch.setattr(
        profile_service,
        "CONFIGCAT_API",
        StubConfigCatAPI("empleo"),
    )

    result = profile_service.get_avatar_status_key()

    assert result == "empleo"


def test_get_profile_technologies_returns_badges():
    result = profile_service.get_profile_technologies()

    assert result
    assert result[0].name == "Angular"
    assert result[0].icon_class == "fa-brands fa-angular"


def test_get_profile_technologies_returns_empty_list_when_config_is_empty(monkeypatch):
    monkeypatch.setattr(profile_service.profile_const, "TECHNOLOGIES", [])

    result = profile_service.get_profile_technologies()

    assert result == []


def test_get_profile_technologies_skips_invalid_entries(monkeypatch):
    monkeypatch.setattr(
        profile_service.profile_const,
        "TECHNOLOGIES",
        [
            {"name": "Angular", "color": "#DD0031", "icon_class": "fa-angular"},
            {"name": "", "color": "#000000", "icon_class": "fa-empty"},
            {"name": "Node.js", "color": " ", "icon_class": "fa-node-js"},
            {"name": "Python", "color": "#3776AB", "icon_class": None},
            "not-a-dict",
        ],
    )

    result = profile_service.get_profile_technologies()

    assert len(result) == 1
    assert result[0].name == "Angular"
    assert result[0].color == "#DD0031"
    assert result[0].icon_class == "fa-angular"


def test_build_avatar_status_falls_back_for_incomplete_catalog_entry(monkeypatch):
    monkeypatch.setitem(
        profile_service.profile_const.AVAILABILITY_STATES,
        "consultoria",
        {
            "text": "",
            "class_name": "is-consulting",
            "icon": "fa-laptop-code",
        },
    )

    result = profile_service.build_avatar_status("consultoria")

    assert result.key == "activo"
    assert result.class_name == "is-active"
