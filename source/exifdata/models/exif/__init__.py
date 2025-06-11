from __future__ import annotations

import os
import json

from exifdata.logging import logger

from exifdata.models import (
    Metadata,
    Namespace,
    Structure,
    Field,
    Value,
    Type,
)

from exifdata.models.exif.enumerations import (
    TagType,
)

from exifdata.models.exif.types import (
    Undefined,
    ASCII,
    Long,
    Short,
    Rational,
    RationalSigned,
    Byte,
)

from exifdata.models.exif.structures import (
    IFD,
    IFDTag,
)

from exifdata.types import (
    ByteOrder,
    Encoding,
)


logger = logger.getChild(__name__)


class Field(Field):
    _tagid: int = None
    _default: object = None

    def __init__(self, *args, tagid: int, default: object = None, **kwargs):
        super().__init__(*args, **kwargs)

        if not isinstance(tagid, int):
            raise TypeError("The 'tagid' argument must have an integer value!")

        self._tagid: int = tagid

        self._default: object = default

    @property
    def tagid(self) -> int:
        return self._tagid

    @property
    def default(self) -> object | None:
        return self._default


class EXIF(Metadata):
    _namespaces: dict[str, Namespace] = {}
    _structures: dict[str, Structure] = {}
    _aliases: dict[str, str] = {}
    _encodings: list[str] = ["UTF-8", "Unicode", "ASCII"]
    _types: dict[str, type] = {}

    # Initialize the model's namespaces from the model configuration file
    with open(
        os.path.join(os.path.dirname(__file__), "data", "schema.json"), "r"
    ) as handle:
        # Ensure the model configuration file is valid
        if not isinstance(namespaces := json.load(handle), dict):
            raise TypeError("The 'namespaces' dictionary isn't valid!")

        # Dynamically create the model namespaces based on the provided configuration
        for identifier, properties in namespaces.items():
            if not isinstance(identifier, str):
                raise TypeError("All namespace dictionary keys must be strings!")

            if not isinstance(properties, dict):
                raise TypeError(
                    "All namespace dictionary top-level values must be dictionaries!"
                )

            if identifier.startswith("@"):
                # If any top-level aliases have been specified, capture those now
                if identifier == "@aliases":
                    _aliases = properties
                continue

            if structures := properties.get("structures"):
                for _structure_id, _structure in structures.items():
                    _structures[_structure.get("name")] = Structure(
                        identifier=_structure_id,
                        **_structure,
                    )

            # Then add the name-spaced fields under the model, first creating the namespace
            if fields := properties.pop("fields"):
                # Each assignment to metadata.namespace adds to the array/list of namespaces
                _namespaces[properties.get("name")] = namespace = Namespace(
                    identifier=identifier,
                    # metadata=self,  # Set later via Metadata.__getattr__()
                    **properties,
                )

                # Now iterate over the fields and add them to the relevant namespace
                for identifier, properties in fields.items():
                    namespace.field = field = Field(
                        namespace=namespace,
                        identifier=identifier,
                        **properties,
                    )

                    # If the namespace has been marked for unwrapping, make its fields
                    # available on the top-level metadata object as well as through the
                    # namespace object itself, via its field name and any aliases:
                    if namespace.unwrap is True:
                        if field.name in _aliases:
                            raise KeyError(
                                f"The field alias, '{field.name}', has already been used!"
                            )

                        _aliases[field.name] = f"{namespace.id}:{field.name}"

                        for alias in field.aliases:
                            if alias in _aliases:
                                raise KeyError(
                                    f"The field alias, '{alias}', has already been used!"
                                )

                            _aliases[alias] = f"{namespace.id}:{field.name}"

    def encode(self, order: ByteOrder = ByteOrder.MSB) -> bytes | None:
        """Provides support for encoding the assigned EXIF metadata field values into
        the binary representation needed for embedding into an image file."""

        encoded: list[bytes] = []

        if not isinstance(order, ByteOrder):
            raise TypeError(
                "The 'order' argument must have a ByteOrder enumeration value!"
            )

        ifd = IFD()

        for namespace in self._namespaces.values():
            for identifier, field in namespace._fields.items():
                if isinstance(value := self._values.get(field.identifier), Value):
                    count: int = (len(value) if isinstance(value, list) else 1)

                    if field.multiple is True and not count in field.count:
                        raise ValueError(
                            "The value count (%d) does not match one of the field counts (%s) for %s!"
                            % (
                                count,
                                field.count,
                                field.identifier,
                            )
                        )

                    data: list[bytes] = []

                    if isinstance(value, list):
                        for value in value:
                            data.append(value.encode(order=order))
                    else:
                        data.append(value.encode(order=order))

                    # logger.debug(data)

                    data: bytes = b"".join(data)

                    # logger.debug(type(value), data)

                    ifd.tag = IFDTag(
                        id=field.tagid,
                        type=TagType.reconcile(field.type).value,
                        count=count,
                        data=data,
                    )

        encoded.append(ifd.encode(order=order))

        return b"".join(encoded) if len(encoded) > 0 else None

    @classmethod
    def decode(
        cls,
        value: bytes | io.BytesIO,
        order: ByteOrder = ByteOrder.MSB,
    ) -> EXIF:
        """Provides support for decoding the provided EXIF metadata payload into its
        corresponding EXIF metadata fields which can then be accessed for use."""

        logger.debug(
            "%s.decode(value: %d, format: %s, order: %s)",
            cls.__name__,
            len(value),
            format,
            order,
        )

        if not isinstance(value, bytes):
            value = io.BytesIO(value)
        elif isinstance(value, io.BytesIO):
            pass
        else:
            raise TypeError("The 'value' argument must have a bytes or BytesIO value!")

        # TODO: Complete implementation of EXIF metadata parsing

        return None


EXIF.register_types(
    Undefined,
    ASCII,
    Long,
    Short,
    Rational,
    RationalSigned,
    Byte,
)
