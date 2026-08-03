from website_frontend.components.avatar_with_status import avatar_with_status
from website_frontend.model.avatar_status import AvatarStatus


def test_avatar_with_status_passes_plain_name_to_avatar() -> None:
    component = avatar_with_status(
        avatar_url="/avatar.jpeg",
        name="Deivis",
        status=AvatarStatus(
            key="activo",
            text="Disponible",
            class_name="is-active",
            icon="fa-bolt",
        ),
    )

    rendered = str(component)

    assert '["Deivis"]' not in rendered
    assert '"Foto de perfil de Deivis"' in rendered
    assert 'Deivis' in rendered
