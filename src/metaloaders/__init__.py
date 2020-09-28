"""A JSON Loader with column and line numbers.

[![Release](
https://img.shields.io/pypi/v/metaloaders?color=success&label=Release&style=flat-square)](
https://pypi.org/project/metaloaders)
[![Documentation](
https://img.shields.io/badge/Documentation-click_here!-success?style=flat-square)](
https://kamadorueda.github.io/metaloaders/)
[![Downloads](
https://img.shields.io/pypi/dm/metaloaders?label=Downloads&style=flat-square)](
https://pypi.org/project/metaloaders)
[![Status](
https://img.shields.io/pypi/status/metaloaders?label=Status&style=flat-square)](
https://pypi.org/project/metaloaders)
[![Coverage](
https://img.shields.io/badge/Coverage-100%25-success?style=flat-square)](
https://kamadorueda.github.io/metaloaders/)
[![License](
https://img.shields.io/pypi/l/metaloaders?color=success&label=License&style=flat-square)](
https://github.com/kamadorueda/metaloaders/blob/latest/LICENSE.md)

# Rationale

At some point in your career you may deal with the problem of loading a JSON
document with the requirement of knowing the positions (line and column) of
the elements.

Metajson deals with that for you.

Let's load a simple JSON document:

    >>> from metaloaders import load

    >>> stream = \"""
    ... {
    ...     "test": 123
    ... }
    ... \"""

    >>> json = load(stream)

Now you can access the outer object meta-data:

    >>> json.raw(recursive=True) == {'test': 123}
        json.start_line == 2
        json.end_line == 4
        json.start_column == 0
        json.end_column == 1

As well as child objects meta-data:

    >>> json.raw()['test'] == Object(
            data=123,
            data_type=Type.NUMBER,
            end_column=15,
            end_line=3,
            start_column=12,
            start_line=3,
        )

Every JSON token contains all possible metadata:

    >>> data_key = Object(
            data='test',
            data_type=Type.STRING,
            end_column=10,
            end_line=3,
            start_column=4,
            start_line=3,
        )
    >>> data_val = Object(
            data=123,
            data_type=Type.NUMBER,
            end_column=15,
            end_line=3,
            start_column=12,
            start_line=3,
        )
    >>> json.data == {data_key: data_val}

# Installing

    $ pip install metaloaders

# Using

    >>> from metaloaders import *  # to import everything

Please read the documentation bellow for more details about every function.
"""

# Standard library
import ast
from enum import (
    Enum,
)
from typing import (
    Any,
    NamedTuple,
    Optional,
)

# Third party libraries
import lark


# Constants
GRAMMAR = r"""
    ?start: value

    ?value: array
          | object
          | number
          | string
          | "false" -> false
          | "null" -> null
          | "true" -> true

    array  : "[" [value ("," value)*] "]"
    object : "{" [pair ("," pair)*] "}"
    number : SIGNED_NUMBER
    pair   : string ":" value
    string : ESCAPED_STRING

    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.WS

    %ignore WS
"""


class MetaJsonError(Exception):
    """Base exception for all errors within this package."""


class Type(Enum):
    """Enumeration for all possible `Object` data types."""
    ARRAY: str = 'ARRAY'
    """Indicates an array data-type: Example: `[]`"""
    FALSE: str = 'FALSE'
    """Indicates a boolean data-type: Example: `false`"""
    NUMBER: str = 'NUMBER'
    """Indicates a numeric data-type: Example: `123.4`"""
    NULL: str = 'NULL'
    """Indicates a null data-type: Example: `null`"""
    OBJECT: str = 'OBJECT'
    """Indicates an object data-type: Example: `{}`"""
    STRING: str = 'STRING'
    """Indicates a string data-type: Example: `"example"`"""
    TRUE: str = 'TRUE'
    """Indicates a boolean data-type: Example: `true`"""


class Object(NamedTuple):
    """Represents any JSON token and its metadata."""
    data: Any
    """Contains the inner element data."""
    data_type: Type
    """Defines the inner element type."""
    end_column: int
    """End column for the element."""
    end_line: int
    """End line for the element."""
    start_column: int
    """Start column for the element."""
    start_line: int
    """Start line for the element."""

    def raw(self, recursive: bool = False) -> Any:
        """Simplifies the inner element so it's easier to work with."""
        data: Any
        if self.data_type is Type.ARRAY:
            data = [val.raw(recursive=recursive) for val in self.data]
        elif self.data_type is Type.FALSE:
            data = self.data
        elif self.data_type is Type.NUMBER:
            data = self.data
        elif self.data_type is Type.NULL:
            data = self.data
        elif self.data_type is Type.OBJECT:
            data = {
                key.raw(): (
                    val.raw(recursive=recursive)
                    if recursive
                    else val
                )
                for key, val in self.data.items()
            }
        elif self.data_type is Type.STRING:
            data = self.data
        elif self.data_type is Type.TRUE:
            data = self.data
        else:
            raise NotImplementedError(data)

        return data


def load(stream: str) -> Object:
    """Loads a string representation of a JSON document as an `Object` class.

    Raises `MetaJsonError` if any parsing error occur.
    """
    parser = lark.Lark(
        grammar=GRAMMAR,
        parser='lalr',
        propagate_positions=True,
    )

    try:
        obj = parser.parse(stream)
    except lark.exceptions.LarkError as exc:
        raise MetaJsonError(f'Unable to parse stream: {exc}')
    else:
        data: Object = _simplify(obj)
        return data


def _simplify(obj: Any) -> Any:
    data: Any
    data_type: Optional[Type]

    if isinstance(obj, lark.Tree):
        if obj.data == 'object':
            data = dict(map(_simplify, obj.children))
            data_type = Type.OBJECT
        elif obj.data == 'array':
            data = list(map(_simplify, obj.children))
            data_type = Type.ARRAY
        elif obj.data == 'pair':
            data = (
                _simplify(obj.children[0]),
                _simplify(obj.children[1]),
            )
            data_type = None
        elif obj.data == 'null':
            data = None
            data_type = Type.NULL
        elif obj.data == 'true':
            data = True
            data_type = Type.TRUE
        elif obj.data == 'false':
            data = False
            data_type = Type.FALSE
        elif obj.data == 'string':
            data = ast.literal_eval(obj.children[0].value)  # type: ignore
            data_type = Type.STRING
        elif obj.data == 'number':
            data = ast.literal_eval(obj.children[0].value)  # type: ignore
            data_type = Type.NUMBER
        else:
            raise NotImplementedError(obj)
    else:
        raise NotImplementedError(obj)

    return data if data_type is None else Object(
        data=data,
        data_type=data_type,
        end_column=obj.end_column - 1,  # type: ignore
        end_line=obj.end_line,  # type: ignore
        start_column=obj.column - 1,  # type: ignore
        start_line=obj.line,  # type: ignore
    )
