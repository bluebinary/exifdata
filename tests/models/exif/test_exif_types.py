import pytest

from exifdata.models.exif.types import (
    ASCII,
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


def test_type_ascii_encoding_example_one():
    """Test the EXIF metadata field ASCII data type, by encoding a sample string that
    contains non-ASCII characters, which have been assigned registered replacements."""

    uncoded: str = "Copyright © Example Organisation® 2025"

    assert isinstance(uncoded, str)

    # Encode the string to ASCII, after replacing any registered replacements
    encoded: bytes = ASCII(uncoded).encode()

    assert isinstance(encoded, bytes)

    # Note that both the "©" and the "®" have been replaced by the registered
    # replacement strings "(c)" and "(r)" respectively:
    assert encoded == b"Copyright (c) Example Organisation(r) 2025"


def test_type_ascii_encoding_example_two():
    """Test the EXIF metadata field ASCII data type, by encoding a sample string that
    contains a mix of registered replacement characters, diacritics and other characters
    that are outside of the ASCII range that haven't been assigned replacements here to
    test the normalisation of the string and the replacement of other characters."""

    uncoded: str = "The Amazing® Café contains non-ASCII characters like ℗"

    assert isinstance(uncoded, str)

    # Encode the string to ASCII, after replacing any registered replacements
    encoded: bytes = ASCII(uncoded).encode()

    assert isinstance(encoded, bytes)

    # Note that the "℗" has been replaced by the generic replacement "?" as no specific
    # replacement had been registered with the ASCII class for this character; and the
    # diacritic on Café has been replaced by its closest matching ASCII-equivalent:
    assert encoded == b"The Amazing(r) Cafe contains non-ASCII characters like ?"
