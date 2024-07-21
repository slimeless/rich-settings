from typing import Tuple
from rich.table import Table
from rich.panel import Panel
from rich.style import Style
from rich.console import ConsoleOptions, RenderResult, Console

from .base.abstract import AbstractVisualizeExecutor, AbstractActionMixin, AbstractActionExecutorMixin, AbstractField
from .base.styles import SELECTED


class BaseVisualizeExecutor(AbstractVisualizeExecutor):

    def __init__(self, fields: Tuple[AbstractField, AbstractField], columns: Tuple[str, str], style: Style = SELECTED):
        self.fields = fields
        self.columns = columns
        self.style = style
        self.selected = 0

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        table = Table(box=None, show_header=False)
        for i, *row in enumerate(zip(self.columns, self.fields)):
            table.add_row(*(str(x) for x in row[0]), style=self.style if i == self.selected else None)

        yield Panel.fit(table, border_style='blue', title_align='right', title="[bold blue]Settings", style='none',
                        subtitle_align='left', subtitle=f'[bold blue]{self.selected}')

    def validate(self, negative: bool = False) -> None:
        field = self.fields[self.selected]
        put_action = True if isinstance(field, AbstractActionMixin) else False
        field.validate(negative, put_action)


