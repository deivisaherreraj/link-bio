import reflex as rx

from website_frontend.styles.colors import Color

class FloatButton(rx.Component):
    library = "antd"
    tag = "FloatButton"
    # icon: rx.Var[rx.el.Img]
    href: rx.Var[str]
    tooltip: rx.Var[str]
    target = "_blank"
    badge = {"dot": True, "color": Color.PRIMARY.value}

float_button = FloatButton.create