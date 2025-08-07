from __future__ import annotations

import re
import datetime
import enumerific
import base64
import abc
import maxml

from exifdata.configuration import secrets
from exifdata.logging import logger

from exifdata.framework import (
    Type,
    Field,
    Value,
)

from deliciousbytes import (
    ByteOrder,
    Encoding,
)


logger = logger.getChild(__name__)


class Value(Value):
    @abc.abstractmethod
    def encode(self, element: maxml.Element):
        pass


class Integer(int, Value):
    _encoding: Encoding = Encoding.Unicode

    def __new__(cls, *args, value: int = None, **kwargs):
        if value is None:
            if len(args) >= 1:
                value = args[0]

        return super().__new__(cls, value)

    def encode(self, element: maxml.Element = None) -> bytes:
        return str(self).encode(self.encoding.value)

    @classmethod
    def decode(cls, value: bytes) -> Integer:
        if not isinstance(value, bytes):
            raise TypeError("The 'value' argument must have a bytes value!")

        # As decode is a class method we need to access _encoding via its named variable
        # as the matching instance property is not yet available:
        value = value.decode(cls._encoding.value)

        # Create a new instance of the class, initialized with the decoded value:
        return cls(value=int(value))


class Real(float, Value):
    _encoding: Encoding = Encoding.Unicode

    def __new__(cls, *args, value: float = None, **kwargs):
        if value is None:
            if len(args) >= 1:
                value = args[0]

        if not isinstance(value, (int, float)):
            raise TypeError("The 'value' argument must have a float or integer value!")

        return super().__new__(cls, float(value))

    def encode(self, element: maxml.Element = None) -> bytes:
        return str(self).encode(self.encoding.value)

    @classmethod
    def decode(cls, value: bytes) -> Real:
        if not isinstance(value, bytes):
            raise TypeError("The 'value' argument must have a bytes value!")

        # As decode is a class method we need to access _encoding via its named variable
        # as the matching instance property is not yet available:
        value = value.decode(cls._encoding.value)

        # Create a new instance of the class, initialized with the decoded value:
        return cls(value=float(value))


