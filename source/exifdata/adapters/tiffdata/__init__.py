from __future__ import annotations

from exifdata.logging import logger
from exifdata.framework.adapter import Adapter
from exifdata.framework import Metadata, Field, Value
from exifdata.models.exif import EXIF
from exifdata.models.iptc import IPTC, IPTCFormat
from exifdata.models.xmp import XMP

from deliciousbytes import ByteOrder

from tiffdata import TIFF, IFD

import os

logger = logger.getChild(__name__)


class TIFFData(Adapter):
    """Supports working with images through the TIFFData library, including the ability
    extracting and decoding, as well as, encoding and embedding of image metadata."""

    # Mapping between TIFF metadata tag names and EXIFData model classes
    _mapping: dict[str, Metadata] = {
        "EXIFIFD": EXIF,
        "RichTIFFIPTC": IPTC,
        "XMLPacket": XMP,
    }

    _image: TIFF = None

    @classmethod
    def open(cls, filepath: str, **kwargs) -> TIFFData:
        """Supports opening the specified image file from disk. The image must exist at
        the specified filepath, and the image must use a supported image format."""

        if not isinstance(filepath, str):
            raise TypeError("The 'filepath' argument must have a string value!")
        elif not os.path.exists(filepath):
            raise ValueError(
                f"The 'filepath' argument, '{filepath}', references a file that does not exist!"
            )
        elif not os.path.isfile(filepath):
            raise ValueError(
                f"The 'filepath' argument, '{filepath}', references a something other than a file!"
            )

        if isinstance(image := TIFF(filepath), TIFF):
            return cls(image=image, **kwargs)
        else:
            raise RuntimeError(
                f"Unable to load the specified image file, '{filepath}', using the TIFFData library!"
            )

    @classmethod
    def load(cls, image: TIFF, **kwargs) -> TIFFData:
        """Supports working with the specified in-memory image. The image argument must
        reference a TIFFData TIFF class instance, for a supported TIFF file format."""

        if not isinstance(image, TIFF):
            raise TypeError(
                "The 'image' argument must reference a TIFFData 'TIFF' class instance!"
            )

        return cls(image=image, **kwargs)

    def __new__(cls, *args, **kwargs) -> TIFFData:
        return super().__new__(cls)

    def __init__(self, image: TIFF):
        if not isinstance(image, TIFF):
            raise TypeError(
                "The 'image' argument must reference a TIFFData 'TIFF' class instance!"
            )
        self._image = image

    @property
    def image(self) -> TIFF:
        return self._image

    @property
    def mapping(self) -> dict[str, Metadata]:
        return self._mapping

    def fields(self) -> list[str]:
        fields: list[str] = []

        for ifd in self.image:
            for tag in ifd:
                fields.append(tag.name)

        return fields

    def get(self, field: str, ifd: int | IFD | bool = True, **kwargs) -> bytes | None:
        """Supports getting raw metadata payload values for the specified field."""

        logger.debug(
            "%s.get(field: %s, ifd: %s)",
            self.__class__.__name__,
            field,
            ifd,
        )

        if isinstance(field, Field):
            field = field.name
        elif isinstance(field, str):
            pass
        else:
            raise TypeError("The 'field' argument must have a Field or string value!")

        if not isinstance(ifd, (int, IFD, bool)):
            raise TypeError(
                "The 'ifd' argument must have an integer, IFD or boolean value!"
            )

        return self.image.get(key=field, ifd=ifd, **kwargs)

    def set(
        self,
        field: Field | str,
        value: bytes,
        ifd: int | IFD | bool = False,
        **kwargs,
    ) -> Adapter:
        """Supports setting raw metadata payload values for the specified field."""

        logger.debug(
            "%s.set(field: %s, value: %s, ifd: %s)",
            self.__class__.__name__,
            field,
            type(value),
            ifd,
        )

        if isinstance(field, Field):
            field = field.name
        elif isinstance(field, str):
            pass
        else:
            raise TypeError("The 'field' argument must have a Field or string value!")

        if not isinstance(ifd, (int, IFD, bool)):
            raise TypeError(
                "The 'ifd' argument must have an integer, IFD or boolean value!"
            )

        if not isinstance(value, (bytes, bytearray)):
            if isinstance(value, Value):
                logger.debug(
                    "The value for '%s' should have a bytes or bytearray value, but was %s!",
                    field,
                    type(value),
                )

                value = value.encode(order=self.image.order)
            else:
                raise TypeError(
                    "The value for '%s' should have a bytes or bytearray value, not %s!"
                    % (
                        field,
                        type(value),
                    )
                )

                return self

        self.image.set(key=field, value=value, ifd=ifd, **kwargs)

        return self

    def erase(self, payloads: list[str] = None, ifd: int | IFD | bool = True) -> None:
        """Supports erasing the raw metadata payloads with the specified names."""

        logger.debug(
            "%s.erase(payloads: %s, ifd: %s)",
            self.__class__.__name__,
            payloads,
            ifd,
        )

        if payloads is None:
            payloads: list[str] = list(self._mapping.keys())
        elif not isinstance(payloads, list):
            raise TypeError(
                "The 'payloads' argument, if specified, must reference a list of strings!"
            )

        if not isinstance(ifd, (int, IFD, bool)):
            raise TypeError(
                "The 'ifd' argument must have an integer, IFD or boolean value!"
            )

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

            self.image.remove(key=payload, ifd=ifd)

    def byteorder(self) -> ByteOrder:
        return self.image.order

    def decode(self, order: ByteOrder = None) -> None:
        """Supports decoding any metadata payloads from the image."""

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

        raise NotImplementedError

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

    def encode(self, order: ByteOrder = None, ifd: int | IFD | bool = False) -> None:
        """Supports encoding the metadata payloads and embedding them into the image."""

        logger.debug(
            "%s.encode(order: %s, ifd: %s)",
            self.__class__.__name__,
            order,
            ifd,
        )

        if order is None:
            order = self.byteorder()
        elif not isinstance(order, ByteOrder):
            raise TypeError(
                "The 'order' argument, if specified, must reference a ByteOrder enumeration class option!"
            )

        if not isinstance(ifd, (int, IFD, bool)):
            raise TypeError(
                "The 'ifd' argument must have an integer, IFD or boolean value!"
            )

        if self.models is None:
            raise RuntimeError(
                "The 'models' property has not been set; it must reference a Models class instance!"
            )

        for model in self.models:
            if model.name == "EXIF":
                # EXIF metadata fields are written individually via TIFFData
                for field, value in model.items():
                    # TODO: Value may need to be encoded, according to the needs of the
                    # EXIF field that the value will be assigned to
                    self.set(field=field, value=value, ifd=ifd)
            else:
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
                            self.set(field=fieldname, value=encoded, ifd=ifd)
                            break

    def save(self, order: ByteOrder = None, **kwargs) -> None:
        """Supports saving the image to storage via the adapter."""

        logger.debug(
            "%s.save(order: %s, kwargs: %s)", self.__class__.__name__, order, kwargs
        )

        return self.image.save(**kwargs)
