import pytest

from exifdata.models.exif.types import (
    Value,
    ASCII,
    UTF8,
    String,
)


def test_type_ascii_add_replacement_valid():
    """Test the EXIF metadata field ASCII data type, by testing the addition of an ASCII
    replacement for a non-ASCII string that may appear in incoming string values."""

    ASCII.add_replacement(search="®", replacement="(r)")

    # The ASCII type class defines the replacement between "©" and "(c)" out-of-the box
    # and are accessible for testing via the class' private _replacements variable:
    assert len(ASCII._replacements) == 2
    assert ASCII._replacements == {"©": "(c)", "®": "(r)"}


def test_type_ascii_add_replacement_invalid():
    """Test the EXIF metadata field ASCII data type, by testing the addition of an ASCII
    replacement for a non-ASCII string that may appear in incoming string values."""

    with pytest.raises(ValueError) as exception:
        # Attempt to register a replacement for a non-ASCII character, by also supplying
        # a non-ASCII character as the replacement; this should result in a ValueError:
        ASCII.add_replacement(search="®", replacement="℗")

        assert (
            str(exception)
            == "ValueError: The 'replacement' argument must contain an ASCII-compatible string value!"
        )


def test_type_ascii_encoding_example_zero():
    """Test the EXIF metadata field ASCII data type, by encoding a sample string."""

    uncoded: str = "Hello World"

    assert isinstance(uncoded, str)
    assert len(uncoded) == 11

    ascii: ASCII = ASCII(uncoded)

    assert isinstance(ascii, ASCII)
    assert isinstance(ascii, Value)

    # Encode the string to ASCII, after replacing any registered replacements
    encoded: bytes = ascii.encode()

    assert isinstance(encoded, bytes)

    # Ensure that the encoded ASCII string ends with the expected NUL terminating byte
    assert len(encoded) == len(uncoded) + 1
    assert encoded.endswith(b"\x00")
    assert encoded == b"Hello World\x00"


def test_type_ascii_encoding_example_one():
    """Test the EXIF metadata field ASCII data type, by encoding a sample string that
    contains non-ASCII characters, which have been assigned registered replacements."""

    uncoded: str = "Copyright © Example Organisation® 2025"

    assert isinstance(uncoded, str)

    ascii: ASCII = ASCII(uncoded)

    assert isinstance(ascii, ASCII)
    assert isinstance(ascii, Value)

    # Encode the string to ASCII, after replacing any registered replacements
    encoded: bytes = ascii.encode()

    assert isinstance(encoded, bytes)

    # Note that both the "©" and the "®" have been replaced by the registered
    # replacement strings "(c)" and "(r)" respectively:
    assert encoded == b"Copyright (c) Example Organisation(r) 2025\x00"


def test_type_ascii_encoding_example_two():
    """Test the EXIF metadata field ASCII data type, by encoding a sample string that
    contains a mix of registered replacement characters, diacritics and other characters
    that are outside of the ASCII range that haven't been assigned replacements here to
    test the normalisation of the string and the replacement of other characters."""

    uncoded: str = "The Amazing® Café contains non-ASCII characters like ℗\x00"

    assert isinstance(uncoded, str)

    ascii: ASCII = ASCII(uncoded)

    assert isinstance(ascii, ASCII)
    assert isinstance(ascii, Value)

    # Encode the string to ASCII, after replacing any registered replacements
    encoded: bytes = ascii.encode()

    assert isinstance(encoded, bytes)

    # Note that the "℗" has been replaced by the generic replacement "?" as no specific
    # replacement had been registered with the ASCII class for this character; and the
    # diacritic on Café has been replaced by its closest matching ASCII-equivalent:
    assert encoded == b"The Amazing(r) Cafe contains non-ASCII characters like ?\x00"


def test_type_string_encoding_example_one():
    """Test the EXIF metadata field String psuedo data type, by encoding a string that
    contains only ASCII characters; this must result in the value being encoded using
    the ASCII character set and the value being represented as an instance of the ASCII
    data type class as created via the instantiation of the String class."""

    uncoded: str = "This string contains only ASCII characters"

    assert isinstance(uncoded, str)

    string: String = String(uncoded)

    # Ensure that the String class automatically returned an instance of the ASCII data
    # type class based on the absence of non-ASCII characters in the input string
    assert isinstance(string, ASCII)
    assert isinstance(string, String)
    assert isinstance(string, Value)

    encoded: bytes = string.encode()

    assert isinstance(encoded, bytes)

    assert encoded == b"This string contains only ASCII characters\x00"


def test_type_string_encoding_example_two():
    """Test the EXIF metadata field String psuedo data type, by encoding a string that
    contains some non-ASCII characters; this must result in the value being encoded
    using the UTF-8 character set and the value being represented as an instance of the
    UTF8 data type class as created via the instantiation of the String class."""

    uncoded: str = "This string contains ASCII and UTF-8 characters like ℗"

    assert isinstance(uncoded, str)

    string: String = String(uncoded)

    # Ensure that the String class automatically returned an instance of the UTF-8 data
    # type class based on the presence of non-ASCII characters in the input string
    assert isinstance(string, UTF8)
    assert isinstance(string, String)
    assert isinstance(string, Value)

    encoded: bytes = string.encode()

    assert isinstance(encoded, bytes)

    assert (
        encoded
        == b"This string contains ASCII and UTF-8 characters like \xe2\x84\x97\x00"
    )
