from __future__ import annotations

import abc


from exifdata.logging import logger


logger = logger.getChild(__name__)


class Adapter(metaclass=abc.ABCMeta):
    """The Adapter abstract class defines the interface for Adapters used by EXIFData to
    work with raw image metadata through various means such as PyVIPS or EXIFTool."""

    _models: Models = None

    @property
    @classmethod
    def name(cls) -> str:
        """Obtain the name of the adapter for logging and error message use."""

        return cls.__name__

    @property
    def models(self) -> Models | None:
        """Return the Models class instance reference for use by the adapter."""

        return self._models

    @models.setter
    def models(self, models: Models):
        """Support setting the Models class instance reference for use by the adapter."""

        from exifdata import Models

        if not isinstance(models, Models):
            raise TypeError(
                "The 'models' argument must reference a Models class instance!"
            )

        self._models = models

    @classmethod
    @abc.abstractmethod
    def open(cls, filepath: str) -> Adapter:
        """Supports opening the specified image file from disk. The image must exist at
        the specified filepath, and the image must use a supported image format."""

        pass

    @classmethod
    def associate(cls, image: object, **kwargs) -> Adapter:
        """Supports working with the specified in-memory image. The image argument must
        reference an in-memory image, and the image must use a supported file format;
        the method associates the provided image with the Models class, but does not
        attempt to extract or decode any existing metadata embedded in the image."""

        cls.load(image=image, decode=False, **kwargs)

    @classmethod
    @abc.abstractmethod
    def load(cls, image: object, **kwargs) -> Adapter:
        """Supports working with the specified in-memory image. The image argument must
        reference an in-memory image, and the image must use a supported file format."""

        pass

    @abc.abstractmethod
    def get(self, name: str, **kwargs) -> bytes | None:
        """Supports getting a raw metadata payload of the specified name."""

        pass

    @abc.abstractmethod
    def set(self, name: str, value: bytes, **kwargs) -> Adapter:
        """Supports setting a raw metadata payload of the specified name and value."""

        return self

    @abc.abstractmethod
    def erase(self, payloads: list[str] = None, **kwargs) -> None:
        """Supports erasing the raw metadata payloads with the specified names."""

        pass

    @abc.abstractmethod
    def decode(self, **kwargs) -> None:
        """Supports decoding the available metadata payloads in the image."""

        pass

    @abc.abstractmethod
    def encode(self, **kwargs) -> None:
        """Supports encoding and embedding the assigned metadata into the image."""

        pass

    @abc.abstractmethod
    def save(self, **kwargs) -> None:
        """Supports saving the in-memory image."""

        pass
