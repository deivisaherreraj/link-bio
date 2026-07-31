from website_frontend.services import schedule_service


class StubConfigCatAPI:
    def __init__(self, schedule: dict) -> None:
        self.schedule_data = schedule

    def schedule(self) -> dict:
        return self.schedule_data


def test_get_live_schedule_returns_adapter_schedule(monkeypatch):
    schedule = {"0": "18:00"}
    monkeypatch.setattr(
        schedule_service,
        "CONFIGCAT_API",
        StubConfigCatAPI(schedule),
    )

    result = schedule_service.get_live_schedule()

    assert result == schedule


def test_get_next_live_date_uses_schedule_and_timezone(monkeypatch):
    schedule = {"1": "20:30"}
    calls = []

    def fake_next_date(received_schedule: dict, timezone: str) -> str:
        calls.append((received_schedule, timezone))
        return "Martes, 01 de Enero a las 15:30 | Zona horaria: Bogota"

    monkeypatch.setattr(schedule_service, "get_live_schedule", lambda: schedule)
    monkeypatch.setattr(schedule_service, "next_date", fake_next_date)

    result = schedule_service.get_next_live_date("America/Bogota")

    assert result == "Martes, 01 de Enero a las 15:30 | Zona horaria: Bogota"
    assert calls == [(schedule, "America/Bogota")]


def test_get_next_live_date_returns_empty_string_for_empty_schedule(monkeypatch):
    monkeypatch.setattr(schedule_service, "get_live_schedule", lambda: {})

    result = schedule_service.get_next_live_date("America/Bogota")

    assert result == ""
