import reflex as rx

from website_frontend.components.status_badge import status_badge
from website_frontend.model.featured import Featured
from website_frontend.shared.urls import (
    is_actionable_external_url,
)
from website_frontend.styles.colors import BackgroundColor
from website_frontend.styles.fonts import FontSize, FontWeight
from website_frontend.styles.styles import Color, Margin, Padding, Spacing


def _link_href(url: str | None | rx.Var) -> str | rx.Var:
    if hasattr(url, "to"):
        return url.to(str)

    return url or "#"


def link_featured(featured: Featured) -> rx.Component:
    action_links = []
    capability_badges = []

    if featured.github_url is not None:
        capability_badges.append(
            rx.text(
                "Código abierto",
                padding_y=Padding.SMALL.value,
                padding_x=Padding.DEFAULT.value,
                font_size=FontSize.TINY.value,
                color=Color.WHITE.value,
                background_color=Color.BG_WHITE_TRANSPARENT.value,
                border_radius="999px",
                class_name="backdrop-blur-sm",
                as_="span",
            )
        )
        action_links.append(
            rx.link(
                rx.icon("github"),
                href=_link_href(featured.github_url),
                is_external=True,
                aria_label="Ver código en GitHub",
                color=Color.GRAY.value,
                font_size=FontSize.DEFAULT.value,
                class_name="hover:text-text-primary transition-colors",
            )
        )

    if featured.live_url is not None:
        capability_badges.append(
            rx.text(
                "Live demo",
                padding_y=Padding.SMALL.value,
                padding_x=Padding.DEFAULT.value,
                font_size=FontSize.TINY.value,
                color=Color.WHITE.value,
                background_color=BackgroundColor.LIGHT.value,
                border_radius="999px",
                class_name="backdrop-blur-sm",
                as_="span",
            )
        )
        action_links.append(
            rx.link(
                rx.icon("external-link"),
                href=_link_href(featured.live_url),
                is_external=True,
                aria_label="Ver proyecto en vivo",
                color=Color.GRAY.value,
                font_size=FontSize.DEFAULT.value,
                class_name="hover:text-text-primary transition-colors",
            )
        )

    return rx.flex(
        rx.text(
            "Proyecto destacado",
            font_size=FontSize.TINY.value,
            font_weight=FontWeight.SEMI_BOLD.value,
            color=Color.PRIMARY.value,
            text_transform="uppercase",
            letter_spacing="0.08em",
            as_="span",
        ),
        rx.hstack(
            rx.heading(
                featured.title,
                font_size=FontSize.EXTRA_LARGE.value,
                font_weight=FontWeight.BOLD.value,
                color=Color.WHITE.value,
                flex="1 1 0%",
                as_="h3",
                line_height="1.2",
            ),
            status_badge(featured.status),
            align_items="flex-start",
            justify="between",
            width="100%",
            flex_wrap="wrap",
            spacing=Spacing.EXTRA_SMALL.value,
        ),
        rx.cond(
            featured.description is not None,
            rx.text(
                featured.description,
                font_size=FontSize.SMALL.value,
                color=Color.GRAY.value,
                class_name="line-clamp-3",
                line_height="1.55",
                as_="p",
            ),
        ),
        rx.cond(
            bool(capability_badges),
            rx.flex(
                *capability_badges,
                flex_wrap="wrap",
                gap="0.5rem",
            ),
        ),
        rx.cond(
            featured.technologies != [],
            rx.flex(
                rx.foreach(
                    featured.technologies,
                    lambda tech: rx.text(
                        tech,
                        padding_y=Padding.SMALL.value,
                        padding_x=Padding.DEFAULT.value,
                        font_size=FontSize.TINY.value,
                        color=Color.WHITE.value,
                        background_color=Color.BG_WHITE_TRANSPARENT.value,
                        border_radius="999px",
                        class_name="backdrop-blur-sm",
                        as_="span",
                    ),
                ),
                flex_wrap="wrap",
                gap="0.5rem",
            ),
        ),
        rx.hstack(
            rx.cond(
                featured.href != None,
                rx.link(
                    rx.hstack(
                        rx.text(
                            "Ver Detalles",
                        ),
                        rx.icon(
                            "arrow-right",
                            font_size=FontSize.SMALL.value,
                        ),
                        spacing=Spacing.VERY_SMALL.value,
                        align="center",
                    ),
                    href=_link_href(featured.href),
                    is_external=(
                        False
                        if hasattr(featured.href, "to")
                        else is_actionable_external_url(featured.href)
                    ),
                    font_size=FontSize.SMALL.value,
                    font_weight=FontWeight.SEMI_BOLD.value,
                    color=Color.WHITE.value,
                    display="flex",
                    align_items="center",
                    gap="0.25rem",
                    z_index="10",
                    aria_label=f"Ver detalles del proyecto {featured.title}",
                    padding_y=Padding.SMALL.value,
                    padding_x=Padding.DEFAULT.value,
                    border_radius="999px",
                    background_color=Color.PRIMARY.value,
                    class_name="transition-all z-10 hover:brightness-110",
                ),
            ),
            rx.hstack(
                *action_links,
                spacing=Spacing.SMALL.value,
                z_index="10",
                justify="end",
            ),
            justify="between",
            align="center",
            width="100%",
            margin_top=Margin.MEDIUM.value,
        ),
        direction="column",
        spacing=Spacing.SMALL.value,
        width="100%",
        padding=Padding.SMALL.value,
    )
