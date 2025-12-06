from enum import Enum


class Color(Enum):
    PRIMARY = "#0099FF"
    SECONDARY = "#087ec4"
    BACKGROUND = "#0C151D"
    CONTENT = "#1f2937"
    PURPLE = "#9146ff"
    GRAY = "#94a3b8"
    WHITE = "#ffffff"
    TRANSPARENT = "transparent"
    BG_WHITE_TRANSPARENT = "rgba(255,255,255,0.1)"
    BG_BLACK_TRANSPARENT = "rgba(0,0,0,0.4)"
    BG_BLACK_TRANSPARENT_STRONG = "rgba(0,0,0,0.7)"


class TextColor(Enum):
    HEADER = "#F1F2F4"
    BODY = "#C3C7CB"
    FOOTER = "#203E58"
    TRANSPARENT = "transparent"
