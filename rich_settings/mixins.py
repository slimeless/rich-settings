from typing import Any


class DataclassActionMixin:
    def execute(self, dataclass: Any, field_name: str, current_value: Any):
        setattr(dataclass, field_name, current_value)