class Rational(str, Value):
    """Entered as a floating-point value, but stored as two integers separated by '/' as
    the value that is stored is the ratio representing the value, e.g. 0.75 = 3/4."""

    _encoding: Encoding = Encoding.Unicode
    _numerator: int = None
    _denominator: int = None

    class RationalParts(object):
        def __init__(self, value: float, numerator: int, denominator: int):
            self.value = value
            self.numerator = numerator
            self.denominator = denominator

        def __str__(self) -> str:
            return f"{self.numerator}/{self.denominator}"

        def __float__(self) -> float:
            return float(self.numerator) / float(self.denominator)

    @classmethod
    def parse(cls, value: float | int | str | bytes) -> RationalParts:
        numerator: int | str = None
        denominator: int | str = None

        if isinstance(value, (float, int)):
            if isinstance(value, int):
                value = float(value)

            (numerator, denominator) = value.as_integer_ratio()
        elif isinstance(value, str):
            if not re.match(r"^([0-9]+)/([0-9]+)$", value):
                raise ValueError(
                    "When passed as a string, the rational 'value' argument must match the expected format of x/y, where both x and y are integer values!"
                )

            (numerator, denominator) = value.split("/")

            numerator = int(numerator)
            denominator = int(denominator)

            value = float(numerator) / float(denominator)
        else:
            raise TypeError(
                "The 'value' argument must have a float, integer, or string value!"
            )

        return cls.RationalParts(
            value=value,
            numerator=numerator,
            denominator=denominator,
        )

    def __new__(
        cls,
        *args,
        value: float | int | str = None,
        numerator: int = None,
        denominator: int = None,
        **kwargs,
    ):
        if value is None:
            if len(args) >= 1:
                value = args[0]

        # Parsed the provided input value, which may be a float, integer or string rational
        parsed = cls.parse(value)

        # Create the new instance, storing the parsed float value as the primary representation
        instance = super().__new__(cls, str(parsed))

        # Store the parsed numerator and denominator
        instance._numerator = numerator if not numerator is None else parsed.numerator
        instance._denominator = (
            denominator if not denominator is None else parsed.denominator
        )

        return instance

    def __float__(self) -> float:
        return float(self._numerator) / float(self._denominator)

    def __str__(self) -> str:
        return f"{self._numerator}/{self._denominator}"

    @property
    def numerator(self) -> int:
        return self._numerator

    @numerator.setter
    def numerator(self, numerator: int) -> Rational:
        if not isinstance(numerator, int):
            raise TypeError("The 'numerator' property must have an integer value!")

        self._numerator = numerator

        return self

    @property
    def denominator(self) -> int:
        return self._denominator

    @denominator.setter
    def denominator(self, denominator: int) -> Rational:
        if not isinstance(denominator, int):
            raise TypeError("The 'denominator' property must have an integer value!")

        self._denominator = denominator

        return self

    @property
    def value(self) -> str:
        return str(self)

    @value.setter
    def value(self, value: float | int | str) -> Rational:
        if not isinstance(value, (float, int, str)):
            raise TypeError(
                "The 'value' argument must have a float, integer or string value!"
            )

        parsed = self.__class__.parsed(value)

        self._value = str(parsed)
        self._numerator = parsed.numerator
        self._denominator = parsed.denominator

        return self

    def encode(self, element: maxml.Element = None) -> bytes:
        return str(self).encode(self.encoding.value)

    @classmethod
    def decode(cls, value: bytes) -> Rational:
        if not isinstance(value, bytes):
            raise TypeError("The 'value' argument must have a bytes value!")

        # As decode is a class method we need to access _encoding via its named variable
        # as the matching instance property is not yet available:
        value = value.decode(cls._encoding.value)

        parsed: cls.RationalParts = cls.parse(value)

        # Create a new instance of the class, initialized with the decoded value:
        return cls(
            value=float(parsed),
            numerator=parsed.numerator,
            denominator=parsed.denominator,
        )


class Boolean(Value):
    """Boolean values are represented as 'True' or 'False' strings, with accomodation of
    lower-cased 'true' or 'false' for non-conforming applications."""

    _encoding: Encoding = Encoding.Unicode
    _nullable: bool = False

    def __init__(
        self,
        value: bool,
        nullable: bool = None,
        field: Field = None,
        **kwargs,
    ):
        super().__init__(value=value, **kwargs)

        if nullable is None and isinstance(field, Field):
            self._nullable = field.nullable
        elif isinstance(nullable, bool):
            self._nullable = nullable

    def __bool__(self) -> bool:
        """As we cannot subclass bool in Python, the best we can do is allow this class
        to be interpreted as a bool via the __bool__ magic method."""

        return self.value is True

    @property
    def nullable(self) -> bool:
        return self._nullable

    def validate(self, value: object) -> bool:
        if self.nullable and not (value is True or value is False or value is None):
            raise ValueError(
                "The 'value' is invalid for the '%s' class; must be True, False or None!"
                % (self.__class__.__name__)
            )
        elif not (value is True or value is False):
            raise ValueError(
                "The 'value' is invalid for the '%s' class; must be True or False!"
                % (self.__class__.__name__)
            )

        return True

    def encode(self, element: maxml.Element = None) -> bytes:
        if self.value is None and self.nullable is True:
            return ""
        else:
            return str("True" if bool(self) else "False").encode(self.encoding.value)

    @classmethod
    def decode(cls, value: bytes) -> Boolean:
        if not isinstance(value, bytes):
            raise TypeError("The 'value' argument must have a bytes value!")

        # As decode is a class method we need to access _encoding via its named variable
        # as the matching instance property is not yet available:
        value = value.decode(cls._encoding.value)

        # Create a new instance of the class, initialized with the decoded value:
        return cls(value=(value.lower() == "true"))


