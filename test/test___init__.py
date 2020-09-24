# Standard library
from json import (
    dumps as dump,
)
import textwrap
from typing import (
    Any,
)
# Local libraries
from metajson import (
    Object,
    load,
    Type,
)


def test_metajson_load_1() -> None:
    assert load("""
        "x"
    """) == Object(
        data='x',
        data_type=Type.STRING,
        end_column=11,
        end_line=2,
        start_column=8,
        start_line=2,
    )


def test_metajson_load_2() -> None:
    data: Any = {
        'a': 123,
        'b': True,
        'c': None,
        'd': "string",
    }
    data = [data]
    data = {"data": data}
    data = [data]
    data = {"data": data}

    assert load(dump(data, indent=2)) == Object(
        data={
            Object(
                data='data',
                data_type=Type.STRING,
                end_column=8,
                end_line=2,
                start_column=2,
                start_line=2,
            ): Object(
                data=[
                    Object(
                        data={
                            Object(
                                data='data',
                                data_type=Type.STRING,
                                end_column=12,
                                end_line=4,
                                start_column=6,
                                start_line=4,
                            ): Object(
                                data=[
                                    Object(
                                        data={
                                            Object(
                                                data='a',
                                                data_type=Type.STRING,
                                                end_column=13,
                                                end_line=6,
                                                start_column=10,
                                                start_line=6,
                                            ): Object(
                                                data=123,
                                                data_type=Type.NUMBER,
                                                end_column=18,
                                                end_line=6,
                                                start_column=15,
                                                start_line=6,
                                            ),
                                            Object(
                                                data='b',
                                                data_type=Type.STRING,
                                                end_column=13,
                                                end_line=7,
                                                start_column=10,
                                                start_line=7,
                                            ): Object(
                                                data=True,
                                                data_type=Type.TRUE,
                                                end_column=19,
                                                end_line=7,
                                                start_column=15,
                                                start_line=7,
                                            ),
                                            Object(
                                                data='c',
                                                data_type=Type.STRING,
                                                end_column=13,
                                                end_line=8,
                                                start_column=10,
                                                start_line=8,
                                            ): Object(
                                                data=None,
                                                data_type=Type.NULL,
                                                end_column=19,
                                                end_line=8,
                                                start_column=15,
                                                start_line=8,
                                            ),
                                            Object(
                                                data='d',
                                                data_type=Type.STRING,
                                                end_column=13,
                                                end_line=9,
                                                start_column=10,
                                                start_line=9,
                                            ): Object(
                                                data='string',
                                                data_type=Type.STRING,
                                                end_column=23,
                                                end_line=9,
                                                start_column=15,
                                                start_line=9,
                                            ),
                                        },
                                        data_type=Type.OBJECT,
                                        end_column=9,
                                        end_line=10,
                                        start_column=8,
                                        start_line=5,
                                    ),
                                ],
                                data_type=Type.ARRAY,
                                end_column=7,
                                end_line=11,
                                start_column=14,
                                start_line=4,
                            ),
                        },
                        data_type=Type.OBJECT,
                        end_column=5,
                        end_line=12,
                        start_column=4,
                        start_line=3,
                    ),
                ],
                data_type=Type.ARRAY,
                end_column=3,
                end_line=13,
                start_column=10,
                start_line=2,
            ),
        },
        data_type=Type.OBJECT,
        end_column=1,
        end_line=14,
        start_column=0,
        start_line=1,
    )


def test_metajson_load_3() -> None:
    stream = textwrap.dedent("""
    {
        "test": 123
    }
    """)

    json = load(stream)

    assert json.start_line == 2
    assert json.end_line == 4
    assert json.start_column == 0
    assert json.end_column == 1
    assert json.raw(recursive=True) == {'test': 123}
    assert json.raw() == {
        'test': Object(
            data=123,
            data_type=Type.NUMBER,
            end_column=15,
            end_line=3,
            start_column=12,
            start_line=3,
        ),
    }
    data_key = Object(
        data='test',
        data_type=Type.STRING,
        end_column=10,
        end_line=3,
        start_column=4,
        start_line=3,
    )
    data_val = Object(
        data=123,
        data_type=Type.NUMBER,
        end_column=15,
        end_line=3,
        start_column=12,
        start_line=3,
    )
    assert json.data == {data_key: data_val}
