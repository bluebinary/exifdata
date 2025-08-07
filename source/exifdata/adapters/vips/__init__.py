from __future__ import annotations

from exifdata.logging import logger
from exifdata.framework.adapter import Adapter
from exifdata.framework import Metadata
from exifdata.models.exif import EXIF
from exifdata.models.iptc import IPTC, IPTCFormat
from exifdata.models.xmp import XMP

from deliciousbytes import ByteOrder

import os

# pyvips is imported (just once) when any instances of the VIPS class are created
# as such pyvips is an optional dependency for the project, providing more flexibility
# import pyvips as vips
vips: pyvips = None


logger = logger.getChild(__name__)


class VIPS(Adapter):
    """Supports working with images through the PyVIPS library, including the ability to
    open images from files, work with in-memory PyVIPS images, saving images to files,
    and of course the extraction and decoding and encoding and embedding of metadata."""

    _image: vips.Image = None

    # Mapping between PyVIPS metadata payload field names and EXIFData model classes
    _mapping: dict[str, Metadata] = {
        "exif-data": EXIF,
        "iptc-data": IPTC,
        "xmp-data": XMP,
    }

    @classmethod
    def _import_dependencies(cls):
        """Import the required dependencies for this adapter. As the use of the adapter
        is optional, the associated dependencies and their import is optional too."""

        try:
            if globals()["vips"] is None:
                import pyvips

                globals()["vips"] = pyvips
        except ImportError as exception:
            raise RuntimeError(
                f"To use the '{cls.__name__}' adapter, the PyVIPS library must be installed: '{exception}'!"
            )

    @classmethod
    def open(cls, filepath: str, options: str = "") -> VIPS:
        """Supports opening the specified image file from disk. The image must exist at
        the specified filepath, and the image must use a supported image format."""

        cls._import_dependencies()

        if not isinstance(filepath, str):
            raise TypeError("The 'filepath' argument must have a string value!")
        elif not os.path.exists(filepath):
            raise ValueError(
                f"The 'filepath' argument, '{filepath}', references a file that does not exist!"
            )

        if not isinstance(options, str):
            raise TypeError(
                "The 'options' argument, used by PyVIPS.Image.new_from_file(), must have a string value!"
            )

        if isinstance(image := vips.Image.new_from_file(filepath, options), vips.Image):
            return cls(image=image)
        else:
            raise RuntimeError(
                f"Unable to load the specified image file, '{filepath}', using PyVIPS!"
            )

    @classmethod
    def load(cls, image: vips.Image) -> VIPS:
        """Supports working with the specified in-memory image. The image must reference
        a PyVIPS Image class instance, and the image must use a supported file format.
        """

        cls._import_dependencies()

        if not isinstance(image, vips.Image):
            raise TypeError(
                "The 'image' argument must reference a PyVIPS 'Image' class instance!"
            )

        return cls(image=image)

    def __new__(cls, *args, **kwargs) -> VIPS:
        cls._import_dependencies()

        return super().__new__(cls)

    def __init__(self, image: vips.Image):
        if not isinstance(image, vips.Image):
            raise TypeError(
                "The 'image' argument must reference a PyVIPS 'Image' class instance!"
            )
        self._image = image

    @property
    def image(self) -> vips.Image:
        return self._image

    @property
    def mapping(self) -> dict[str, Metadata]:
        return self._mapping

    def fields(self) -> list[str]:
        return self.image.get_fields()

    def get(self, name: str) -> bytes | None:
        if not isinstance(name, str):
            raise TypeError("The 'name' argument must have a string value!")

        if name in self.fields():
            return self.image.get(name)

    def set(self, name: str, value: bytes) -> Adapter:
        if not isinstance(name, str):
            raise TypeError("The 'name' argument must have a string value!")

        if not isinstance(value, bytes):
            raise TypeError("The 'value' argument must have a bytes value!")

        logger.debug(
            "%s.set(name: %s, value: %d)", self.__class__.__name__, name, len(value)
        )

        self.image.set_type(vips.type_from_name("VipsBlob"), name, value)

        return self

    def byteorder(self) -> ByteOrder:
        # TODO: Determine the byte order from the current image if possible!
        return ByteOrder.MSB

    def decode(self, order: ByteOrder = None) -> None:
        logger.debug("%s.decode(order: %s)", self.__class__.__name__, order)

        if order is None:
            order = self.byteorder()
        elif not isinstance(order, ByteOrder):
            raise TypeError(
                "The 'order' argument, if specified, must reference a ByteOrder enumeration class option!"
            )

        if self.models is None:
            raise RuntimeError(
                "The 'models' property has not been set; it must reference a Models class instance!"
            )

        # Iterate through the mapping, attempting to extract each of the named metadata
        # payloads, and if present in the current image, pass these to the decode method
        # of the relevant metadata model class to attempt to decode the data for use:
        for fieldname, cläss in self.mapping.items():
            if isinstance(data := self.get(fieldname), bytes):
                logger.debug(
                    "%s.decode() Successfully obtained '%s' metadata for the %s model",
                    self.__class__.__name__,
                    fieldname,
                    cläss,
                )

                if isinstance(model := cläss.decode(value=data, order=order), cläss):
                    self.models.update(model)
            elif isinstance(data := self.get(fieldname), object) and not data is None:
                logger.debug(
                    "%s.decode() Unable to obtain '%s' metadata for the %s model as bytes, but found: %s",
                    self.__class__.__name__,
                    fieldname,
                    cläss,
                    type(data),
                )
            else:
                logger.debug(
                    "%s.decode() Unable to obtain '%s' metadata for the %s model!",
                    self.__class__.__name__,
                    fieldname,
                    cläss,
                )

    def erase(self, payloads: list[str] = None) -> None:
        """Supports erasing the raw metadata payloads with the specified names."""

        logger.debug("%s.erase(payloads: %s)", self.__class__.__name__, payloads)

        if payloads is None:
            payloads: list[str] = list(self._mapping.keys())
        elif not isinstance(payloads, list):
            raise TypeError(
                "The 'payloads' argument, if specified, must reference a list of strings!"
            )

        # Get the list of current payload fields embedded within the image
        fields: list[str] = self.image.get_fields()

        # Iterate through the list of payloads to remove from the image
        for payload in payloads:
            if not isinstance(payload, str):
                raise TypeError(
                    "The 'payloads' argument, if specified, must reference a list of strings!"
                )
            elif not payload in self._mapping:
                raise ValueError(
                    f"The 'payload' argument, specified a field, '{payload}', that is not supported!"
                )

            # If the payload is not present in the image, there is nothing to remove
            if payload not in fields:
                continue

            self.image.remove(payload)

    def encode(self, order: ByteOrder = None) -> None:
        logger.debug("%s.encode(order: %s)", self.__class__.__name__, order)

        if order is None:
            order = self.byteorder()
        elif not isinstance(order, ByteOrder):
            raise TypeError(
                "The 'order' argument, if specified, must reference a ByteOrder enumeration class option!"
            )

        if self.models is None:
            raise RuntimeError(
                "The 'models' property has not been set; it must reference a Models class instance!"
            )

        for model in self.models:
            # TODO: REMOVE THIS
            # if model.name == "XMP":
            #     import datetime, os
            #
            #     filename = os.path.expanduser(
            #         f"~/Downloads/00094701.{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.xml"
            #     )
            #     with open(filename, "wb+") as file:
            #         file.write(model.encode(pretty=True, order=order))

            options: dict[str, object] = dict()

            if model.name == "IPTC":
                # IPTC written to the RichTIFFIPTC Tag (33723) does not require the
                # "Photoshop" preamble required for the Adobe Resources Tag (34377)
                # so we configure the IPTC model to generate the payload in its raw
                # form; that is without the "Photoshop" preamble:
                options = dict(format=IPTCFormat.RAW)

            if isinstance(encoded := model.encode(order=order, **options), bytes):
                for fieldname, cläss in self.mapping.items():
                    if isinstance(model, cläss):
                        self.set(name=fieldname, value=encoded)
                        break

    def save(self, order: ByteOrder = None, **kwargs) -> None:
        logger.debug(
            "%s.save(order: %s, kwargs: %s)", self.__class__.__name__, order, kwargs
        )
        pass
