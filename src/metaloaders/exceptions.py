"""Exceptions raised by this package."""


class MetaloaderError(Exception):
    """Base exception for all errors within this package."""


class MetaloaderNotImplemented(MetaloaderError):
    """Something is yet not implemented in the library."""
