from __future__ import annotations

import abc
import typing

from exifdata.configuration import secrets
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

        if not issubclass(klass, framework.Value):
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
                    (framework.Namespace, framework.Groupspace),
                ):
                    self._aliases[namespace.alias] = framework.Groupspace(
                        aliased, namespace
                    )
                else:
                    self._aliases[namespace.alias] = namespace

            logger.debug(
                "%s.__init__() alias => %s/%s => %s"
                % (self.__class__.__name__, namespace.name, namespace.alias, namespace)
            )

        for name, thing in self._aliases.items():
            # logger.debug(" >>> alias => %s => %s (%s)" % (name, thing, type(thing)))
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
        elif isinstance(namespace := self._namespaces.get(name), framework.Namespace):
            namespace._metadata = self

            value = namespace
        elif isinstance(namespace := self._aliases.get(name), framework.Namespace):
            namespace._metadata = self

            value = namespace
        elif isinstance(groupspace := self._aliases.get(name), framework.Groupspace):
            groupspace._metadata = self

            value = groupspace
        elif isinstance(alias := self._aliases.get(name), str):
            (prefix, named) = alias.split(":")

            if isinstance(
                namespace := self._namespaces.get(prefix), framework.Namespace
            ):
                namespace._metadata = self

                value = namespace.__getattr__(named)
            elif isinstance(
                namespace := self._aliases.get(prefix), framework.Namespace
            ):
                namespace._metadata = self

                value = namespace.__getattr__(named)
            elif isinstance(
                groupspace := self._aliases.get(prefix), framework.Groupspace
            ):
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

        if isinstance(value, framework.Namespace):
            raise AttributeError(
                f"The Metadata class does not support setting the '{name}' namespace!"
            )
        elif isinstance(alias := self._aliases.get(name), str):
            (prefix, named) = alias.split(":", maxsplit=1)

            if isinstance(
                namespace := self._namespaces.get(prefix), framework.Namespace
            ):
                namespace._metadata = self

                return namespace.__setattr__(named, value)
            elif isinstance(
                namespace := self._aliases.get(prefix), framework.Namespace
            ):
                namespace._metadata = self

                return namespace.__setattr__(named, value)
            elif isinstance(
                groupspace := self._aliases.get(prefix), framework.Groupspace
            ):
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

            if (
                isinstance(namespace, framework.Namespace)
                and not namespace is _namespace
            ):
                continue

            for _identifier, _field in _namespace._fields.items():
                # logger.debug(" >>>>>>> checking field: %s" % (_field.id))

                if isinstance(field, framework.Field) and field is _field:
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
        if not isinstance(namespace, framework.Namespace):
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
                if isinstance(value := self._values.get(field.id), framework.Value):
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
        self,
        encoding: str = None,
        order: ByteOrder = ByteOrder.LSB,
        **kwargs,
    ) -> bytes:
        raise NotImplementedError

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
                    if isinstance(value, framework.Value):
                        values[namespace.name][field.name] = value.value
                    else:
                        values[namespace.name][field.name] = value
                elif all is True:
                    values[namespace.name][field.name] = None

        return values
