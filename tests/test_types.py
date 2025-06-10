from exifdata.types import (
    ByteOrder,
    Int,
    Int8,
    Int16,
    Int32,
    Int64,
    UInt,
    UInt8,
    UInt16,
    UInt32,
    UInt64,
    Char,
    SignedLong,
    SignedChar,
    Long,
    SignedLong,
    LongLong,
    SignedLongLong,
    Bytes,
    Bytes8,
    Bytes16,
    Bytes32,
    Bytes64,
    Bytes128,
    Bytes256,
    String,
)

from conftest import print_bytes_hex


def test_byte_order():
    assert ByteOrder.MSB is ByteOrder.BigEndian
    assert ByteOrder.MSB is ByteOrder.Motorolla

    assert ByteOrder.LSB is ByteOrder.LittleEndian
    assert ByteOrder.LSB is ByteOrder.Intel


def test_int():
    value: Int = Int(4000050)

    assert isinstance(value, int)
    assert isinstance(value, Int)

    assert value == 4000050

    encoded: bytes = value.encode(order=ByteOrder.BigEndian)
    assert isinstance(encoded, bytes)
    assert encoded == b"\x00\x00\x00\x00\x00\x3d\x09\x32"

    encoded: bytes = value.encode(order=ByteOrder.LittleEndian)
    assert isinstance(encoded, bytes)
    assert encoded == b"\x32\x09\x3d\x00\x00\x00\x00\x00"


def test_int8():
    value: Int8 = Int8(127)

    assert isinstance(value, int)
    assert isinstance(value, Int)
    assert isinstance(value, Int8)

    assert value == 127

    encoded: bytes = value.encode(order=ByteOrder.BigEndian)
    assert isinstance(encoded, bytes)
    assert encoded == b"\x7f"

    encoded: bytes = value.encode(order=ByteOrder.LittleEndian)
    assert isinstance(encoded, bytes)
    assert encoded == b"\x7f"


def test_int8_overflow():
    value: Int8 = Int8(129)

    assert isinstance(value, int)
    assert isinstance(value, Int)
    assert isinstance(value, Int8)

    assert value == -127  # int8 129 overflows to -127

    encoded: bytes = value.encode(order=ByteOrder.BigEndian)
    assert isinstance(encoded, bytes)
    assert encoded == b"\x81"

    encoded: bytes = value.encode(order=ByteOrder.LittleEndian)
    assert isinstance(encoded, bytes)
    assert encoded == b"\x81"


def test_int16():
    value: Int16 = Int16(127)

    assert isinstance(value, int)
    assert isinstance(value, Int)
    assert isinstance(value, Int16)

    assert value == 127

    encoded: bytes = value.encode(order=ByteOrder.BigEndian)
    assert isinstance(encoded, bytes)
    assert encoded == b"\x00\x7f"

    encoded: bytes = value.encode(order=ByteOrder.LittleEndian)
    assert isinstance(encoded, bytes)
    assert encoded == b"\x7f\x00"


def test_int32():
    value: Int32 = Int32(127)

    assert isinstance(value, int)
    assert isinstance(value, Int)
    assert isinstance(value, Int32)

    assert value == 127

    encoded: bytes = value.encode(order=ByteOrder.BigEndian)
    assert isinstance(encoded, bytes)
    assert encoded == b"\x00\x00\x00\x7f"

    encoded: bytes = value.encode(order=ByteOrder.LittleEndian)
    assert isinstance(encoded, bytes)
    assert encoded == b"\x7f\x00\x00\x00"


def test_int64():
    value: Int64 = Int64(127)

    assert isinstance(value, int)
    assert isinstance(value, Int)
    assert isinstance(value, Int64)

    assert value == 127

    encoded: bytes = value.encode(order=ByteOrder.BigEndian)
    assert isinstance(encoded, bytes)
    assert encoded == b"\x00\x00\x00\x00\x00\x00\x00\x7f"

    encoded: bytes = value.encode(order=ByteOrder.LittleEndian)
    assert isinstance(encoded, bytes)
    assert encoded == b"\x7f\x00\x00\x00\x00\x00\x00\x00"


def test_uint8():
    value: UInt8 = UInt8(127)

    assert isinstance(value, int)
    assert isinstance(value, Int)
    assert isinstance(value, UInt)
    assert isinstance(value, UInt8)

    assert value == 127

    encoded: bytes = value.encode(order=ByteOrder.BigEndian)
    assert isinstance(encoded, bytes)
    assert encoded == b"\x7f"

    encoded: bytes = value.encode(order=ByteOrder.LittleEndian)
    assert isinstance(encoded, bytes)
    assert encoded == b"\x7f"


def test_uint8_overflow():
    value: UInt8 = UInt8(256)

    assert isinstance(value, int)
    assert isinstance(value, Int)
    assert isinstance(value, UInt)
    assert isinstance(value, UInt8)

    assert value == 0  # uint8 256 overflows to 0

    encoded: bytes = value.encode(order=ByteOrder.BigEndian)
    assert isinstance(encoded, bytes)
    assert encoded == b"\x00"

    encoded: bytes = value.encode(order=ByteOrder.LittleEndian)
    assert isinstance(encoded, bytes)
    assert encoded == b"\x00"


def test_uint16():
    value: UInt16 = UInt16(127)

    assert isinstance(value, int)
    assert isinstance(value, Int)
    assert isinstance(value, UInt)
    assert isinstance(value, UInt16)

    assert value == 127

    encoded: bytes = value.encode(order=ByteOrder.BigEndian)
    assert isinstance(encoded, bytes)
    assert encoded == b"\x00\x7f"

    encoded: bytes = value.encode(order=ByteOrder.LittleEndian)
    assert isinstance(encoded, bytes)
    assert encoded == b"\x7f\x00"


def test_uint32():
    value: UInt32 = UInt32(4000050)

    assert isinstance(value, int)
    assert isinstance(value, Int)
    assert isinstance(value, UInt)
    assert isinstance(value, UInt32)

    encoded: bytes = value.encode(order=ByteOrder.BigEndian)
    assert isinstance(encoded, bytes)
    assert encoded == b"\x00\x3d\x09\x32"

    encoded: bytes = value.encode(order=ByteOrder.LittleEndian)
    assert isinstance(encoded, bytes)
    assert encoded == b"\x32\x09\x3d\x00"


def test_bytes64():
    value: UInt32 = UInt32(4000050)

    assert isinstance(value, int)
    assert isinstance(value, Int)
    assert isinstance(value, UInt)
    assert isinstance(value, UInt32)

    value: Bytes64 = Bytes64(bytearray([byte for byte in bytes(value)]))

    assert isinstance(value, bytes)
    assert isinstance(value, Bytes)
    assert isinstance(value, Bytes64)

    encoded: bytes = value.encode(order=ByteOrder.MSB)
    assert isinstance(encoded, bytes)
    assert encoded == b"\x00\x00\x00\x00\x00\x3d\x09\x32"

    encoded: bytes = value.encode(order=ByteOrder.LSB)
    assert isinstance(encoded, bytes)
    assert encoded == b"\x32\x09\x3d\x00\x00\x00\x00\x00"
