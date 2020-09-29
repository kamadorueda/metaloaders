# Standard library
from typing import (
    Any,
)
# Local libraries
from metaloaders.model import (
    Node,
    Type,
)
from metaloaders.yaml import (
    load,
)


def test_load_1() -> None:
    pass


def test_load_2() -> None:
    pass


def test_load_3() -> None:
    yaml = load('test: 123')

    assert yaml.start_line == 1
    assert yaml.end_line == 1
    assert yaml.start_column == 0
    assert yaml.end_column == 9
    assert yaml.inner['test'] == Node(
        data=123,
        data_type=Type.NUMBER,
        end_column=9,
        end_line=1,
        start_column=6,
        start_line=1,
    )

    key = Node(
        data='test',
        data_type=Type.STRING,
        end_column=4,
        end_line=1,
        start_column=0,
        start_line=1,
    )
    val = Node(
        data=123,
        data_type=Type.NUMBER,
        end_column=9,
        end_line=1,
        start_column=6,
        start_line=1,
    )
    assert yaml.data == {key: val}
