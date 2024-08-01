#!/usr/bin/env python3
"""
function's parameters and return values with the appropriate types
"""
from typing import Mapping, Any, Union, TypeVar


T = TypeVar('T')
Resultype = Union[Any, T]
Defaultype = Union[T, None]


def safely_get_value(dct: Mapping, key: Any,
                     default: Defaultype = None) -> Resultype:
    """
    returns the value
    """
    if key in dct:
        return dct[key]
    else:
        return default
