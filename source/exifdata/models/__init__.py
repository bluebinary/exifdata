from __future__ import annotations

import abc
import typing
import enumerific


from exifdata.logging import logger

from exifdata.types import (
    caselesslist,
    caselessdict,
)

from exifdata.types import (
    ByteOrder,
    Encoding,
)


from exifdata.configuration import secrets


logger = logger.getChild(__name__)


__type__ = type


class Type(enumerific.Enumeration):
    @property
    def klass(cls):
        return cls.value


class Structure(object):
    _identifier: str = None
    _name: str = None
    _type: str = None
    _kind: str = None

    def __init__(self, identifier: str, name: str, type: str, kind: str = None):
        self._identifier: str = identifier
        self._name: str = name
        self._type: str = type
        self._kind: str = kind

    @property
    def id(self) -> str:
        return self._identifier

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> str:
        return self._type

    @property
    def kind(self) -> str:
        return self._kind


class Field(object):
    _namespace: Namespace = None
    _structure: Structure = None
    _identifier: str | int = None
    _name: str = None
    _types: str | tuple[str] = None
    _aliases: list[str] = None
    _pseudonym: list[str] = None
    _encoding: Encoding = None
    _unit: str = None
    _tag: int = None
    _ordered: bool = False
    _minimum: int | float = None
    _maximum: int | float = None
    _options: list[object] = None
    _closed: bool = True
    _nullable: bool = False
    _required: bool = False
    _readonly: bool = False
    _count: int | tuple[int] = 1
    _multiple: bool = False
    _combine: bool = False
    _label: str = None
    _definition: str = None
    _related: Field = None
    _section: str = None

    def __init__(
        self,
        namespace: Namespace,
        identifier: str | int,
        name: str,
        type: str | list[str] | tuple[str] | set[str],
        structure: Structure | str = None,
        alias: str | list[str] = None,
        pseudonym: str | list[str] | dict[str, str] = None,
        encoding: Encoding | str = None,
        unit: str = None,
        tag: int = None,
        ordered: bool = False,
        minimum: int | float = None,
        maximum: int | float = None,
        options: list[object] = None,
        closed: bool = True,
        nullable: bool = False,
        required: bool = False,
        readonly: bool = False,
        count: int | tuple[int] = 1,
        multiple: bool = False,
        combine: bool = False,
        label: str = None,
        definition: str = None,
        related: Field | str = None,
        section: str = None,
    ):
        # logger.debug(
        #     "%s.__init__(name: %s, type: %s, tag: %s, count: %s, description: %s, namespace: %s)"
        #     % (self.__class__.__name__, name, type, tag, count, description, namespace)
        # )

        if isinstance(namespace, Namespace):
            self._namespace: Namespace = namespace
        else:
            raise TypeError(
                "The 'namespace' argument must have a Namespace class instance value!"
            )

        if isinstance(identifier, (str, int)):
            self._identifier: str | int = identifier
        else:
            raise TypeError("The 'id' argument must have a string or integer value!")

        if isinstance(name, str):
            self._name: str = name
        else:
            raise TypeError("The 'name' argument must have a string value!")

        if isinstance(type, str):
            self._types = tuple([type])
        # elif isinstance(type, Type):
        #     self._types = tuple([type])
        # elif isinstance(type, str):
        #     if Type.validate(type) is True:
        #         self._type = tuple([Type.reconcile(type)])
        #     else:
        #         raise TypeError(
        #             "The 'type' argument must have a valid 'Type' enumeration or string value, not: %r!" % (type)
        #         )
        elif isinstance(type, (list, set, tuple)):
            for _type in type:
                if not isinstance(_type, str):
                    raise TypeError(
                        "The 'type' argument must have a valid 'Type' enumeration or string value, not: %r!"
                        % (type)
                    )
            self._types = tuple(type)
        else:
            raise TypeError(
                "The 'type' argument must have a valid 'Type' enumeration or string value, not %s!"
                % (type)
            )

        if alias is None:
            self._aliases = []
        elif isinstance(alias, str):
            self._aliases = [alias]
        elif isinstance(alias, list):
            self._aliases = list(alias)

        if pseudonym is None:
            self._pseudonym = []
        elif isinstance(pseudonym, str):
            self._pseudonym = [pseudonym]
        elif isinstance(pseudonym, list):
            self._pseudonym = pseudonym
        elif isinstance(pseudonym, dict):
            self._pseudonym = [value for value in pseudonym.values()]

        self._unit: str = unit
        self._label: str = label
        self._tag: int = tag

        if isinstance(ordered, bool):
            self._ordered: bool = ordered
        else:
            raise TypeError(
                "The 'ordered' argument, if specified, must have a boolean value!"
            )

        if minimum is None:
            pass
        elif isinstance(minimum, (int, float)):
            self._minimum: int | float = minimum
        else:
            raise TypeError(
                "The 'minimum' argument, if specified, must have an integer or float value!"
            )

        if maximum is None:
            pass
        elif isinstance(maximum, (int, float)):
            self._maximum: int | float = maximum
        else:
            raise TypeError(
                "The 'maximum' argument, if specified, must have an integer or float value!"
            )

        if options is None:
            pass
        elif isinstance(options, list):
            self._options: list[object] = options
        elif isinstance(options, dict):
            self._options: list[object] = options.keys()
        else:
            raise TypeError(
                "The 'options' argument, if specified, must have a list value!"
            )

        if isinstance(closed, bool):
            self._closed: bool = closed
        else:
            raise TypeError(
                "The 'closed' argument, if specified, must have a boolean value!"
            )

        if isinstance(nullable, bool):
            self._nullable: bool = nullable
        else:
            raise TypeError(
                "The 'nullable' argument, if specified, must have a boolean value!"
            )

        if isinstance(required, bool):
            self._required: bool = required
        else:
            raise TypeError(
                "The 'required' argument, if specified, must have a boolean value!"
            )

        if isinstance(readonly, bool):
            self._readonly: bool = readonly
        else:
            raise TypeError(
                "The 'readonly' argument, if specified, must have a boolean value!"
            )

        if isinstance(count, int):
            self._count = tuple([count])
        elif isinstance(count, (set, tuple, list)):
            for value in count:
                if not isinstance(value, int):
                    raise TypeError(
                        "The 'count' argument, if specified, must have an integer or tuple of integers value!"
                    )
            self._count = tuple(count)
        else:
            raise TypeError(
                "The 'count' argument, if specified, must have an integer or tuple of integers value, not %s!"
                % (__type__(count))
            )

        if isinstance(multiple, bool):
            self._multiple = multiple
        else:
            raise TypeError(
                "The 'multiple' argument, if specified, must have an boolean value!"
            )

        if isinstance(combine, bool):
            self._combine = combine
        else:
            raise TypeError(
                "The 'combine' argument, if specified, must have an boolean value!"
            )

        if encoding is None:
            pass
        elif isinstance(encoding, Encoding):
            self._encoding = encoding
        elif isinstance(encoding, str):
            if Encoding.validate(encoding) is True:
                self._encoding = Encoding.reconcile(encoding)
            else:
                raise TypeError(
                    "The 'encoding' argument, if specified, must have a valid Encoding enumeration or string value, not: %s!"
                    % (encoding)
                )
        else:
            raise TypeError(
                "The 'encoding' argument, if specified, must have an Encoding enumeration or string value!"
            )

        if structure is None:
            pass
        elif isinstance(structure, str):
            if structure in namespace.structures:
                self._structure: Structure = namespace.structures[structure]
            else:
                raise ValueError(
                    "The 'structure' argument, if specified, must reference a valid Structure, not %s!"
                    % (structure)
                )
        elif isinstance(structure, Structure):
            self._structure: Structure = structure
        else:
            raise TypeError(
                "The 'structure' argument, if specified, must have a string name or Structure class instance value!"
            )

        if definition is None:
            pass
        elif isinstance(definition, str):
            self._definition: str = definition
        else:
            raise TypeError(
                "The 'definition' argument, if specified, must have a string value!"
            )

        if section is None:
            pass
        elif isinstance(section, str):
            self._section: str = section
        else:
            raise TypeError(
                "The 'section' argument, if specified, must have a string value!"
            )

    def __str__(self) -> str:
        return f"<Field({self.id})>"

    @property
    def id(self) -> str | int:
        return self._identifier

    @property
    def identifier(self) -> str | int:
        return self._identifier

    @property
    def name(self) -> str:
        return self._name

    @property
    def names(self) -> caselesslist[str]:
        return caselesslist(
            [self._name] + [self._identifier] + self._aliases + self._pseudonym
        )

    @property
    def type(self) -> str:
        return self.types[0]

    @property
    def types(self) -> tuple[str]:
        if isinstance(self._types, str):
            return tuple([self._types])
        elif isinstance(self._types, tuple):
            return self._types
        else:
            raise TypeError(
                "The list of types has not been initialized correctly, types should be stored as a tuple, not %s!"
                % (__type__(self._types))
            )

    @property
    def aliases(self) -> list[str]:
        return self._aliases

    @property
    def pseudonym(self) -> list[str]:
        return self._pseudonym

    @property
    def encoding(self) -> Encoding:
        return self._encoding

    @property
    def unit(self) -> str:
        return self._unit

    @property
    def tag(self) -> int:
        return self._tag

    @property
    def ordered(self) -> bool:
        return self._ordered

    @property
    def minimum(self) -> int | float | None:
        return self._minimum

    @property
    def maximum(self) -> int | float | None:
        return self._maximum

    @property
    def options(self) -> list[object]:
        return self._options

    @property
    def closed(self) -> bool:
        return self._closed

    @property
    def nullable(self) -> bool:
        return self._nullable

    @property
    def required(self) -> bool:
        return self._required

    @property
    def readonly(self) -> bool:
        return self._readonly

    @property
    def count(self) -> int | tuple[int]:
        return self._count

    @property
    def multiple(self) -> bool:
        return self._multiple

    @property
    def combine(self) -> bool:
        return self._combine

    @property
    def label(self) -> str | None:
        return self._label

    @property
    def definition(self) -> str | None:
        return self._definition

    @property
    def namespace(self) -> Namespace:
        return self._namespace

    @namespace.setter
    def namespace(self, namespace: Namespace):
        if not isinstance(namespace, Namespace):
            raise TypeError(
                "The 'namespace' property must be assigned to a Namespace class instance!"
            )
        self._namespace = namespace

    @property
    def structure(self) -> Structure:
        return self._structure

    @structure.setter
    def structure(self, structure: Structure):
        if not isinstance(structure, Structure):
            raise TypeError(
                "The 'structure' property must be assigned to a Structure class instance!"
            )
        self._structure = structure

    @property
    def section(self) -> str:
        return self._section

    def value(self, value: object, metadata: Metadata = None) -> Value:
        raise NotImplementedError

        if metadata is None:
            pass
        elif not isinstance(metadata, Metadata):
            raise TypeError(
                "The 'metadata' argument, if specified, must reference a Metadata class instance!"
            )

        return self.type.klass(
            field=self,
            metadata=metadata,
            value=value,
        )


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
        elif not isinstance(field, Field):
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
        elif isinstance(metadata, Metadata):
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
            "The '%s.decode()' method has not been implemented!"
            % (self.__class__.__name__)
        )


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
        elif not isinstance(metadata, Metadata):
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
                if isinstance(structure, Structure):
                    self._structures[identifier] = structure
                elif isinstance(structure, dict):
                    self._structures[identifier] = Structure(
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
                f"The '%s' namespace does not have a '%s' attribute!"
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

            if isinstance(value, Value):
                self._metadata._values[field.id] = value
            else:
                if not isinstance(
                    klass := self._metadata._types.get(field.type), __type__
                ):
                    raise ValueError(
                        f"The field type, '{field.type}', does not map to a registered value type!"
                    )

                if not issubclass(klass, Value):
                    raise ValueError(
                        f"The field type, '{field.type}', does not map to a registered Value subclass!"
                    )

                if field.combine is False and isinstance(value, (list, tuple, set)):
                    values: list[Value] = []

                    for val in value:
                        if isinstance(val, Value):
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
                f"The '%s' namespace does not have a '%s' attribute!"
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
        if not isinstance(field, Field):
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
        if not isinstance(value, Value):
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
        if not isinstance(metadata, Metadata):
            raise TypeError(
                "The 'metadata' argument must reference a Metadata class instance!"
            )

        self._metadata: Metadata = metadata

        if not isinstance(field, Field):
            raise TypeError(
                "The 'field' argument must reference a Field class instance!"
            )

        if isinstance(value, Value):
            self._metadata._values[field.id] = value
        else:
            if not isinstance(klass := self._metadata._types.get(field.type), __type__):
                raise ValueError(
                    f"The field type, '{field.type}', does not map to a registered value type!"
                )

            if not issubclass(klass, Value):
                raise ValueError(
                    f"The field type, '{field.type}', does not map to a registered Value subclass!"
                )

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
                self._metadata._values[field.id],
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


class Groupspace(object):
    _namespaces: set[Namespace] = None
    _metadata: Metadata = None

    def __init__(self, *args):
        self._namespaces: list[Namespace] = set()

        for arg in args:
            if isinstance(arg, Namespace):
                self._namespaces.add(arg)
            elif isinstance(arg, Groupspace):
                for namespace in arg.namespaces:
                    self._namespaces.add(namespace)

    @property
    def namespaces(self) -> set[Namespace]:
        return self._namespaces

    @property
    def metadata(self) -> Metadata | None:
        return self._metadata

    @metadata.setter
    def metadata(self, metadata: Metadata):
        if not isinstance(metadata, Metadata):
            raise TypeError(
                "The 'metadata' argument must have a Metadata class instance value!"
            )
        self._metadata = metadata

    def __getattr__(self, name: str):
        logger.debug("%s.__getattr__(name: %s)" % (self.__class__.__name__, name))

        for namespace in self._namespaces:
            if name in namespace:
                namespace._metadata = self.metadata
                return namespace.__getattr__(name)

        raise AttributeError(f"The groupspace has no '{name}' attribute!")

    def __setattr__(self, name: str, value: object):
        logger.debug(
            "%s.__setattr__(name: %s, value: %s)"
            % (self.__class__.__name__, name, value)
        )

        if name.startswith("_"):
            return super().__setattr__(name, value)

        for namespace in self._namespaces:
            if name in namespace:
                namespace._metadata = self.metadata
                return namespace.__setattr__(name, value)

        raise AttributeError(f"The groupspace has no '{name}' attribute!")


class Metadata(object):
    _namespaces: caselessdict[str, Namespace] = None
    _aliases: caselessdict[str, Namespace | Field] = None
    # _fields: caselessdict[str, Field] = None
    _values: caselessdict[str, Value] = None
    _special: list[str] = None
    _types: dict[str, Value] = None

    @classmethod
    def register_type(cls, type: str, klass: Value):
        if not isinstance(type, str):
            raise TypeError("The 'type' argument must have a string value!")

        if not issubclass(klass, Value):
            raise TypeError("The 'klass' argument must be a Value subclass type!")

        cls._types[type] = klass

    @classmethod
    def register_types(cls, *types: tuple[type]):
        if not isinstance(types, (list, tuple)):
            raise TypeError("The 'types' argument must reference a list of types!")

        for _type in types:
            cls.register_type(_type.__name__, _type)

    @classmethod
    def type_by_name(cls, type: str) -> Value:
        if not isinstance(type, str):
            raise TypeError("The 'type' argument must have a string value!")

        if not type in cls._types:
            raise KeyError(
                f"The specified 'type' name, '{type}', does not correspond to a registered type!"
            )

        return cls._types[type]

    @classmethod
    def field_by_id(cls, id: str) -> tuple[Namespace, Field] | None:
        for name, namespace in cls._namespaces.items():
            for field in namespace.fields.values():
                if field.id == id:
                    return (namespace, field)

    @classmethod
    def field_by_name(cls, name: str) -> tuple[Namespace, Field] | None:
        for name, namespace in cls._namespaces.items():
            for field in namespace.fields.values():
                if field.name == name:
                    return (namespace, field)

    @classmethod
    def field_by_property(
        cls, property: str, value: object
    ) -> tuple[Namespace, Field] | None:
        logger.debug(
            "%s.field_by_property(property: %s, value: %s, %s)"
            % (cls.__name__, property, value, type(value))
        )

        for name, namespace in cls._namespaces.items():
            for field in namespace.fields.values():
                if not (attr := getattr(field, property, None)) is None:
                    if isinstance(attr, type(value)) and attr == value:
                        return (namespace, field)
                    elif isinstance(attr, list) and value in attr:
                        return (namespace, field)

    @classmethod
    def from_exiftool_fields(cls, fields: dict[str, object]) -> Metadata:
        pass

    def __init__(self, namespaces: dict[str, Namespace] = None):
        logger.debug(
            "%s.__init__(namespaces: %s)" % (self.__class__.__name__, namespaces)
        )

        self._namespaces: caselessdict[str, Namespace] = caselessdict(
            namespaces or self._namespaces or {}
        )
        self._aliases: caselessdict[str, Namespace | Field] = caselessdict(
            self._aliases or {}
        )

        # Map any aliased namespaces
        for name, namespace in self._namespaces.items():
            if namespace.alias:
                if isinstance(
                    aliased := self._aliases.get(namespace.alias),
                    (Namespace, Groupspace),
                ):
                    self._aliases[namespace.alias] = Groupspace(aliased, namespace)
                else:
                    self._aliases[namespace.alias] = namespace

            logger.debug(
                "%s.__init__() alias => %s/%s => %s"
                % (self.__class__.__name__, namespace.name, namespace.alias, namespace)
            )

        for name, thing in self._aliases.items():
            # logger.debug(" >>> alias => %s => %s (%s)" % (name, thing, __type__(thing)))
            if isinstance(thing, str):
                if not ":" in thing:
                    raise ValueError(
                        "Top-level field aliases must have a ':' separator character between the namespace and field names!"
                    )
                elif len(thing.split(":")) > 2:
                    raise ValueError(
                        "Top-level field aliases must comprise of only two parts separated by a single ':' character between the namespace and field names!"
                    )

        # self._fields: caselessdict[str, Field] = caselessdict()
        self._values: caselessdict[str, Value] = caselessdict()
        self._special: list[str] = [
            prop for prop in dir(self) if not prop.startswith("_")
        ]

    def __getattr__(self, name: str) -> object:
        logger.debug("%s.__getattr__(name: %s)" % (self.__class__.__name__, name))

        value: object = None

        if name.startswith("_") or name in self._special:
            value = super().__getattr__(name)
        elif isinstance(namespace := self._namespaces.get(name), Namespace):
            namespace._metadata = self

            value = namespace
        elif isinstance(namespace := self._aliases.get(name), Namespace):
            namespace._metadata = self

            value = namespace
        elif isinstance(groupspace := self._aliases.get(name), Groupspace):
            groupspace._metadata = self

            value = groupspace
        elif isinstance(alias := self._aliases.get(name), str):
            (prefix, named) = alias.split(":")

            if isinstance(namespace := self._namespaces.get(prefix), Namespace):
                namespace._metadata = self

                value = namespace.__getattr__(named)
            elif isinstance(namespace := self._aliases.get(prefix), Namespace):
                namespace._metadata = self

                value = namespace.__getattr__(named)
            elif isinstance(groupspace := self._aliases.get(prefix), Groupspace):
                groupspace._metadata = self

                value = groupspace.__getattr__(named)
            else:
                raise AttributeError(
                    f"The Metadata class does not have an '{name}' aliased attribute!"
                )
        else:
            raise AttributeError(
                f"The Metadata class does not have an '{name}' attribute!"
            )

        # logger.debug("%s.__getattr__(name: %s) -> %s" % (self.__class__.__name__, name, value))

        return value

    def __setattr__(self, name: str, value: object):
        if name.startswith("_") or name in self._special:
            return super().__setattr__(name, value)

        logger.debug(
            "%s.__setattr__(name: %s, value: %s)"
            % (self.__class__.__name__, name, value)
        )

        if isinstance(value, Namespace):
            raise AttributeError(
                f"The Metadata class does not support setting the '{name}' namespace!"
            )
        elif isinstance(alias := self._aliases.get(name), str):
            (prefix, named) = alias.split(":", maxsplit=1)

            if isinstance(namespace := self._namespaces.get(prefix), Namespace):
                namespace._metadata = self

                return namespace.__setattr__(named, value)
            elif isinstance(namespace := self._aliases.get(prefix), Namespace):
                namespace._metadata = self

                return namespace.__setattr__(named, value)
            elif isinstance(groupspace := self._aliases.get(prefix), Groupspace):
                groupspace._metadata = self

                return groupspace.__setattr__(named, value)
            else:
                raise AttributeError(
                    f"The Metadata class does support setting the '{name}' attribute!"
                )
        else:
            raise AttributeError(
                f"The Metadata class does not support setting the '{name}' attribute!"
            )

    def __str__(self) -> str:
        return f"<Metadata({self.__class__.__name__}) @ 0x%x>" % (id(self))

    def __bool__(self) -> bool:
        return len(self._values) > 0

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def get(self, name: str, default: object = None) -> object | None:
        raise NotImplementedError

    def set(
        self,
        value: Value | object,
        name: str = None,
        field: Field = None,
        namespace: Namespace = None,
    ):
        logger.debug(
            "%s.set(value: %r, name: %s, field: %s, namespace: %s)"
            % (self.__class__.__name__, value, name, field, namespace)
        )

        if name is None and field is None:
            raise ValueError(
                "To set a value on the model, a field name or field class reference must be provided via the 'name' or 'field' arguments!"
            )

        for _identifier, _namespace in self._namespaces.items():
            # logger.debug(" >>>>>>> checking namespace: %s, %s" % (_identifier, _namespace))

            if isinstance(namespace, Namespace) and not namespace is _namespace:
                continue

            for _identifier, _field in _namespace._fields.items():
                # logger.debug(" >>>>>>> checking field: %s" % (_field.id))

                if isinstance(field, Field) and field is _field:
                    # logger.debug(" >>>>>>>> found field: %s to set with %s" % (_field.id, value))
                    return _namespace.set(metadata=self, field=_field, value=value)
                elif isinstance(name, str) and name in _field.names:
                    # logger.debug(" >>>>>>>> found field: %s to set with %s" % (_field.id, value))
                    return _namespace.set(metadata=self, field=_field, value=value)

        raise AttributeError(f"Setting the '{name or field.name}' attribute failed!")

    @property
    @typing.final
    def namespace(self) -> None:
        raise NotImplementedError

    @namespace.setter
    @typing.final
    def namespace(self, namespace: Namespace):
        if not isinstance(namespace, Namespace):
            raise TypeError(
                "The 'namespace' property must be assigned a Namespace class instance value!"
            )

        if namespace.id in self._namespaces:
            raise KeyError(
                f"A namespace with the identifier '{namespace.id}' already exists!"
            )

        self._namespaces[namespace.id] = namespace

        if namespace.alias:
            self._aliases[namespace.alias] = namespace

        logger.debug(
            "%s.namespace[%s/%s] = %s"
            % (self.__class__.__name__, namespace.name, namespace.alias, namespace)
        )

    @property
    @typing.final
    def namespaces(self) -> dict[str, Namespace]:
        # logger.debug("%s.namespaces => %s" % (self.__class__.__name__, self._namespaces))
        return self._namespaces

    @property
    @typing.final
    def aliases(self) -> dict[str, Namespace | Groupspace]:
        # logger.debug("%s.aliases => %s" % (self.__class__.__name__, self._aliases))
        return self._aliases

    # @property
    # @typing.final
    # NOTE: The name conflicts with the value() method defined below
    # def values(self) -> dict[str, Value]:
    #     return self._values

    @property
    @typing.final
    def fields(self) -> dict[str, Field]:
        # logger.debug("%s.fields()" % (self.__class__.__name__))

        fields: dict[str, Field] = {}

        for identifier, namespace in self._namespaces.items():
            # logger.debug(" - %s" % (identifier))

            for identifier, field in namespace._fields.items():
                # logger.debug("  - %s (%s)" % (identifier, field.name))

                if field.identifier in fields:
                    raise KeyError(
                        f"A field with the identifier '{field.id}' already exists!"
                    )

                fields[field.id] = field

        return fields

    @typing.final
    def items(
        self, all: bool = False
    ) -> typing.Generator[tuple[Field, Value], None, None]:
        """Return the fields and values currently held by this metadata model."""

        if not isinstance(all, bool):
            raise TypeError("The 'all' argument must have a boolean value!")

        for namespace in self._namespaces.values():
            for field in namespace._fields.values():
                if isinstance(value := self._values.get(field.id), Value):
                    yield (field, value)
                elif all is True:
                    yield (field, None)

    @typing.final
    def keys(self) -> list[str]:
        keys: list[str] = []

        for namespace in self._namespaces.values():
            for key in namespace._fields.keys():
                keys.append(key)

        return keys

    @typing.final
    def values(self) -> list[Value]:
        values: list[Value] = []

        for namespace in self._namespaces.values():
            for field in namespace._fields.values():
                if not (value := self._values.get(field.id)) is None:
                    values.append(value)
                else:
                    values.append(None)

        return values

    @abc.abstractmethod
    def encode(
        self, encoding: str = None, order: ByteOrder = ByteOrder.LSB, **kwargs
    ) -> bytes:
        encoded: list[bytes] = []

        for namespace in self._namespaces.values():
            if namespace.utilized is False and all is False:
                continue

            for field in namespace._fields.values():
                if not namespace.name in values:
                    values[namespace.name] = caselessdict()

                if not (value := self._values.get(field.id)) is None:
                    encoded.append(value.encode(order=order))

        return b"".join(encoded)

    @abc.abstractmethod
    def decode(self, value: bytes) -> Metadata:
        raise NotImplementedError

    @typing.final
    def dump(self, all: bool = True) -> caselessdict[str, object]:
        if not isinstance(all, bool):
            raise TypeError("The 'all' argument must have a boolean value!")

        values: caselessdict[str, object] = caselessdict()

        for namespace in self._namespaces.values():
            if namespace.utilized is False and all is False:
                continue

            for field in namespace._fields.values():
                if not namespace.name in values:
                    values[namespace.name] = caselessdict()

                if not (value := self._values.get(field.id)) is None:
                    if isinstance(value, Value):
                        values[namespace.name][field.name] = value.value
                    else:
                        values[namespace.name][field.name] = value
                elif all is True:
                    values[namespace.name][field.name] = None

        return values
