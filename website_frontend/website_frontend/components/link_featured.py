import reflex as rx

from website_frontend.components.status_badge import status_badge
from website_frontend.model.featured import Featured
from website_frontend.styles.fonts import FontSize, FontWeight
from website_frontend.styles.styles import Color, Margin, Padding, Spacing


def link_featured(featured: Featured) -> rx.Component:
    """
    Versión Reflex de FeaturedCard:
    - Usa PageState.get_project_status para resolver la config del estado.
    - Usa un componente independiente status_badge para el badge.
    - Renderiza technologies con rx.foreach y flex-wrap.
    """
    return rx.flex(
        # Título + badge de estado
        rx.hstack(
            rx.heading(
                featured.title,
                font_size=FontSize.EXTRA_LARGE.value,
                font_weight=FontWeight.BOLD.value,
                color=Color.WHITE.value,
                flex="1 1 0%",
                as_="h3",
            ),
            # Badge de estado (solo si status_info existe)
            rx.cond(
                featured.status,
                status_badge(featured.status),
            ),
            align_items="flex-start",
            justify="between",
            direction="column-reverse",
            spacing=Spacing.EXTRA_SMALL.value,
        ),
        # Descripción
        rx.cond(
            featured.description is not None,
            rx.text(
                featured.description,
                font_size=FontSize.SMALL.value,
                color=Color.GRAY.value,
                class_name="line-clamp-2",
                as_="p",
            ),
        ),
        # Chips de tecnologías
        rx.cond(
            featured.technologies != [],
            rx.flex(
                rx.foreach(
                    featured.technologies,
                    lambda tech: rx.text(
                        tech,
                        pading_y=Padding.SMALL.value,
                        padding_x=Padding.DEFAULT.value,
                        font_size=FontSize.TINY.value,
                        color=Color.WHITE.value,
                        background_color=Color.BG_WHITE_TRANSPARENT.value,
                        border_radius="0.375rem",
                        class_name="backdrop-blur-sm",
                        as_="span",
                    ),
                ),
                flex_wrap="wrap",
                gap="0.5rem",
            ),
        ),
        # Acciones
        rx.hstack(
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
                href=featured.href,
                is_external=True,
                font_size=FontSize.SMALL.value,
                font_weight=FontWeight.MEDIUM.value,
                color=Color.PRIMARY.value,
                display="flex",
                align_items="center",
                gap="0.25rem",
                z_index="10",
                aria_label=f"Ver detalles del proyecto {featured.title}",
                class_name=("hover:text-primary-light transition-colors z-10"),
            ),
            rx.hstack(
                rx.cond(
                    featured.github_url is not None,
                    rx.link(
                        rx.icon("github"),
                        href=featured.github_url,
                        is_external=True,
                        aria_label="Ver código en GitHub",
                        color=Color.GRAY.value,
                        font_size=FontSize.DEFAULT.value,
                        class_name=("hover:text-text-primary transition-colors"),
                    ),
                ),
                rx.cond(
                    featured.live_url is not None,
                    rx.link(
                        rx.icon("external-link"),
                        href=featured.live_url,
                        is_external=True,
                        aria_label="Ver proyecto en vivo",
                        color=Color.GRAY.value,
                        font_size=FontSize.DEFAULT.value,
                        class_name=("hover:text-text-primary transition-colors"),
                    ),
                ),
                spacing=Spacing.SMALL.value,
                z_index="10",
                justify="end",
            ),
            justify="between",
            align="center",
            margin_top=Margin.MEDIUM.value,
        ),
        direction="column",
        spacing=Spacing.SMALL.value,
        width="100%",
    )
