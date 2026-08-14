from collections.abc import Mapping


def fail_closed_event(
    *,
    event: str,
    integration: str,
    operation: str,
    context: Mapping[str, object] | None = None,
) -> dict[str, object]:
    return {
        "event": event,
        "integration": integration,
        "operation": operation,
        "fail_closed": True,
        **(dict(context) if context is not None else {}),
    }
