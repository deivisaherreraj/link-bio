import datetime

import reflex as rx

import website_frontend.constants.site_constants as site_const
from website_frontend.components.info_text import info_text
from website_frontend.components.link_button import link_button
from website_frontend.state.page_state import PageState
from website_frontend.styles.colors import Color
from website_frontend.styles.fonts import FontSize
from website_frontend.styles.styles import Margin, Padding, Spacing
from website_frontend.views.profile import profile


def header(details=True) -> rx.Component:
    return rx.vstack(
        # ProfileHeader
        profile(
            name=PageState.profile_info.full_name,
            handle=PageState.profile_info.handle,
            headline=PageState.profile_info.headline,
            tech_stack_summary=PageState.profile_info.tech_stack_summary,
            avatar_url=PageState.profile_info.avatar_url,
            avatar_status=PageState.avatar_status,
            github_url=PageState.github_url,
            linkedin_url=PageState.linkedin_url,
            email=PageState.profile_info.email,
        ),
        rx.cond(
            details,
            rx.vstack(
                rx.flex(
                    rx.spacer(),
                    rx.spacer(),
                    info_text(f"{experience()}+", "años de experiencia"),
                    rx.spacer(),
                    info_text("100+", "aplicaciones creadas"),
                    rx.spacer(),
                    rx.spacer(),
                    width="100%",
                    text_align="center",
                ),
                rx.cond(
                    PageState.live_status.live,
                    link_button(
                        href=site_const.TWITCH_URL,
                        title="En directo",
                        description=PageState.live_status.title,
                        icon="fa-brands fa-twitch",
                        icon_color=Color.PURPLE.value,
                        border_color=Color.PURPLE.value,
                        animated=True,
                    ),
                    rx.box(
                        rx.cond(
                            PageState.next_live,
                            link_button(
                                href=site_const.TWITCH_URL,
                                title="Próximo directo",
                                description=PageState.next_live,
                                icon="fa-brands fa-twitch",
                                icon_color=Color.PURPLE.value,
                                border_color=Color.PURPLE.value,
                                animated=True,
                            ),
                        ),
                        width="100%",
                        on_mount=PageState.check_schedule,
                    ),
                ),
                # Introduction a mi Bio
                rx.el.Section.create(
                    rx.text(
                        PageState.profile_info.bio_short,
                        as_="p",
                        font_size=FontSize.MEDIUM.value,
                        color=Color.GRAY.value,
                    ),
                    padding_top=Padding.ZERO.value,
                    padding_bottom=Padding.ZERO.value,
                ),
                width="100%",
                margin_bottom=Margin.VERY_BIG.value,
            ),
        ),
        width="100%",
        spacing=Spacing.BIG.value,
        align_items="start",
        on_mount=[PageState.check_live, PageState.load_profile],
    )


def experience() -> int:
    return datetime.date.today().year - 2013