class ASCII(str, Value):
    _encoding: Encoding = Encoding.ASCII

    def __new__(cls, *args, value: str = None, **kwargs):
        if value is None:
            if len(args) >= 1:
                value = args[0]

        return super().__new__(cls, value)

    def __str__(self) -> str:
        return self

    def __bytes__(self) -> bytes:
        return str.encode(self, self.encoding.value)

    def encode(self, element: maxml.Element = None) -> bytes:
        return str.encode(self, self.encoding.value)

    @classmethod
    def decode(cls, value: bytes) -> ASCII:
        if not isinstance(value, bytes):
            raise TypeError("The 'value' argument must have a bytes value!")

        value = value.decode(cls._encoding.value)

        return cls(value=value)


class Unicode(str, Value):
    _encoding: Encoding = Encoding.Unicode

    def __new__(cls, *args, value: str = None, **kwargs):
        if value is None:
            if len(args) >= 1:
                value = args[0]

        return super().__new__(cls, value)

    def __str__(self) -> str:
        return self

    def __bytes__(self) -> bytes:
        return str.encode(self, self.encoding.value)

    def encode(self, element: maxml.Element = None) -> bytes:
        return str.encode(self, self.encoding.value)

    @classmethod
    def decode(cls, value: bytes) -> Unicode:
        if not isinstance(value, bytes):
            raise TypeError("The 'value' argument must have a bytes value!")

        value = value.decode(cls._encoding.value)

        return cls(value=value)


class Bytes(bytes, Value):
    _encoding: Encoding = Encoding.Bytes

    def __new__(cls, *args, value: bytes = None, **kwargs):
        if value is None:
            if len(args) >= 1:
                value = args[0]

        return super().__new__(cls, value)

    def __str__(self) -> str:
        return object.__str__(self)

    def __bytes__(self) -> bytes:
        return self

    def encode(self, element: maxml.Element = None) -> bytes:
        # possible encoded bytes prefix: "data:image/jpeg;base64,xxxx" where xxxx is b64
        # determine if prefix is needed, and add to decode also if so
        return base64.b64encode(self)

    @classmethod
    def decode(cls, value: bytes) -> Bytes:
        if not isinstance(value, bytes):
            raise TypeError("The 'value' argument must have a bytes value!")

        value = base64.b64decode(value)

        return cls(value=value)


class Text(Unicode):
    pass


