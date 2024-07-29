from rich.table import Table
from inspect import signature


def get_table_data(table: Table):
    header = tuple(row.header for row in table.columns)
    rows = list(zip(*[row.cells for row in table.columns]))
    return header, rows


def get_table_style(table: Table):
    dict_of_styles = table.__dict__
    valid_keys = set(
        param.name for param in signature(Table.__init__).parameters.values()
    )
    validated_style_dict = {
        key: dict_of_styles[key] for key in dict_of_styles if key in valid_keys
    }

    return validated_style_dict
