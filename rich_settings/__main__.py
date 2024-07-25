from dataclasses import dataclass
from typing import Literal

from readchar import readkey, key
from rich.console import Console, ConsoleOptions
from rich.live import Live

from .visualize import (
    BaseVisualizeExecutor,
    LiteralDataclassVisualizeExecutor,
)

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


def render(renderable_obj: BaseVisualizeExecutor):
    with Live(renderable_obj, auto_refresh=False) as live:
        while True:
            ch = readkey()
            if ch == key.UP or ch == "k":
                renderable_obj.selected = max(0, renderable_obj.selected - 1)
            if ch == key.DOWN or ch == "j":
                renderable_obj.selected = min(
                    len(renderable_obj.columns) - 1, renderable_obj.selected + 1
                )

            if ch == key.RIGHT or ch == "l":
                renderable_obj.validate()

            if ch == key.LEFT or ch == "h":
                renderable_obj.validate(negative=True)

            if ch == key.ENTER:
                if hasattr(renderable_obj, "execute_action_queue"):
                    renderable_obj.execute_action_queue()
                    return "[bold green]Success!"

            live.update(renderable_obj, refresh=True)


class Render:
    def __init__(self, renderable_obj: BaseVisualizeExecutor):
        self.renderable_obj = renderable_obj

    def __rich_console__(self, console: Console, options: ConsoleOptions):
        from os import devnull

        file = open(devnull, "w")
        console.file = file
        render(self.renderable_obj)
        return ""


if __name__ == "__main__":
    a = User()
    renderable = LiteralDataclassVisualizeExecutor(a)

    cons.print(Render(renderable))
    print(a)
