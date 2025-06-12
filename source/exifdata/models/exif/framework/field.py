from __future__ import annotations

from exifdata.logging import logger
from exifdata.framework.field import Field


logger = logger.getChild(__name__)


class Field(Field):
    _tagid: int = None
    _default: object = None

    def __init__(self, *args, tagid: int, default: object = None, **kwargs):
        super().__init__(*args, **kwargs)

        if not isinstance(tagid, int):
            raise TypeError("The 'tagid' argument must have an integer value!")

        self._tagid: int = tagid

        self._default: object = default

    @property
    def tagid(self) -> int:
        return self._tagid

    @property
    def default(self) -> object | None:
        return self._default
