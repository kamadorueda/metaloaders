"""A JSON Loader with column and line numbers.

[![Release](
https://img.shields.io/pypi/v/metajson?color=success&label=Release&style=flat-square)](
https://pypi.org/project/metajson)
[![Documentation](
https://img.shields.io/badge/Documentation-click_here!-success?style=flat-square)](
https://kamadorueda.github.io/metajson/)
[![Downloads](
https://img.shields.io/pypi/dm/metajson?label=Downloads&style=flat-square)](
https://pypi.org/project/metajson)
[![Status](
https://img.shields.io/pypi/status/metajson?label=Status&style=flat-square)](
https://pypi.org/project/metajson)
[![Coverage](
https://img.shields.io/badge/Coverage-100%25-success?style=flat-square)](
https://kamadorueda.github.io/metajson/)
[![License](
https://img.shields.io/pypi/l/metajson?color=success&label=License&style=flat-square)](
https://github.com/kamadorueda/metajson/blob/latest/LICENSE.md)

# Installing

    $ pip install metajson

# Using

    >>> from metajson import *  # to import everything

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


class Type(Enum):
    ARRAY: str = 'ARRAY'
    FALSE: str = 'FALSE'
    NUMBER: str = 'NUMBER'
    NULL: str = 'NULL'
    OBJECT: str = 'OBJECT'
    STRING: str = 'STRING'
    TRUE: str = 'TRUE'


class MetaJsonError(Exception):
    pass


class Object(NamedTuple):
    data: Any
    data_type: Type
    end_column: int
    end_line: int
    start_column: int
    start_line: int


def load(stream: str) -> Object:
    parser = lark.Lark(
        grammar=GRAMMAR,
        parser='lalr',
        lexer='standard',
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
