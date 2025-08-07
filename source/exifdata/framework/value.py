from __future__ import annotations

import abc
import typing

from exifdata.logging import logger
from exifdata import framework

from caselessly import (
    caselesslist,
    caselessdict,
)

from deliciousbytes import (
    ByteOrder,
    Encoding,
)


logger = logger.getChild(__name__)


class Value(object):
    _field: Field = None
    _value: object = None
    _encoding: Encoding = None
    _metadata: Metadata = None
    _order: ByteOrder = None

    @typing.final
    def __init__(
        self,
        value: object = None,
        field: Field = None,
        order: ByteOrder = ByteOrder.MSB,
        encoding: Encoding = None,
        metadata: Metadata = None,
        **kwargs,
    ):
        logger.debug(
            "%s.__init__(value: %s, field: %s, order: %s, encoding: %s, metadata: %s, kwargs: %s)"
            % (
                self.__class__.__name__,
                value,
                field,
                order,
                encoding,
                metadata,
                kwargs,
            )
        )

        if field is None:
            pass
        elif not isinstance(field, framework.Field):
            raise TypeError(
                "The 'field' argument, if specified, must reference a Field class instance!"
            )

        self._field = field

        if isinstance(order, ByteOrder):
            self._order: ByteOrder = order
        else:
            raise TypeError(
                "The 'order' argument must be an ByteOrder enumeration value!"
            )

        if encoding is None:
            self._encoding: Encoding = self.__class__._encoding
        elif isinstance(encoding, Encoding):
            self._encoding: Encoding = encoding
        else:
            raise TypeError(
                "The 'encoding' argument must be an Encoding enumeration value!"
            )

        if metadata is None:
            pass
        elif isinstance(metadata, framework.Metadata):
            self._metadata = metadata
        else:
            raise TypeError(
                "The 'metadata' argument, if specified, must reference a Metadata class instance!"
            )

        try:
            if self.validate(value=value) is True:
                self._value = value
            else:
                raise ValueError(
                    "The 'value' is invalid for the '%s' class!"
                    % (self.__class__.__name__)
                )
        except ValueError as exception:
            raise ValueError(str(exception)) from exception

    def validate(self, value: object) -> bool:
        return (not value is None) or (self.field and self.field.nullable)

    @property
    @typing.final
    def field(self) -> Field | None:
        return self._field

    @property
    @typing.final
    def encoding(self) -> Encoding:
        return self._encoding or self.__class__._encoding

    @property
    @typing.final
    def metadata(self) -> Metadata | None:
        return self._metadata

    @property
    @typing.final
    def value(self) -> object:
        return self._value

    @abc.abstractmethod
    def encode(self, order: ByteOrder = None) -> bytes:
        raise NotImplementedError(
            "The '%s.encode()' method has not been implemented!"
            % (self.__class__.__name__)
        )

    @classmethod
    @abc.abstractmethod
    def decode(cls, value: bytes) -> Value:
        raise NotImplementedError(
            "The '%s.decode()' method has not been implemented!" % (cls.__name__)
        )
