from __future__ import annotations

import re
import datetime
import enumerific
import fractions

from exifdata.logging import logger

from exifdata.models import (
    Type,
    Value,
)

from exifdata import types

from exifdata.types import (
    ByteOrder,
    Encoding,
    Int,
    UInt8,
    UInt16,
    UInt32,
    Short,
    Long,
)


logger = logger.getChild(__name__)


class Empty(Value):
    """An empty value."""

    _tagid: int = 0


class Byte(Value):
    """An 8-bit unsigned integer."""

    _tagid: int = 1


class ASCII(Value):
    """An 8-bit byte containing one 7-bit ASCII code. The final byte is terminated with
    NULL[00.H]. The ASCII count shall include NULL."""

    _tagid: int = 2

    def encode(self, order: ByteOrder = ByteOrder.MSB) -> bytes:
        if not isinstance(self.value, str):
            raise ValueError(
                "The %s class does not have a string value!" % (self.__class__.__name__)
            )

        encoded = self.value.encode("ASCII")

        if order is ByteOrder.LSB:
            encoded = bytes(reversed(bytearray(encoded)))

        return encoded

    @classmethod
    def decode(cls, value: bytes, order: ByteOrder = ByteOrder.MSB) -> ASCII:
        if not isinstance(value, bytes):
            raise ValueError("The 'value' argument must have a bytes value!")

        if order is ByteOrder.LSB:
            value = bytes(reversed(bytearray(value)))

        decoded: str = value.decode("ASCII")

        return ASCII(value=decoded)


class Short(Short, Value):
    """A 16-bit (2-byte) unsigned integer."""

    _tagid: int = 3

    @classmethod
    def decode(cls, value: bytes) -> Short:
        if not isinstance(value, bytes):
            raise TypeError("The 'value' argument must have a 'bytes' value!")

        return Short(Int.decode(value))


class Long(Value):
    """A 32-bit (4-byte) unsigned integer."""

    _tagid: int = 4


class Rational(Value):
    """Two long integers used to hold a rational number. The first long is the numerator
    and the second long expresses the denominator."""

    _tagid: int = 5

    def __init__(
        self,
        value: float | str = None,
        numerator: int = None,
        denominator: int = None,
        **kwargs,
    ):
        if value is None:
            if not isinstance(numerator, int):
                raise ValueError(
                    "If no 'value' argument has been specified, both the 'numerator' and 'denominator' arguments must be specified!"
                )
            if not isinstance(denominator, int):
                raise ValueError(
                    "If no 'value' argument has been specified, both the 'numerator' and 'denominator' arguments must be specified as integers!"
                )
        elif isinstance(value, (int, float, str)):
            if isinstance(value, int):
                numerator = value
                denominator = 1
            elif fraction := fractions.Fraction(value):
                numerator = int(fraction.numerator)
                denominator = int(fraction.denominator)
            else:
                raise ValueError("The 'value' could not be parsed into a fraction!")
        else:
            raise ValueError(
                "Either the 'value' or 'numerator' and 'denominator' arguments must be specified!"
            )

        self.numerator = numerator
        self.denominator = denominator

        super().__init__(value=f"{numerator}/{denominator}", **kwargs)

    @property
    def numerator(self) -> types.Long:
        return self._numerator

    @numerator.setter
    def numerator(self, numerator: int):
        if not isinstance(numerator, int):
            raise TypeError("The 'numerator' argument must have an integer value!")
        self._numerator = types.Long(numerator)

    @property
    def denominator(self) -> types.Long:
        return self._denominator

    @denominator.setter
    def denominator(self, denominator: int):
        if not isinstance(denominator, int):
            raise TypeError("The 'denominator' argument must have an integer value!")
        self._denominator = types.Long(denominator)

    def encode(self, order: ByteOrder = ByteOrder.MSB) -> bytes:
        encoded: list[bytes] = []

        encoded.append(self.numerator.encode(order=order))

        encoded.append(self.denominator.encode(order=order))

        return b"".join(encoded)

    @classmethod
    def decode(cls, value: bytes, order: ByteOrder = ByteOrder.MSB) -> Rational:
        if not isinstance(value, bytes):
            raise TypeError("The 'value' argument must have a bytes value!")

        if not len(value) == 4:  # 4 bytes * 8 bits = 32 bits (two UInt16s)
            raise ValueError(
                "The provided bytes 'value' is not the expected length of 4 bytes (32 bits)!"
            )

        numerator: UInt16 = UInt16.decode(value[0:2], order=order)

        denominator: UInt16 = UInt16.decode(value[2:4], order=order)

        return Rational(numerator=numerator, denominator=denominator)


class Undefined(Value):
    """An 8-bit byte that may take any value depending on the field definition."""

    _tagid: int = 7


class LongSigned(Value):
    """A 32-bit (4-byte) signed integer (2's complement notation)."""

    _tagid: int = 9


class RationalSigned(Value):
    """Two signed long integers. The first signed long is the numerator and the second
    signed long is the denominator."""

    _tagid: int = 10


class UTF8(Value):
    """An 8-bit byte representing a string according to UTF-8[22]. The final byte is
    terminated with NULL[00.H]. A BOM (Byte Order Mark) shall not be used. The UTF-8
    count shall include NULL. This is defined independently by this standard, rather
    than in TIFF 6.0."""

    _tagid: int = 129


class DateTime(Value):
    def __init__(
        self, value: str | datetime.datetime, format: str = "%Y-%m-%d %H:%M:%S"
    ):
        if isinstance(value, str):
            value = datetime.datetime.strptime(value, format)
        elif isinstance(value, datetime.datetime):
            pass
        else:
            raise TypeError(
                "The 'value' must either be a date represented as a string or a datetime instance!"
            )

        if not isinstance(value, datetime.datetime):
            raise ValueError(
                "The 'value' must be a valid date that can be represented as a datetime instance!"
            )

        super().__init__(value=value.strftime(format))

    def encode(
        self, order: ByteOrder = ByteOrder.MSB, encoding: Encoding = Encoding.UTF8
    ) -> bytes:
        encoded = self.value.encode(encoding.value)

        if order is ByteOrder.MSB:
            pass
        elif order is ByteOrder.LSB:
            encoded = bytes(reversed(bytearray(encoded)))

        return encoded

    @classmethod
    def decode(
        cls,
        value: bytes,
        order: ByteOrder = ByteOrder.MSB,
        encoding: Encoding = Encoding.UTF8,
    ) -> DateTime:
        if not isinstance(value, bytes):
            raise TypeError("The 'value' argument must have a bytes value!")

        if order is ByteOrder.LSB:
            decoded = bytes(reversed(bytearray(value)))

        decoded = value.decode(encoding.value)

        return DateTime(value=decoded)


# class Type(Type, aliased=True):
#     Byte = Byte
#     ASCII = ASCII
#     Short = Short
#     Long = Long
#     Rational = Rational
#     Undefined = Undefined
#     LongSigned = LongSigned
#     RationalSigned = RationalSigned
#     UTF8 = UTF8
