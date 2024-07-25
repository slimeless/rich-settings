from dataclasses import dataclass
from typing import Literal

from rich.console import Console

from .render import Form

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


if __name__ == "__main__":
    a = User()

    form = Form.from_raw_literal_dataclass(dataclass=a)
    cons.print(form)
    print(a)
