from __future__ import annotations

import os
import json
import io

from exifdata.logging import logger

from exifdata.models import (
    Metadata,
    Namespace,
    Structure,
    Field,
    Value,
    Type,
)

from exifdata.models.iptc.enumerations import (
    IPTCFormat,
    RecordID,
    RecordInfo,
)

from exifdata.models.iptc.structures import (
    Records,
    Record,
)

from exifdata.models.iptc.types import (
    # Undefined,
    # ASCII,
    Long,
    Short,
    # Rational,
    # RationalSigned,
    # Byte,
    String,
)

from exifdata.types import (
    ByteOrder,
    Encoding,
    UInt8,
    UInt16,
    UInt32,
    Int32,
)


logger = logger.getChild(__name__)


class Field(Field):
    _bytes_min: int = None
    _bytes_max: int = None
    _repeatable: bool = None
    _record_id: RecordID = None

    def __init__(
        self,
        *args,
        tagid: int,
        bytes_min: int,
        bytes_max: int,
        repeatable: bool,
        record_id: RecordID = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self._tagid: int = tagid
        self._bytes_min: int = bytes_min
        self._bytes_max: int = bytes_max
        self._repeatable: bool = repeatable
        self._record_id: RecordID = record_id

    @property
    def tagid(self) -> int:
        return self._tagid

    @property
    def dataset_id(self) -> int:
        return self._tagid

    @property
    def bytes_min(self) -> int:
        return self._bytes_min

    @property
    def bytes_max(self) -> int:
        return self._bytes_max

    @property
    def repeatable(self) -> bool:
        return self._repeatable

    @property
    def record_id(self) -> RecordID | None:
        return self._record_id

    @record_id.setter
    def record_id(self, record_id: RecordID) -> RecordID | None:
        if not isinstance(record_id, RecordID):
            raise TypeError(
                "The 'record_id' argument must reference a RecordID class instance!"
            )

        self._record_id = record_id


class Namespace(Namespace):
    def __init__(self, *args, tagid: int, **kwargs):
        super().__init__(*args, **kwargs)
        self._tagid: int = tagid

    @property
    def tagid(self) -> int:
        return self._tagid

    @property
    def record_id(self) -> int:
        return self._tagid


class IPTC(Metadata):
    _namespaces: dict[str, Namespace] = {}
    _structures: dict[str, Structure] = {}
    _aliases: dict[str, str] = {}
    _encodings: list[str] = ["UTF-8", "Unicode", "ASCII"]
    _types: dict[str, type] = {}

    _app13prefix: bytearray = [
        b"P",
        b"h",
        b"o",
        b"t",
        b"o",
        b"s",
        b"h",
        b"o",
        b"p",
        b" ",
        b"3",
        b".",
        b"0",
        b"\x00",
    ]

    # Initialize the model's namespaces from the model configuration file
    with open(
        os.path.join(os.path.dirname(__file__), "data", "schema.json"), "r"
    ) as handle:
        # Ensure the model configuration file is valid
        if not isinstance(namespaces := json.load(handle), dict):
            raise TypeError("The 'namespaces' dictionary isn't valid!")

        # Dynamically create the model namespaces based on the provided configuration
        for identifier, properties in namespaces.items():
            # logger.debug(" - Namespace: %s" % (identifier))

            if not isinstance(identifier, str):
                raise TypeError("All namespace dictionary keys must be strings!")

            if not isinstance(properties, dict):
                raise TypeError(
                    "All namespace dictionary top-level values must be dictionaries!"
                )

            if identifier.startswith("@"):
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
                # logger.debug(properties)

                # Each assignment to metadata.namespace adds to the array/list of namespaces
                _namespaces[properties.get("name")] = namespace = Namespace(
                    identifier=identifier,
                    # metadata=self,  # Set later via Metadata.__getattr__()
                    **properties,  # pass the properties via dictionary expansion
                )

                # Now iterate over the fields and add them to the relevant namespace
                for identifier, properties in fields.items():
                    # logger.debug("  - Field: %s (%s)" % (identifier, properties.get("name")))

                    namespace.field = field = Field(
                        namespace=namespace,
                        identifier=identifier,
                        **properties,  # pass the properties via dictionary expansion
                    )

                    field.record_id = RecordID.register(
                        name=field.name,
                        value=RecordInfo(
                            record_id=namespace.tagid,
                            dataset_id=field.tagid,
                            type=field.type,
                        ),
                    )

    @property
    def record(self):
        raise NotImplementedError

    @record.setter
    def record(self, record: Record):
        """Support assigning IPTC metadata model field values via IPTC Record instances
        which makes it easier to reconstruct an IPTC metadata model from Records decoded
        from a raw IPTC bytes payload."""

        logger.debug("%s.record() => %s" % (self.__class__.__name__, record))

        if not isinstance(record, Record):
            raise TypeError(
                "The 'record' argument must reference a Record class instance!"
            )

        logger.debug(
            "%s.record() => [%s] %s, %s, %s, %s => %r"
            % (
                self.__class__.__name__,
                id(record.id),
                record.id,
                record.id.record_id,
                record.id.dataset_id,
                record.id.type,
                record.value,
            )
        )

        # Attempt to find the metadata model field by its record.id property value
        if result := self.field_by_property(property="record_id", value=record.id):
            (namespace, field) = result

            # If the field was found, set the fields value within the relevant namespace
            # of the current IPTC metadata model instance (self):
            namespace.set(metadata=self, field=field, value=record.value)
        else:
            raise ValueError(
                f"Unable to find a field on the IPTC metadata model with record ID: {record.id}!"
            )

    def encode(
        self,
        order: ByteOrder = ByteOrder.MSB,
        format: IPTCFormat = IPTCFormat.APP13,
    ) -> bytes:
        """Provides support for encoding the assigned IPTC metadata field values into
        the binary representation needed for embedding into an image file."""

        encoded: list[bytes] = []

        if not isinstance(order, ByteOrder):
            raise TypeError(
                "The 'order' argument must have a ByteOrder enumeration value!"
            )

        if not isinstance(format, IPTCFormat):
            raise TypeError(
                "The 'format' argument must have an IPTCFormat enumeration value!"
            )

        if len(self._values) == 0:
            logger.warning(
                "No IPTC metadata fields were assigned values, so there is nothing to encode!"
            )
            return None

        if format is IPTCFormat.APP13:
            # Include the standard APP13 "Photoshop 3.0" prefix
            encoded.extend(self.__class__._app13prefix)

            # Include the 8BIM marker, noting a binary structure within the APP13 block
            encoded.append(b"8")
            encoded.append(b"B")
            encoded.append(b"I")
            encoded.append(b"M")

            # Include the 0x04 0x04 Photoshop APP13 resource ID for IPTC-IIM
            encoded.append(UInt8(0x04).encode(order=order))
            encoded.append(UInt8(0x04).encode(order=order))

            # Include required empty string/data
            encoded.append(UInt16(0x00).encode(order=order))
            encoded.append(UInt16(0x00).encode(order=order))
            encoded.append(UInt8(0x00).encode(order=order))
            encoded.append(b":")

        elif format is IPTCFormat.RAW:
            pass

        #         # Iterate through the namespaces and fields to emit the metadata in a fixed
        #         # order based on when the field name is encountered during iteration:
        #         for namespace in self._namespaces.values():
        #             if namespace.utilized is False:
        #                 continue
        #
        #             for identifier, field in namespace._fields.items():
        #                 if not (value := self._values.get(field.identifier)) is None:
        #                     if record := Record(
        #                         id=field.record_id,
        #                         value=value,
        #                     ):
        #                         logger.debug("0x%02x, 0x%02x, %s, %s" % (field.record_id.record_id, field.record_id.dataset_id, field.identifier, field.record_id.type))
        #
        #                         encoded.append(record.encode(order=order))

        # from utilities import print_bytes_hex_debug

        # Iterate over the values, encoding them as we go so that the encoded version of
        # the IPTC tags matches the order that they were decoded or added:
        for field_id, value in self._values.items():
            if result := self.field_by_id(field_id):
                (namespace, field) = result

                if record := Record(
                    id=field.record_id,
                    value=value,
                ):
                    # logger.debug("0x%02x, 0x%02x, %s, %s" % (
                    #     record.id.record_id,
                    #     record.id.dataset_id,
                    #     field.identifier,
                    #     record.id.type,
                    # ))
                    # logger.debug("%r" % (value))

                    encoded.append(record.encode(order=order))

                    # print_bytes_hex_debug(encoded[-1])

        return b"".join(encoded)

    @classmethod
    def decode(
        cls,
        value: bytes | io.BytesIO,
        format: IPTCFormat = IPTCFormat.APP13,
        order: ByteOrder = ByteOrder.MSB,
    ) -> IPTC:
        """Provides support for decoding the provided IPTC metadata payload into its
        corresponding IPTC metadata fields which can then be accessed for use."""

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

        if not isinstance(format, IPTCFormat):
            raise TypeError(
                "The 'format' argument must have an IPTCFormat enumeration value!"
            )

        if format is IPTCFormat.APP13:
            iptc_found: bool = False

            # Ensure the "Photoshop 3.0" prefix is present to mark the APP13 EXIF tag
            while byte := value.read(1):
                index = value.tell()

                logger.debug(
                    "%02d => 0x%02x, %r, %r",
                    index,
                    int(byte.hex(), 16),
                    byte,
                    cls._app13prefix[index - 1],
                )

                if index == len(cls._app13prefix):
                    break
                elif not cls._app13prefix[index - 1] == byte:
                    raise ValueError(
                        "The 'value' prefix does not contain the expected %r value at offset %d, but %r!"
                        % (
                            cls._app13prefix[index - 1],
                            index,
                            byte,
                        )
                    )

            # There could be other metadata in APP13 before and after the IPTC tags
            while byte := value.read(1):
                index = value.tell()

                logger.debug("%02d => 0x%02x, %r", index, int(byte.hex(), 16), byte)

                # If an 8 is encountered, it could be the start of the 8BIM marker that
                # denotes that a binary data structure is nested within the APP13 block
                if byte == b"8":
                    if next := value.read(3):
                        if next == b"BIM":
                            for i, b in enumerate(next, start=index + 1):
                                b = bytes([b])

                                logger.debug(
                                    "%02d => 0x%02x, %r", i, int(b.hex(), 16), b
                                )

                                index += 1

                            break

            # There could be other metadata in APP13 before and after the IPTC tags
            while byte := value.read(1):
                index = value.tell()

                logger.debug("%02d +> 0x%02x, %r", index, int(byte.hex(), 16), byte)

                # Now look for the 0x04 0x04 Photoshop APP13 resource ID for IPTC-IIM
                if int(byte.hex(), 16) == 0x04:
                    if next := value.read(1):
                        if int(next.hex(), 16) == 0x04:
                            for i, b in enumerate(next, start=index + 1):
                                b = bytes([b])

                                logger.debug(
                                    "%02d +> 0x%02x, %r", i, int(b.hex(), 16), b
                                )

                                index += 1

                            logger.debug(">>> Found IPTC")

                            iptc_found = True

                            break

            if iptc_found is False:
                return None

        elif format is IPTCFormat.RAW:
            while byte := value.read(1):
                index = value.tell()

                logger.debug("%02d ~> 0x%02x, %r", index, int(byte.hex(), 16), byte)

                if index == 0 and not byte == 0x1C:
                    raise ValueError(
                        "The 'value' does not begin with the expected '0x1C' IPTC record marker!"
                    )

        records: list[Record] = []

        while byte := value.read(1):
            index = value.tell()

            logger.debug("%02d ~> 0x%02x, %r", index, int(byte.hex(), 16), byte)

            if int(byte.hex(), 16) == 0x1C:
                record_id = value.read(1)

                dataset_id = value.read(1)

                # logger.debug(">>> Found IPTC Record(id: %s, dataset: %s)", record_id, dataset_id)

                length = value.read(2)

                # If the length value is the special 0x8004 marker, it denotes that the
                # data length is encoded in the following four bytes as a 32-bit integer
                if length[0] == 0x80 and length[1] == 0x04:
                    length = value.read(4)

                # We then decode the length value from its encoded form
                datalength: Int32 = Int32.decode(value=length, order=order)

                # We can then read the correct amount of data from the buffer
                data = value.read(datalength)

                # Next we assemble the raw data extracted from the buffer for decoding
                # by the Record class:
                if record := Record.decode(
                    value=b"".join(
                        [
                            bytes([0x1C]),
                            record_id,
                            dataset_id,
                            length,
                            data,
                        ]
                    )
                ):
                    records.append(record)

        if len(records) > 0:
            iptc = IPTC()

            for record in records:
                logger.debug(" >>> Record ID => %s", record.id)
                iptc.record = record

            return iptc


IPTC.register_types(
    # Undefined,
    # ASCII,
    Long,
    Short,
    # Rational,
    # RationalSigned,
    # Byte,
    String,
)
