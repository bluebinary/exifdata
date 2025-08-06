from __future__ import annotations

from exifdata.logging import logger

from exifdata.framework import (
    Value,
)

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
    # String,
)

from exifdata.models.iptc.enumerations import (
    RecordID,
)

from exifdata.models.iptc.types import (
    String,
)


logger = logger.getChild(__name__)


class Records(object):
    """The IPTC class represents the IPTC metadata container.

    The container comprises of one or more Record entities.
    """

    _records: list[Record] = None

    def __init__(self):
        self._records: list[Record] = []

    @property
    def records(self) -> list[Record]:
        return self._records

    @property
    def record(self):
        raise NotImplementedError

    @record.setter
    def record(self, record: Record):
        if not isinstance(record, Record):
            raise TypeError(
                "The 'record' argument must reference a Record class instance!"
            )
        self._records.append(record)

    def encode(self, order: ByteOrder = ByteOrder.MSB) -> bytes:
        encoded: list[bytes] = []

        for record in self._records:
            encoded.append(record.encode(order=order))

        return b"".join(encoded)

    @classmethod
    def decode(cls, value: bytes, order: ByteOrder = ByteOrder.MSB) -> Records:
        raise NotImplementedError


class Record(object):
    """
    All IPTC Records comprise of the following components:
    +---------------+-----------------------------------------------------------------+
    | Fixed Marker  | One byte fixed marker value: 0x1C                               |
    +---------------+-----------------------------------------------------------------+
    | Record ID     | One byte record identifier value: 0xXX                          |
    |               | NOTE: The record ID is extracted from the RecordID enumeration  |
    +---------------+-----------------------------------------------------------------+
    | DataSet ID    | One byte dataset identifier value: 0xXX                         |
    |               | NOTE: The dataset ID is extracted from the RecordID enumeration |
    +---------------+-----------------------------------------------------------------+
    | Value Length  | Two or four bytes denoting the length of the data that follows  |
    |               | If the length of the bytes encoded data is less than 0x8000 the |
    |               | value length is encoded as two bytes; if it is longer then the  |
    |               | length is encoded as four bytes but the four bytes are prefixed |
    |               | with a fixed marker value of two bytes: 0x80 0x04 so that the   |
    |               | encoded length ultimately would consist of six bytes            |
    +---------------+-----------------------------------------------------------------+
    | Value         | Variable number of bytes of the encoded data                    |
    +---------------+-----------------------------------------------------------------+
    """

    _id: RecordID = None
    _value: Value = None
    _level: int = 0

    def __init__(self, id: RecordID, value: Value):
        if not isinstance(id, RecordID):
            raise TypeError(
                "The 'id' argument must reference a 'RecordID' enumeration value!"
            )

        self._id: RecordID = id

        if not isinstance(value, Value):
            raise TypeError(
                "The 'value' argument must reference a 'Value' value, not %s!"
                % (type(value))
            )

        self._value: Value = value

    @property
    def level(self) -> int:
        # TODO: What is this for?
        return self._level

    @property
    def id(self) -> RecordID:
        return self._id

    @property
    def value(self) -> Value:
        return self._value

    @property
    def length(self) -> UInt:
        return UInt(len(self._value))

    def encode(self, order: ByteOrder = ByteOrder.MSB) -> bytes:
        logger.debug("%s.encode(order: %s)" % (self.__class__.__name__, order))

        encoded: list[bytes] = []

        # Each IPTC record is denoted with an 0x1c byte
        encoded.append(bytes([0x1C]))

        # This is followd by the record ID tag
        encoded.append(self.id.record_id.encode(order=order))

        # This is followed by the dataset ID
        encoded.append(self.id.dataset_id.encode(order=order))

        # This is followed by the encoded length of the data value
        if self.length < 0x8000:
            encoded.append(UInt16(self.length).encode(order=order))
        else:
            encoded.append(bytes([0x80, 0x04]))
            encoded.append(UInt32(self.length).encode(order=order))

        # This is followed by the encoded data
        encoded.append(self.value.encode(order=order))

        # TODO: Can this be simplified with say bytes(bytearray(encoded))?
        return b"".join(encoded)

    @classmethod
    def decode(cls, value: bytes) -> Record:
        if not isinstance(value, bytes):
            raise TypeError("The 'value' argument must have a bytes value!")

        if not value[0] == 0x1C:
            raise ValueError(
                "The 'value' does not begin with the expected 0x1c IPTC record marker!"
            )

        record_id: UInt8 = UInt8(int(value[1]))
        dataset_id: UInt8 = UInt8(int(value[2]))

        if not isinstance(
            id := RecordID.reconcile(record_id=record_id, dataset_id=dataset_id),
            RecordID,
        ):
            raise ValueError(
                "Reconciling the record and dataset IDs failed; the provided raw value is invalid!"
            )

        logger.debug(
            "%s.decode() id => %s, record.id => %s, dataset.id => %s, type => %s",
            cls.__name__,
            id,
            id.record_id,
            id.dataset_id,
            id.type,
        )

        from exifdata.models.iptc import IPTC

        # if not id.type in locals():
        #     raise ValueError(
        #         f"The 'Value' subclass, '{id.type}', associated with '{id}' cannot be found in the current scope!"
        #     )

        # klass = locals()[id.value.type]

        if not isinstance(klass := IPTC.type_by_name(id.type), type):
            raise ValueError(
                f"The 'Value' subclass, '{id.type}', associated with '{id}' has not been registered with the 'IPTC' metadata class!"
            )

        if not issubclass(klass, Value):
            raise TypeError(
                f"The subclass, '{id.type}', associated with '{id}' is not a 'Value' subclass!"
            )

        length: Int16 = Int16.decode(value[3 : 3 + 2], order=ByteOrder.MSB)

        offset: int = 0

        # logger.debug("length[0] => 0x%02x, length[1] => 0x%02x" % (length[0], length[1]))

        # For values longer than 0x8000 (32,768) bytes, the length is prefixed by the
        # special fixed marker 0x80 0x04 to note that the length that follows is encoded
        # into four bytes as an signed 32 bit integer, as 32,767 is the largest number
        # that can fit into a signed 16 bit integer; as such the data section is offset
        # by an additional four bytes from the start of the record (two bytes for the
        # special fixed marker and the two additional bytes of the 32 bit unsigned int):
        if length[0] == 0x80 and length[1] == 0x04:
            length: Int32 = Int32(value[5 : 5 + 2])
            # For records with a length more than or equal to 0x8000 (32, 768) bytes,
            # the preamble of the record is one byte for the record ID, one byte for the
            # dataset ID, the two byte fixed marker denoting the four byte length, then
            # the length encoded as four bytes, then the remainder of the bytes are the
            # value; thus the combined length of the preamble is eight bytes:
            offset = 9
        else:
            # For records with a length less than 0x8000 (32,768) bytes, the preamble of
            # the record is one byte for the record ID, one byte for the dataset ID, two
            # bytes for the length, then the remainder of the bytes are the value; thus
            # the combined length of the preamble is four bytes (one + one + two)
            offset = 5

        if not len(value[offset:]) == length:
            raise ValueError(
                f"The raw data length ({len(value[offset:])}) does not match the expected length ({length})!"
            )

        record = Record(id=id, value=klass.decode(value[offset:]))

        logger.debug("%s.decode() record.value => %r", cls.__name__, record.value)

        return record


# class DataSet(object):
#     _id: DataSetID = None
#
#     def __init__(self, id: DataSetID):
#         if not isinstance(id, DataSetID):
#             raise TypeError(
#                 "The 'id' argument must reference a 'DataSetID' enumeration value!"
#             )
#
#         self._id: DataSetID = id
#
#         self._datasets: list[DataSet] = []
#
#     @property
#     def id(self) -> DataSetID:
#         return self._id
#
#     # TODO: Can this be simplified with say bytes(bytearray(encoded))?
#     def encode(self, order: ByteOrder = ByteOrder.MSB) -> bytes:
#         encoded: list[bytes] = []
#
#         encoded.append(self.id.encode(order=order))
#
#         for dataset in self._datasets:
#             encoded.append(dataset.encode(order=order))
#
#         return b"".join(encoded)
#
#     @classmethod
#     def decode(cls, value: bytes) -> DataSet:
#         pass
