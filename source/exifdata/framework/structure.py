from __future__ import annotations


from exifdata.logging import logger
from exifdata import framework


logger = logger.getChild(__name__)


class Structure(object):
    _identifier: str = None
    _name: str = None
    _type: str = None
    _kind: str = None

    def __init__(self, identifier: str, name: str, type: str, kind: str = None):
        self._identifier: str = identifier
        self._name: str = name
        self._type: str = type
        self._kind: str = kind

    @property
    def id(self) -> str:
        return self._identifier

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> str:
        return self._type

    @property
    def kind(self) -> str:
        return self._kind
