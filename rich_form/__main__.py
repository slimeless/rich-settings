from dataclasses import dataclass

from rich.console import Console
from rich.panel import Panel

from .field import LiteralField, BoolField
from .render import Form


@dataclass
class Example:
    flag: bool = BoolField(
        aliases=("ON", "OFF"),
        desc_symbol="*",
        description="Bool flag with values (True/False)",
        field_name="example flag",
    )
    list: str = LiteralField(
        values=("A", "B", "C"),
        desc_symbol="*",
        description="List of values",
        field_name="example list",
    )


if __name__ == "__main__":
    example = Example()
    example_repr = repr(example)
    form = Form(example)
    cons = Console()

    cons.print(form)
    panel = Panel.fit(
        f"[bold green]{example_repr} --> {repr(example)}",
        border_style="green",
        title="Changes",
    )

    cons.print(panel)
