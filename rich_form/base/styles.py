from dataclasses import dataclass
from typing import Optional

from rich.align import AlignMethod
from rich.padding import PaddingDimensions
from rich.style import Style, StyleType
from rich.text import TextType


@dataclass
class PanelStyle:
    title: Optional[TextType] = None
    title_align: AlignMethod = "center"
    subtitle: Optional[TextType] = None
    subtitle_align: AlignMethod = "center"
    safe_box: Optional[bool] = None
    style: StyleType = "none"
    border_style: StyleType = "none"
    width: Optional[int] = None
    height: Optional[int] = None
    padding: PaddingDimensions = (0, 1)
    highlight: bool = False


SELECTED = Style(color="black", bold=True, bgcolor="green")
BASIC = PanelStyle(title='[bold green]Data', border_style="green")
