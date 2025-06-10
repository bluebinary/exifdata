from __future__ import annotations

import ctypes
import enumerific


from exifdata.logging import logger


class caselesslist(list):
    """Supports finding a string within a list of strings regardless of the case."""

    def __contains__(self, value: str) -> bool:
        # logger.debug("%s.__contains__(value: %s) %s" % (self.__class__.__name__, value, self))

        if not isinstance(value, str):
            raise TypeError(
                f"The '{self.__class__.__name__}' class only supports comparing string values!"
            )

        value = value.casefold()

        for val in self:
            if not isinstance(val, str):
                raise TypeError(
                    f"The '{self.__class__.__name__}' class only supports comparing string values!"
                )
            elif val.casefold() == value:
                return True

        return False

    def __eq__(self, other: list) -> bool:
        for index, value in enumerate(self):
            if not isinstance(value, str):
                raise TypeError(
                    f"The '{self.__class__.__name__}' class only supports comparing string values!"
                )
            if not isinstance(other[index], str):
                raise TypeError(
                    f"The '{self.__class__.__name__}' class only supports comparing string values!"
                )
            if not value.casefold() == other[index].casefold():
                return False
        return True


class caselessdict(dict):
    _keymap: dict[str, str] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._keymap: dict[str, str] = {}

        for key in self.keys():
            _key = key.casefold() if isinstance(key, str) else key
            self._keymap[_key] = key

    def __contains__(self, key: str) -> bool:
        _key = key.casefold() if isinstance(key, str) else key
        return _key in self._keymap

    def __eq__(self, other: dict) -> bool:
        if not isinstance(other, dict):
            raise TypeError("The 'other' argument must have a dictionary value!")

        if not len(self) == len(other):
            return False

        for key, value in other.items():
            _key = key.casefold() if isinstance(key, str) else key

            if not _key in self._keymap:
                return False
            elif not self[self._keymap[_key]] == value:
                return False

        return True

    def __setitem__(self, key: object, value: object):
        _key = key.casefold() if isinstance(key, str) else key

        self._keymap[_key] = key

        super().__setitem__(self._keymap[_key], value)

    def __getitem__(self, key: object) -> object:
        _key = key.casefold() if isinstance(key, str) else key

        if not _key in self._keymap:
            raise KeyError(f"The dictionary does not contain a '{key}' key!")

        return super().__getitem__(self._keymap[_key])

    def __delitem__(self, key: str):
        _key = key.casefold() if isinstance(key, str) else key

        if _key in self._keymap:
            result = super().__delitem__(self._keymap[_key])
            del self._keymap[_key]
            return result
        else:
            raise KeyError(f"The dictionary does not contain a '{key}' key!")

    def get(self, key: object, default: object = None) -> object | None:
        _key = key.casefold() if isinstance(key, str) else key

        if isinstance(_key, str) and _key in self._keymap:
            return self[self._keymap[_key]]

        return default

    def keys(self) -> caselesslist[str]:
        return caselesslist(super().keys())


class Encoding(enumerific.Enumeration, aliased=True):
    Undefined = None
    ASCII = "ascii"
    Bytes = "bytes"
    Unicode = "utf-8"
    UTF8 = "utf-8"
    UTF16 = "utf-16"
    UTF32 = "utf-32"


class ByteOrder(enumerific.Enumeration, aliased=True):
    """Define the two styles of byte ordering - big-endian and little-endian"""

    # Most significant byte ordering
    MSB = "big"

    # Least significant byte ordering
    LSB = "little"

    # Vendor aliases
    Motorolla = MSB
    Intel = LSB

    # Endian aliases
    BigEndian = MSB
    LittleEndian = LSB


