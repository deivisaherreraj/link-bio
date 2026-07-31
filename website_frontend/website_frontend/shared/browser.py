import reflex as rx

LOCAL_TIMEZONE_SCRIPT = "Intl.DateTimeFormat().resolvedOptions().timeZone"


def lang() -> rx.Component:
    return rx.script("document.documentElement.lang='es'")
