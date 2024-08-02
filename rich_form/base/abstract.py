from abc import ABC, abstractmethod
from typing import Any

from rich.console import Console, ConsoleOptions, RenderResult


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
    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        pass

    @abstractmethod
    def validate(self, *args, **kwargs):
        pass


class AbstractForm(ABC):

    @abstractmethod
    def render(self) -> Any:
        pass
