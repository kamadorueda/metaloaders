# Standard library
import ast
from typing import (
    Any,
    Optional,
)

# Third party libraries
import lark

# Local libraries
from metaloaders.exceptions import (
    MetaloaderError,
)
from metaloaders.model import (
    Node,
    Type,
)

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


def load(stream: str) -> Node:
    """Loads a string representation of a JSON document as an `Node` class.

    Raises `MetaloaderError` if any parsing error occur.
    """
    parser = lark.Lark(
        grammar=GRAMMAR,
        parser='lalr',
        propagate_positions=True,
    )

    try:
        obj = parser.parse(stream)
    except lark.exceptions.LarkError as exc:
        raise MetaloaderError(f'Unable to parse stream: {exc}')
    else:
        data: Node = _simplify(obj)
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

    return data if data_type is None else Node(
        data=data,
        data_type=data_type,
        end_column=obj.end_column - 1,  # type: ignore
        end_line=obj.end_line,  # type: ignore
        start_column=obj.column - 1,  # type: ignore
        start_line=obj.line,  # type: ignore
    )
