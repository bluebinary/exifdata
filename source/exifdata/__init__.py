from __future__ import annotations

from exifdata.logging import logger

from exifdata.framework import Metadata

from exifdata.models.exif import EXIF
from exifdata.models.iptc import IPTC, IPTCFormat
from exifdata.models.xmp import XMP

from exifdata.adapters import (
    Adapter,
    EXIFTool,
    TIFFData,
    VIPS,
)

from deliciousbytes import ByteOrder

import os


class Models(object):
    """The Models class encapsulates EXIFData metadata models into a singular type."""

    _adapter: Adapter = VIPS
    _models: list[Metadata] = None
    _modeltypes: list[Metadata] = [
        EXIF,
        IPTC,
        XMP,
    ]

    @classmethod
    def adapt(cls, adapter: Adapter) -> Adapter:
        """Support setting the Models' adapter class that interfaces with the image."""

        logger.debug("%s.adapter(adapter: %s)", cls.__name__, adapter)

        if not isinstance(adapter, type):
            raise TypeError(
                "The 'adapter' argument must reference an Adapter subclass!"
            )
        elif not issubclass(adapter, Adapter):
            raise TypeError(
                "The 'adapter' argument must reference an Adapter subclass!"
            )

        cls._adapter = adapter

        return cls

    @classmethod
    def open(cls, filepath: str, decode: bool = True, **kwargs) -> Models:
        """Supports extracting image metadata from an image file and creating the
        corresponding instances of the EXIFData library image metadata model classes
        for each of the metadata payloads that are present in the provided image."""

        logger.debug(
            "%s.open(filepath: %s, decode: %s, kwargs: %s)",
            cls.__name__,
            filepath,
            decode,
            kwargs,
        )

        if not isinstance(filepath, str):
            raise TypeError("The 'filepath' argument must have a string value!")
        elif not os.path.exists(filepath):
            raise ValueError(
                f"The 'filepath' argument, '{filepath}', references a file that does not exist!"
            )

        if isinstance(
            adapter := cls._adapter.open(filepath=filepath, **kwargs), Adapter
        ):
            return cls(adapter=adapter, decode=decode, **kwargs)
        else:
            raise RuntimeError(
                f"Unable to load the specified image file, '{filepath}', using the '{adapter.name}' adapter!"
            )

    @classmethod
    def associate(cls, image: object, **kwargs) -> Models:
        return cls.load(image=image, decode=False, **kwargs)

    @classmethod
    def load(cls, image: object, decode: bool = True, **kwargs) -> Models:
        """Supports extracting image metadata from an image object and creating the
        corresponding instances of the EXIFData library image metadata model classes
        for each of the metadata payloads that are present in the provided image."""

        logger.debug(
            "%s.load(image: %s, decode: %s, kwargs: %s)",
            cls.__name__,
            image,
            decode,
            kwargs,
        )

        if isinstance(adapter := cls._adapter.load(image=image, **kwargs), Adapter):
            return cls(adapter=adapter, decode=decode, **kwargs)
        else:
            raise RuntimeError(
                f"Unable to load the specified image file, '{image}', using the '{adapter.name}' adapter!"
            )

    def __init__(self, adapter: Adapter, decode: bool = True, **kwargs):
        logger.debug(
            "%s.__init__(adapter: %s, decode: %s, kwargs: %s)",
            self.__class__.__name__,
            adapter,
            decode,
            kwargs,
        )

        self._models: list[Models] = []

        if not isinstance(adapter, Adapter):
            raise TypeError(
                "The 'adapter' argument must reference an Adapter class instance!"
            )

        # The Adapter instance *must* be assigned a reference to the Models instance
        adapter.models = self

        self._adapter: Adapter = adapter

        if not isinstance(decode, bool):
            raise TypeError("The 'decode' argument must have a boolean value!")

        # Extract and decode the image's existing metadata, creating the relevant models
        if decode is True:
            self.decode()

        # Otherwise, create an empty suite of models into which metadata can be assigned
        elif decode is False:
            for modeltype in self._modeltypes:
                if issubclass(modeltype, Metadata):
                    self._models.append(modeltype())

    def __len__(self) -> int:
        """Return the count of models currently held by the Models class."""

        logger.debug("%s.__len__()", self.__class__.__name__)

        return len(self._models)

    def __iter__(self) -> Metadata:
        """Support iteration through the models current held by the Models class."""

        logger.debug("%s.__iter__()", self.__class__.__name__)

        for model in self._models:
            yield model

    @property
    def adapter(self) -> Adapter:
        """Return the currently configured Adapter class."""

        return self._adapter

    @property
    def model(self):
        raise NotImplementedError

    @model.setter
    def model(self, model: Metadata):
        """Support assiging Metadata model instances to the Models class; when assigned
        the method checks if the model has alredy been assigned or not, and if not, it
        is appended to the list of assigned Metadata model instances."""

        logger.debug("%s.model(model: %s)", self.__class__.__name__, model)

        if not isinstance(model, Metadata):
            raise TypeError(
                "The 'model' argument must reference a Model class instance!"
            )

        for _model in self._models:
            if isinstance(model, _model.__class__):
                raise ValueError(
                    f"An instance of the '{model.__class__.__name__}' model has already been assigned!"
                )

        self._models.append(model)

    def update(self, model: Metadata):
        """Support updating Metadata model instances on the Models class; when assigned
        the method checks if the model has alredy been assigned or not; if it has been
        assigned previously, it will overwrite the old instance, and if it has not been
        assigned, it is appended to the list of assigned Metadata model instances."""

        logger.debug(
            "%s.update(model: %s) => %s", self.__class__.__name__, model, self._models
        )

        if not isinstance(model, Metadata):
            raise TypeError(
                "The 'model' argument must reference a Model class instance!"
            )

        # If the model has already been specified, update it with the provided model
        for _index, _model in enumerate(self._models):
            if isinstance(model, _model.__class__):
                self._models[_index] = model
                break
        else:
            self._models.append(model)

    @property
    def exif(self) -> EXIF:
        """Return the EXIF metadata model instance if it is present in the models, or
        create and assign the instance if it did not previously exist."""

        logger.debug("%s.exif()", self.__class__.__name__)

        for model in self._models:
            if isinstance(model, EXIF):
                return model

        model = EXIF()

        self._models.append(model)

        return model

    @property
    def iptc(self) -> IPTC:
        """Return the IPTC metadata model instance if it is present in the models, or
        create and assign the instance if it did not previously exist."""

        logger.debug("%s.iptc()", self.__class__.__name__)

        for model in self._models:
            if isinstance(model, IPTC):
                return model

        model = IPTC()

        self._models.append(model)

        return model

    @property
    def xmp(self) -> XMP:
        """Return the XMP metadata model instance if it is present in the models, or
        create and assign the instance if it did not previously exist."""

        logger.debug("%s.xmp()", self.__class__.__name__)

        for model in self._models:
            if isinstance(model, XMP):
                return model

        model = XMP()

        self._models.append(model)

        return model

    def assign(self, name: str, value: object, models: list[str] = None, **kwargs):
        """Support assigning a value to any metadata model that has a field with a matching fully-qualified name or registered fully-qualified alias name."""

        logger.debug(
            "%s.assign(name: %r, value: %r)",
            self.__class__.__name__,
            name,
            value,
        )

        found: bool = False

        fullname: str = name

        prefix: str = None

        if len(parts := name.split(":", maxsplit=1)) == 2:
            (prefix, name) = parts

        modelprefixes: list[str] = []

        for model in self._models:
            modelprefixes.append(model.name.lower())

        for model in self._models:
            if models and not model.name in models:
                continue
            elif prefix:
                if prefix.lower() in modelprefixes:
                    if not model.name.lower() == prefix.lower():
                        continue
                else:
                    name = fullname

            if match := model.field_by_property(property="names", value=name):
                (namespace, field) = match

                logger.debug(
                    "%s.assign() Found '%s.%s.%s'",
                    self.__class__.__name__,
                    model.name,
                    namespace.name,
                    field.name,
                )

                found = True

                try:
                    model.set(namespace=namespace, field=field, value=value, **kwargs)
                except ValueError as exception:
                    logger.warning(
                        "%s.assign() The '%s' field failed validation: %s",
                        self.__class__.__name__,
                        name,
                        str(exception),
                    )

        if found is False:
            logger.warning(
                "%s.assign() The '%s' field could not be found on any model!",
                self.__class__.__name__,
                fullname,
            )

    def erase(self, payloads: list[str] = None) -> Models:
        """Supports erasing the raw metadata payloads with the specified names."""

        logger.debug(
            "%s.erase(payloads: %s)",
            self.__class__.__name__,
            payloads,
        )

        self.adapter.erase(payloads=payloads)

        return self

    def decode(self, order: ByteOrder = ByteOrder.MSB, **kwargs) -> Models:
        """Support decoding the current metadata from the in-memory image"""

        logger.debug(
            "%s.decode(order: %s, kwargs: %s)", self.__class__.__name__, order, kwargs
        )

        self.adapter.decode(order=order, **kwargs)

        return self

    def encode(self, order: ByteOrder = ByteOrder.MSB, **kwargs) -> Models:
        """Support encoding the current metadata and updating the in-memory image"""

        logger.debug(
            "%s.encode(order: %s, kwargs: %s)",
            self.__class__.__name__,
            order,
            kwargs,
        )

        self.adapter.encode(order=order, **kwargs)

        return self

    def save(self, **kwargs) -> object:
        """Support saving the current metadata to the image."""

        return self.adapter.save(**kwargs)


__all__ = [
    "Metadata",
    "EXIF",
    "IPTC",
    "IPTCFormat",
    "XMP",
    "Adapter",
    "EXIFTool",
    "TIFFData",
    "VIPS",
    "Models",
    "ByteOrder",
]
