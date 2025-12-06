from enum import Enum


class Font(Enum):
    DEFAULT = "Poppins"
    TITLE = "Poppins"
    LOGO = "ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,Liberation Mono,Courier New,monospace"


class FontSize(Enum):
    TINY = "0.75rem"
    SMALL = "0.875rem"
    MEDIUM = "1rem"
    DEFAULT = "1.125rem"
    LARGE = "1.25rem"
    EXTRA_LARGE = "1.5rem"
    TITLE = "2rem"


class FontWeight(Enum):
    EXTRA_LIGHT = "100"
    THIN = "200"
    LIGHT = "300"
    NORMAL = "400"
    MEDIUM = "500"
    SEMI_BOLD = "600"
    BOLD = "700"
    EXTRA_BOLD = "800"
    BLACK = "900"
    HEAVY = "950"
