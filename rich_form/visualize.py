from queue import Queue
from typing import Tuple, Any, Literal, get_args
from dataclasses import fields as dataclass_fields
from rich.console import ConsoleOptions, RenderResult, Console
from rich.panel import Panel
from rich.style import Style
from rich.table import Table

from .base.abstract import AbstractVisualizeExecutor, AbstractField
from .base.styles import SELECTED, PanelStyle
from .field import BaseBoolField, BoolField, LiteralField


class BaseVisualizeExecutor[FieldType: AbstractField](AbstractVisualizeExecutor):
    action_queue = Queue()

    def __init__(
        self,
        fields: Tuple[FieldType, ...],
        columns: Tuple[str, ...],
        selected_style: Style | str = None,
        panel: PanelStyle = None,
    ):
        self.fields = fields
        self.columns = columns
        self.selected_style = selected_style if selected_style else SELECTED
        self.panel = panel
        self.selected = 0

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        table = Table(box=None, show_header=False)
        for i, *row in enumerate(zip(self.columns, self.fields)):
            table.add_row(
                *(str(x) for x in row[0]),
                style=self.selected_style if i == self.selected else None,
            )

        yield Panel.fit(
            table,
            **self.panel.__dict__
            if self.panel
            else {"border_style": "blue", "title": "[bold blue]Fields"},
        )

    def validate(self, negative: bool = False) -> None:
        field = self.fields[self.selected]
        put_action = True if hasattr(field, "action") else False
        maybe_action = field.validate(negative, put_action=put_action)
        if maybe_action:
            self.action_queue.put(maybe_action)


class BoolVisualizeExecutor(BaseVisualizeExecutor[BaseBoolField]):
    def __init__(
        self,
        columns: Tuple[str, ...],
        selected_style: str | Style = None,
        panel: PanelStyle = None,
    ):
        fields = tuple(BaseBoolField() for _ in range(len(columns)))
        super().__init__(
            fields=fields, columns=columns, selected_style=selected_style, panel=panel
        )


class BoolDataclassVisualizeExecutor(BaseVisualizeExecutor[BoolField]):
    def __init__(
        self,
        dataclass: Any,
        selected_style: str | Style = None,
        panel: PanelStyle = None,
    ):
        self.dataclass = dataclass
        columns = tuple(
            str(key.name)
            for key in dataclass_fields(self.dataclass)
            if key.type is bool
        )
        fields = tuple(
            BoolField(field_name=key.name, current=key.default)
            for key in dataclass_fields(self.dataclass)
            if key.name in columns
        )
        super().__init__(
            fields=fields, columns=columns, selected_style=selected_style, panel=panel
        )

    def execute_action_queue(self):
        while not self.action_queue.empty():
            action = self.action_queue.get()
            action(self.dataclass)


class LiteralDataclassVisualizeExecutor(BaseVisualizeExecutor[LiteralField]):
    def __init__(
        self,
        dataclass: Any,
        selected_style: str | Style = None,
        panel: PanelStyle = None,
    ):
        self.dataclass = dataclass
        columns = tuple(
            str(key.name)
            for key in dataclass_fields(self.dataclass)
            if type(key.type) is type(Literal[""])
        )

        fields = tuple(
            LiteralField(
                values=get_args(key.type),
                field_name=key.name,
                current=key.default,
                alias=tuple(str(x) for x in get_args(key.type)),
            )
            for key in dataclass_fields(self.dataclass)
            if str(key.name) in columns
        )
        super().__init__(
            fields=fields, columns=columns, selected_style=selected_style, panel=panel
        )

    def execute_action_queue(self):
        while not self.action_queue.empty():
            action = self.action_queue.get()
            action(self.dataclass)


class MultiDataclassVisualizeExecutor(BaseVisualizeExecutor[AbstractField]):
    def __init__(
        self,
        dataclass: Any,
        selected_style: str | Style = None,
        panel: PanelStyle = None,
    ):
        self.dataclass = dataclass
        columns = tuple(
            str(key.name)
            for key in dataclass_fields(self.dataclass)
            if isinstance(key.type, AbstractField)
        )
        fields = tuple(
            field.default
            for field in dataclass_fields(self.dataclass)
            if str(field.name) in columns
        )
        super().__init__(
            fields=fields, columns=columns, selected_style=selected_style, panel=panel
        )

    def execute_action_queue(self):
        while not self.action_queue.empty():
            action = self.action_queue.get()
            action(self.dataclass)
