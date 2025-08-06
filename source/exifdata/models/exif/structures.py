from __future__ import annotations

import enumerific
import builtins

from deliciousbytes import (
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
    Bytes,
    Bytes8,
    Bytes16,
    Bytes32,
    Bytes64,
    Bytes128,
    Bytes256,
)


class IFD(object):
    """This class represents an Image File Directory or IFD used within EXIF compatible
    image file formats such as TIFF and JPEG to hold image and metadata information.

    IFD0 is the first IFD in an EXIF file and contains the main image data, including
    resolution, color space, and other essential image attributes. It also stores EXIF
    metadata like camera settings, date, and time.

    IFD1 is often used to store information about a thumbnail image, which is a smaller
    version of the main image, and it's included to allow faster previews. All tags from
    IFD0 may also be present in IFD1.

    IFD2, while less common, can exist to store additional image data or information
    about related images, such as linked images or other image formats.

    All IFDs comprise the following components:
    +---------------+-----------------------------------------------------------------+
    | Tag Count     | Two bytes holding the count of tags that follow                 |
    +---------------+-----------------------------------------------------------------+
    | Tags          | One or more byte-encoded IFDTag values, the length of which can |
    |               | be determined by multiplying the tag count by 12                |
    +---------------+-----------------------------------------------------------------+
    | Next Offset   | Four bytes holding the pointer to the next IFD or 0 if none     |
    +---------------+-----------------------------------------------------------------+

    The tag count is stored as a short integer (UInt16) comprised of 2 bytes or 16 bits
    The tags are encoded according to the format specified for IFDTag below
    The next offset is stored as a long integer (UInt32) comprised of 4 bytes or 32 bits
    """

    _count: UInt16 = None
    _tags: list[IFDTag] = None
    _next: UInt32 = None

    def __init__(self, count: UInt16 = 0, tags: list[IFDTag] = None, next: UInt32 = 0):
        if not isinstance(count, int):
            raise TypeError("The 'count' argument must have an integer value!")
        elif not (0 <= count <= UInt16.MAX):
            raise TypeError(
                "The 'count' argument must have an integer value between 1 - %d!"
                % (UInt16.MAX)
            )

        self._count: UInt16 = UInt16(count)

        if tags is None:
            self._tags: list[IFDTag] = []
        elif not isinstance(tags, list):
            raise TypeError("The 'tags' argument must have a list value!")
        else:
            for tag in tags:
                if not isinstance(tag, IFDTag):
                    raise TypeError(
                        "Each entry in the 'tags' list must be an IFDTag class instance!"
                    )

            self._tags: list[IFDTag] = tags

        if not isinstance(next, int):
            raise TypeError("The 'next' argument must have an integer value!")
        elif not 0 <= next <= UInt32.MAX:
            raise TypeError(
                "The 'next' argument must have an integer value between 0 - %d!"
                % (UInt32.MAX)
            )

        self._next: UInt32 = UInt32(next)

    @property
    def count(self) -> UInt32:
        """Two bytes representing the number of tags that follow the IFD"""
        return self._count

    @property
    def tags(self) -> list[IFDTag]:
        """Variable number of bytes holding the tag data, where the number can be found
        by multiplying the number of tags by twelve."""
        return self._tags

    @property
    def tag(self):
        raise NotImplementedError

    @tag.setter
    def tag(self, tag: IFDTag) -> IFD:
        """Variable number of bytes holding the tag data, where the number can be found
        by multiplying the number of tags by twelve."""

        if not isinstance(tag, IFDTag):
            raise TypeError(
                "The 'tag' argument must reference an IFDTag class instance!"
            )

        self._tags.append(tag)
        self._count += 1

        return self

    @property
    def next(self) -> UInt32:
        """Four bytes holding a possible offset to the next IFD, if an IFD follows."""
        return self._next

    def encode(self, order: ByteOrder = ByteOrder.MSB) -> bytes:
        encoded: list[bytes] = []

        # Assemble the bytes that represent the IFD metadata and data
        encoded.append(self.count.encode(order=order))

        for tag in self._tags:
            encoded.append(tag.encode(order=order))

        encoded.append(self.next.encode(order=order))

        return b"".join(encoded)


