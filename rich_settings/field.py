from functools import partial
from itertools import cycle, islice
from typing import Tuple, Any

from .base.abstract import AbstractField


class FieldBase[FieldType](AbstractField):
    _value_type = FieldType
    current_value = None
    current_alias = None

    def __init__(
        self, values: Tuple[FieldType, FieldType], alias: Tuple[str, str]
    ) -> None:
        if self.__validate_val_and_alias(values, alias):
            self.values = values
            self.alias = alias

    def __validate_val_and_alias(self, val: Tuple, alias: Tuple) -> bool:
        if len(val) != len(alias):
            raise ValueError("Values and aliases must be the same length")  # !
        if not all([isinstance(x, self._value_type) for x in val]):
            raise ValueError(f"Values must be a {self._value_type}")
        if len(val) == 0 or len(alias) == 0:
            return True

    def __move_current(self, negative: bool) -> None:
        if not self.current_value:
            self.current_value = self.values[0]
        else:
            if negative:
                iter_current = islice(
                    cycle(reversed(self.values)),
                    self.values.index(self.current_value),
                    None,
                )
            else:
                iter_current = islice(
                    cycle(self.values), self.values.index(self.current_value), None
                )
            self.current_value = next(iter_current)

    def validate(self, negative: bool = False, *args, **kwargs) -> None:
        self.__move_current(negative)
        index = self.values.index(self.current_value)
        self.current_alias = self.alias[index]

    def __str__(self):
        return self.current_alias


class BoolField(FieldBase[bool]):
    _value_type = bool

    def __init__(self, current_value: bool = None):
        values = (True, False)
        aliases = ("Yes", "No")
        super().__init__(values=values, alias=aliases)

        self.values = values
        self.alias = aliases
        self.current_value = current_value if current_value is not None else values[0]
        self.current_alias = self.alias[self.values.index(self.current_value)]

    def __move_current(self, *args, **kwargs) -> None:
        self.current_value = not self.current_value


class BoolDataclassField(BoolField):
    def __init__(self, field_name: str, current_value: bool = None):
        self.field_name = field_name
        super().__init__(current_value=current_value)

    def action(self, dataclass: Any):
        setattr(dataclass, self.field_name, self.current_value)

    def __move_current(self, *args, **kwargs) -> None:
        self.current_value = not self.current_value

    def validate(self, put_action: bool = False, *args, **kwargs) -> None:
        self.__move_current()
        index = self.values.index(self.current_value)
        self.current_alias = self.alias[index]
        if put_action:
            return partial(self.action)