class Int(int):
    _length: int = 8  # 8 bytes, 64-bit signed integer
    _signed: bool = True
    _order: ByteOrder = ByteOrder.MSB
    # In Python 3, the int type is unbounded and can store arbitarily large numbers, and
    # as there is no integer infinity, we must use the float infinity sentinels instead:
    _minimum: int = float("-inf")
    _maximum: int = float("inf")

    def __new__(cls, value, base: int = 10, **kwargs):
        logger.debug(
            "%s.__new__(cls: %s, value: %s, base: %s, kwargs: %s)"
            % (cls.__name__, cls, value, base, kwargs)
        )

        if not isinstance(value, (int, float, str, bytes, bytearray)):
            raise ValueError(
                "The 'value' argument must have an integer, float, string, bytes or bytearray value!"
            )

        if not isinstance(base, int):
            raise ValueError("The 'base' argument must have an integer value!")

        if isinstance(value, (int, float)):
            return super().__new__(cls, value)
        elif isinstance(value, (str, bytes, bytearray)):
            return super().__new__(cls, value, base=base)

    def __init__(cls, *args, **kwargs):
        pass

    def __bytes__(self) -> bytes:
        return self.encode()

    def __len__(self) -> int:
        return len(bytes(self))

    @property
    def length(self) -> int:
        return self._length

    @property
    def signed(self) -> bool:
        return self._signed

    @property
    def order(self) -> ByteOrder:
        return self._order

    @order.setter
    def order(self, order: ByteOrder):
        if not isinstance(order, ByteOrder):
            raise TypeError(
                "The 'order' argument must have a ByteOrder enumeration value!"
            )
        self._order = order

    @classmethod
    @property
    def MIN(cls) -> int:
        return cls._minimum

    @classmethod
    @property
    def MAX(cls) -> int:
        return cls._maximum

    def __getitem__(self, key: int) -> bytes:
        encoded: bytes = bytes(self)

        if not (isinstance(key, int) and key >= 0):
            raise TypeError("The 'key' argument must have a positive integer value!")

        if key >= len(encoded):
            raise KeyError(
                "The 'key' argument must have a positive integer value that is in range of the element indicies that are available!"
            )

        return encoded[key]

    def __setitem__(self, key: int, value: int):
        raise NotImplementedError

    def __delitem__(self, key: int, value: int):
        raise NotImplementedError

    def encode(self, order: ByteOrder = None) -> bytes:
        if order is None:
            order = self.order
        elif not isinstance(order, ByteOrder):
            raise TypeError(
                "The 'order' argument must have a ByteOrder enumeration value!"
            )

        return self.to_bytes(
            length=self.length, byteorder=order.value, signed=self.signed
        )

    @classmethod
    def decode(cls, value: bytes, order: ByteOrder = ByteOrder.MSB) -> Int:
        if not isinstance(value, bytes):
            raise TypeError("The 'value' argument must have a bytes value!")

        if not isinstance(order, ByteOrder):
            raise TypeError(
                "The 'order' argument must have a ByteOrder enumeration value!"
            )

        decoded = cls(int.from_bytes(value, byteorder=order.value, signed=cls._signed))

        logger.debug(
            "%s.decode(value: %r, order: %r) => %r"
            % (cls.__name__, value, order, decoded)
        )

        return decoded

    def __add__(self, other: int) -> Int:
        """Addition"""
        if not isinstance(other, int):
            raise TypeError("The 'other' argument must have an integer value!")
        return self.__class__(int(self) + int(other))

    def __mul__(self, other: int) -> Int:
        """Multiply"""
        if not isinstance(other, int):
            raise TypeError("The 'other' argument must have an integer value!")
        return self.__class__(int(self) * int(other))

    def __truediv__(self, other: int) -> Int:
        """True division"""
        if not isinstance(other, int):
            raise TypeError("The 'other' argument must have an integer value!")
        return self.__class__(int(self) / int(other))

    def __floordiv__(self, other: int) -> Int:
        """Floor division"""
        if not isinstance(other, int):
            raise TypeError("The 'other' argument must have an integer value!")
        return self.__class__(int(self) // int(other))

    def __sub__(self, other: int) -> Int:
        """Subtraction"""
        if not isinstance(other, int):
            raise TypeError("The 'other' argument must have an integer value!")
        return self.__class__(int(self) - int(other))

    def __mod__(self, other: int) -> Int:
        """Modulo"""
        if not isinstance(other, int):
            raise TypeError("The 'other' argument must have an integer value!")
        return self.__class__(int(self) % int(other))

    def __pow__(self, other: int) -> Int:
        """Power"""
        if not isinstance(other, int):
            raise TypeError("The 'other' argument must have an integer value!")
        return self.__class__(int(self) ** int(other))

    def __rshift__(self, other: int) -> Int:
        """Right bit shift"""
        if not isinstance(other, int):
            raise TypeError("The 'other' argument must have an integer value!")
        return self.__class__(int(self) >> int(other))

    def __lshift__(self, other: int) -> Int:
        """Left bit shift"""
        if not isinstance(other, int):
            raise TypeError("The 'other' argument must have an integer value!")
        return self.__class__(int(self) << int(other))

    def __and__(self, other: int) -> Int:
        """Binary AND"""
        if not isinstance(other, int):
            raise TypeError("The 'other' argument must have an integer value!")
        return self.__class__(int(self) & int(other))

    def __or__(self, other: int) -> Int:
        """Binary OR"""
        if not isinstance(other, int):
            raise TypeError("The 'other' argument must have an integer value!")
        return self.__class__(int(self) | int(other))

    def __xor__(self, other: int) -> Int:
        """Binary XOR"""
        if not isinstance(other, int):
            raise TypeError("The 'other' argument must have an integer value!")
        return self.__class__(int(self) ^ int(other))

    def __iadd__(self, other: int) -> Int:
        """Asignment addition"""
        if not isinstance(other, int):
            raise TypeError("The 'other' argument must have an integer value!")
        return self.__class__(int(self) + int(other))

    def __imul__(self, other: int) -> Int:
        """Asignment multiply"""
        if not isinstance(other, int):
            raise TypeError("The 'other' argument must have an integer value!")
        return self.__class__(int(self) * int(other))

    def __idiv__(self, other: int) -> Int:
        """Asignment true division"""
        if not isinstance(other, int):
            raise TypeError("The 'other' argument must have an integer value!")
        return self.__class__(int(self) / int(other))

    def __ifloordiv__(self, other: int) -> Int:
        """Asignment floor division"""
        if not isinstance(other, int):
            raise TypeError("The 'other' argument must have an integer value!")
        return self.__class__(int(self) // int(other))

    def __isub__(self, other: int) -> Int:
        """Asignment subtract"""
        if not isinstance(other, int):
            raise TypeError("The 'other' argument must have an integer value!")
        return self.__class__(int(self) - int(other))

    def __imod__(self, other: int) -> Int:
        """Asignment modulo"""
        if not isinstance(other, int):
            raise TypeError("The 'other' argument must have an integer value!")
        return self.__class__(int(self) % int(other))

    def __ipow__(self, other: int) -> Int:
        """Asignment power"""
        if not isinstance(other, int):
            raise TypeError("The 'other' argument must have an integer value!")
        return self.__class__(int(self) ** int(other))

    def __irshift__(self, other: int) -> Int:
        """Asignment right bit shift"""
        if not isinstance(other, int):
            raise TypeError("The 'other' argument must have an integer value!")
        return self.__class__(int(self) >> int(other))

    def __ilshift__(self, other: int) -> Int:
        """Asignment left bit shift"""
        if not isinstance(other, int):
            raise TypeError("The 'other' argument must have an integer value!")
        return self.__class__(int(self) << int(other))

    def __iand__(self, other: int) -> Int:
        """Asignment AND"""
        if not isinstance(other, int):
            raise TypeError("The 'other' argument must have an integer value!")
        return self.__class__(int(self) & int(other))

    def __ior__(self, other: int) -> Int:
        """Asignment OR"""
        if not isinstance(other, int):
            raise TypeError("The 'other' argument must have an integer value!")
        return self.__class__(int(self) | int(other))

    def __ixor__(self, other: int) -> Int:
        """Asignment XOR"""
        if not isinstance(other, int):
            raise TypeError("The 'other' argument must have an integer value!")
        return self.__class__(int(self) ^ int(other))

    def __neg__(self) -> Int:
        """Unary negation"""
        return self.__class__(-int(self))

    def __pos__(self) -> Int:
        """Unary positive"""
        return self.__class__(+int(self))

    def __invert__(self) -> Int:
        """Unary invert"""
        return self.__class__(~int(self))


class Int8(Int):
    _length: int = 1
    _signed: bool = True
    _minimum: int = -128
    _maximum: int = +127

    def __new__(cls, value: int, *args, **kwargs):
        if not isinstance(value, int):
            raise ValueError("The 'value' argument must have an integer value!")

        int8 = ctypes.c_int8(value)

        return super().__new__(cls, int8.value, *args, **kwargs)


class Int16(Int):
    _length: int = 2
    _signed: bool = True
    _minimum: int = -32768
    _maximum: int = +32767

    def __new__(cls, value: int, *args, **kwargs):
        if not isinstance(value, int):
            raise ValueError("The 'value' argument must have an integer value!")

        int16 = ctypes.c_int16(value)

        return super().__new__(cls, int16.value, *args, **kwargs)


class Int32(Int):
    _length: int = 4
    _signed: bool = True
    _minimum: int = -2_147_483_648
    _maximum: int = +2_147_483_647

    def __new__(cls, value: int, *args, **kwargs):
        if not isinstance(value, int):
            raise ValueError("The 'value' argument must have an integer value!")

        int32 = ctypes.c_int32(value)

        return super().__new__(cls, int32.value, *args, **kwargs)


class Int64(Int):
    _length: int = 8
    _signed: bool = True
    _minimum: int = -9_223_372_036_854_775_808
    _maximum: int = +9_223_372_036_854_775_807

    def __new__(cls, value: int, *args, **kwargs):
        if not isinstance(value, int):
            raise ValueError("The 'value' argument must have an integer value!")

        int64 = ctypes.c_int64(value)

        return super().__new__(cls, int64.value, *args, **kwargs)


class UInt(Int):
    _length: int = None
    _signed: bool = False
    _minimum: int = 0
    _maximum: int = float("inf")


class UInt8(UInt):
    _length: int = 1
    _minimum: int = 0
    _maximum: int = 255

    def __new__(cls, value: int, *args, **kwargs):
        if not isinstance(value, int):
            raise ValueError("The 'value' argument must have an integer value!")

        uint8 = ctypes.c_uint8(value)

        return super().__new__(cls, uint8.value, *args, **kwargs)


class UInt16(UInt):
    _length: int = 2
    _minimum: int = 0
    _maximum: int = 65535

    def __new__(cls, value: int, *args, **kwargs):
        if not isinstance(value, int):
            raise ValueError("The 'value' argument must have an integer value!")

        uint16 = ctypes.c_uint16(value)

        return super().__new__(cls, uint16.value, *args, **kwargs)


class UInt32(UInt):
    _length: int = 4
    _minimum: int = 0
    _maximum: int = 4294967295

    def __new__(cls, value: int, *args, **kwargs):
        if not isinstance(value, int):
            raise ValueError("The 'value' argument must have an integer value!")

        uint32 = ctypes.c_uint32(value)

        return super().__new__(cls, uint32.value, *args, **kwargs)


class UInt64(UInt):
    _length: int = 8
    _minimum: int = 0
    _maximum: int = 1.844674407370955e19

    def __new__(cls, value: int, *args, **kwargs):
        if not isinstance(value, int):
            raise ValueError("The 'value' argument must have an integer value!")

        uint64 = ctypes.c_uint64(value)

        return super().__new__(cls, uint64.value, *args, **kwargs)


class Char(UInt8):
    def __new__(cls, value: int | str | bytes, *args, **kwargs):
        if not isinstance(value, (int, str, bytes)):
            raise ValueError(
                "The 'value' argument must have an integer, string or bytes value!"
            )

        if isinstance(value, (str, bytes)):
            if isinstance(value, bytes):
                value = value.decode()

            if len(value) > 1:
                raise ValueError(
                    "The 'value' argument, if provided as a string or as bytes, cannot be longer than one character!"
                )

            value = ord(value[0])

        return super().__new__(cls, value, *args, **kwargs)

    def __str__(self) -> str:
        return chr(self)


class SignedChar(Int8):
    def __new__(cls, value: int | str | bytes, *args, **kwargs):
        if not isinstance(value, (int, str, bytes)):
            raise ValueError(
                "The 'value' argument must have an integer, string or bytes value!"
            )

        if isinstance(value, (str, bytes)):
            if isinstance(value, bytes):
                value = value.decode()

            if len(value) > 1:
                raise ValueError(
                    "The 'value' argument, if provided as a string or as bytes, cannot be longer than one character!"
                )

            value = ord(value[0])

        return super().__new__(cls, value, *args, **kwargs)

    def __str__(self) -> str:
        return chr(self)


class Short(UInt16):
    """A short integer is an unsigned integer at least 16-bits wide."""

    pass


class SignedShort(Int16):
    """A signed short integer is an signed integer at least 16-bits wide."""

    pass


class Long(UInt32):
    """A long integer is an unsigned integer at least 32-bits wide."""

    pass


class SignedLong(Int32):
    """A signed long integer is an signed integer at least 32-bits wide."""

    pass


class LongLong(UInt64):
    """A long long integer is an unsigned integer at least 64-bits wide."""

    pass


class SignedLongLong(UInt64):
    """A signed long long integer is an signed integer at least 64-bits wide."""

    pass


class Bytes(bytes):
    _length: int = None

    def __new__(cls, value: bytes | bytearray | Int, length: int = None):
        if isinstance(value, Int):
            value = value.encode(order=ByteOrder.MSB)

        if not isinstance(value, (bytes, bytearray)):
            raise TypeError(
                "The 'value' argument must have a 'bytes' value or reference a 'bytesarray' instance!"
            )

        self = super().__new__(cls, value)

        if length is None:
            pass
        elif isinstance(length, int) and length >= 1:
            self._length: int = length
        else:
            raise TypeError(
                "The 'length' argument, if specified, must have a positive integer value!"
            )

        return self

    @property
    def length(self) -> int | None:
        return self._length

    def encode(
        self, order: ByteOrder = ByteOrder.MSB, length: int = None, raises: bool = True
    ) -> bytes:
        if not isinstance(order, ByteOrder):
            raise TypeError(
                "The 'order' argument must have a ByteOrder enumeration value!"
            )

        if length is None:
            length = self._length
        elif not (isinstance(length, int) and length >= 1):
            raise TypeError(
                "The 'length' argument, if specified, must have a positive integer value!"
            )

        if not isinstance(raises, bool):
            raise TypeError("The 'raises' argument must have a boolean value!")

        encoded: bytesarray = bytearray()

        if order is ByteOrder.MSB:
            for index, byte in enumerate(self):
                # logger.debug("%s.encode(order: MSB) index => %s, byte => %s (%x)" % (self.__class__.__name__, index, byte, byte))
                encoded.append(byte)

            while len(encoded) < length:
                encoded.insert(0, 0)
        elif order is ByteOrder.LSB:
            for index, byte in enumerate(reversed(self)):
                # logger.debug("%s.encode(order: LSB) index => %s, byte => %s (%x)" % (self.__class__.__name__, index, byte, byte))
                encoded.append(byte)

            while len(encoded) < length:
                encoded.append(0)

        if raises is True and self.length and len(encoded) > self.length:
            raise ValueError(
                "The encoded bytes value is longer than that allowed by the Bytes subclass; the value encodes to %d bytes whereas the class allows %d bytes; ensure the value is in range, use a larger Bytes subclass or use the base Bytes class which by default imposes no length restrictions!"
                % (len(encoded), self.length)
            )

        return bytes(encoded)

    @classmethod
    def decode(value: bytes) -> Bytes:
        pass


class Bytes8(Bytes):
    _length: int = 1  # 1 byte = 8 bits (1 * 8 = 8)


class Bytes16(Bytes):
    _length: int = 2  # 2 bytes = 16 bits (2 * 8 = 16)


class Bytes32(Bytes):
    _length: int = 4  # 4 bytes = 32 bits (4 * 8 = 32)


class Bytes64(Bytes):
    _length: int = 8  # 8 bytes = 64 bits (8 * 8 = 64)


class Bytes128(Bytes):
    _length: int = 16  # 16 bytes = 128 bits (16 * 8 = 128)


class Bytes256(Bytes):
    _length: int = 32  # 32 bytes = 256 bits (32 * 8 = 256)


class String(str):
    def __new__(cls, value: str, *args, **kwargs):
        return super().__new__(cls, value, *args, **kwargs)

    def __init__(cls, *args, **kwargs):
        pass

    def encode(
        self, order: ByteOrder = ByteOrder.MSB, encoding: Encoding = Encoding.Unicode
    ):
        if order is ByteOrder.MSB:
            return bytes(bytearray(str.encode(self, encoding.value)))
        elif order is ByteOrder.MSB:
            return bytes(reversed(bytearray(str.encode(self, encoding.value))))
        else:
            raise TypeError(
                "The 'order' argument is invalid; it must have a 'ByteOrder' enumeration value, not: %s!"
                % (type(order))
            )

    @classmethod
    def decode(cls, value: bytes, encoding: Encoding = Encoding.Unicode) -> String:
        if not isinstance(value, bytes):
            raise TypeError("The 'value' argument must have a 'bytes' value!")

        return String(value.decode(encoding.value))
