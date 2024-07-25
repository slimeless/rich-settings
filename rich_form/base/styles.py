from typing import Literal

from rich.style import Style
from dataclasses import dataclass

from rich.text import Text

SELECTED = Style(color="black", bold=True, bgcolor="green")


@dataclass
class PanelStyle:
    border_style: str | Style
    title: str | Text
    subtitle: str | Text
    style: str | Style = "none"
    title_align: Literal["left", "center", "right"] = "center"
    subtitle_align: Literal["left", "center", "right"] = "center"
