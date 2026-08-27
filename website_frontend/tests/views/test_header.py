from website_frontend.views.header import _intro_paragraph, header


def test_header_renders_intro_paragraph_with_emphasis_below_live_banner() -> None:
    rendered = str(header())

    assert "Back-End" in rendered
    assert "Front-End" in rendered
    assert "proyectos, contenido, formas de contacto" in rendered


def test_intro_paragraph_uses_strong_emphasis() -> None:
    rendered = str(_intro_paragraph())

    assert "strong" in rendered.lower()
    assert "desarrollador Full-Stack" in rendered
    assert "software confiable, escalable y de alto impacto" in rendered
