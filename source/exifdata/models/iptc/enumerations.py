from __future__ import annotations

import enumerific

from deliciousbytes import UInt8


class IPTCFormat(enumerific.Enumeration):
    """The IPTCFormat enumeration class provides a controlled vocabulary of supported
    IPTC encoding formats which are used when encoding and decoding IPTC payloads."""

    APP13 = 1
    RAW = 2


class RecordInfo(object):
    """The RecordInfo class holds information about an IPTC Record, including its record
    ID, data set ID, and data type; this is used when encoding and decoding records."""

    _record_id: UInt8 = None
    _dataset_id: UInt8 = None
    _type: object = None

    def __init__(self, record_id: UInt8, dataset_id: UInt8, type: object):
        if not isinstance(record_id, int):
            raise TypeError("The 'record_id' argument must have an integer value!")

        self._record_id: UInt8 = UInt8(record_id)

        if not isinstance(dataset_id, int):
            raise TypeError("The 'dataset_id' argument must have an integer value!")

        self._dataset_id: UInt8 = UInt8(dataset_id)

        if not isinstance(type, object):
            raise TypeError("The 'type' argument must have an type value!")

        self._type: object = type

    @property
    def record_id(self) -> int:
        return self._record_id

    @property
    def dataset_id(self) -> int:
        return self._dataset_id

    @property
    def type(self) -> object:
        return self._type

    def __eq__(self, other: RecordInfo) -> bool:
        if not isinstance(other, RecordInfo):
            raise TypeError(
                "The 'other' argument must reference another RecordInfo class instance!"
            )

        if self.record_id == other.record_id and self.dataset_id == other.dataset_id:
            return True

        return False


class RecordID(enumerific.extensible.Enumeration):
    """The RecordID class provides a controlled vocabulary of IPTC Record IDs."""

    # Caption = "2#120"
    # Copyright = "2#116"

    @property
    def record_id(self) -> UInt8:
        return self.value.record_id

    @property
    def dataset_id(self) -> UInt8:
        return self.value.dataset_id

    @property
    def type(self) -> object:
        # return UInt8(int(self.value.split("#")[0]))
        return self.value.type

    def __eq__(self, other: RecordID | RecordInfo | int) -> bool:
        if isinstance(other, (RecordID, RecordInfo)):
            if not self.record_id == other.record_id:
                return False
            if not self.dataset_id == other.dataset_id:
                return False
            if not self.type == other.type:
                return False
            return True
        elif isinstance(other, int):
            if not self.record_id == other:
                return False
            return True
        else:
            raise TypeError(
                "The 'other' argument must reference a RecordID or RecordInfo class instance!"
            )

    @classmethod
    def reconcile(
        self,
        *args,
        info: RecordInfo = None,
        record_id: int = None,
        dataset_id: int = None,
        **kwargs,
    ):
        if isinstance(info, RecordInfo):
            for option in self.__members__.values():
                if info == option:
                    return option
        elif isinstance(record_id, int) and isinstance(dataset_id, int):
            for option in self.__members__.values():
                if option.record_id == record_id and option.dataset_id == dataset_id:
                    return option
        else:
            return super().reconcile(*args, **kwargs)
