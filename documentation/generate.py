#!/usr/bin/env python

"""The generate script generates documentation for the metadata models by combining
overview information provided in a metadata model specific template with metadata for
each model field sourced from the model's schema configuration files."""

from __future__ import annotations

import os
import json
import logging

from typing import Generator

# Configure the logger
logger = logging.getLogger("exifdata").getChild(__name__)

# Obtain the current directory path
directory = os.path.dirname(__file__)

# Configure the path to the metadata models' schema configuration files
modelspath = os.path.join(directory, "..", "source", "exifdata", "models")


class Field(object):
    """The documentation Field class represents the documentation about a field."""

    def __init__(
        self,
        name: str,
        identifier: str,
        label: str = None,
        required: bool = False,
        **kwargs,
    ):
        if not isinstance(name, str):
            raise TypeError("The 'name' argument must have a string value!")

        self.name = name

        if not isinstance(identifier, str):
            raise TypeError("The 'identifier' argument must have a string value!")

        self.identifier = identifier

        if label is None:
            pass
        elif not isinstance(label, str):
            raise TypeError("The 'label' argument must have a string value!")

        self.label = label

        self.required = required or False

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}({self.name})>"

    @staticmethod
    def sort(value: dict, priority: list[str] = None) -> dict:
        """Provide support for performing a custom sort on a dictionary with the option
        to prioritize some keys over others by sorting those keys higher (earlier)."""

        def priority_sort(item: tuple[str, object]) -> tuple[int, str]:
            (key, value) = item

            if priority and key in priority:
                # Higher priority (negative value) + alphabetical for prioritized keys
                return (-1, key)
            else:
                # Standard sorting for others + alphabetical for others
                return (0, key)

        sort = dict(sorted(value.items(), key=priority_sort))

        if priority:
            temp: dict[str, object] = {}

            for key in priority:
                if key in sort:
                    temp[key] = sort[key]
                    del sort[key]

            for key in sort:
                temp[key] = sort[key]

            sort = temp

        return sort

    @property
    def info(self) -> dict[str, object]:
        """Return the list of field properties sourced from the metadata model schema."""

        info: dict[str, object] = {}

        for attribute in dir(self):
            if attribute.startswith("_") or attribute in [
                "info",
                "assemble",
                "format",
                "sort",
                "path",
                "namespace",
            ]:
                continue
            info[attribute] = getattr(self, attribute)

        return self.sort(
            info,
            priority=["identifier", "name", "label", "tagid", "bytes_min", "bytes_max"],
        )

    def __getattr__(self, name: str) -> object | None:
        if name.startswith("_") or name in ["name", "identifier", "label", "path"]:
            return super().__getattribute__(name)
        else:
            return getattr(self, name, None)

    @staticmethod
    def format(value: object, attribute: str, monospaced: bool = False) -> str:
        """Provide support for formatting schema configuration values for use within the
        field configuration documentation sections."""

        if value is None:
            return "–"
        elif value is True:
            return "Yes"
        elif value is False:
            return "No"
        elif isinstance(value, list):
            return "; ".join([str(val) for val in value])
        elif isinstance(value, dict):
            return "; ".join([f"{key}: {val}" for key, val in value.items()])
        elif isinstance(value, str):
            value = value.strip()

            if attribute in ["definition"] and len(value) and not value.endswith("."):
                value = value + "."

            if monospaced is True:
                value = "`" + value + "`"

            return value
        else:
            return str(value)

    @property
    def path(self) -> str:
        """Provide a way to assemble the field "path" which is the dotted property path
        that can be used to read and set the metadata model field's value."""

        # When a namespace is unwrapped, it means its fields can be accessed at the top
        # level of the metadata model class instance, rather than being nested within a
        # namespace, thus the path would be the name of the variable holding the model
        # and then the property name (spelled with any combination of casing):
        if self.namespace.unwrap is True:
            return f"{self.namespace.model.path}.{self.name}"

        # For namespaces that are not configured to be unwrapped, the property path must
        # include the name of the namespace as part of the property access:
        else:
            return f"{self.namespace.model.path}.{self.namespace.path}.{self.name}"

    def assemble(self) -> Generator[str, None, None]:
        """Generate a summary of the current field for inclusion in the documentation."""

        labels: dict[str, str] = {
            "name": "Name",
            "identifier": "ID",
            "label": "Label",
            "definition": "Definiton",
            "type": "Type",
            "bytes_min": "Minimum bytes",
            "bytes_max": "Maximum bytes",
            "required": "Required?",
            "readonly": "Read Only?",
            "repeatable": "Repeatable?",
            "multiple": "Multiple?",
            "tagid": "Tag ID",
            "default": "Default Value",
            "count": "Count/Length",
            "section": "Citaton",
            "ordered": "Ordered?",
            "combine": "Combine?",
            "alias": "Alias",
            "pseudonym": "Pseudonym",
            "structure": "Structure",
            "tag": "Tag",
            "unit": "Unit",
            "options": "Options",
            "closed": "Closed?",
            "nullable": "Nullable?",
            "minimum": "Minimum Value",
            "maximum": "Maximum Value",
            "related": "Related Field",
            "encoding": "Encoding",
        }

        monospaced: list[str] = [
            "identifier",
            "path",
            "tagid",
        ]

        yield "### The `{identifier}` field has the following configuration:".format(
            identifier=self.identifier,
        )

        yield ""

        yield "| Attribute | Value    |"
        yield "|-----------|----------|"
        yield "| Path      | `{path}` |".format(path=self.path)

        missing: set[str] = set()

        for attribute, value in self.info.items():
            yield "| {attribute} | {value} |".format(
                attribute=labels[attribute] if attribute in labels else attribute,
                value=self.format(
                    value=value,
                    attribute=attribute,
                    monospaced=(attribute in monospaced),
                ),
            )

            if not attribute in labels:
                missing.add(attribute)

        if len(missing) > 0:
            logger.error(
                f"The following schema fields are missing from the labels lookup list: {[m for m in missing]}!"
            )


