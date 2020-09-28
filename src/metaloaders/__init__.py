"""JSON/YAML loaders with column and line numbers.

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

    >>> json.raw()['test'] == Node(
            data=123,
            data_type=Type.NUMBER,
            end_column=15,
            end_line=3,
            start_column=12,
            start_line=3,
        )

Every JSON token contains all possible metadata:

    >>> data_key = Node(
            data='test',
            data_type=Type.STRING,
            end_column=10,
            end_line=3,
            start_column=4,
            start_line=3,
        )
    >>> data_val = Node(
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