class Date(datetime.datetime, Value):
    """DateTime formatted values using the format: YYYY:mm:dd HH:MM:SS[.ss][+/-HH:MM]"""

    _encoding: Encoding = Encoding.Unicode

    @classmethod
    def parse(cls, value: datetime.datetime | str) -> datetime.datetime:
        """Parse a string value into a datetime value if possible, and return a datetime
        value immediately if one was provided without any parsing or modification."""

        if isinstance(value, datetime.datetime):
            return value
        elif isinstance(value, str):
            if matched := re.match(
                r"(?P<year>\d{4})(\:|\-)(?P<month>\d{2})(\:|\-)(?P<day>\d{2})T(?P<hour>\d{2})\:(?P<minute>\d{2})\:(?P<second>\d{2})(?P<offsign>\-|\+)(?P<offhour>\d{2})(\:)?(?P<offminute>\d{2})",
                value,
            ):
                value = ":".join(
                    [
                        matched.group("year"),
                        matched.group("month"),
                        matched.group("day"),
                    ]
                )

                value += "T"

                value += ":".join(
                    [
                        matched.group("hour"),
                        matched.group("minute"),
                        matched.group("second"),
                    ]
                )

                value += (
                    (matched.group("offsign") or "+")
                    + matched.group("offhour")
                    + matched.group("offminute")
                )
            else:
                value = value.replace("-", ":")

            logger.debug("%s.parse(value: %s)", cls.__name__, value)

            try:
                # Parse YYYY-mm-ddTHH:MM:SS:TH:TM to datetime value
                return datetime.datetime.strptime(value, "%Y:%m:%dT%H:%M:%S%z")
            except ValueError:
                try:
                    # Parse YYYY-mm-ddTHH:MM:SS.ssssss to datetime value
                    return datetime.datetime.strptime(value, "%Y:%m:%dT%H:%M:%S.%f")
                except ValueError:
                    try:
                        # Parse YYYY:mm:dd HH:MM:SS[.ss][+/-HH:MM] to datetime value
                        return datetime.datetime.strptime(
                            value, "%Y:%m:%d %H:%M:%S.%f%z"
                        )
                    except ValueError:
                        try:
                            # Parse YYYY:mm:dd HH:MM:SS[.ss] to datetime value
                            return datetime.datetime.strptime(
                                value, "%Y:%m:%d %H:%M:%S.%f"
                            )
                        except ValueError:
                            try:
                                # Parse YYYY:mm:dd HH:MM:SS to datetime value
                                return datetime.datetime.strptime(
                                    value, "%Y:%m:%d %H:%M:%S"
                                )
                            except ValueError:
                                try:
                                    # Parse YYYY:mm:dd to datetime value
                                    return datetime.datetime.strptime(value, "%Y:%m:%d")
                                except ValueError as exception:
                                    raise exception

    def __new__(
        cls,
        *args,
        value: datetime.datetime | str = None,
        format: str = "%Y:%m:%d %H:%M:%S",
        **kwargs,
    ):
        if value is None:
            if len(args) >= 1:
                value = args[0]

        if not isinstance(value, (datetime.datetime, str)):
            raise TypeError(
                "The 'value' argument must have a 'datetime.datetime' class instance value!"
            )

        if isinstance(value, str):
            value = cls.parse(value)

        if not isinstance(value, datetime.datetime):
            raise TypeError(
                "The 'value' argument value could not be converted to a valid 'datetime.datetime' class instance value!"
            )

        instance = super().__new__(
            cls,
            value.year,
            value.month,
            value.day,
            value.hour,
            value.minute,
            value.second,
            value.microsecond,
            value.tzinfo,
        )

        instance._value = value

        return instance

    def __str__(self) -> str:
        return datetime.datetime.__str__(self)

    def __bytes__(self) -> bytes:
        return str.encode(str(self), self.encoding.value)

    def encode(self, element: maxml.Element = None) -> bytes:
        return str.encode(str(self), self.encoding.value)

    @classmethod
    def decode(cls, value: bytes) -> Date:
        if not isinstance(value, bytes):
            raise TypeError("The 'value' argument must have a bytes value!")

        value = value.decode(cls._encoding.value)

        return cls(value=value)


class DateTime(Date):
    pass


class Time(datetime.time, Value):
    """Time formatted values using the format: HH:MM:SS[.ss][+/-HH:MM]"""

    _encoding: Encoding = Encoding.Unicode

    @classmethod
    def parse(cls, value: datetime.time | str) -> datetime.time:
        """Parse a string value into a time value if possible, and return a time
        value immediately if one was provided without any parsing or modification."""

        if isinstance(value, datetime.time):
            return value
        elif isinstance(value, str):
            try:
                # Parse YYYY:mm:dd HH:MM:SS[.ss][+/-HH:MM] to datetime value
                return datetime.datetime.strptime(value, "%H:%M:%S.%s%z").time()
            except ValueError:
                try:
                    # Parse YYYY:mm:dd HH:MM:SS[.ss] to datetime value
                    return datetime.datetime.strptime(value, "%H:%M:%S.%s").time()
                except ValueError:
                    try:
                        # Parse YYYY:mm:dd HH:MM:SS to datetime value
                        return datetime.datetime.strptime(value, "%H:%M:%S").time()
                    except ValueError:
                        try:
                            # Parse YYYY:mm:dd to datetime value
                            return datetime.datetime.strptime(value, "%Y:%m:%d").time()
                        except ValueError as exception:
                            raise exception

    def __new__(
        cls,
        *args,
        value: datetime.time | str = None,
        format: str = "%H:%M:%S",
        **kwargs,
    ):
        if value is None:
            if len(args) >= 1:
                value = args[0]

        if not isinstance(value, (datetime.time, str)):
            raise TypeError(
                "The 'value' argument must have a 'datetime.time' class instance value!"
            )

        if isinstance(value, str):
            value = cls.parse(value)

        if not isinstance(value, datetime.time):
            raise TypeError(
                "The 'value' argument value could not be converted to a valid 'datetime.time' class instance value!"
            )

        instance = super().__new__(
            cls,
            value.hour,
            value.minute,
            value.second,
            value.microsecond,
            value.tzinfo,
        )

        instance._value = value

        return instance

    def __str__(self) -> str:
        return datetime.time.__str__(self)

    def __bytes__(self) -> bytes:
        return str.encode(str(self), self.encoding.value)

    def encode(self, element: maxml.Element = None) -> bytes:
        return str.encode(str(self), self.encoding.value)

    @classmethod
    def decode(cls, value: bytes) -> Date:
        if not isinstance(value, bytes):
            raise TypeError("The 'value' argument must have a bytes value!")

        value = value.decode(cls._encoding.value)

        return cls(value=value)


