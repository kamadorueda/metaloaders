# Standard library
import json

# Local libraries
from metajson import (
    JsonObject,
    load,
    Type,
)


def test_metajson_load_1() -> None:
    assert load("""
        "x"
    """) == JsonObject(
        data='x',
        data_type=Type.STRING,
        end_column=11,
        end_line=2,
        start_column=8,
        start_line=2,
    )


def test_metajson_load_2() -> None:
    data = {
        'a': 123,
        'b': True,
        'c': None,
        'd': "string",
    }
    data = [data]
    data = {"data": data}
    data = [data]
    data = {"data": data}

    assert load(json.dumps(data, indent=2)) == JsonObject(
        data={
            JsonObject(
                data='data',
                data_type=Type.STRING,
                end_column=8,
                end_line=2,
                start_column=2,
                start_line=2,
            ): JsonObject(
                data=[
                    JsonObject(
                        data={
                            JsonObject(
                                data='data',
                                data_type=Type.STRING,
                                end_column=12,
                                end_line=4,
                                start_column=6,
                                start_line=4,
                            ): JsonObject(
                                data=[
                                    JsonObject(
                                        data={
                                            JsonObject(
                                                data='a',
                                                data_type=Type.STRING,
                                                end_column=13,
                                                end_line=6,
                                                start_column=10,
                                                start_line=6,
                                            ): JsonObject(
                                                data=123,
                                                data_type=Type.NUMBER,
                                                end_column=18,
                                                end_line=6,
                                                start_column=15,
                                                start_line=6,
                                            ),
                                            JsonObject(
                                                data='b',
                                                data_type=Type.STRING,
                                                end_column=13,
                                                end_line=7,
                                                start_column=10,
                                                start_line=7,
                                            ): JsonObject(
                                                data=True,
                                                data_type=Type.TRUE,
                                                end_column=19,
                                                end_line=7,
                                                start_column=15,
                                                start_line=7,
                                            ),
                                            JsonObject(
                                                data='c',
                                                data_type=Type.STRING,
                                                end_column=13,
                                                end_line=8,
                                                start_column=10,
                                                start_line=8,
                                            ): JsonObject(
                                                data=None,
                                                data_type=Type.NULL,
                                                end_column=19,
                                                end_line=8,
                                                start_column=15,
                                                start_line=8,
                                            ),
                                            JsonObject(
                                                data='d',
                                                data_type=Type.STRING,
                                                end_column=13,
                                                end_line=9,
                                                start_column=10,
                                                start_line=9,
                                            ): JsonObject(
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
