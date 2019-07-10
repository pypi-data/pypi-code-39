from .generated import BaseColor, TableauColor, XkcdColor, Css4Color, Color
from .colormaps import LabelColorMap

__version__ = "0.2.0"
__version_info__ = tuple(int(n) for n in __version__.split("."))

__all__ = ["BaseColor", "TableauColor", "XkcdColor", "Css4Color", "Color", "LabelColorMap"]
