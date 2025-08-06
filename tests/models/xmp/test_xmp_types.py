import base64
import datetime

from exifdata.models.xmp.types import (
    Boolean,
    Integer,
    Real,
    Rational,
    Date,
    Text,
    Time,
    TimecodeFormat,
    Timecode,
    Bytes,
    Unicode,
    ASCII,
)


def test_type_integer():
    encoded = Integer(value=123)

    assert isinstance(encoded, Integer)
    assert isinstance(encoded, int)

    # As Integer is a subclass of 'int' we can compare values directly
    assert encoded == 123

    assert encoded.value == 123
    assert encoded.encode() == b"123"

    decoded = Integer.decode(b"456")

    # As Integer is a subclass of 'int' we can compare values directly
    assert decoded == 456

    assert decoded.value == 456
    assert decoded.encode() == b"456"


def test_type_real():
    encoded = Real(value=123.456)

    assert isinstance(encoded, Real)
    assert isinstance(encoded, Real)

    # As Real is a subclass of 'float' we can compare values directly
    assert encoded == 123.456

    assert encoded.value == 123.456
    assert encoded.encode() == b"123.456"

    decoded = Real.decode(b"456.123")

    # As Real is a subclass of 'float' we can compare values directly
    assert decoded == 456.123

    assert decoded.value == 456.123
    assert decoded.encode() == b"456.123"


def test_type_rational():
    encoded = Rational(value=0.75)

    assert isinstance(encoded, Rational)
    assert isinstance(encoded, str)

    assert str(encoded) == "3/4"
    assert float(encoded) == 0.75
    assert encoded.value == "3/4"
    assert encoded.encode() == b"3/4"

    encoded.numerator = 1
    encoded.denominator = 2

    assert encoded.encode() == b"1/2"
    assert str(encoded) == "1/2"
    assert float(encoded) == 0.5
    assert encoded.value == "1/2"

    decoded = Rational.decode(b"4/9")

    assert decoded.numerator == 4
    assert decoded.denominator == 9
    assert float(decoded) == 0.4444444444444444
    assert str(decoded) == "4/9"
    assert decoded.encode() == b"4/9"


def test_type_boolean():
    encoded = Boolean(value=True)

    assert isinstance(encoded, Boolean)
    assert not isinstance(encoded, bool)  # we cannot subclass bool, so we don't do so

    assert encoded.value is True
    assert encoded.encode() == b"True"

    decoded = Boolean.decode(b"False")

    assert isinstance(decoded, Boolean)
    assert not isinstance(decoded, bool)

    assert decoded.value is False
    assert decoded.encode() == b"False"


def test_type_ascii():
    encoded = ASCII(value="hello")

    assert isinstance(encoded, ASCII)
    assert isinstance(encoded, str)

    assert encoded.value == "hello"
    assert encoded.encode() == b"hello"

    decoded = ASCII.decode(b"hello")

    assert isinstance(decoded, ASCII)
    assert isinstance(decoded, str)

    assert decoded.value == "hello"
    assert decoded.encode() == b"hello"


def test_type_unicode():
    encoded = Unicode(value="hello")

    assert isinstance(encoded, Unicode)
    assert isinstance(encoded, str)

    assert encoded.value == "hello"
    assert encoded.encode() == b"hello"

    decoded = Unicode.decode(b"hello")

    assert isinstance(decoded, Unicode)
    assert isinstance(decoded, str)

    assert decoded.value == "hello"
    assert decoded.encode() == b"hello"


def test_type_bytes():
    """Note that byte values cannot be stored directly in XMP; they must first be base64
    encoded; hence the testing of the Bytes class against a base64 encoded value."""

    encoded = Bytes(value=b"hello")

    testval: bytes = base64.b64encode(b"hello")

    assert isinstance(encoded, Bytes)
    assert isinstance(encoded, bytes)

    assert encoded.value == b"hello"
    assert encoded.encode() == testval

    decoded = Bytes.decode(testval)

    assert isinstance(decoded, Bytes)
    assert isinstance(decoded, bytes)

    assert decoded.value == b"hello"
    assert decoded.encode() == testval