class IFDTag(object):
    """IFD Tag

    An IFD Tag comprises of the following components, consisting of 12 bytes:
    +---------------+-----------------------------------------------------------------+
    | Tag ID        | Two bytes holding the tag ID                                    |
    +---------------+-----------------------------------------------------------------+
    | Data Type     | Two bytes holding the data type indicator, from those below:    |
    |               | * 0 = Empty                                                     |
    |               | * 1 = Byte - 8-bit unsigned integer                             |
    |               | * 2 = ASCII - 8-bit holding 7-bit ASCII code, null-terminated   |
    |               | * 3 = Short - 16-bit signed integer                             |
    |               | * 4 = Long - 32-bit signed integer                              |
    |               | * 5 = Rational - two longs; holding numerator and denominator   |
    |               | * 7 = Undefined - 8-bit byte holding any value per field specs  |
    |               | * 9 = SLong (Signed) - 32-bit signed integer (2's compliment)   |
    |               | * 10 = SRational (Signed) - signed rational of two signed-longs |
    |               | * 129 = UTF-8 - 8-bit byte UTF-8 string, null-terminated        |
    +---------------+-----------------------------------------------------------------+
    | Data Count    | Four bytes holding the count of data values that follow         |
    +---------------+-----------------------------------------------------------------+
    | Data / Offset | Four bytes holding the data or a pointer to the data            |
    +---------------+-----------------------------------------------------------------+
    """

    _id: UInt16 = None
    _type: UInt16 = None
    _count: UInt32 = None
    _data: Bytes32 = None

    def __init__(self, id: UInt16, type: UInt16, count: UInt32, data: Bytes32):
        if not isinstance(id, int):
            raise TypeError("The 'id' argument must have an integer value!")
        elif not 1 <= id <= UInt16.MAX:
            raise TypeError(
                "The 'id' argument must have an integer value between 1 - %d!"
                % (UInt16.MAX)
            )

        self._id: UInt16 = UInt16(id)

        if not isinstance(type, int):
            raise TypeError(
                "The 'type' argument must have an integer value, not %s!"
                % (builtins.type(type))
            )
        elif not 1 <= type <= UInt16.MAX:
            raise TypeError(
                "The 'type' argument must have an integer value between 1 - %d!"
                % (UInt16.MAX)
            )

        self._type: UInt16 = UInt16(type)

        if not isinstance(count, int):
            raise TypeError(
                "The 'count' argument must have an integer value, not %s!"
                % (builtins.type(count))
            )
        elif not 1 <= count <= UInt32.MAX:
            raise TypeError(
                "The 'count' argument must have an integer value between 1 - %d!"
                % (UInt32.MAX)
            )

        self._count: UInt32 = UInt32(count)

        if isinstance(data, Int):
            data = data.encode(order=ByteOrder.MSB)
        elif not isinstance(data, bytes):
            raise TypeError("The 'data' argument must have a bytes value!")

        self._data: bytes = Bytes32(data)

    @property
    def id(self) -> UInt16:
        """The tag ID."""
        return self._id

    @property
    def type(self) -> UInt16:
        """The data type represented as an byte-encoded integer."""
        return self._type

    @property
    def count(self) -> UInt32:
        """The number of data values of the specified type that follow in the data."""
        return self._count

    @property
    def data(self) -> Bytes32:
        """The data value itself, if it fits in the four bytes available, or a pointer
        to the data if it won't fit, which could be to the beginning of another IFD."""
        return self._data

    def encode(self, order: ByteOrder = ByteOrder.MSB) -> bytes:
        encoded: list[bytes] = []

        # Assemble the bytes that represent the IFDTag metadata and data
        encoded.append(self.id.encode(order=order))  # Tag ID; Two bytes
        encoded.append(self.type.encode(order=order))  # Data Type; Two bytes
        encoded.append(self.count.encode(order=order))  # Data Count; Four bytes

        # Data; Four bytes, or Pointer to the data if longer than four bytes
        encoded_data = self.data.encode(order=order, raises=False)

        # If encoded data requires more than 4 bytes, the offset to the data is recorded
        # rather than the data; the data is stored following the IFD
        if len(encoded_data) > 4:
            # TODO: Patch the location of the data later when we know the offset
            encoded.append(UInt32(0xFFFFFFFF).encode(order=order))
        else:
            encoded.append(encoded_data)

        return b"".join(encoded) if encoded else None
