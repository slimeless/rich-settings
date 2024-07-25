from rich.console import ConsoleOptions, Console
from rich.style import Style
from .base.abstract import AbstractForm
from readchar import readkey, key
from rich.live import Live
from .visualize import BaseVisualizeExecutor


class BaseForm(AbstractForm):
    def __init__(self, renderable: BaseVisualizeExecutor) -> None:
        self.renderable = renderable

    def render(self):
        with Live(self.renderable, auto_refresh=False) as live:
            while True:
                ch = readkey()
                if ch == key.UP or ch == "k":
                    self.renderable.selected = max(0, self.renderable.selected - 1)
                if ch == key.DOWN or ch == "j":
                    self.renderable.selected = min(
                        len(self.renderable.columns) - 1, self.renderable.selected + 1
                    )

                if ch == key.RIGHT or ch == "l":
                    self.renderable.validate()

                if ch == key.LEFT or ch == "h":
                    self.renderable.validate(negative=True)

                if ch == key.ENTER:
                    if hasattr(self.renderable, "execute_action_queue"):
                        self.renderable.execute_action_queue()
                        return

                live.update(self.renderable, refresh=True)

    def __rich_console__(self, console: Console, options: ConsoleOptions):
        from os import devnull

        file = open(devnull, "w")
        console.file = file
        self.render()
        return ""


class Form(BaseForm):
    def __init__(
        self,
        dataclass: ...,
        style: Style | str = None,
        selected_style: Style | str = None,
    ):
        from .visualize import MultiDataclassVisualizeExecutor

        super().__init__(MultiDataclassVisualizeExecutor(dataclass=dataclass))

    @classmethod
    def from_raw_boolean_dataclass(
        cls,
        dataclass: ...,
        style: Style | str = None,
        selected_style: Style | str = None,
    ):
        from .visualize import BoolDataclassVisualizeExecutor

        instance = cls.__new__(cls)

        super(Form, instance).__init__(
            renderable=BoolDataclassVisualizeExecutor(dataclass=dataclass)
        )

        return instance

    @classmethod
    def from_raw_literal_dataclass(
        cls,
        dataclass: ...,
        style: Style | str = None,
        selected_style: Style | str = None,
    ):
        from .visualize import LiteralDataclassVisualizeExecutor

        instance = cls.__new__(cls)
        super(Form, instance).__init__(
            renderable=LiteralDataclassVisualizeExecutor(dataclass=dataclass)
        )

        return instance
