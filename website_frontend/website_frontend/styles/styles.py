import reflex as rx

from enum import Enum
from .colors import Color, TextColor
from .fonts import Font, FontSize, FontWeight

# Constants
MAX_WIDTH = "680px"
BOUNCEIN_ANIMATION = "animate__animated animate__bounceInDown"

# Styles
STYLESHEETS = [
    "https://fonts.googleapis.com/css2?family=Poppins:wght@300;500&display=swap",
    "https://fonts.googleapis.com/css2?family=Comfortaa:wght@500&display=swap",
    "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap",
    "https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css",
    "/css/styles.css",
    "/css/grid_background.css",
]


# Logo
class Logo(Enum):
    HEIGHT = "3.3em"
    WIDTH = "4em"


# Sizes
class Size(Enum):
    ZERO = "0px !important"
    VERY_SMALL = "0.25em"
    SMALL = "0.5em"
    MEDIUM = "0.8em"
    DEFAULT = "1em"
    LARGE = "1.5em"
    BIG = "2em"
    VERY_LARGE = "3.5em"
    VERY_BIG = "4em"


# Spacing
class Spacing(Enum):
    ZERO = "0"
    VERY_SMALL = "1"
    EXTRA_SMALL = "2"
    SMALL = "3"
    DEFAULT = "4"
    LARGE = "5"
    BIG = "6"
    MEDIUM_BIG = "7"
    EXTRA_BIG = "8"
    VERY_BIG = "9"


# Radius
class Radius(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    FULL = "full"


# Margin
class Margin(Enum):
    ZERO = "0px"
    VERY_SMALL = "2px"
    SMALL = "4px"
    MEDIUM = "8px"
    DEFAULT = "12px"
    LARGE = "16px"
    BIG = "24px"
    VERY_BIG = "32px"


# Padding
class Padding(Enum):
    ZERO = "0px"
    VERY_SMALL = "2px"
    SMALL = "4px"
    MEDIUM = "8px"
    DEFAULT = "12px"
    LARGE = "16px"
    BIG = "24px"
    VERY_BIG = "32px"


BASE_STYLE = {
    "font_family": Font.DEFAULT.value,
    "font_weight": FontWeight.LIGHT.value,
    rx.heading: {
        "color": TextColor.HEADER.value,
        "font_family": Font.TITLE.value,
        "font_weight": FontWeight.MEDIUM.value,
    },
    rx.button: {
        "width": "100%",
        "height": "100%",
        "padding": Size.SMALL.value,
        "border_radius": Size.DEFAULT.value,
        "color": TextColor.HEADER.value,
        "background_color": Color.CONTENT.value,
        "white_space": "normal",
        "text_align": "start",
        "--cursor-button": "pointer",
        "_hover": {"background_color": Color.SECONDARY.value},
    },
    rx.link: {"color": TextColor.BODY.value, "text_decoration": "none", "_hover": {}},
}

navbar_title_style = dict(
    font_family=Font.LOGO.value,
    font_weight=FontWeight.BLACK.value,
    font_size=Size.LARGE.value,
)

title_style = dict(
    width="100%",
    font_weight=FontWeight.MEDIUM.value,
    font_size=FontSize.DEFAULT.value,
    margin_bottom=Margin.LARGE.value,
)

button_title_style = dict(
    font_family=Font.TITLE.value,
    font_weight=FontWeight.MEDIUM.value,
    color=TextColor.HEADER.value,
)

button_body_style = dict(font_weight=FontWeight.LIGHT.value, color=TextColor.BODY.value)
