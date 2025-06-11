from __future__ import annotations

from exifdata.logging import logger
from exifdata import framework


logger = logger.getChild(__name__)


class Groupspace(object):
    _namespaces: set[Namespace] = None
    _metadata: Metadata = None

    def __init__(self, *args):
        from exifdata.framework.namespace import Namespace

        self._namespaces: list[Namespace] = set()

        for arg in args:
            if isinstance(arg, Namespace):
                self._namespaces.add(arg)
            elif isinstance(arg, Groupspace):
                for namespace in arg.namespaces:
                    self._namespaces.add(namespace)

    @property
    def namespaces(self) -> set[Namespace]:
        return self._namespaces

    @property
    def metadata(self) -> Metadata | None:
        return self._metadata

    @metadata.setter
    def metadata(self, metadata: Metadata):
        from exifdata.framework.metadata import Metadata

        if not isinstance(metadata, Metadata):
            raise TypeError(
                "The 'metadata' argument must have a Metadata class instance value!"
            )
        self._metadata = metadata

    def __getattr__(self, name: str):
        logger.debug("%s.__getattr__(name: %s)" % (self.__class__.__name__, name))

        for namespace in self._namespaces:
            if name in namespace:
                namespace._metadata = self.metadata
                return namespace.__getattr__(name)

        raise AttributeError(f"The groupspace has no '{name}' attribute!")

    def __setattr__(self, name: str, value: object):
        logger.debug(
            "%s.__setattr__(name: %s, value: %s)"
            % (self.__class__.__name__, name, value)
        )

        if name.startswith("_"):
            return super().__setattr__(name, value)

        for namespace in self._namespaces:
            if name in namespace:
                namespace._metadata = self.metadata
                return namespace.__setattr__(name, value)

        raise AttributeError(f"The groupspace has no '{name}' attribute!")
