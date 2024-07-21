from itertools import cycle, islice
from queue import Queue
from typing import Tuple, Any

from .base.abstract import AbstractField, AbstractActionMixin


class FieldBase[FieldType](AbstractField):
    _value_type = FieldType
    current_value = None
    current_alias = None

    def __init__(self, values: Tuple[FieldType] | Tuple[FieldType, FieldType],
                 alias: Tuple[str] | Tuple[str, str]) -> None:
        if self.__validate_val_and_alias(values, alias):
            self.values = values
            self.alias = alias

    @staticmethod
    def __validate_val_and_alias(val: Tuple, alias: Tuple) -> bool:
        if len(val) != len(alias):
            raise ValueError('Values and aliases must be the same length')  # !
        if type(val) is not Tuple[FieldType]:
            raise ValueError(f'Values must be a {FieldType}')
        if len(val) == 0 or len(alias) == 0:
            return True

    def __move_current(self, negative: bool) -> None:
        if not self.current_value:
            self.current_value = self.values[0]
        else:
            if negative:
                iter_current = islice(cycle(reversed(self.values)), self.values.index(self.current_value), None)
            else:
                iter_current = islice(cycle(self.values), self.values.index(self.current_value), None)
            self.current_value = next(iter_current)

    def validate(self, negative: bool = False, put_action: bool = False, **kwargs) -> None:
        self.__move_current(negative)
        index = self.values.index(self.current_value)
        self.current_alias = self.alias[index]

    def __str__(self):
        return self.current_alias


class BoolField(FieldBase[bool]):
    def __init__(self):
        super().__init__(values=(True, False), alias=('Yes', 'No'))


class FlagDataclassField(BoolField, AbstractActionMixin):
    __action_queue = Queue()

    def action(self, dataclass: Any, field_name: str):
        setattr(dataclass, field_name, self.current_value)