def test_type_text():
    encoded = Text(value="hello")

    assert isinstance(encoded, Text)
    assert isinstance(encoded, str)

    assert encoded.value == "hello"
    assert encoded.encode() == b"hello"

    decoded = Text.decode(b"hello")

    assert isinstance(decoded, Text)
    assert isinstance(decoded, str)

    assert decoded.value == "hello"
    assert decoded.encode() == b"hello"


def test_type_datetime():
    encoded = Date(value="2025:02:04 11:43:23")

    assert isinstance(encoded, Date)
    assert isinstance(encoded, datetime.datetime)

    assert encoded.year == 2025
    assert encoded.month == 2
    assert encoded.day == 4
    assert encoded.hour == 11
    assert encoded.minute == 43
    assert encoded.second == 23

    # As the Date class is a subclass of datetime.datetime, we can compare directly
    assert encoded == datetime.datetime(2025, 2, 4, 11, 43, 23)

    assert str(encoded) == "2025-02-04 11:43:23"
    assert bytes(encoded) == b"2025-02-04 11:43:23"
    assert encoded.encode() == b"2025-02-04 11:43:23"

    decoded = Date.decode(b"2025:02:04 11:43:23")

    assert isinstance(decoded, Date)
    assert isinstance(decoded, datetime.datetime)

    # As the Date class is a subclass of datetime.datetime, we can compare directly
    assert decoded == datetime.datetime(2025, 2, 4, 11, 43, 23)
    assert str(decoded) == "2025-02-04 11:43:23"
    assert bytes(decoded) == b"2025-02-04 11:43:23"
    assert decoded.encode() == b"2025-02-04 11:43:23"


def test_type_time():
    encoded = Time(value="11:43:23")

    assert isinstance(encoded, Time)
    assert isinstance(encoded, datetime.time)

    assert encoded.hour == 11
    assert encoded.minute == 43
    assert encoded.second == 23

    # As the Time class is a subclass of datetime.time, we can compare directly
    assert encoded == datetime.time(11, 43, 23)
    assert str(encoded) == "11:43:23"
    assert bytes(encoded) == b"11:43:23"
    assert encoded.encode() == b"11:43:23"

    decoded = Time.decode(b"11:43:23")

    assert isinstance(decoded, Time)
    assert isinstance(decoded, datetime.time)

    # As the Time class is a subclass of datetime.time, we can compare directly
    assert decoded == datetime.time(11, 43, 23)
    assert str(decoded) == "11:43:23"
    assert bytes(decoded) == b"11:43:23"
    assert decoded.encode() == b"11:43:23"


def test_type_timecode():
    encoded = Timecode(value="11:43:23:12")

    assert isinstance(encoded, Timecode)
    assert isinstance(encoded, datetime.time)

    assert encoded.hour == 11
    assert encoded.minute == 43
    assert encoded.second == 23
    assert encoded.frame == 12

    assert encoded == datetime.time(11, 43, 23, 12)
    assert str(encoded) == "11:43:23:12"
    assert bytes(encoded) == b"11:43:23:12"
    assert encoded.encode() == b"11:43:23:12"

    # As the Timecode class is a subclass of datetime.time, we can compare directly
    decoded = Timecode.decode(b"11:43:23;02", format=TimecodeFormat.TimecodeDrop2997)

    assert isinstance(decoded, Timecode)
    assert isinstance(decoded, datetime.time)

    assert decoded.hour == 11
    assert decoded.minute == 43
    assert decoded.second == 23
    assert decoded.frame == 2

    # As the Timecode class is a subclass of datetime.time, we can compare directly
    assert decoded == datetime.time(11, 43, 23, 2)
    assert str(decoded) == "11:43:23;02"
    assert bytes(decoded) == b"11:43:23;02"
    assert decoded.encode() == b"11:43:23;02"
