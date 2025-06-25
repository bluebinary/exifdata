import pytest

from exifdata.models.iptc.types import (
    ByteOrder,
    Short,
    Long,
    String,
)


def test_type_short():
    """Test the IPTC metadata field Short unsigned data type."""

    # Note that IPTC's short is unsigned, unlike the signed C-standard short type
    encoded = Short(value=123)

    assert encoded.signed is False

    assert isinstance(encoded, Short)
    assert isinstance(encoded, int)

    # As `Short` is a subclass of `int` we can compare values directly
    assert encoded == 123
    assert encoded.value == 123
    assert encoded.encode(order=ByteOrder.MSB) == b"\x00\x7b"
    assert encoded.encode(order=ByteOrder.LSB) == b"\x7b\x00"

    # 0x01 0xc8 (MSB) == 456
    decoded = Short.decode(value=b"\x01\xc8", order=ByteOrder.MSB)

    assert isinstance(decoded, Short)
    assert isinstance(decoded, int)

    # As `Short` is a subclass of `int` we can compare values directly
    assert decoded == 456
    assert decoded.value == 456
    assert decoded.encode(order=ByteOrder.MSB) == b"\x01\xc8"
    assert decoded.encode(order=ByteOrder.LSB) == b"\xc8\x01"


def test_type_long():
    """Test the IPTC metadata field Long data type."""

    encoded = Long(value=123)

    assert isinstance(encoded, Long)
    assert isinstance(encoded, int)

    # As `Long` is a subclass of `int` we can compare values directly
    assert encoded == 123
    assert encoded.value == 123
    assert encoded.encode(order=ByteOrder.MSB) == b"\x00\x00\x00\x7b"
    assert encoded.encode(order=ByteOrder.LSB) == b"\x7b\x00\x00\x00"

    # 0x01 0xc8 0x01 0xc8 (MSB) == 29884872
    decoded = Long.decode(value=b"\x01\xc8\x01\xc8", order=ByteOrder.MSB)

    assert isinstance(decoded, Long)
    assert isinstance(decoded, int)

    # As `Long` is a subclass of `int` we can compare values directly
    assert decoded == 29884872
    assert decoded.value == 29884872
    assert decoded.encode(order=ByteOrder.MSB) == b"\x01\xc8\x01\xc8"
    assert decoded.encode(order=ByteOrder.LSB) == b"\xc8\x01\xc8\x01"


def test_type_string():
    """Test the IPTC metadata field String data type."""

    encoded = String(value="hello")

    assert isinstance(encoded, String)
    assert isinstance(encoded, str)

    # As String is a subclass of 'str' we can compare values directly
    assert encoded == "hello"

    assert encoded.value == "hello"
    assert encoded.encode() == b"hello"

    decoded = String.decode(b"hello")

    assert isinstance(decoded, String)
    assert isinstance(decoded, str)

    # As String is a subclass of 'str' we can compare values directly
    assert decoded == "hello"

    assert decoded.value == "hello"
    assert decoded.encode() == b"hello"