class Namespace(object):
    """The documentation Namespace class represents the documentation about a namespace."""

    _model: Model = None

    def __init__(
        self,
        name: str,
        identifier: str = None,
        label: str = None,
        alias: str = None,
        fields: dict[str, dict | Field] = None,
        unwrap: bool = None,
        **kwargs,
    ):
        self.name = name
        self.identifier = identifier
        self.label = label
        self.unwrap = unwrap or False
        self.alias = alias
        self.fields: dict[str, dict | Field] = {}

        for identifier, field in (fields or {}).items():
            if isinstance(field, Field):
                self.fields[identifier] = field
            elif isinstance(field, dict):
                self.fields[identifier] = Field(
                    identifier=identifier, namespace=self, **field
                )

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}({self.name})>"

    @property
    def path(self) -> str:
        return f"{self.alias if self.alias else self.name}".lower()


class Model(object):
    """The documentation Model class represents the documentation about a model."""

    def __init__(
        self,
        name: str,
        documentation: str,
        template: str,
        readable: bool = False,
        writable: bool = False,
    ):
        self.namespaces: list[Namespace] = []

        if not isinstance(name, str):
            raise TypeError("The 'name' argument must have a string value!")

        self.name: str = name

        if not isinstance(documentation, str):
            raise TypeError("The 'documentation' argument must have a string value!")

        self.documentation: str = documentation

        if not isinstance(template, str):
            raise TypeError("The 'template' argument must have a string value!")

        self.template: str = template

        if not isinstance(readable, bool):
            raise TypeError("The 'readable' argument must have a boolean value!")

        self.readable: bool = readable

        if not isinstance(writable, bool):
            raise TypeError("The 'writable' argument must have a boolean value!")

        self.writable: bool = writable

    @property
    def namespace(self):
        raise NotImplementedError

    @namespace.setter
    def namespace(self, namespace: Namespace):
        if not isinstance(namespace, Namespace):
            raise TypeError(
                f"The 'namespace' argument must reference a {Namespace} class instance!"
            )

        namespace.model = self

        self.namespaces.append(namespace)

    def generate(self) -> str:
        """Generate the documentation for the model by combining the informaton held in
        the associated template with field metadata sourced from the model's schema."""

        document: str = None

        with open(self.template, "r") as file:
            document = file.read()

        lines: list[str] = [line for line in self.assemble()]

        document = document.replace("{{fields}}", "\n".join(lines) if lines else "")

        with open(self.documentation, "w+") as file:
            file.write(document)

        return self.documentation

    @staticmethod
    def spoken(count: int) -> str:
        """Convert a number from its integer form to its spoken form."""

        if not isinstance(count, int):
            raise TypeError("The 'count' argument must have an integer value!")

        numbers: list[str] = [
            "zero",
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
            "ten",
            "eleven",
            "twelve",
            "thirteen",
            "fourteen",
            "fifteen",
            "sixteen",
            "seventeen",
            "eighteen",
            "nineteen",
            "twenty",
        ]

        if 0 <= count < len(numbers):
            return numbers[count]
        else:
            return str(count)

    @staticmethod
    def pluralise(plural: str, singular: str, count: int) -> str:
        """Return the plural or singular form of the provided word based on the count."""

        if not isinstance(plural, str):
            raise TypeError("The 'plural' argument must have a string value!")

        if not isinstance(singular, str):
            raise TypeError("The 'singular' argument must have a string value!")

        if not isinstance(count, int):
            raise TypeError("The 'count' argument must have an integer value!")

        return plural if count == 0 or count > 1 else singular

    @property
    def path(self) -> str:
        return f"{self.name}".lower()

    def assemble(self) -> Generator[str, None, None]:
        count: int = len(self.namespaces)

        actions: list[str] = []

        if self.readable is True:
            actions.append("reading")

        if self.writable is True:
            actions.append("writing")

        yield "The EXIFData library provides support for {actions} {model} metadata model fields. The model provides {count} {namespaces}.".format(
            actions=" and ".join(actions),
            model=self.name.upper(),
            count=self.spoken(count),
            namespaces=self.pluralise("namespaces", "namespace", count),
            are=self.pluralise("are", "is", count),
        )

        yield ""

        for namespace in self.namespaces:
            count: int = len(namespace.fields)

            if count == 0:
                yield "The {model} metadata model's `{namespace}` namespace does not currently offer any known fields.".format(
                    model=self.name.upper(),
                    namespace=namespace.name,
                )
            else:
                yield "The {model} metadata model's `{namespace}` namespace offers {count} {fields} which {are} listed below along with a link to each field's technical information:".format(
                    model=self.name.upper(),
                    namespace=namespace.name,
                    count=self.spoken(count),
                    fields=self.pluralise("fields", "field", count),
                    are=self.pluralise("are", "is", count),
                )

                yield ""
                yield "| Namespace  | Field Path | Field Name | Required? | Info |"
                yield "|------------|------------|------------|:---------:|------|"

                for identifier, field in namespace.fields.items():
                    yield "| `{namespace}` | `{path}` | {name} | {required} | {info} |".format(
                        namespace=namespace.name,
                        path=field.path,
                        name=field.name,
                        required="Yes" if field.required else "No",
                        info=f"[🔗](#{model.name}-{namespace.name}-{field.name})".lower(),
                    )

                yield ""

                yield "The technical details of each field may be found below:"

                yield ""

                for identifier, field in namespace.fields.items():
                    yield """<a id="{link}"></a>""".format(
                        link=f"{model.name}-{namespace.name}-{field.name}".lower(),
                    )

                    for line in field.assemble():
                        yield line

                    yield ""

            yield ""


