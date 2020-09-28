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

At some point in your career you may deal with the problem of loading data
documents and knowing the positions (line and column) of
the elements.

Metaloaders deals with that for you!

We support JSON and YAML, and welcome contributions for other formats!.

# Installing

    $ pip install metaloaders

# Using

    >>> from metaloaders.json import load  # to import the JSON loader
    >>> load('{"foo": "bar"}')

    >>> from metaloaders.yaml import load  # to import the YAML loader
    >>> load('foo: bar')

Please read the documentation bellow for more details about every function.
"""
