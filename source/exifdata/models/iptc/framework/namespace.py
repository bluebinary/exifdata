from __future__ import annotations

from exifdata.logging import logger
from exifdata.framework.namespace import Namespace


logger = logger.getChild(__name__)


class Namespace(Namespace):
    def __init__(self, *args, tagid: int, **kwargs):
        super().__init__(*args, **kwargs)
        self._tagid: int = tagid

    @property
    def tagid(self) -> int:
        return self._tagid

    @property
    def record_id(self) -> int:
        return self._tagid
