from functools import partial
from itertools import cycle, islice
from typing import Tuple, Any

from .base.abstract import AbstractField


class FieldBase[FieldType](AbstractField):
    _value_type = FieldType
    current_value = None
    current_alias = None

    def __init__(
        self, values: Tuple[FieldType, FieldType], alias: Tuple[str, str], current=None
    ) -> None:
        try:
            self.__validate_val_and_alias(val=values, alias=alias, current=current)
            self.values = values
            self.alias = alias
            self.current_value = current if current is not None else values[0]
            self.current_alias = self.alias[self.values.index(self.current_value)]
        except Exception as e:
            raise e

    def __validate_val_and_alias(self, val: Tuple, alias: Tuple, current: Any) -> None:
        if len(val) != len(alias):
            raise ValueError("Values and aliases must be the same length")  # !
        if not all([isinstance(x, self._value_type) for x in val]):
            raise ValueError(f"Values must be a {self._value_type}")
        if len(val) == 0 or len(alias) == 0:
            raise ValueError("Values and aliases must not be empty")
        if current not in val and current is not None:
            raise ValueError(f"Current value must be one of {val}")

    def __move_current(self, negative: bool) -> None:
        match negative, len(self.values):
            case False, 2:
                iter_current = cycle(self.values)
            case True, 2:
                iter_current = cycle(reversed(self.values))
            case True, _:
                iter_current = islice(
                    cycle(reversed(self.values)),
                    self.values.index(self.current_value),
                    None,
                )

            case False, _:
                iter_current = islice(
                    cycle(self.values), self.values.index(self.current_value), None
                )
            case _:
                raise ValueError("Something went wrong!")
        self.current_value = next(iter_current)
        index = self.values.index(self.current_value)
        self.current_alias = self.alias[index]

    def validate(self, negative: bool = False, *args, **kwargs) -> None:
        self.__move_current(negative)
        if kwargs.get("put_action") and hasattr(self, "action"):
            action_func = self.action
            return partial(action_func)

    def __str__(self):
        return self.current_alias


class BoolField(FieldBase[bool]):
    _value_type = bool

    def __init__(self, aliases: Tuple[str, str] = ("ON", "OFF"), current=None):
        values = (True, False)
        super().__init__(values=values, alias=aliases, current=current)


class BoolDataclassField(BoolField):
    def __init__(self, field_name: str, current: bool = None):
        self.field_name = field_name
        super().__init__(current=current)

    def action(self, dataclass: Any):
        setattr(dataclass, self.field_name, self.current_value)