class Models(object):
    """The documentation Models class represents a group of documentation Model classes."""

    def __init__(self, filepath: str, filenames: list[str] = None):
        self._models: list[Model] = []

        for schema in self.search(filepath=filepath, filenames=filenames):
            self.assemble(schema=schema)

    @property
    def model(self):
        raise NotImplementedError

    @model.setter
    def model(self, model: Model):
        if not isinstance(model, Model):
            raise TypeError(
                f"The 'model' argument must reference a {Model} class instance!"
            )
        self._models.append(model)

    def __len__(self) -> int:
        """Support iteration over the assigned Model instances."""

        return len(self._models)

    def __iter__(self) -> Generator[Model, None, None]:
        """Support iteration over the assigned Model instances."""

        for model in self._models:
            yield model

    def search(
        self, filepath: str, filenames: list[str] = None
    ) -> Generator[str, None, None]:
        """Search for the metadata model schema configuration files under the specified path."""

        logger.debug(
            "%s.search(filepath: %s, filenames: %s)",
            self.__class__.__name__,
            filepath,
            filenames,
        )

        if filenames is None:
            filenames = ["schema.json"]
        elif not isinstance(filenames, list):
            raise TypeError(
                "The 'filenames' argument, if specified, must reference a list of filenames to find!"
            )

        for path, directories, files in os.walk(filepath):
            for file in files:
                if file not in filenames:
                    continue
                yield os.path.abspath(os.path.join(path, file))

    def assemble(self, schema: str):
        """Instantiate and assemble the documentation models which hold metadata about
        the current metadata model for use in generating its documentation."""

        logger.debug("%s.assemble(schema: %s)", self.__class__.__name__, schema)

        name: str = os.path.dirname(os.path.dirname(schema)).split("/")[-1]

        # Parse the schema and gather information about the model's namespaces and fields
        with open(schema, "r") as file:
            if data := json.load(file):
                if keys := list(data.keys()):
                    documentation: str = os.path.join(directory, "models", f"{name}.md")
                    template: str = os.path.join(directory, "templates", f"{name}.md")

                    # Create a documentation Model instance
                    self.model = model = Model(
                        name=name,
                        documentation=documentation,
                        template=template,
                    )

                    for key in keys:
                        if key.startswith("@"):
                            if key == "@aliases":
                                model.aliases = data[key]
                            elif key == "@read":
                                model.readable = data[key]
                            elif key == "@write":
                                model.writable = data[key]
                            continue

                        # Create a documentation Namespace instance and associate it
                        # with the documentation Model instance
                        model.namespace = namespace = Namespace(**data[key])

                        logger.debug(
                            " - Key: %s, Name: %s, Label: %s, Unwrap: %s",
                            key,
                            namespace.name,
                            namespace.label,
                            namespace.unwrap,
                        )

                        if (count := len(namespace.fields)) > 0:
                            logger.info(
                                f"The '{namespace}' namespace has no {count} fields"
                            )
                        else:
                            logger.warning(
                                f"The '{namespace}' namespace has no configured fields!"
                            )


# Find the metadata models, and generate documentation for each:
if models := Models(filepath=modelspath):
    for model in models:
        logger.debug(f"Generating documentation for the {model.name} model...")
        model.generate()
