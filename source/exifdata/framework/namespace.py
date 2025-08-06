from __future__ import annotations

import typing

from exifdata.logging import logger
from exifdata import framework

from caselessly import (
    caselesslist,
    caselessdict,
)


logger = logger.getChild(__name__)


class Namespace(object):
    _identifier: str = None
    _name: str = None
    _uri: str = None
    _prefix: str = None
    _alias: str = None
    _metadata: Metadata = None
    _definition: str = None
    _structures: caselessdict[str, Structure] = None
    _fields: caselessdict[str, Field] = None
    _fieldmap: caselessdict[str, Field] = None
    _special: list[str] = None
    _utilized: bool = False
    _unwrap: bool = False

    def __init__(
        self,
        identifier: str,
        name: str,
        uri: str = None,
        prefix: str = None,
        alias: str = None,
        label: str = None,
        definition: str = None,
        metadata: Metadata = None,
        structures: dict[str, Structure | dict] = None,
        unwrap: bool = False,
    ):
        # logger.debug(
        #     "%s.__init__(uri: %s, prefix: %s, name: %s, description: %s)"
        #     % (self.__class__.__name__, uri, prefix, name, description)
        # )

        if not isinstance(identifier, str):
            raise TypeError("The 'identifier' argument must have a string value!")

        self._identifier: str = identifier

        if not isinstance(name, str):
            raise TypeError("The 'name' argument must have a string value!")

        self._name: str = name

        if uri is None:
            pass
        elif not isinstance(uri, str):
            raise TypeError(
                "The 'uri' argument, if specified, must have a string value!"
            )

        self._uri: str = uri

        if prefix is None:
            pass
        elif not isinstance(prefix, str):
            raise TypeError(
                "The 'prefix' argument, if specified, must have a string value!"
            )

        self._prefix: str = prefix

        if alias is None:
            pass
        elif not isinstance(alias, str):
            raise TypeError(
                "The 'alias' argument, if specified, must have a string value for: %s!"
                % (identifier)
            )

        self._alias: str = alias

        if label is None:
            pass
        elif not isinstance(label, str):
            raise TypeError(
                "The 'label' argument, if specified, must have a string value!"
            )

        self._label: str = label

        if definition is None:
            pass
        elif not isinstance(definition, str):
            raise TypeError(
                "The 'definition' argument, if specified, must have a string value!"
            )

        self._definition: str = definition

        if metadata is None:
            pass
        elif not isinstance(metadata, framework.Metadata):
            raise TypeError(
                "The 'metadata' argument, if specified, must reference a Metadata class instance!"
            )

        self._metadata = metadata

        if not isinstance(unwrap, bool):
            raise TypeError(
                "The 'unwrap' argument, if specified, must have a boolean value!"
            )

        self._unwrap = unwrap

        self._structures: caselessdict[str, Structure] = caselessdict()

        if structures is None:
            pass
        elif isinstance(structures, dict):
            for identifier, structure in structures.items():
                if isinstance(structure, framework.Structure):
                    self._structures[identifier] = structure
                elif isinstance(structure, dict):
                    self._structures[identifier] = framework.Structure(
                        identifier=identifier,
                        **structure,
                    )

        self._fields: caselessdict[str, Field] = caselessdict()
        self._fieldmap: caselessdict[str, Field] = caselessdict()
        self._special = [prop for prop in dir(self) if not prop.startswith("_")]

    def __str__(self) -> str:
        return f"<Namespace({self.id})>"

    def __contains__(self, name: str) -> bool:
        return name in self._fieldmap

    def __getattr__(self, name: str) -> object | None:
        logger.debug("%s.__getattr__(name: %s)" % (self.__class__.__name__, name))

        value: object = None

        if name.startswith("_") or name in self._special:
            value = super().__getattr__(name)

        elif field := self._fieldmap.get(name):
            if self._metadata and field.id in self._metadata._values:
                value = self._metadata._values[field.id].value
        else:
            raise AttributeError(
                "The '%s' namespace does not have a '%s' attribute!"
                % (
                    self.id,
                    name,
                )
            )

        # logger.debug("%s.__getattr__(name: %s) -> %s" % (self.__class__.__name__, name, value))

        return value

    def __setattr__(
        self,
        name: str,
        value: Value | object | list[Value] | tuple[Value] | set[Value],
    ):
        logger.debug(
            "%s.__setattr__(name: %s, value: %s)"
            % (self.__class__.__name__, name, value)
        )

        if name.startswith("_") or name in self._special:
            return super().__setattr__(name, value)

        # TODO: Convert field.name to field.identifier
        elif field := self._fieldmap.get(name):
            if field.readonly is True:
                raise NotImplementedError(f"The '{field.name}' field is readonly!")

            if isinstance(value, framework.Value):
                self._metadata._values[field.id] = value
            else:
                if not isinstance(klass := self._metadata._types.get(field.type), type):
                    raise ValueError(
                        f"The field type, '{field.type}', does not map to a registered value type!"
                    )

                if not issubclass(klass, framework.Value):
                    raise ValueError(
                        f"The field type, '{field.type}', does not map to a registered Value subclass!"
                    )

                if field.combine is False and isinstance(value, (list, tuple, set)):
                    values: list[Value] = []

                    for val in value:
                        if isinstance(val, framework.Value):
                            values.append(val)
                        else:
                            values.append(
                                klass(
                                    field=field,
                                    metadata=self._metadata,
                                    value=val,
                                )
                            )

                    self._metadata._values[field.id] = values
                else:
                    self._metadata._values[field.id] = klass(
                        field=field,
                        metadata=self._metadata,
                        value=value,
                    )

            self._utilized = True
        else:
            raise AttributeError(
                "The '%s' namespace does not have a '%s' attribute!"
                % (
                    self.id,
                    name,
                )
            )

    @property
    def id(self) -> str:
        return self._identifier

    # NOTE: Conflicts with any field named 'identifier'
    # @property
    # def identifier(self) -> str:
    #     return self._identifier

    @property
    def name(self) -> str:
        return self._name

    @property
    def uri(self) -> str:
        return self._uri

    @property
    def prefix(self) -> str:
        return self._prefix

    @property
    def alias(self) -> str | None:
        return self._alias

    @property
    def definition(self) -> str | None:
        return self._definition

    @property
    def metadata(self) -> Metadata:
        return self._metadata

    @property
    def structures(self) -> list[Structure]:
        return self._structures

    @property
    def utilized(self) -> bool:
        return self._utilized

    @property
    def unwrap(self) -> bool:
        return self._unwrap

    @property
    def fields(self) -> dict[str, Field]:
        return self._fields

    @fields.setter
    def fields(self, fields: dict[str, Field]):
        raise NotImplementedError

    @property
    def field(self) -> None:
        raise NotImplementedError

    @field.setter
    def field(self, field: Field):
        if not isinstance(field, framework.Field):
            raise TypeError(
                "The 'field' property must be assigned a Field class instance value!"
            )

        if field.name in self._fields:
            raise KeyError(
                f"A field with the identifier '{field.name}' already exists!"
            )

        self._fields[field.name] = self._fieldmap[field.name] = field

        if field.aliases:
            for alias in field.aliases:
                if alias in self._fieldmap:
                    raise KeyError(
                        f"A field with the identifier '{alias}' already exists, so another field cannot alias the same identifier!"
                    )
                self._fieldmap[alias] = field

        # logger.debug("%s.field[%s] = %s" % (self.__class__.__name__, field.name, field))

    @property
    def value(self):
        raise NotImplementedError

    @value.setter
    def value(self, value: Value):
        if not isinstance(value, framework.Value):
            raise TypeError(
                "The 'value' argument must reference a Value class instance!"
            )

        if value.metadata is None:
            raise TypeError(
                "The Value class instance referenced by the 'value' argument must have an assigned 'metadata' value in order to be set via this setter, otherwise, the metadata model that the value should be associated with cannot be determined!"
            )

        if value.field is None:
            raise TypeError(
                "The Value class instance referenced by the 'value' argument must have an assigned 'field' value in order to be set via this setter, otherwise, the field name that the value should be associated with cannot be determined!"
            )

        self._metadata: Metadata = value.metadata

        self._metadata._values[value.field.id] = value

    def get(self, metadata: Metadata, field: Field) -> object:
        raise NotImplementedError

    def set(self, metadata: Metadata, field: Field, value: Value | object):
        if not isinstance(metadata, framework.Metadata):
            raise TypeError(
                "The 'metadata' argument must reference a Metadata class instance!"
            )

        self._metadata: Metadata = metadata

        if not isinstance(field, framework.Field):
            raise TypeError(
                "The 'field' argument must reference a Field class instance!"
            )

        if isinstance(value, framework.Value):
            self._metadata._values[field.id] = value
        else:
            if not isinstance(klass := self._metadata._types.get(field.type), type):
                raise ValueError(
                    f"The field type, '{field.type}', does not map to a registered value type!"
                )

            if not issubclass(klass, framework.Value):
                raise ValueError(
                    f"The field type, '{field.type}', does not map to a registered Value subclass!"
                )

            if value is None:
                if field.id in self._metadata._values:
                    del self._metadata._values[field.id]
            else:
                self._metadata._values[field.id] = klass(
                    field=field,
                    metadata=self._metadata,
                    value=value,
                )

        logger.debug(
            "%s.set(metadata: %s, field: %s, value: %r) => %r"
            % (
                self.__class__.__name__,
                metadata,
                field,
                value,
                self._metadata._values.get(field.id),
            )
        )

        self._utilized = True

    def items(self) -> typing.Generator[tuple[str, Field], None, None]:
        for name, field in self._fields.items():
            yield (name, field)

    def keys(self) -> typing.Generator[str, None, None]:
        for name in self._fields.keys():
            yield name

    def values(self) -> typing.Generator[Field, None, None]:
        for value in self._fields.values():
            yield value
