from __future__ import annotations

from exifdata.logging import logger
from exifdata.configuration import secrets
from exifdata.framework.adapter import Adapter
from exifdata.framework import Metadata
from exifdata.models.exif import EXIF
from exifdata.models.iptc import IPTC
from exifdata.models.xmp import XMP

from deliciousbytes import ByteOrder

import subprocess
import os

logger = logger.getChild(__name__)


class EXIFTool(Adapter):
    _command: str = secrets.get("exiftool")
    _filepath: str = None
    _metadata: dict[str, object] = None

    @property
    @classmethod
    def binary(cls) -> str:
        if not isinstance(cls._command, str):
            raise TypeError(
                f"To use the '{cls.__name__}' adapter, the 'EXIFTOOL' environment variable must be set and point to an installed copy of the exiftool command line tool!"
            )
        elif not os.path.exists(cls._command):
            raise TypeError(
                f"The '{cls.__name__}._command' attribute value, '{cls._command}', references a path that does not exist!"
            )
        elif not os.path.isfile(cls._command):
            raise TypeError(
                f"The '{cls.__name__}._command' attribute value, '{cls._command}', references a path that is not a file!"
            )
        elif not os.access(cls._command, os.X_OK):
            raise TypeError(
                f"The '{cls.__name__}._command' attribute value, '{cls._command}', references a file that does not have exec permissions!"
            )
        return cls._command

    @classmethod
    def open(cls, filepath: str, **kwargs) -> EXIFTool:
        """Supports opening the specified image file from disk. The image must exist at
        the specified filepath, and the image must use a supported image format."""

        if not isinstance(filepath, str):
            raise TypeError("The 'filepath' argument must have a string value!")
        elif not os.path.exists(filepath):
            raise ValueError(
                f"The 'filepath' argument, '{filepath}', references a file that does not exist!"
            )

        return cls(filepath=filepath)

    @classmethod
    def load(cls, metadata: dict[str, object]) -> EXIFTool:
        """Supports working with the specified metadata dictionary."""

        raise NotImplementedError

    def __init__(self, filepath: str = None, metadata: dict[str, object] = None):
        if filepath is None:
            pass
        elif not isinstance(filepath, str):
            raise TypeError("The 'filepath' argument must have a string value!")
        elif not os.path.exists(filepath):
            raise ValueError(
                f"The 'filepath' argument value, '{filepath}', references a path that does not exist!"
            )

        self._filepath = filepath

        if metadata is None:
            self._metadata: dict[str, object] = {}
        elif isinstance(metadata, dict):
            self._metadata: dict[str, object] = metadata
        else:
            raise TypeError(
                "The 'metadata' argument, if specified, must have a dictionary value!"
            )

    @property
    def filepath(self) -> str:
        return self._filepath

    @property
    def metadata(self) -> dict[str, object]:
        return self._metadata

    def get(self, name: str) -> bytes | None:
        raise NotImplementedError

    def set(self, name: str, value: bytes) -> Adapter:
        raise NotImplementedError

    def byteoder(self) -> ByteOrder:
        # TODO: Determine the byte order from the current image if possible!
        return ByteOrder.MSB

    def decode(self, metadata: dict[str, object] = None) -> None:
        """Supports creating and populating instances of the EXIFData metadata model
        classes from a dictionary of EXIFTool command line option fields and values."""

        if self.models is None:
            raise RuntimeError(
                "The 'models' property has not been set; it must reference a Models class instance!"
            )

        if metadata is None:
            logger.warning(
                "%s.decode(metadata: %s) - no fields set; need to pull metadata from the specified image!",
                self.__class__.__name__,
                metadata,
            )
            metadata = self.metadata
        elif not isinstance(metadata, dict):
            raise RuntimeError(
                "The 'metadata' argument, if specified, must have a dictionary value!"
            )

        if isinstance(metadata, dict):
            for name, value in metadata.items():
                self.models.assign(name=name, value=value)

    def erase(self, payloads: list[str] = None) -> None:
        """Supports erasing the raw metadata payloads with the specified names."""
        pass

    def encode(self) -> None:
        if self.models is None:
            raise RuntimeError(
                "The 'models' property has not been set; it must reference a Models class instance!"
            )
        pass

    def save(self, **kwargs) -> None:
        # TODO: Determine the byte order from the current image if possible!
        pass
