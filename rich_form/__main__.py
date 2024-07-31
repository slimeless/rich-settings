from dataclasses import dataclass
from typing import Literal

from rich.console import Console
from .render import Form
from .field import LiteralField, BoolField
from rich.table import Table

cons = Console()


def generate_table(rows, columns):
    table = Table(show_header=True, header_style="bold magenta")

    for i in range(columns):
        table.add_column(f"Column {i + 1}", width=12)

    for i in range(rows):
        row_data = [f"Row {i + 1}, Col {j + 1}" for j in range(columns)]
        table.add_row(*row_data)

    return table


@dataclass
class Player:
    is_fullscreen: bool = True
    is_maximized: bool = False
    is_animated: bool = False
    exc: str = ""


@dataclass
class User:
    name: Literal["Kirill", "Alex", "Alexey", "Vlad"] = "Kirill"
    age: Literal[21, 22] = 22


@dataclass
class User1:
    name: str = LiteralField(values=(0, 1, 2, 3, 4), field_name="name")
    age: bool = BoolField(
        field_name="age", current=False, aliases=("enable", "disable")
    )


if __name__ == "__main__":
    table = generate_table(5, 5)
    a = User1()
    form = Form(a)
    res = form.render(cons)
    print(res)
