"""Metaloader for JSON documents.
"""

# Standard library
from typing import (
    Any,
)

# Third party libraries
from ruamel import (
    yaml as _yaml,
)

# Local libraries
from metaloaders.exceptions import (
    MetaloaderError,
    MetaloaderNotImplemented,
)
from metaloaders.model import (
    Node,
)
from metaloaders.yaml import (
    Loader as YAMLLoader,
    load as load_as_yaml,
)
from metaloaders.json import (
    load as load_as_json,
)


class Loader(YAMLLoader):  # pylint: disable=abstract-method,too-many-ancestors
    """YAML loader with overridden constructors that propagate positions.

    In normal circumstances you should not use this directly, but it is left
    here in order to ease extension when needed.
    """


def load(stream: str, fmt: str) -> Node:
    if fmt in {'yml', 'yaml'}:
        return load_as_yaml(stream, loader_cls=Loader)

    if fmt in {'json'}:
        return load_as_json(stream)

    raise NotImplementedError(fmt)


def _multi_constructor(
    loader: Loader,
    tag_suffix: str,
    node: _yaml.Node,  # type: ignore
) -> Any:
    if tag_suffix not in {'Condition', 'Ref'}:
        tag_suffix = f'Fn::{tag_suffix}'

    if tag_suffix == "Fn::GetAtt":
        constructor: Any = construct_getatt
    elif isinstance(node, _yaml.ScalarNode):  # type: ignore
        constructor = loader.construct_scalar
    elif isinstance(node, _yaml.SequenceNode):  # type: ignore
        constructor = loader.construct_sequence
    elif isinstance(node, _yaml.MappingNode):  # type: ignore
        constructor = loader.construct_mapping
    else:
        raise MetaloaderNotImplemented(f'Bad tag: !{tag_suffix}')

    return {
        tag_suffix: constructor(node),
    }


def construct_getatt(
    node: _yaml.Node,  # type: ignore
) -> Any:
    if isinstance(node.value, str):
        return node.value.split(".", 1)

    if isinstance(node.value, list):
        return [s.value for s in node.value]

    raise MetaloaderError(f'Unexpected node type: {type(node.value)}')


def _override() -> None:
    Loader.add_multi_constructor("!", _multi_constructor)


# Side effects
_override()
