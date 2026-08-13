from urllib.parse import urlparse


def is_actionable_href(url: str | None) -> bool:
    if url is None:
        return False

    candidate = url.strip()
    return bool(candidate) and candidate not in {"/", "#"}


def is_actionable_external_url(url: str | None) -> bool:
    if not is_actionable_href(url):
        return False

    parsed = urlparse(url.strip())
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)
