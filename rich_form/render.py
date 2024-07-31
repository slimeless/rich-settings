from readchar import readkey, key
from rich.console import Console
from rich.live import Live
from rich.style import Style
from rich.table import Table

from .base.abstract import AbstractForm
from .base.styles import PanelStyle
from .visualize import BaseVisualizeExecutor


class BaseForm(AbstractForm):
    def __init__(self, renderable: BaseVisualizeExecutor) -> None:
        self.renderable = renderable

    def _render(self):
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
                        res = self.renderable.execute_action_queue()
                        return res

                live.update(self.renderable, refresh=True)

    def render(self, console: Console):
        from os import devnull

        file = open(devnull, "w")
        console.file = file
        res = self._render()
        return res


class Form(BaseForm):
    def __init__(
        self,
        dataclass: ...,
        panel: PanelStyle = None,
        selected_style: Style | str = None,
    ):
        from .visualize import MultiDataclassVisualizeExecutor

        super().__init__(
            renderable=MultiDataclassVisualizeExecutor(
                dataclass=dataclass, selected_style=selected_style, panel=panel
            )
        )

    @classmethod
    def from_raw_boolean_dataclass(
        cls,
        dataclass: ...,
        panel: PanelStyle = None,
        selected_style: Style | str = None,
    ):
        from .visualize import BoolDataclassVisualizeExecutor

        instance = cls.__new__(cls)

        super(Form, instance).__init__(
            renderable=BoolDataclassVisualizeExecutor(
                dataclass=dataclass, selected_style=selected_style, panel=panel
            )
        )

        return instance

    @classmethod
    def from_raw_literal_dataclass(
        cls,
        dataclass: ...,
        panel: PanelStyle = None,
        selected_style: Style | str = None,
    ):
        from .visualize import LiteralDataclassVisualizeExecutor

        instance = cls.__new__(cls)
        super(Form, instance).__init__(
            renderable=LiteralDataclassVisualizeExecutor(
                dataclass=dataclass, selected_style=selected_style, panel=panel
            )
        )

        return instance

    @classmethod
    def from_rich_table(cls, table: Table):
        from .visualize import StaticTableVisualizeExecutor

        instance = cls.__new__(cls)
        super(Form, instance).__init__(
            renderable=StaticTableVisualizeExecutor(table=table)
        )

        return instance
