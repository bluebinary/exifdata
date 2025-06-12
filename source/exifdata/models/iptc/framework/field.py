from __future__ import annotations

from exifdata.logging import logger
from exifdata.models.iptc.enumerations import RecordID
from exifdata.framework.field import Field

logger = logger.getChild(__name__)


class Field(Field):
    _bytes_min: int = None
    _bytes_max: int = None
    _repeatable: bool = None
    _record_id: RecordID = None

    def __init__(
        self,
        *args,
        tagid: int,
        bytes_min: int,
        bytes_max: int,
        repeatable: bool,
        record_id: RecordID = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self._tagid: int = tagid
        self._bytes_min: int = bytes_min
        self._bytes_max: int = bytes_max
        self._repeatable: bool = repeatable
        self._record_id: RecordID = record_id

    @property
    def tagid(self) -> int:
        return self._tagid

    @property
    def dataset_id(self) -> int:
        return self._tagid

    @property
    def bytes_min(self) -> int:
        return self._bytes_min

    @property
    def bytes_max(self) -> int:
        return self._bytes_max

    @property
    def repeatable(self) -> bool:
        return self._repeatable

    @property
    def record_id(self) -> RecordID | None:
        return self._record_id

    @record_id.setter
    def record_id(self, record_id: RecordID) -> RecordID | None:
        if not isinstance(record_id, RecordID):
            raise TypeError(
                "The 'record_id' argument must reference a RecordID class instance!"
            )

        self._record_id = record_id
