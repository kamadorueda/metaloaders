"""Metaloader for YAML documents.

Let's load a simple YAML document:

    >>> from metaloaders import load

    >>> yaml = load('test: 123')

Now you can access the outer object meta-data:

    >>> yaml.start_line == 1
        yaml.end_line == 1
        yaml.start_column == 0
        yaml.end_column == 9

As well as child objects meta-data:

    >>> yaml.inner['test'] == Node(
            data=123,
            data_type=Type.NUMBER,
            end_column=9,
            end_line=1,
            start_column=6,
            start_line=1,
        )

Every YAML token contains all possible metadata:

    >>> yaml.data == {key: val}
        # Where:
        #
        # key = Node(
        #     data='test',
        #     data_type=Type.STRING,
        #     end_column=4,
        #     end_line=1,
        #     start_column=0,
        #     start_line=1,
        # )
        #
        # val = Node(
        #     data=123,
        #     data_type=Type.NUMBER,
        #     end_column=9,
        #     end_line=1,
        #     start_column=6,
        #     start_line=1,
        # )
"""

# Standard library
from collections.abc import (
    Generator,
)
from contextlib import (
    suppress,
)
from functools import (
    wraps as mimic_function,
)
from typing import (
    Any,
    Callable,
    List,
)

# Third party library
from ruamel import (
    yaml as _yaml,
)

# Local libraries
from metaloaders.model import (
    Node,
    Type,
)
from metaloaders.exceptions import (
    MetaloaderError,
)


def load(stream: str) -> Node:
    """Loads a string representation of a document.

    Raises `metaloaders.exceptions.MetaloaderError` if any parsing error occur.
    """
    # pylint: disable=protected-access
    items: List[Node] = []
    loader = Loader(stream)

    try:
        while loader._constructor.check_data():
            items.append(loader._constructor.get_data())
    except _yaml.YAMLError as exc:  # type: ignore
        raise MetaloaderError(f'Unable to parse stream: {exc}')
    else:
        if len(items) == 0:
            return Node(
                data=None,
                data_type=Type.NULL,
                end_column=0,
                end_line=1,
                start_column=0,
                start_line=1,
            )

        if len(items) == 1:
            return items[0]

        return Node(
            data=items,
            data_type=Type.ARRAY,
            end_column=items[-1].end_column,
            end_line=items[-1].end_line,
            start_column=items[0].start_column,
            start_line=items[0].start_line,
        )
    finally:
        loader._parser.dispose()
        with suppress(AttributeError):
            loader._reader.reset_reader()
        with suppress(AttributeError):
            loader._scanner.reset_scanner()


class Loader(  # pylint: disable=abstract-method,too-many-ancestors
    _yaml.SafeLoader,  # type: ignore
):
    """YAML loader with overridden constructors that propagate positions.

    In normal circumstances you should not use this directly, but it is left
    here in order to ease extension when needed.
    """


def _factory(constructor: str, data_type: Type) -> Callable[..., Node]:

    constructor_func = getattr(Loader, f'construct_{constructor}')

    @mimic_function(constructor_func)
    def wrapper(
        self: Loader,
        node: _yaml.Node,  # type: ignore
        *args: Any,
        **kwargs: Any,
    ) -> Node:
        result = constructor_func(self, node, *args, **kwargs)

        if isinstance(result, Generator):
            result = tuple(result)
            result = result[0] if len(result) == 1 else result

        return Node(
            data=result,
            data_type=data_type,
            end_column=node.end_mark.column,
            end_line=node.end_mark.line + 1,
            start_column=node.start_mark.column,
            start_line=node.start_mark.line + 1,
        )

    return wrapper


def _override() -> None:
    for data_type, constructor, tag in [
        (Type.ARRAY, 'yaml_pairs', 'tag:yaml.org,2002:pairs'),
        (Type.ARRAY, 'yaml_set', 'tag:yaml.org,2002:set'),
        (Type.ARRAY, 'yaml_seq', 'tag:yaml.org,2002:seq'),
        (Type.BINARY, 'yaml_binary', 'tag:yaml.org,2002:binary'),
        (Type.BOOLEAN, 'yaml_bool', 'tag:yaml.org,2002:bool'),
        (Type.DATETIME, 'yaml_timestamp', 'tag:yaml.org,2002:timestamp'),
        (Type.NULL, 'yaml_null', 'tag:yaml.org,2002:null'),
        (Type.NUMBER, 'yaml_int', 'tag:yaml.org,2002:int'),
        (Type.NUMBER, 'yaml_float', 'tag:yaml.org,2002:float'),
        (Type.OBJECT, 'yaml_omap', 'tag:yaml.org,2002:omap'),
        (Type.OBJECT, 'yaml_map', 'tag:yaml.org,2002:map'),
        (Type.STRING, 'yaml_str', 'tag:yaml.org,2002:str'),
    ]:
        Loader.add_constructor(tag, _factory(constructor, data_type))


# Side effects
_override()
