from dataclasses import dataclass
from typing import Literal

from rich.console import Console
from .render import Form
from .base.styles import PanelStyle
from .field import LiteralField, BoolField

cons = Console()


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
    name: str = LiteralField(values=(0, 1, 2, 3, 4), alias=('a', 'b', 'c', 'd', 'e'), field_name='name')
    age: bool = BoolField(field_name='age', current=False, aliases=('enable', 'disable'))


if __name__ == "__main__":
    a = User1()
    form = Form(dataclass=a)
    cons.print(form)
    print(a)
