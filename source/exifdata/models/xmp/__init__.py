from __future__ import annotations

import os
import json
import enumerific
import maxml

from exifdata.logging import logger
from exifdata.configuration import secrets

from exifdata.models import (
    Metadata,
    Type,
    Namespace,
    Structure,
    Field,
    Value,
)

from exifdata.models.xmp.types import (
    Integer,
    Boolean,
    Real,
    Rational,
    Text,
    Date,
    DateTime,
    Time,
    Timecode,
    GUID,
    URL,
    URI,
    Struct,
    Thumbnail,
    AgentName,
    ProperName,
    ContactInfo,
    ResourceRef,
    RenditionClass,
    ResourceEvent,
    Version,
    Job,
    Colorants,
    Font,
    Dimensions,
    Layer,
    Marker,
    Track,
    Media,
    CFAPattern,
    BeatSpliceStretch,
    ResampleStretch,
    TimeScaleStretch,
    ProjectLink,
    LanguageAlternative,
    Ancestor,
    DeviceSettings,
    Flash,
    OECFSFR,
    MIMEType,
    Locale,
)

from exifdata.types import (
    ByteOrder,
    Encoding,
)


logger = logger.getChild(__name__)


class XMP(Metadata):
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

        # Define the required top-level document namespaces
        namespaces = {
            "x": "http://ns.adobe.com/x/1.0",
            "xmlns": "http://ns.adobe.com/xmlns/1.0",
            # "rdf":   "http://ns.adobe.com/rdf/1.0",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        }

        # maxml.Element.register_namespace("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")

        # Register the required top-level document namespaces
        for prefix, uri in namespaces.items():
            maxml.Element.register_namespace(prefix, uri)

        # Register the required document schema namespaces, sourced from configuration
        for namespace in _namespaces.values():
            maxml.Element.register_namespace(namespace.prefix, namespace.uri)

    @classmethod
    def from_exiftool_fields(cls, fields: dict[str, object]) -> XMP | None:
        """This method provides support for mapping metadata field values specified with
        the field names that EXIFTool uses to the matching fields supported by XMP."""

        if not isinstance(fields, dict):
            raise TypeError("The 'fields' argument must have a dictionary value!")

        xmp = XMP()

        for name, value in fields.items():
            if match := XMP.field_by_property(property="names", value=name):
                (namespace, field) = match

                try:
                    xmp.set(namespace=namespace, field=field, value=value)
                except ValueError as exception:
                    logger.error(
                        "%s.from_exiftool_fields() The '%s' field failed validation: %s"
                        % (cls.__name__, name, str(exception))
                    )
            else:
                logger.warning(
                    "%s.from_exiftool_fields() The '%s' field could not be found!"
                    % (cls.__name__, name)
                )

        return xmp or None

    def encode(
        self,
        encoding: str = "UTF-8",
        pretty: bool = False,
        wrap: bool = False,
        order: ByteOrder = None,  # ignored, but here for consistency with other models
    ) -> bytes:
        """Generate an encoded version of the XMP metadata suitable for embedding into
        an image file. By default the generated XML string will be compacted without any
        whitespace characters to minimise space requirements. For readability the output
        can be pretty printed to include whitespace by setting pretty to True."""

        if not isinstance(encoding, str):
            raise TypeError("The 'encoding' argument must have a string value!")

        if not encoding.lower() in [enc.lower() for enc in self.__class__._encodings]:
            raise ValueError(
                "The 'encoding' argument must have one of the following values: %s"
                % (", ".join(self.__class__._encodings))
            )

        if encoding.upper() == "UTF-8":
            encoding == "Unicode"

        if not isinstance(pretty, bool):
            raise TypeError("The 'pretty' argument must have a boolean value!")

        if not isinstance(wrap, bool):
            raise TypeError("The 'wrap' argument must have a boolean value!")

        if order is None:
            pass
        elif not isinstance(order, ByteOrder):
            raise TypeError(
                "The 'order' argument must have a ByteOrder enumeration value!"
            )

        root: maxml.Element = maxml.Element("x:xmpmeta", namespace="adobe:ns:meta/")

        # TODO: Customize this
        root.set("x:xmptk", "Adobe XMP Core 9.1-c002 79.f354efc70, 2023/11/09-12:05:53")

        rdf: maxml.Element = root.subelement("rdf:RDF")

        description: maxml.Element = rdf.subelement("rdf:Description")

        description.set("rdf:about", "")

        for identifier, namespace in self._namespaces.items():
            if namespace.utilized is True:
                # Map the namespace prefix and URI into the description node
                description.set(f"xmlns:{namespace.prefix}", namespace.uri)

                # Map the individual namespace fields into the description node
                for identifier, field in namespace._fields.items():
                    parent: maxml.Element = description

                    if structure := field.structure:
                        if struct := description.find(structure.identifier):
                            if bag := struct.find("rdf:Bag"):
                                if listing := bag.find("rdf:li"):
                                    parent = listing
                                else:
                                    pass
                            else:
                                pass
                        elif struct := description.subelement(structure.identifier):
                            if structure.type == "Bag":
                                if bag := struct.subelement("rdf:Bag"):
                                    if listing := bag.subelement(
                                        "rdf:li",
                                        **{
                                            "rdf:parseType": "Resource",
                                        },
                                    ):
                                        parent = listing
                            else:
                                raise TypeError(
                                    "The 'structure.type' of '%s' is not currently supported!"
                                    % (structure.type)
                                )

                    if not (value := self._values.get(field.identifier)) is None:
                        if element := parent.subelement(field.identifier):
                            if isinstance(value, list):
                                if sequence := element.subelement("rdf:Seq"):
                                    for index, val in enumerate(value):
                                        if li := sequence.subelement("rdf:li"):
                                            encoded = val.encode(element=li)

                                            if encoded is None:
                                                continue
                                            elif isinstance(encoded, bytes):
                                                encoded = encoded.decode(encoding)
                                            elif not isinstance(
                                                encoded, (int, str, float)
                                            ):
                                                raise TypeError(
                                                    "The call to 'value.encoded()' returned a %s value; check the implementation of %s.encoded() to ensure that it returns a value appropriate for the metadata model!"
                                                    % (
                                                        type(encoded),
                                                        encoded.__class__.__name__,
                                                    ),
                                                )

                                            li.text = encoded
                            else:
                                encoded = value.encode(element=element)

                                # For values that haven't been encoded to a usable type
                                if encoded is None:
                                    continue
                                elif isinstance(encoded, Value):
                                    raise TypeError(
                                        "The call to 'value.encoded()' returned a Value class instance; check the implementation of %s.encoded() to ensure that it returns a value appropriate for the metadata model!"
                                        % (encoded.__class__.__name__),
                                    )
                                elif isinstance(encoded, bytes):
                                    encoded = encoded.decode(encoding)
                                elif not isinstance(encoded, (int, str, float)):
                                    raise TypeError(
                                        "The call to 'value.encoded()' returned a %s value; check the implementation of %s.encoded() to ensure that it returns a value appropriate for the metadata model!"
                                        % (type(encoded), encoded.__class__.__name__),
                                    )

                                element.text = encoded

        encoded = root.tostring(
            pretty=pretty,
        )

        if wrap is True:
            encoded = "".join(
                [
                    """<?xpacket begin="\ufeff" id="W5M0MpCehiHzreSzNTczkc9d"?>""",
                    encoded,
                    """<?xpacket end="w"?>""",
                ]
            )

        if encoding:
            encoded = encoded.encode(encoding)

        return encoded

    @classmethod
    def decode(
        cls,
        value: bytes | str = None,
        encoding: str = "UTF-8",
        order: ByteOrder = ByteOrder.MSB,
    ) -> XMP:
        """Provides support for decoding the provided XMP metadata payload into its
        corresponding XMP metadata fields which can then be accessed for use."""

        logger.debug(
            "%s.decode(value: %s, encoding: %s, order: %s)",
            cls.__name__,
            len(value),
            encoding,
            order,
        )

        if not isinstance(value, bytes):
            raise TypeError("The 'value' argument must have a bytes or string value!")

        if not isinstance(encoding, str):
            raise TypeError("The 'encoding' argument must have a string value!")

        if order is None:
            pass
        elif not isinstance(order, ByteOrder):
            raise TypeError(
                "The 'order' argument, if specified, must have a ByteOrder value!"
            )

        if isinstance(value, bytes):
            value = value.decode(encoding)

        # logger.debug("*" * 100)
        # logger.debug(type(value))
        # logger.debug(value)
        # logger.debug("*" * 100)

        # document = maxml.Document.from_string(value)

        # TODO: Complete implementation of XMP metadata parsing

        return None


XMP.register_types(
    Integer,
    Boolean,
    Real,
    Rational,
    Text,
    Date,
    DateTime,
    Time,
    Timecode,
    GUID,
    URL,
    URI,
    Struct,
    Thumbnail,
    AgentName,
    ProperName,
    ContactInfo,
    ResourceRef,
    RenditionClass,
    ResourceEvent,
    Version,
    Job,
    Colorants,
    Font,
    Dimensions,
    Layer,
    Marker,
    Track,
    Media,
    CFAPattern,
    BeatSpliceStretch,
    ResampleStretch,
    TimeScaleStretch,
    ProjectLink,
    LanguageAlternative,
    Ancestor,
    DeviceSettings,
    Flash,
    OECFSFR,
    MIMEType,
    Locale,
)
