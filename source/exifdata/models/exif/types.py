from __future__ import annotations

import datetime
import fractions

from exifdata.logging import logger

from exifdata.framework import (
    Type,
    Value,
)

from deliciousbytes import (
    ByteOrder,
    Encoding,
    Int,
    UInt8,
    UInt16,
    UInt32,
    Short,
    UnsignedShort,
    SignedShort,
    Long,
    UnsignedLong,
    SignedLong,
)


logger = logger.getChild(__name__)


# The EXIF metadata standard defines the following data types:

# | ID | Type                   |  Format    | Size             |
# |----|------------------------|------------|------------------|
# | 0  | Empty                  |            | 0 bytes          |
# | 1  | Unsigned Byte          | byte       | 1-byte, 8-bits   |
# | 2  | ASCII String           | const char | 1-byte, 8-bits   |
# | 3  | Unsigned Short         | short      | 2-bytes, 16-bits |
# | 4  | Unsigned Long          | long       | 4-bytes, 32-bits |
# | 5  | Unsigned Rational      | two longs  | 8 bytes, 64-bits |
# | 6  | Signed Byte            | byte       | 1-byte, 8-bits   |
# | 7  | Undefined              |            | 1-byte, 8-bits   |
# | 8  | Signed Short           | short      | 2-bytes, 16-bits |
# | 9  | Signed Long            | long       | 4-bytes, 32-bits |
# | 10 | Signed Rational        | two longs  | 8 bytes, 64-bits |
# | 11 | Single-Precision Float | float      | 4-bytes, 32-bits |
# | 12 | Double-Precision Float | double     | 8-bytes, 64-bits |


class Empty(Value):
    """An empty value."""

    _tagid: int = 0
    _length: int = 1


class Byte(Int, Value):
    """An 8-bit unsigned integer."""

    _tagid: int = 1
    _length: int = 1
    _signed: bool = False


class ASCII(Value):
    """An 8-bit byte containing one 7-bit ASCII code. The final byte is terminated with
    NULL[00.H]. The ASCII count shall include the terminating NULL."""

    _tagid: int = 2
    _length: int = 1

    def encode(self, order: ByteOrder = ByteOrder.MSB) -> bytes:
        if not isinstance(self.value, str):
            raise ValueError(
                "The %s class does not have a string value!" % (self.__class__.__name__)
            )

        encoded: bytes = self.value.encode("ASCII")

        # Byte order is not relevant for data types that have individual values which
        # fit within single bytes, such as ASCII encoded characters from an ASCII string
        if order is ByteOrder.LSB:
            # encoded = bytes(reversed(bytearray(encoded)))
            pass

        return encoded

    @classmethod
    def decode(cls, value: bytes, order: ByteOrder = ByteOrder.MSB) -> ASCII:
        if not isinstance(value, bytes):
            raise ValueError("The 'value' argument must have a bytes value!")

        # Byte order is not relevant for data types that have individual values which
        # fit within single bytes, such as ASCII encoded characters from an ASCII string
        if order is ByteOrder.LSB:
            # value = bytes(reversed(bytearray(value)))
            pass

        decoded: str = value.decode("ASCII")

        return ASCII(value=decoded)


class Short(UnsignedShort, Value):
    """A 16-bit (2-byte) unsigned integer."""

    _tagid: int = 3
    _length: int = 2
    _signed: bool = False

    @classmethod
    def decode(cls, value: bytes) -> Short:
        if not isinstance(value, bytes):
            raise TypeError("The 'value' argument must have a 'bytes' value!")

        return Short(Int.decode(value))


class Long(UnsignedLong, Value):
    """A 32-bit (4-byte) unsigned integer."""

    _tagid: int = 4
    _length: int = 4
    _signed: bool = False


class Rational(Value):
    """Two unsigned long integers used to hold a rational number. The first long is the
    numerator and the second long expresses the denominator. Occupies 8-bytes, 64-bits.
    """

    _tagid: int = 5
    _length: int = 8
    _signed: bool = False

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
    def numerator(self) -> Long:
        return self._numerator

    @numerator.setter
    def numerator(self, numerator: int):
        if not isinstance(numerator, int):
            raise TypeError("The 'numerator' argument must have an integer value!")

        if self._signed is True:
            self._numerator = SignedLong(numerator)
        elif self._signed is False:
            self._numerator = UnsignedLong(numerator)

    @property
    def denominator(self) -> Long:
        return self._denominator

    @denominator.setter
    def denominator(self, denominator: int):
        if not isinstance(denominator, int):
            raise TypeError("The 'denominator' argument must have an integer value!")

        if self._signed is True:
            self._denominator = SignedLong(denominator)
        elif self._signed is False:
            self._denominator = UnsignedLong(denominator)

    def encode(self, order: ByteOrder = ByteOrder.MSB) -> bytes:
        encoded: list[bytes] = []

        encoded.append(self.numerator.encode(order=order))

        encoded.append(self.denominator.encode(order=order))

        return b"".join(encoded)

    @classmethod
    def decode(cls, value: bytes, order: ByteOrder = ByteOrder.MSB) -> Rational:
        if not isinstance(value, bytes):
            raise TypeError("The 'value' argument must have a bytes value!")

        # Expect value to be 8 bytes, 64 bits in length for two long (32-bit) integers
        if not (length := len(value)) == 8:
            raise ValueError(
                "The provided bytes 'value' does not have the expected length of 8 bytes (64 bits), but rather: %d!"
                % (length)
            )

        if cls._signed is True:
            numerator: SignedLong = SignedLong.decode(value[0:4], order=order)
            denominator: SignedLong = SignedLong.decode(value[4:8], order=order)
        elif cls._signed is False:
            numerator: UnsignedLong = UnsignedLong.decode(value[0:4], order=order)
            denominator: UnsignedLong = UnsignedLong.decode(value[4:8], order=order)

        return Rational(numerator=numerator, denominator=denominator)


class SignedByte(Byte, Value):
    """An 8-bit signed integer."""

    _tagid: int = 6
    _length: int = 1
    _signed: bool = True


class Undefined(Value):
    """An 8-bit byte that may take any value depending on the field definition."""

    _tagid: int = 7
    _length: int = 1


class LongSigned(SignedLong, Value):
    """A 32-bit (4-byte) signed integer (2's complement notation)."""

    _tagid: int = 9
    _length: int = 4
    _signed: bool = True


class RationalSigned(Rational):
    """Two signed long integers. The first signed long is the numerator and the second
    signed long is the denominator. Occupies 8-bytes, 64-bits."""

    _tagid: int = 10
    _length: int = 8
    _signed: bool = True


class UTF8(Value):
    """An 8-bit byte representing a string according to UTF-8[22]. The final byte is
    terminated with NULL[00.H]. A BOM (Byte Order Mark) shall not be used. The UTF-8
    count shall include NULL. This is defined independently by this standard, rather
    than in TIFF 6.0."""

    _tagid: int = 129
    _length: int = 1


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


__all__ = [
    "Empty",
    "Byte",
    "ASCII",
    "Short",
    "Long",
    "Rational",
    "SignedByte",
    "Undefined",
    "LongSigned",
    "RationalSigned",
    "UTF8",
    "DateTime",
]