class TimecodeFormat(enumerific.Enumeration):
    Timecode24 = 1
    Timecode25 = 2
    TimecodeDrop2997 = 3
    TimecodeNonDrop2997 = 4
    Timecode30 = 5
    Timecode50 = 6
    TimecodeDrop5994 = 7
    TimecodeNonDrop5994 = 8
    Timecode60 = 9
    Timecode23976 = 10


class Timecode(datetime.time, Value):
    """Timecode formatted values using the format: hh:mm:ss:ff"""

    _encoding: Encoding = Encoding.Unicode
    _format: TimecodeFormat = TimecodeFormat.Timecode24
    _frame: int = 0

    @classmethod
    def parse(cls, value: datetime.time | str) -> datetime.time:
        """Parse a string value into a time value if possible, and return a time
        value immediately if one was provided without any parsing or modification."""

        if isinstance(value, datetime.time):
            return value
        elif isinstance(value, str):
            if matches := re.match(
                r"^(?P<hours>[0-9]{1,}):(?P<minutes>[0-9]{2}):(?P<seconds>[0-9]{2})[\:\;\.]{1}(?P<frame>[0-9]{2,4})$",
                value,
            ):
                instance = datetime.time(
                    int(matches.group("hours")),
                    int(matches.group("minutes")),
                    int(matches.group("seconds")),
                    int(matches.group("frame")),
                )

                return instance

    def __new__(
        cls,
        *args,
        value: datetime.time | str = None,
        format: TimecodeFormat = TimecodeFormat.Timecode24,
        **kwargs,
    ):
        if value is None:
            if len(args) >= 1:
                value = args[0]

        if not isinstance(value, (datetime.time, str)):
            raise TypeError(
                "The 'value' argument must have a 'datetime.time' class instance value!"
            )

        if isinstance(value, str):
            value = cls.parse(value)

        if not isinstance(value, datetime.time):
            raise TypeError(
                "The 'value' argument value could not be converted to a valid 'datetime.time' class instance value!"
            )

        if not isinstance(format, TimecodeFormat):
            raise TypeError(
                "The 'format' argument must have a 'TimecodeFormat' enumeration value!"
            )

        instance = super().__new__(
            cls,
            value.hour,
            value.minute,
            value.second,
            value.microsecond,
        )

        instance._value = value
        instance._frame = value.microsecond
        instance._format = format

        return instance

    def __init__(self, *args, format: TimecodeFormat = None, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        value = self.strftime("%H:%M:%S")

        # Drop-Frame Timecodes use a semi-colon between the timestamp and frame number
        if self.format in [
            TimecodeFormat.TimecodeDrop2997,
            TimecodeFormat.TimecodeDrop5994,
        ]:
            value += ";"
        else:
            value += ":"

        value += str("%02d" % (self._frame))

        return value

    def __bytes__(self) -> bytes:
        return str.encode(str(self), self.encoding.value)

    def encode(self, element: maxml.Element = None) -> bytes:
        return str.encode(str(self), self.encoding.value)

    @classmethod
    def decode(
        cls, value: bytes, format: TimecodeFormat = TimecodeFormat.Timecode24
    ) -> Date:
        if not isinstance(value, bytes):
            raise TypeError("The 'value' argument must have a bytes value!")

        value = value.decode(cls._encoding.value)

        return cls(value=value, format=format)

    @property
    def format(self) -> TimecodeFormat:
        return self._format

    @property
    def frame(self) -> int:
        return self._frame


class URI(Unicode):
    pass


class URL(URI):
    pass


class Thumbnail(Bytes):
    pass


class ResourceRef(Value):
    pass


class ResourceEvent(Value):
    pass


class GUID(Value):
    pass


class RenditionClass(Value):
    pass


class Struct(Value):
    pass


class Version(Value):
    pass


class Job(Value):
    pass


class Colorants(Value):
    pass


class Font(Value):
    pass


class Dimensions(Value):
    pass


class BeatSpliceStretch(Value):
    pass


class Media(Value):
    pass


class Marker(Value):
    pass


class ProjectLink(Value):
    pass


class ResampleStretch(Value):
    pass


class TimeScaleStretch(Value):
    pass


class Track(Value):
    pass


class ProperName(Text):
    """A simple text value denoting the name of a person or organization, expressed as a
    Text value."""

    pass


class AgentName(Text):
    """The name of an XMP processor, expressed as a Text value. It is recommended that
    the value use this formatting convention:

        "Organization Software Name Version (Token; Token; ...)"

    Where:
     * Organization: The name of the company or organization providing the
        software, however, no spaces are allowed in this field.
     * SoftwareName: The full name of the software (spaces are allowed here if needed)
     * Version: The version of the software, again without spaces, such as "1.0.1".
     * Tokens: Can be used to identify an operating system, plug-ins, and other detailed
        versioning information.

    Example: "BlueBinary EXIFData 1.0.1 (af24e1d)"
    """

    _value: str = None
    _organization: str = None
    _software: str = None
    _version: str = None
    _tokens: list[str] = None

    def __init__(
        self,
        value: str = None,
        organization: str = None,
        software: str = None,
        version: str = None,
        tokens: list[str] = None,
        **kwargs,
    ):
        if value is None:
            if organization is None or software is None or version is None:
                raise ValueError(
                    "The AgentName class must be initialized with a value string or an organization, software name and version number, and optional tokens!"
                )

        if isinstance(value, str):
            self._value = value

        if isinstance(organization, str):
            self._organization = organization

        if isinstance(software, str):
            self._software = software

        if isinstance(version, str):
            self._version = version

        if isinstance(tokens, list):
            self._tokens = tokens

        super().__init__(value=self.value, **kwargs)

    @property
    def value(self) -> str:
        if self._value:
            value = self._value
        else:
            value = "{self._organization} {self._software} {self._version}"

            if self._tokens:
                value += "(" + ", ".join(self._tokens) + ")"

        return value


class ContactInfo(Value):
    pass


class LanguageAlternative(Value):
    """Represents a string that may have one or more alternative language versions"""

    class Localized(object):
        """The Localized string holds a string value along with its assigned language
        and country code."""

        def __init__(self, text: str, language: str, country: str):
            if not isinstance(text, str):
                raise TypeError("The 'text' argument must have a string value!")

            self._text: str = text

            if not isinstance(language, str):
                raise TypeError("The 'language' argument must have a string value!")

            self._language: str = language

            if not isinstance(country, str):
                raise TypeError("The 'country' argument must have a string value!")

            self._country: str = country

        @property
        def key(self) -> str:
            return f"{self._language}-{self._country}"

        @property
        def text(self) -> str:
            return self._text

        @property
        def value(self) -> str:
            return self._text

        @property
        def language(self) -> str:
            return self._language

        @property
        def country(self) -> str:
            return self._country

        @property
        def isocode(self) -> str:
            return f"{self._language}-{self._country}"

    _alternates: list[Localized] = None

    @classmethod
    def parse(cls, value: str, language: str = None, country: str = None) -> Localized:
        if not isinstance(value, str):
            raise TypeError("The 'value' argument must have a string value!")

        if language is None:
            pass
        elif not isinstance(language, str):
            raise TypeError(
                "The 'language' argument, if specified, must have a string value!"
            )

        if country is None:
            pass
        elif not isinstance(country, str):
            raise TypeError(
                "The 'country' argument, if specified, must have a string value!"
            )

        if matched := re.match(
            r"^((?P<language>[a-z]{2})(\-(?P<country>[A-Z]{2}))?\:)?(?P<text>.*)$",
            value,
        ):
            language = matched.group("language") or language or secrets.get("language")

            country = matched.group("country") or country or secrets.get("country")

            text = matched.group("text")

            return cls.Localized(text=text, language=language, country=country)

    def __init__(self, value: str | list[str] = None, **kwargs):
        self._alternates: list[self.__class__.Localized] = []

        if isinstance(value, str):
            if parsed := self.parse(value):
                self._alternates.append(parsed)
        elif isinstance(value, list):
            for val in value:
                if not isinstance(val, str):
                    raise TypeError(
                        "The 'value' argument must have a string value or must reference a list of string values!"
                    )

                if parsed := self.parse(val):
                    self._alternates.append(parsed)
        else:
            raise TypeError(
                "The 'value' argument must have a string value or must reference a list of string values!"
            )

        super().__init__(value=value, **kwargs)

    @property
    def alternates(self) -> list[Localized]:
        return self._alternates

    # <Iptc4xmpCore:AltTextAccessibility>
    #     <rdf:Alt>
    #         <rdf:li xml:lang='x-default'>Insert text here.</rdf:li>
    #         <rdf:li xml:lang='zxx'>Insert text here.</rdf:li>
    #     </rdf:Alt>
    # </Iptc4xmpCore:AltTextAccessibility>

    def encode(self, element: maxml.Element) -> None:
        maxml.Element.register_namespace(
            prefix="xml",
            uri="http://www.w3.org/XML/1998/namespace",
        )

        if len(self.alternates) > 0:
            if alt := element.subelement("rdf:Alt"):
                for alternate in self.alternates:
                    if li := alt.subelement("rdf:li"):
                        li.set("xml:lang", alternate.isocode)
                        li.text = alternate.text


class Ancestor(Value):
    pass


class Layer(Value):
    pass


class CFAPattern(Value):
    pass


class DeviceSettings(Value):
    pass


class Flash(Value):
    pass


class OECFSFR(Value):
    pass


class MIMEType(Value):
    pass


class Locale(Value):
    pass


class Type(Type):
    Integer = Integer
    Boolean = Boolean
    Real = Real
    Rational = Rational
    Text = Text
    Date = Date
    DateTime = DateTime
    Time = Time
    Timecode = Timecode
    GUID = GUID
    URL = URL
    URI = URI
    Struct = Struct
    Thumbnail = Thumbnail
    AgentName = AgentName
    ProperName = ProperName
    ContactInfo = ContactInfo
    ResourceRef = ResourceRef
    RenditionClass = RenditionClass
    ResourceEvent = ResourceEvent
    Version = Version
    Job = Job
    Colorants = Colorants
    Font = Font
    Dimensions = Dimensions
    Layer = Layer
    Marker = Marker
    Track = Track
    Media = Media
    CFAPattern = CFAPattern
    BeatSpliceStretch = BeatSpliceStretch
    ResampleStretch = ResampleStretch
    TimeScaleStretch = TimeScaleStretch
    ProjectLink = ProjectLink
    LanguageAlternative = LanguageAlternative
    Ancestor = Ancestor
    DeviceSettings = DeviceSettings
    Flash = Flash
    OECFSFR = OECFSFR
    MIMEType = MIMEType
    Locale = Locale
