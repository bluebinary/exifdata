from __future__ import annotations

from exifdata.logging import logger
from exifdata.framework.field import Field

logger = logger.getChild(__name__)


class Field(Field):
    _localised: bool = None

    def __init__(
        self,
        *args,
        localised: bool = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        if localised is None:
            pass
        elif not isinstance(localised, bool):
            raise TypeError(
                "The 'localised' argument, if specified, must have a boolean value!"
            )

        self._localised: bool = localised

    @property
    def localised(self) -> bool | None:
        return self._localised
