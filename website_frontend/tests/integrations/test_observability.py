import logging

from website_frontend.integrations.observability import (
    fail_closed_event,
    log_fail_closed_event,
)


def test_fail_closed_event_payload_remains_compatible():
    assert fail_closed_event(
        event="example_failed_closed",
        integration="example",
        operation="fetch",
        context={"error_type": "RuntimeError"},
    ) == {
        "event": "example_failed_closed",
        "integration": "example",
        "operation": "fetch",
        "fail_closed": True,
        "error_type": "RuntimeError",
    }


def test_log_fail_closed_event_emits_structured_warning(caplog):
    logger = logging.getLogger("test.observability")

    with caplog.at_level("WARNING", logger=logger.name):
        result = log_fail_closed_event(
            logger,
            event="example_failed_closed",
            integration="example",
            operation="fetch",
            context={"error_type": "RuntimeError"},
        )

    assert result is None
    record = caplog.records[-1]
    assert record.message == "example_failed_closed"
    assert record.event == "example_failed_closed"
    assert record.integration == "example"
    assert record.operation == "fetch"
    assert record.fail_closed is True
    assert record.error_type == "RuntimeError"
