from __future__ import annotations

import os
import json
import io

from exifdata.logging import logger

from exifdata.framework import (
    Metadata,
    Structure,
    Value,
    Type,
)

from exifdata.models.iptc.framework.field import Field
from exifdata.models.iptc.framework.namespace import Namespace

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
    Short,
    Long,
    # Rational,
    # RationalSigned,
    # Byte,
    String,
)

from deliciousbytes import (
    ByteOrder,
    Encoding,
    UInt8,
    UInt16,
    UInt32,
    Int32,
)


logger = logger.getChild(__name__)


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
    _setup: bool = False

    def __new__(cls):
        """Initialize the model's namespaces from the schema configuration file once."""

        # If the setup has already been performed previously, return immediately
        if cls._setup is True:
            return super().__new__(cls)

        with open(
            os.path.join(os.path.dirname(__file__), "data", "schema.json"), "r"
        ) as handle:
            # Ensure the model configuration file is valid
            if not isinstance(namespacesdata := json.load(handle), dict):
                raise TypeError("The 'namespaces' dictionary isn't valid!")

            # Dynamically create the model namespaces based on the provided configuration
            for namespaceid, namespacedata in namespacesdata.items():
                # logger.debug(" - Namespace: %s" % (identifier))

                if not isinstance(namespaceid, str):
                    raise TypeError("All namespace dictionary keys must be strings!")

                if namespaceid.startswith("@"):
                    # If any top-level aliases have been specified, capture those now
                    if namespaceid == "@aliases" and isinstance(namespacedata, dict):
                        aliases = namespacedata
                    continue

                if not isinstance(namespacedata, dict):
                    raise TypeError(
                        "All model schema top-level values must be dictionaries!"
                    )

                if structures := namespacedata.get("structures"):
                    for structureid, structuredata in structures.items():
                        # Assign the new Structure to the top-level _structures dictionary
                        cls._structures[structuredata.get("name")] = Structure(
                            identifier=structureid,
                            **structuredata,
                        )

                # Add the namespaced fields under the model, first creating the namespace
                if fieldsdata := namespacedata.pop("fields"):
                    # Assign the new Namespace to the top-level _namespaces dictionary
                    cls._namespaces[namespacedata.get("name")] = namespace = Namespace(
                        identifier=namespaceid,
                        # metadata=self,  # Set later via Metadata.__getattr__()
                        **namespacedata,  # pass the properties via dictionary expansion
                    )

                    # Now iterate over the fields and add them to the relevant namespace
                    for fieldid, fielddata in fieldsdata.items():
                        # logger.debug("  - Field: %s (%s)" % (fieldid, fielddata.get("name")))

                        namespace.field = field = Field(
                            namespace=namespace,
                            identifier=fieldid,
                            **fielddata,  # pass the properties via dictionary expansion
                        )

                        field.record_id = RecordID.register(
                            name=field.name,
                            value=RecordInfo(
                                record_id=namespace.tagid,
                                dataset_id=field.tagid,
                                type=field.type,
                            ),
                        )

        cls._setup = True

        return super().__new__(cls)

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
            logger.info(
                "No IPTC metadata fields were assigned values, so there is nothing to encode."
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

        # # Iterate through the namespaces and fields to emit the metadata in a fixed
        # # order based on when the field name is encountered during iteration:
        # for namespace in self._namespaces.values():
        # if namespace.utilized is False:
        #     continue
        # for identifier, field in namespace._fields.items():
        #     if not (value := self._values.get(field.identifier)) is None:
        #         if record := Record(
        #             id=field.record_id,
        #             value=value,
        #         ):
        #             logger.debug("0x%02x, 0x%02x, %s, %s" % (field.record_id.record_id, field.record_id.dataset_id, field.identifier, field.record_id.type))
        #             encoded.append(record.encode(order=order))

        # Determine if the Record Version has been set
        found_record_version: bool = False
        for field_id in self._values.keys():
            if result := self.field_by_id(field_id):
                (namespace, field) = result

                if field.record_id == RecordID.RecordVersion:
                    found_record_version = True

        # If not, add the Record Version field for IPTC [> 1C 02 00 00 02 00 04 00 00 <]
        if found_record_version is False:
            record = Record(id=RecordID.RecordVersion, value=Short(0x04))
            encoded.append(record.encode(order=order))

        # Iterate over the values, encoding them as we go so that the encoded version of
        # the IPTC tags matches the order that they were decoded or added:
        for field_id, value in self._values.items():
            if result := self.field_by_id(field_id):
                (namespace, field) = result

                if record := Record(
                    id=field.record_id,
                    value=value,
                ):
                    logger.debug(
                        "0x%02x, 0x%02x, %s, %s, %r"
                        % (
                            record.id.record_id,
                            record.id.dataset_id,
                            field.identifier,
                            record.id.type,
                            value,
                        )
                    )

                    encoded.append(record.encode(order=order))

        if len(encoded) > 0:
            # Pad the IPTC payload so that its length is evenly divisible by four bytes
            while not sum(map(len, encoded)) % 4 == 0:
                encoded.append(UInt8(0x00).encode(order=order))

        return b"".join(encoded)

    @classmethod
    def decode(
        cls,
        value: bytes | bytearray | io.BytesIO,
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

        if isinstance(value, (bytes, bytearray)):
            value = io.BytesIO(value)
        elif isinstance(value, io.BytesIO):
            pass
        else:
            raise TypeError(
                "The 'value' argument must have a bytes, bytearray or io.BytesIO value!"
            )

        if not isinstance(format, IPTCFormat):
            raise TypeError(
                "The 'format' argument must have an IPTCFormat enumeration value!"
            )

        position: int = value.tell()

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
            value.seek(0)

            while isinstance(byte := value.read(1), bytes) and byte:
                index = value.tell()

                logger.debug(
                    "%02d ~> 0x%02x, %r",
                    index,
                    (int(byte.hex(), 16) if byte else 0),
                    byte,
                )

                if index == 0 and not byte == 0x1C:
                    raise ValueError(
                        "The 'value' does not begin with the expected '0x1C' IPTC record marker!"
                    )

        records: list[Record] = []

        value.seek(position)

        while isinstance(byte := value.read(1), bytes) and byte:
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
