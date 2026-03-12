"""Theme and styling constants for charts."""

from typing import ClassVar

class Colors:
    primary: ClassVar[str] = "#4ECDC4"      # Main line and fill color
    title: ClassVar[str] = "#9BD1CE"        # Title text color
    text: ClassVar[str] = "#CCCCCC"         # General text, labels, ticks
    structural: ClassVar[str] = "#666666"   # Grid and spine color
    marker_edge: ClassVar[str] = "white"    # Marker edge color

class Typography:
    title_fontsize: ClassVar[int] = 14
    title_fontweight: ClassVar[str] = "semibold"
    title_pad: ClassVar[int] = 20
    subtitle_fontsize: ClassVar[int] = 10
    subtitle_fontweight: ClassVar[str] = "semibold"
    label_fontsize: ClassVar[int] = 12
    label_fontweight: ClassVar[str] = "semibold"
    tick_fontsize: ClassVar[int] = 10

class Figure:
    figsize: ClassVar[tuple[float, float]] = (8.0, 4.0)
    background_alpha: ClassVar[float] = 0.0   # Transparent background

class Line:
    linestyle: ClassVar[str] = "solid"
    linewidth: ClassVar[float] = 2.5
    alpha: ClassVar[float] = 0.9

class Marker:
    markersize: ClassVar[int] = 6
    markeredgewidth: ClassVar[float] = 1.5

class Fill:
    alpha: ClassVar[float] = 0.2

class Grid:
    linestyle: ClassVar[str] = "--"
    alpha: ClassVar[float] = 0.3

class Axis:
    y_min_margin: ClassVar[float] = 0.95
    y_max_margin: ClassVar[float] = 1.01
    date_format: ClassVar[str] = "%d %b"  # Day number and abbreviated month

class Chart:
    num_x_ticks: ClassVar[int] = 5
