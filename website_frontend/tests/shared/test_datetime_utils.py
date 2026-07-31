from datetime import datetime

from website_frontend.shared import datetime_utils


class FixedBogotaDateTime(datetime):
    @classmethod
    def now(cls, tz=None):
        current = cls(2026, 8, 3, 15, 0, 0)
        if tz is None:
            return current
        return tz.localize(current)


class FixedBuenosAiresDateTime(datetime):
    @classmethod
    def now(cls, tz=None):
        current = cls(2026, 8, 3, 18, 0, 0)
        if tz is None:
            return current
        return tz.localize(current)


def test_next_date_returns_empty_string_for_empty_dates():
    result = datetime_utils.next_date({}, "America/Bogota")

    assert result == ""


def test_next_date_returns_today_when_future_slot_exists(monkeypatch):
    monkeypatch.setattr(datetime_utils, "datetime", FixedBogotaDateTime)

    result = datetime_utils.next_date({"0": "20:30"}, "America/Bogota")

    assert result == "Hoy, 03 de Agosto a las 15:30 | Zona horaria: Bogota"


def test_next_date_skips_passed_slot_and_uses_next_weekday(monkeypatch):
    monkeypatch.setattr(datetime_utils, "datetime", FixedBuenosAiresDateTime)

    result = datetime_utils.next_date(
        {"0": "20:30", "2": "20:30"},
        "America/Argentina/Buenos_Aires",
    )

    assert result == (
        "Miércoles, 05 de Agosto a las 17:30 | Zona horaria: Buenos Aires"
    )
