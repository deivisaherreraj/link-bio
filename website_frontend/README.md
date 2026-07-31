# Website de links de DHerreraJDev

[![Python](https://img.shields.io/badge/Python-3.11+-yellow?style=for-the-badge&logo=python&logoColor=white&labelColor=101010)](https://python.org)
[![FastAPI](https://img.shields.io/badge/Reflex-0.3.10+-5646ED?style=for-the-badge&logo=reflex&logoColor=white&labelColor=101010)](https://fastapi.tiangolo.com)

## Proyecto desarrollado con [Python](https://www.python.org/) y [Reflex](https://reflex.dev/) que representa un sitio web personal estilo "[link in bio](https://dherrerajdev.vercel.app)"

![https://dherrerajdev.vercel.app](../assets/web.png)

## Calidad del proyecto

Comandos base de verificación:

```bash
uv run pytest tests/integrations tests/services tests/shared
uv run ruff check .
uv run ruff format --check .
uv run mypy
```

Para aplicar formato automáticamente:

```bash
uv run ruff format .
```
