from abc import ABC, abstractmethod
from typing import Any

from rich.console import Console, ConsoleOptions, RenderResult


class AbstractActionMixin(ABC):
    @abstractmethod
    def action(self, *args, **kwargs):
        pass


class AbstractActionExecutorMixin(ABC):
    @abstractmethod
    def execute_action(self, *args, **kwargs):
        pass


class AbstractField(ABC):
    current_value = None
    current_alias = None

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def validate(self, *args, **kwargs):
        pass


class AbstractVisualizeExecutor(ABC):

    @abstractmethod
    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        pass

    @abstractmethod
    def validate(self, *args, **kwargs):
        pass
