from abc import ABC, abstractmethod
from typing import Any

from rich.console import Console, ConsoleOptions, RenderResult


class AbstractField(ABC):

    @abstractmethod
    def validate(self, *args, **kwargs):
        pass

    @abstractmethod
    def action(self, *args, **kwargs):
        pass


class AbstractVisualizeExecutor(ABC):

    @abstractmethod
    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        pass

    @abstractmethod
    def _execute_action(self, *args, **kwargs):
        pass

    @abstractmethod
    def _validate(self, *args, **kwargs):
        pass
