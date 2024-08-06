
# Rich Form Library

## Motivation

The Rich Form library was created to provide an easy and visually appealing way to render and interact with forms in the terminal using the Rich library. The idea for creating this library came after reading this [discussion](https://github.com/Textualize/rich/discussions/1785)

## Installation

To install the Rich Form library, you can use pip:

```bash
pip install rich-form
```

## Usage

### Basic Example

Here's a basic example to get you started with the Rich Form library:

```python
from rich.console import Console
from rich_form import Form, BoolField, LiteralField

@dataclass
class Example:
    accept_terms: bool = BoolField(field_name='any name', current=True, aliases=("Yes", "No"))
    favorite_color: str = LiteralField(values=('blue', 'magneta', 'pinky'), field_name='favorite color')

# Initialize the form
example = Example()
form = Form(example)

# Create a console and print the form
console = Console()
console.print(form)
```

### Styling

The Rich Form library allows you to customize the appearance of your forms using styles. You can define styles for different parts of the form:

```python
from rich_form import Form
from rich.style import Style
from rich_form import PanelStyle

selected_style = Style(color="black", bold=True, bgcolor="green")
panel_style = PanelStyle(title="[bold green]Data", border_style="green")

form = Form(example, panel_style=panel_style, selected_style=selected_style)
```

## Components

### Fields

- `BoolField`: A field for boolean values.
- `LiteralField`: A field for literal (string) values.

### Form

The `Form` class is the main component of the Rich Form library. It is used to render and manage the form:

```python
from rich_form import Form

form = Form(dataclass_instance)
```

### Exceptions

The library defines the following exceptions for error handling:

- `FieldValueException`
- `RichFieldException`

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue on GitHub.

## License

This project is licensed under the MIT License.
```
