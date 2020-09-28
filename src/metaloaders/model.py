"""Collection of objects returned by the different loaders."""

# Standard library
from enum import (
    Enum,
)
from typing import (
    Any,
    NamedTuple,
)


class Type(Enum):
    """Enumeration for all possible `Node` data types."""
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


class Node(NamedTuple):
    """Represents any JSON token and its metadata."""
    data: Any
    """Contains the raw inner element data."""
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

    @property
    def inner(self) -> Any:
        """Access the wrapped data by this `Node`.

        The access method follow some rules:

        - Arrays are simplified 1 level: [a, b] -> [a.data, b.data]
        - Objects are simplified on its keys only: {a: b} -> {a.data: b}
        - Everything else returns the inner data as per `Node.data`
        """
        data: Any
        if self.data_type is Type.ARRAY:
            data = [val.data for val in self.data]
        elif self.data_type is Type.OBJECT:
            data = {key.data: val for key, val in self.data.items()}
        elif self.data_type in {
            Type.NULL,
            Type.NUMBER,
            Type.FALSE,
            Type.TRUE,
            Type.STRING,
        }:
            data = self.data
        else:
            raise NotImplementedError()

        return data
