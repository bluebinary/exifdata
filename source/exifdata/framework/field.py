from __future__ import annotations

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

        if isinstance(namespace, framework.Namespace):
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
                % (type(count))
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
                % (type(self._types))
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
        if not isinstance(namespace, framework.Namespace):
            raise TypeError(
                "The 'namespace' property must be assigned to a Namespace class instance!"
            )
        self._namespace = namespace

    @property
    def structure(self) -> Structure:
        return self._structure

    @structure.setter
    def structure(self, structure: Structure):
        if not isinstance(structure, framework.Structure):
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
        elif not isinstance(metadata, framework.Metadata):
            raise TypeError(
                "The 'metadata' argument, if specified, must reference a Metadata class instance!"
            )

        return self.type.klass(
            field=self,
            metadata=metadata,
            value=value,
        )
