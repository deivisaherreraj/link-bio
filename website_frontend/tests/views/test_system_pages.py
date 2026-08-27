from website_frontend.pages.error import error_generic
from website_frontend.pages.maintenance import maintenance
from website_frontend.pages.not_found import not_found


def test_error_page_renders_expected_actions() -> None:
    rendered = str(error_generic())

    assert "Algo sali\\u00f3 mal" in rendered
    assert "Recuperaci\\u00f3n inmediata" in rendered
    assert "Intentar de nuevo" in rendered
    assert "Volver al inicio" in rendered
    assert "fa-solid fa-triangle-exclamation" in rendered


def test_maintenance_page_renders_richer_content() -> None:
    rendered = str(maintenance())

    assert "Mantenimiento en curso" in rendered
    assert "Maintenance active" in rendered
    assert "Tiempo estimado" in rendered
    assert "15" in rendered
    assert "30 minutos" in rendered
    assert "Reintentar ahora" in rendered
    assert rendered.count("fa-solid fa-screwdriver-wrench") == 1
    assert "fa-regular fa-clock" in rendered
    assert "fa-solid fa-newspaper" in rendered
    assert "fa-solid fa-calendar-days" in rendered
    assert "fa-solid fa-shield-heart" not in rendered


def test_not_found_page_renders_dedicated_recovery_paths() -> None:
    rendered = str(not_found())

    assert "P\\u00e1gina no encontrada" in rendered
    assert "404 \\u00b7 Lost route" in rendered
    assert "Explorar el blog" in rendered
    assert "/blog" in rendered
