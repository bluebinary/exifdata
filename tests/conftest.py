import sys, os
import pytest
import logging

logging.getLogger("enumerific").setLevel(level=logging.WARNING)
logging.getLogger("maxml").setLevel(level=logging.WARNING)
logging.getLogger("exifdata").setLevel(level=logging.WARNING)
logging.getLogger("hybridmethod").setLevel(level=logging.WARNING)

path = os.path.join(os.path.dirname(__file__), "..", "source")

sys.path.insert(0, path)  # add 'exifdata' library path for importing into the tests


@pytest.fixture(scope="session", name="data")
def data() -> callable:
    """Create a fixture that can be used to obtain the contents of example data files as
    strings or bytes by specifying the path relative to the /tests/data folder."""

    def fixture(path: str, binary: bool = False) -> str:
        """Read the specified data file, returning its contents either as a string value
        or if requested in binary mode returning the encoded bytes value."""

        if not isinstance(path, str):
            raise TypeError("The 'path' argument must have a string value!")

        if not isinstance(binary, bool):
            raise TypeError("The 'binary' argument must have a boolean value!")

        if not path.endswith(".xml"):
            path += ".xml"

        filepath = os.path.join(os.path.dirname(__file__), "data", path)

        if not os.path.exists(filepath):
            raise ValueError(
                f"The requested example file, '{filepath}', does not exist!"
            )

        # If binary mode has been specified, adjust the read mode accordingly
        mode: str = "rb" if binary else "r"

        with open(filepath, mode) as handle:
            return handle.read()

    return fixture


def print_bytes_hex(data: bytes, prefix: bool = False):
    hex_string = ("" if prefix else " ").join(
        [(r"\x" if prefix else "") + f"{byte:02x}" for byte in data]
    )
    print(('b"' if prefix else "") + hex_string + ('"' if prefix else ""))
