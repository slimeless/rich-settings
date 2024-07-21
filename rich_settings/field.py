from abc import ABC
from itertools import cycle, islice
from queue import Queue
from typing import Tuple

from .base.abstract import AbstractField
from functools import partial


class FieldBase[FieldType](AbstractField, ABC):
    __action_queue = Queue()
    _value_type = FieldType
    current_value = None
    current_alias = None

    def __init__(self, values: Tuple[FieldType] | Tuple[FieldType, FieldType], alias: Tuple[str] | Tuple[str, str]) -> None:
        if self.__validate_val_and_alias(values, alias):
            self.values = values
            self.alias = alias

    @staticmethod
    def __validate_val_and_alias(val: Tuple, alias: Tuple) -> bool:
        if len(val) != len(alias):
            raise ValueError('Values and aliases must be the same length')  # !
        if type(val) is not Tuple[FieldType]:
            raise ValueError(f'Values must be a {FieldType}')
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

    def validate(self, negative: bool = False, put_action: bool = True, **kwargs) -> None:
        self.__move_current(negative)
        index = self.values.index(self.current_value)
        self.current_alias = self.alias[index]
        if put_action:
            self.__action_queue.put(partial(self.action, **kwargs))



