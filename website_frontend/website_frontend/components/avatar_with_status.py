import reflex as rx

from website_frontend.styles.styles import Spacing, Radius

from website_frontend.model.avatar_status import AvatarStatus


def avatar_with_status(
    avatar_url: str, name: str, status: AvatarStatus
) -> rx.Component:
    """
    Componente de avatar con estado.
    Recibe un AvatarStatus ya resuelto desde el PageState.
    """
    return rx.box(
        # Avatar
        rx.avatar(
            name={name},
            size=Spacing.MEDIUM_BIG.value,
            radius=Radius.FULL.value,
            src=avatar_url,
            alt=f"Foto de perfil de {name}",
            class_name="hero__avatar",
        ),
        # Badge de estado
        rx.box(
            rx.el.I.create(
                id="statusIcon",
                class_name=f"fa-solid {status.icon}",
            ),
            rx.box(
                status.text,
                id="statusTooltip",
                class_name="status-tooltip",
                role="status",
            ),
            id="statusBadge",
            class_name=f"status-badge {status.class_name}",
            aria_label="Estado de disponibilidad",
        ),
        class_name="hero__avatar-container",
    )
