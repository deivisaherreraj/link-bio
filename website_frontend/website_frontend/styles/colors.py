from enum import Enum


class Color(Enum):
    PRIMARY = "#0099FF"
    SECONDARY = "#087ec4"
    DISCORD = "#5865F2"
    BACKGROUND = "#0C151D"
    CONTENT = "#1f2937"
    PURPLE = "#9146ff"
    PINK = "#FF90E8"
    GRAY = "#94a3b8"
    GRAY_DARK = "#6B7280"
    RED = "#FF0000"
    ORANGE = "#F59E0B"
    WHITE = "#ffffff"
    WHITE_TRANSPARENT = "#0099ff26"
    BG_WHITE_TRANSPARENT = "#ffffff1a"
    BG_BLACK_TRANSPARENT = "#00000066"
    BG_BLACK_TRANSPARENT_STRONG = "#000000b3"
    TRANSPARENT = "transparent"


class TextColor(Enum):
    HEADER = "#F1F2F4"
    BODY = "#C3C7CB"
    FOOTER = "#203E58"
    TRANSPARENT = "transparent"


class BackgroundColor(Enum):
    SURFACE = "#0D1218"
    SURFACE_HOVER = "#161D26"
    LIGHT = "#ffffff0d"


class BorderColor(Enum):
    DEFAULT = "#ffffff14"
    WHITE_TRANSPARENT = "#ffffff26"
    WHITE_TRANSPARENT_LIGHT = "#ffffff0d"
