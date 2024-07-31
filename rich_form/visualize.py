from dataclasses import fields as dataclass_fields
from queue import Queue
from typing import Tuple, Any, Literal, get_args

from rich.console import ConsoleOptions, RenderResult, Console
from rich.panel import Panel
from rich.style import Style
from rich.table import Table

from .base.abstract import AbstractVisualizeExecutor, AbstractField
from .base.styles import SELECTED, PanelStyle, BASIC
from .base.utils import get_table_data, get_table_style
from .field import BoolField, LiteralField, StaticField


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
        self.panel = panel if panel else BASIC
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

        yield Panel.fit(table, **self.panel.__dict__)

    def validate(self, negative: bool = False) -> None:
        field = self.fields[self.selected]
        put_action = True if hasattr(field, "action") else False
        maybe_action = field.validate(negative, put_action=put_action)
        if maybe_action:
            self.action_queue.put(maybe_action)


class BaseDataclassVisualizeExecutor(BaseVisualizeExecutor[AbstractField]):
    def __init__(
        self,
        dataclass: Any,
        columns: Tuple[str, ...],
        fields: Tuple[AbstractField, ...],
        selected_style: str | Style = None,
        panel: PanelStyle = None,
    ) -> None:
        self.dataclass = dataclass
        super().__init__(
            fields=fields, columns=columns, selected_style=selected_style, panel=panel
        )

    def execute_action_queue(self):
        while not self.action_queue.empty():
            action = self.action_queue.get()
            action(self.dataclass)


class BoolDataclassVisualizeExecutor(BaseDataclassVisualizeExecutor):
    def __init__(
        self,
        dataclass: Any,
        selected_style: str | Style = None,
        panel: PanelStyle = None,
    ):
        columns = tuple(
            str(key.name) for key in dataclass_fields(dataclass) if key.type is bool
        )
        fields = tuple(
            BoolField(field_name=key.name, current=key.default)
            for key in dataclass_fields(dataclass)
            if key.name in columns
        )
        super().__init__(
            fields=fields,
            columns=columns,
            selected_style=selected_style,
            panel=panel,
            dataclass=dataclass,
        )


class LiteralDataclassVisualizeExecutor(BaseDataclassVisualizeExecutor):
    def __init__(
        self,
        dataclass: Any,
        selected_style: str | Style = None,
        panel: PanelStyle = None,
    ):
        columns = tuple(
            str(key.name)
            for key in dataclass_fields(dataclass)
            if type(key.type) is type(Literal[""])
        )

        fields = tuple(
            LiteralField(
                values=get_args(key.type),
                field_name=key.name,
                current=key.default,
                alias=tuple(str(x) for x in get_args(key.type)),
            )
            for key in dataclass_fields(dataclass)
            if str(key.name) in columns
        )
        super().__init__(
            fields=fields,
            columns=columns,
            selected_style=selected_style,
            panel=panel,
            dataclass=dataclass,
        )


class MultiDataclassVisualizeExecutor(BaseDataclassVisualizeExecutor):
    def __init__(
        self,
        dataclass: Any,
        selected_style: str | Style = None,
        panel: PanelStyle = None,
    ):
        columns = tuple(
            str(key.name)
            for key in dataclass_fields(dataclass)
            if isinstance(key.default, AbstractField)
        )
        fields = tuple(
            field.default
            for field in dataclass_fields(dataclass)
            if str(field.name) in columns
        )
        super().__init__(
            fields=fields,
            columns=columns,
            selected_style=selected_style,
            panel=panel,
            dataclass=dataclass,
        )


class StaticTableVisualizeExecutor(BaseVisualizeExecutor[StaticField]):
    def __init__(
        self,
        table: Table,
    ):
        columns, rows = get_table_data(table)
        fields = tuple(StaticField(row) for row in rows)
        self.table_style = get_table_style(table)
        super().__init__(fields=fields, columns=columns)

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        table = Table(**self.table_style)
        for column in self.columns:
            table.add_column(column)
        for i, field in enumerate(self.fields):
            table.add_row(
                *list(field), style=self.selected_style if i == self.selected else None
            )

        yield table

    def execute_action_queue(self):
        headers = self.columns
        return {
            header: data for header, data in zip(headers, self.fields[self.selected])
        }
