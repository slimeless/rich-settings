from functools import partial
from typing import Tuple, Any

from .base.abstract import AbstractField
from .mixins import DataclassActionMixin
from .base.exc import FieldValueException


class FieldBase[FieldType](AbstractField):
    value_type = FieldType
    current_value = None
    current_alias = None

    def __init__(self, values: Tuple[FieldType, ...], alias: Tuple[str, ...] = None, current=None) -> None:
        if not alias:
            alias = tuple([str(x) for x in values])
        try:
            self.__validate_val_and_alias(val=values, alias=alias, current=current)
            self.values = values
            self.alias = alias
            self.current_value = current if current is not None else values[0]
            self.current_alias = self.alias[self.values.index(self.current_value)]
        except Exception as e:
            raise e

    def __validate_val_and_alias(self, val: Tuple, alias: Tuple, current: Any) -> None:
        if self.value_type is not Any:
            if not all(isinstance(x, self.value_type) for x in val):
                raise FieldValueException(f"Values must be of type {FieldType}")
        if len(val) != len(alias):
            raise FieldValueException("Values and aliases must be the same length")  # !
        if len(val) == 0 or len(alias) == 0:
            raise FieldValueException("Values and aliases must not be empty")
        if current not in val and current is not None:
            raise FieldValueException(f"Current value must be one of {val}")

    def __move_current(self, negative: bool) -> None:
        if not self.values:
            raise ValueError("The values list is empty")

        current_index = self.values.index(self.current_value)
        total_values = len(self.values)

        if negative:
            next_index = (current_index - 1) % total_values
        else:
            next_index = (current_index + 1) % total_values
        self.current_value = self.values[next_index]
        self.current_alias = self.alias[next_index]

    def validate(self, negative: bool = False, *args, **kwargs) -> None:
        self.__move_current(negative)
        if kwargs.get("put_action") and hasattr(self, "action"):
            action_func = self.action
            return partial(action_func)

    def __str__(self):
        return self.current_alias


class BaseDataclassField(FieldBase, DataclassActionMixin):

    def __init__(self, field_name: str, values: Tuple[Any, ...], alias: Tuple[str, ...], current=None):
        self.field_name = field_name
        super().__init__(values=values, alias=alias, current=current)

    def action(self, dataclass: Any):
        self.execute(dataclass, self.field_name, self.current_value)


class BoolField(BaseDataclassField):
    value_type = bool

    def __init__(
            self,
            field_name: str,
            current: bool = None,
            aliases: Tuple[str, str] = ("ON", "OFF"),
    ):
        values = (True, False)
        super().__init__(current=current, alias=aliases, values=values, field_name=field_name)


class LiteralField(BaseDataclassField):
    value_type = Any

    def __init__(
            self,
            values: Tuple[Any, ...],
            field_name: str,
            alias: Tuple[str, ...] = None,
            current: Any = None,
    ):
        super().__init__(current=current, values=values, alias=alias, field_name=field_name)


class StaticField(FieldBase[Any]):
    value_type = Any

    def __init__(self, values: Tuple[Any, ...], current=None):
        super().__init__(values=values, current=current)

    def __iter__(self):
        return iter(self.values)

    def validate(self, *args, **kwargs) -> None:
        pass
