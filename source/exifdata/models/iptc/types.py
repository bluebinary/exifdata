from __future__ import annotations

import re
import datetime

from exifdata.logging import logger

from exifdata.framework import (
    Value,
)

from deliciousbytes import (
    Encoding,
    ByteOrder,
    Long,
    Short,
    Bytes,
    String,
    Int,
)


logger = logger.getChild(__name__)


class Value(Value):
    @property
    def value(self) -> object:
        return self


class Short(Short, Value):
    @classmethod
    def decode(cls, value: bytes, **kwargs) -> Short:
        if not isinstance(value, bytes):
            raise TypeError("The 'value' argument must have a 'bytes' value!")

        return Short(Int.decode(value, **kwargs))


class Long(Long, Value):
    @classmethod
    def decode(cls, value: bytes, **kwargs) -> Long:
        if not isinstance(value, bytes):
            raise TypeError("The 'value' argument must have a 'bytes' value!")

        return Long(Int.decode(value, **kwargs))


class String(String, Value):
    def __new__(cls, value: str, **kwargs):
        # As the String class from deliciousbytes subclasses 'str' we can only pass the
        # string value to the superclass' __new__ method; however, the kwargs are passed
        # automatically to all of the superclass' __init__ methods, including Value.
        return super().__new__(cls, value)

    @classmethod
    def decode(
        cls,
        value: bytes,
        order: ByteOrder = ByteOrder.MSB,
        encoding: Encoding = Encoding.Unicode,
    ) -> String:
        if not isinstance(value, bytes):
            raise TypeError("The 'value' argument must have a 'bytes' value!")

        return String(value.decode(encoding.value))
