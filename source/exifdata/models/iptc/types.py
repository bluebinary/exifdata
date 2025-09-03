from __future__ import annotations

import unicodedata

from exifdata.logging import logger

from exifdata.framework import (
    Value,
)

from deliciousbytes import (
    ByteOrder,
    UnsignedShort,
    UnsignedLong,
    String,
    Int,
)

logger = logger.getChild(__name__)


class Value(Value):
    @property
    def value(self) -> object:
        return self


class Short(UnsignedShort, Value):
    @classmethod
    def decode(cls, value: bytes, **kwargs) -> Short:
        if not isinstance(value, bytes):
            raise TypeError("The 'value' argument must have a 'bytes' value!")

        return Short(Int.decode(value, **kwargs))


class Long(UnsignedLong, Value):
    @classmethod
    def decode(cls, value: bytes, **kwargs) -> Long:
        if not isinstance(value, bytes):
            raise TypeError("The 'value' argument must have a 'bytes' value!")

        return Long(Int.decode(value, **kwargs))


class String(String, Value):
    _replacements: dict[str, str] = {
        # The copyright symbol "©" (ordinal 169) is outside the 7-bit ASCII range, 0-128
        # and is common in fields like the Copyright field, so here we replace it with
        # the traditionally used ASCII-compatible "(c)" replacement:
        "©": "(c)",
    }

    def __new__(cls, value: str, **kwargs):
        # As the String class from deliciousbytes subclasses 'str' we can only pass the
        # string value to the superclass' __new__ method; however, the kwargs are passed
        # automatically to all of the superclass' __init__ methods, including Value.
        return super().__new__(cls, value)

    @classmethod
    def add_replacement(cls, search: str, replacement: str):
        """Supports the replacement of strings that may appear in metadata that contains
        characters that are outside the ASCII 7-bit character range, with strings that
        are suitable for use in ASCII-only strings for IPTC metadata."""

        if not isinstance(search, str):
            raise TypeError("The 'search' argument must have a string value!")
        elif len(search.strip()) == 0:
            raise ValueError(
                "The 'search' argument must have a non-empty string value!"
            )

        if not isinstance(replacement, str):
            raise TypeError("The 'replacement' argument must have a string value!")
        elif len(replacement.strip()) == 0:
            raise ValueError(
                "The 'replacement' argument must have a non-empty string value!"
            )
        else:
            try:
                replacement.encode("ASCII")
            except UnicodeError:
                raise ValueError(
                    "The 'replacement' argument must contain an ASCII-compatible string value!"
                )

        cls._replacements[search] = replacement

    def __len__(self) -> int:
        """Return the length of the encoded string to ensure any normalisation or string
        replacements are accounted for in determining the length of the record."""

        return len(self.encode())

    def encode(self, order: ByteOrder = ByteOrder.MSB) -> bytes:
        if not isinstance(value := self.value, str):
            raise ValueError(
                "The %s class does not have a string value!" % (self.__class__.__name__)
            )

        # Normalise non-ASCII characters where possible to their closest ASCII equivalents
        value = unicodedata.normalize("NFKD", value)

        # Filter out the combining characters from the expanded form, such as diacritics
        value = "".join([char for char in value if not unicodedata.combining(char)])

        # Check the string value for the presence of any of the search strings; if
        # one or more are found, replace them with their replacements before encoding;
        # to avoid replacements reformatted strings can be provided that are ASCII-only:
        for search, replacement in self.__class__._replacements.items():
            value = value.replace(search, replacement)

        # Encode the source string, replacing any other characters outside of the ASCII
        # range with a "?" placeholder to indicate the presence of a character that was
        # supplied to the method but should not have been present in an ASCII string:
        encoded: bytes = value.encode("ASCII", errors="replace")

        # IPTC-IIM strings do not need to end with a NUL byte as the length is provided
        # as part of the encoding of the record, immediately before the string value, so
        # that the parsing code knows how many bytes of data are used by the string.
        # if not encoded.endswith(b"\x00"): encoded += b"\x00"

        # Byte order is not relevant for data types that have individual values which
        # fit within single bytes, such as ASCII encoded characters from an ASCII string
        if order is ByteOrder.LSB:
            # encoded = bytes(reversed(bytearray(encoded)))
            pass

        return encoded

    @classmethod
    def decode(cls, value: bytes, order: ByteOrder = ByteOrder.MSB) -> String:
        if not isinstance(value, bytes):
            raise TypeError("The 'value' argument must have a bytes value!")

        # Byte order is not relevant for data types that have individual values which
        # fit within single bytes, such as ASCII encoded characters from an ASCII string
        if order is ByteOrder.LSB:
            # value = bytes(reversed(bytearray(value)))
            pass

        try:
            decoded: str = value.decode("ASCII")
        except UnicodeError:
            decoded: str = value.decode("UTF-8")

        return String(value=decoded)
