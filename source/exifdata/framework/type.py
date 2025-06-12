from __future__ import annotations

import enumerific

from exifdata.logging import logger
from exifdata import framework


logger = logger.getChild(__name__)


class Type(enumerific.Enumeration):
    @property
    def klass(cls):
        return cls.value
