# EXIFData

The EXIFData library for Python provides a simplified and consistent way to work with
embedded image metadata in the EXIF, IPTC and XMP formats. The library can be used to
parse and create metadata in these formats which can be read from or embedded into image
files such as TIFF and JPEG images.

The EXIFData library provides support for parsing and creating raw metadata payloads of
these formats while delegating responsibility to PyVIPS to perform the extraction of and
embedding of the raw metadata payloads. Future versions of the library may offer support
for reading and writing a number of image file formats directly.

### Requirements

The EXIFData library has been tested to work with Python 3.10, 3.11, 3.12 and 3.13, but
has not been tested, nor is its use supported with earlier versions of Python.

### Installation

The library is available from the PyPI repository, so may be added easily to a project's
dependencies via its `requirements.txt` file or similar by referencing the library's
name, `exifdata`, or the library may be installed directly onto your local development
system using `pip install` by entering the following command:

	$ pip install exifdata

If you would like to install the optional `pyvips` dependency with the library, use:

	$ pip install "exifdata[pyvips]"

PyVIPS is needed if you wish to use open images from disk or to work with in-memory
images opened previously by PyVIPS. If you do not already have PyVIPS installed, it is
best to install it along with the library to ensure all functionality is available.

### Conceptual Model

The EXIFData library provides access to each of the supported metadata models as a class
that offers a number of namespaces, with each namespace offering the full selection of
metadata fields provided by that namespace.

The structure of the models is as follows, where each model offers several namespaces,
and each namespace offers many fields, that each provide access to one or more values
depending on the field, its data type, and its semantics:

```
                                            ┌─────────┐        ┌─────────┐
                                      ┌────▶│  Field  ├───────▶│  Value  │
                                      │     └─────────┘        └─────────┘
                    ┌─────────────┐   │     ┌─────────┐        ┌─────────┐
               ┌───▶│  Namespace  ├───┴────▶│  Field  ├───────▶│  Value  │
               │    └─────────────┘         └─────────┘        └─────────┘
┌─────────┐    │    ┌─────────────┐         ┌─────────┐        ┌─────────┐
│  Model  │────┼───▶│  Namespace  │────────▶│  Field  ├───────▶│  Value  │
└─────────┘    │    └─────────────┘         └─────────┘        └─────────┘
               │    ┌─────────────┐         ┌─────────┐        ┌─────────┐
               └───▶│  Namespace  │────┬───▶│  Field  ├───────▶│  Value  │
                    └─────────────┘    │    └─────────┘        └─────────┘
                                       │    ┌─────────┐        ┌─────────┐
                                       └───▶│  Field  ├───────▶│  Value  │
                                            └─────────┘        └─────────┘
```

For example, the `IPTC` model offers several namespaces including the `envelope`, and
`application`, namespaces, while the `XMP` model offers many namespaces of its own
including `basic`, `photoshop`, and `dc`. These namespaces then provide access to the
metadata fields for reading and writing.

To assign a value to the XMP metadata model's `dc.title` field for example, one would
either access an existing instance of the `XMP` model class, or create one, and would
then reference and assign a value to the `title` field held within the `dc` namespace
as follows:

<!--pytest.mark.skip-->

```python
xmp.dc.title = "this is a title"
```

In order to read a value from a field, one would just reference the field like any other
property, and if the field has an assigned value that can be decoded, its value will be
available as an instance of the library's `Value` class.

The `Value` class and its subclasses exist to support encoding and decoding of the raw
value types defined by each of the metadata standards.

<!--pytest.mark.skip-->

```python
print(xmp.dc.title)
```

Furthermore, where possible, the `Value` class types themselves subclass native Python
types including `str`, `int`, `float`, and `datetime`, so these `Value` class instances
can be used interchangeably like the corresponding native type would be used; however by
necessity some of the `Value` subclasses represent structured data types and provide
additional fields or methods to access and assign the nested values, so must be used
directly where the field requires it.

Each metadata model's supported namespaces and fields are documented with information
about the relevant value types, which detail how to access and assign values to each of
the supported fields.

The following table lists the currently supported metadata models along with links to
documentation, detailing each model's available namespaces and fields:

| Metadata Model | Documentation                                              |
|----------------|------------------------------------------------------------|
| EXIF           | [EXIF Namespaces & Fields](./documentation/models/exif.md) |
| IPTC           | [IPTC Namespaces & Fields](./documentation/models/iptc.md) |
| XMP            | [XMP Namespaces & Fields](./documentation/models/xmp.md)   |

The EXIFData library also offers some convenience methods to make it easy to read and
write the supported embedded metadata in supported image file formats; currently the
library relies on the PyVIPS library to read and write the image files, and perform the
extraction and insertion of the raw metadata payloads, before handing off responsibility
to the EXIFData library to decode and encode the raw metadata payloads and their nested
namespaces, fields and values.

See the [Classes & Methods](#classes-and-methods) section below for more information on
the available interfaces and their use; and see the [Supported File Formats](#file-formats)
section for more information on the image file formats that are currently supported by
the library, which includes JPEG, TIFF and Pyramidal TIFF images.

### Example Use: Reading Metadata

The code sample below illustrates the use of the EXIFData library to read metadata:

<!--pytest.mark.skip-->

```python
import exifdata

# Open an image file from disk and attempt to parse its embedded metadata
models = exifdata.Models.open("/path/to/image-file.jpg")

# Print out the existing metadata model assigned fields and values
for model in models:
    print(model.name)
    for field, value in model.items(all=False):
        print(" -> %s => %s" % (field, value))
```

### Example Use: Writing Metadata

The code sample below illustrates the use of the EXIFData library to write metadata:

<!--pytest.mark.skip-->

```python
import exifdata

models = exifdata.Models.open("/path/to/image-file.jpg")

models.xmp.basic.title = "test title"
models.iptc.credit = "test credit"

# Save the image back to disk
models.save()
```

### Example Use: Reading and Writing Metadata with an existing PyVIPS Image

<!--pytest.mark.skip-->

```python
import exifdata
import pyvips

# Open the desired image file using PyVIPS
image = pyvips.Image.new_from_file("/path/to/image-file.tiff")

# Attempt to decode the metadata models from the provided image using EXIFData
models = exifdata.Models.load(image)

# Print out the existing metadata model assigned fields and values
for model in models:
    print(model.name)
    for field, value in model.items(all=False):
        print(" -> %s => %s" % (field, value))

# Set or update the desired metadata fields
models.xmp.basic.title = "test title"
models.iptc.credit = "test credit"

# Encode the updated metadata and embed it into the in-memory image buffer
models.encode()

# Save the image back to disk or capture the image into a buffer as needed
image.tiffsave()
```

⚠️ **Note:** When working directly with a PyVIPS image held in an `Image` class instance
one must remember to save the image or otherwise do something with the updated in-memory
image buffer as the call to the `models.encode()` method only encodes and embeds the
metadata into the in-memory image buffer. While the in-memory image buffer will then
contain the metadata, if one needs to save the image back to disk, that must be handled
as a separate call to PyVIPS.

<a id="classes-and-methods"></a>
### Classes & Methods

#### Models Class Methods & Properties

The `Models` class offers the following methods:

* `adapt(adapter: Adapter)` – The `adapt()` method provides support for associating the
specified `Adapter` class type with the `Models` class to allow the specified adapter to
be used to assist in reading and writing image files.

* `load(filepath: str)` – The `load()` method provides support for loading the specified
image file from the `filepath` which must exist and reference an image in a usable image
file format. If the referenced image file does not exist or cannot be loaded an error is
reported.

* `associate(image: object)` – The `associate()` method provides support for associating
the specified in-memory image with the `Models` class instance, which sets the reference
to the image without attempting to extract or decode any of the pre-existing metadata in
the image.

* `open(image: object)` – The `open()` method provides support for associating the
specified in-memory image with the `Models` class instance, which sets the reference to
the image and then proceeds to attempt extracting and decoding any pre-existing metadata
in the image.

* `update(model: Metadata)` – The `update()` method provides support for updating the
metadata models held by the `Models` class instance with new `Metadata` model subclass
instances if needed; if a matching `Metadata` model subclass has already been registered
with the `Models` class then it will be replaced by the provided `Metadata` instance and
if no match is found then the the provided `Metadata` instance will be registered.

* `assign(name: str, value: object)` – The `assign()` method provides support to assign
metadata model values to any of the supported metadata models via the metadata field's
fully qualified name, along with a supported value. If the provided name can be matched
with a name associated with one or more metadata model fields, and if the provided value
is valid, then the value will be assigned to the matching metadata model fields. This
offers an alternative method to setting metadata model field values via the property
accessor pattern.

* `erase(payloads: list[str] = None)` – The `erase()` method provides support for erasing
erasable metadata held in the associated image from either the specified payloads if one
or more supported payload names are specified, or from all of the metadata payloads if
no payloads are specified. The payloads and/or their embedded fields that are removed
from an image are dependent on the metadata payload as some fields are mandatory so they
cannot be removed, such as many of the fields in the EXIF payload. 

* `decode(order: ByteOrder)` – The `decode()` method provides support for decoding the
embedded metadata payloads contained in the associated image file, and if metadata is
found within the image and can be successfully decoded, the relevant metadata model
field values will be populated with the decoded values. The values can then be read and
otherwise used, and if desired, the values can be modified or cleared, before saving the
updated metadata back to the associated image.

* `encode(order: ByteOrder)` – The `encode()` method provides support for encoding the
assigned metadata model field values into encoded metadata payloads suitable for storing
into the associated image file.

The `Models` class offers the following properties:

* `adapter` (`Adapter`) – The `adapter` property provides access to the reference to the
current `Adapter` class instance associated with the `Models` class. The `Adapter` class
is used by the `Models` class to interact with image data and raw metadata via various
libraries such as PyVIPS, EXIFTool and TIFFData.

* `model` (`Metadata`) - The `model` property provides support for assigning one or more
`Metadata` model class instances to the `Models` class. The property can only be used to
assign `Metadata` model class instances to the `Models` class, it cannot be used to get
any of the assigned `Metadata` model class instances; instead this can be achieved by
iterating over the `Models` class instance as the `Models` class supports the iterator
protocol to provide access to the assigned `Metadata` model class instances using the
standard `for ... in ...` pattern.

* `exif` (`EXIF`) – The `exif` property provides support for accessing the `EXIF` model
instance associated with the `Models` class, which can then be used to access any of the
decoded metadata model field values or to assign or clear metadata model field values
associated with the EXIF metadata model.

* `iptc` (`IPTC`) – The `iptc` property provides support for accessing the `IPTC` model
instance associated with the `Models` class, which can then be used to access any of the
decoded metadata model field values or to assign or clear metadata model field values
associated with the IPTC metadata model.

* `xmp` (`XMP`) – The `xmp` property provides support for accessing the `XMP` model
instance associated with the `Models` class, which can then be used to access any of the
decoded metadata model field values or to assign or clear metadata model field values
associated with the XMP metadata model.

#### Metadata

The `Metadata` class provides the following methods:

* `register_type(type: Type, klass: Value)` – The `register_type()` method is used by
the EXIFData library internally to register `Value` subclass types for field types, as
defined by their `Type` enumeration class option values. The `Value` subclasses provide
support for encoding and decoding metadata model field values according to the needs of
the specific metadata model. The method should not be used directly unless developing an
update for the EXIFData library.

* `register_types(*types: tuple[type])` – The `register_types()` method is used by the
EXIFData library internally to register multiple `Value` subclass types for field types.
The `Value` subclasses provide support for encoding and decoding metadata model field
values according to the needs of the specific metadata model. The method should not be
used directly unless developing an update for the EXIFData library.

* `type_by_name(name: str)` (`Value` | `None`) – The `type_by_name()` method provides
support for accessing a registered `Value` type subclass by its name. This method is
used internally by the library and likely does not need to be used directly unless
developing an update for the EXIFData library.

* `field_by_id(id: str)` (`Field` | `None`) – The `field_by_id()` provides support for
looking up a  field by its identifier. If a match can be found the matching `Field` will
be returned, otherwise the method will return `None`.

* `field_by_name(name: str)` (`Field` | `None`) – The `field_by_name()` provides support
for looking up a  field by its name. If a match can be found the matching `Field` will
be returned, otherwise the method will return `None`.

* `field_by_property(property: str, value: object)` (`Field` | `None`) – The
`field_by_property()` method provides support for looking up a field by one of its named
properties where a match is sought for the specified value. If a match can be found the
matching `Field` will be returned, otherwise the method will return `None`.

* `get(name: str, default: object = None)` – The `get()` method provides support for
obtaining the value set for the named metadata model class field, if a value has
previously been assigned. If no value was previously assigned the method will return the
default value if one has been assigned or `None`.

* `set(value: Value, name: str = None, field: Field = None, namespace: Namespace = None)`
– The `set()` method provides support for setting a value on the metadata model class.
If the provided value held in a `Value` subclass instance has its own reference to a
`Field` class instance, the field name can be determined from the `Field` and does not
need to be specified directly, otherwise the `name` argument can optionally be specified
to provide the field name. If a `Namespace` class instance is optionally specified via
the `namespace` argument, then the field value will be stored within that namespace; if
a namespace is not specified directly, but a `Field` class instance is referenced by the
value, then the namespace can be determined from the `Field` class instance.

* `items(all: bool = False)` (`Generator`) – The `items()` method provides support for
iterating over the metadata model's fields and associated values. The generator yields
`tuple` values that hold a `Field` class instance and its corresponding `Value` class
instance for all the metadata model fields that have assigned values. If the `all` flag
is set to `True` the method will yield a `tuple` holding a `Field` class instance and a
`Value` class instance for every registered field in the metadata model, even if some of
the fields do not have assigned values. The returned `Value` class instances in those
cases will hold `None` values indicating that the field does not have an assigned value.

* `keys()` (`list[str]`) – The `keys()` method provides support for obtaining a list of
all of the names of the fields associated with the metadata model class.

* `values()` (`list[Value]`) – The `values()` method provides support for obtaining a
list of all of the values of the fields associated with the metadata model class, where
the values are held in `Value` subclass instances. Where a field does not have a current
value, a `Value` subclass instance holding a `None` value will be returned in its place
indicating that the field does not have an assigned value; the order of the items in the
list matches the order of the field names provided by the `keys()` method so the two can
be used together if needed as an alternative way of accessing the field names and values.

* `encode(order: ByteOrder)` - The `encode()` method provides support for encoding the
metadata model's assigned metadata fields and values into a binary format suitable for
embedding within the associated image.

* `decode(order: ByteOrder)` - The `decode()` method provides support for decoding the
binary encoded metadata payload obtained from the associated image and attempting to
parse the fields and values from the payload, and if successful, assigning those fields
and corresponding values to the current metadata model class instance for later use.

* `dump(all: bool = False)` (`caselessdict[str, object]`) – The `dump()` method is used
for development and can be used to obtain a dictionary of the metadata model's assigned
values with each value being associated against the model's field name. A dictionary is
returned that supports case-less matching of its keys so values can be retrieved if a
match can be found for the key regardless of if the casing of the key. If the `all` flag
is set to `True` the dictionary will be populated with the full list of metadata model
fields even if no value has been assigned to that field in the current model instance.

The `Metadata` class provides the following properties:

* `name` (`str`) – The `name` property provides access to the `Metadata` model subclass'
name, such as "EXIF", "IPTC" and "XMP".

* `namespace` (`Namespace`) – The `namespace` property provides access to get and set
the model's currently assigned `Namespace` class instance. This property is used by the
library internally and likely does not need to be used directly unless developing an
update for the EXIFData library.

* `namespaces` (`dict[str, Namespace]`) – The `namespaces` property provides access to a
dictionary of the model's currently assigned `Namespace` class instances. This property
is used by the library internally and likely does not need to be used directly unless
developing an update for the EXIFData library.

* `aliases` (`dict[str, Namespace | Groupspace]`) – The `aliases` property provides
access to a dictionary of the model's currently assigned `Namespace` and `Groupspace`
class instances. These are used to keep track of aliases for the namespaces which make
working with the namespaces easier as some have long and unwieldy assigned names in the
specifications, and the library offers shorter more concise names where practical. This
property is used by the library internally and likely does not need to be used directly
unless developing an update for the EXIFData library.

* `fields` (`dict[str, Value]`) – The `fields` property provides access to the metadata
model's fields via a dictionary where the keys are the field names and the values are
the assigned `Field` class instances holding information about the field that has been
sourced from the metadata model configuration.

* `values` (`dict[str, Value]`) – The `values` property provides access to the metadata
model's currently assigned field values via a dictionary where the keys are the field
names and the values are the assigned `Value` subclass instances holding the value.

#### Namespace

The `Namespace` class provides a structured method for grouping metadata model fields by
their namespace, and providing support for a metadata model to hold multiple namespaces
simultaneously each with their own set of metadata fields and values. The namespaces are
created dynamically when the metadata model classes are parsed with the namespaces being
determined from the metadata model class' schema configuration.

The `Namespace` class provides the following methods:

* `get(metadata: Metadata, field: Field)` (`Value` | `None`) – The `get()` method can be
used to obtain the specified metadata model field value, if it has been set previously,
with the value being returned as a `Value` subclass instance if a value has been set.

* `set(metadata: Metadata, field: Field, value: Value)` – The `set()` method can be used
to set the specified metadata model field value to value held by the assigned `Value`
subclass instance.

* `items()` (`Generator`)  – The `items()` method provides support for iterating over
the namespace's assigned fields. The generator yields `tuple` values that hold the name
of the field and the corresponding `Field` class instance.

* `keys()` (`list[str]`) – The `keys()` method provides support for obtaining a list of
all of the names of the fields associated with the namespace class instance.

* `values()` (`list[Value]`) – The `values()` method provides support for obtaining a
list of all of the values of the fields associated with the namespace instance, where
the values are held in `Value` subclass instances. Where a field does not have a current
value, a `Value` subclass instance holding a `None` value will be returned in its place
indicating that the field does not have an assigned value; the order of the items in the
list matches the order of the field names provided by the `keys()` method so the two can
be used together if needed as an alternative way of accessing the field names and values.

The `Namespace` class provides the following properties:

* `id` (`str`) – The `id` property provides access to the namespace's identifier.

* `name` (`str`) – The `name` property provides access to the namespace's name.

* `uri` (`str`) – The `uri` property provides access to the namespace's URI.

* `prefix` (`str`) – The `prefix` property provides access to the namespace's prefix.

* `alias` (`str` | `None`) – The `alias` property provides access to the namespace's
alias, if one has been set, otherwise `None` will be returned.

* `definition` (`str` | `None`) – The `definition` property provides access to the
namespace's descriptive definition, sourced from the metadata model class' schema if one
has been set, otherwise `None` will be returned.

* `metadata` (`Metadata`) – The `metadata` property provides access to get and set the
namespace's associated `Metadata` model class instance.

* `structures` (`list[Structure]`) – The `structures` property provides access to the
list of `Structure` class instances associated with the namespace, if any have been set
in the metadata model class' schema.

* `utilized` (`bool`) – The `utilized` property provides support for determining if the
current `Namespace` class instance has been utilized in the current program, which means
that at least one metadata model field has been set within the namespace. The property
will return `True` if at least one field has been set or `False` otherwise. This status
is used internally by the library when encoding a metadata model's data, whereby if the
namespace has not been utilized, it will be excluded by the encoding process. 

* `unwrap` (`bool`) – The `unwrap` property provides access to the `unwrap` property set
in the metadata model class' schema, which the library uses to determine if it should
"unwrap" the namespaces fields into its parent's namespace – that is to make the fields
directly accessible from the parent `Metadata` model class rather than indirectly via
the namespace. This field is used internally by the library and likely does not need to
be used directly unless developing an update for the EXIFData library.

* `fields` (`dict[str, Field]`) – The `fields` property is used internally by the library
to associate registered metadata model fields against the namespace. The property expects
a dictionary with string keys holding the fully qualified field names and `Field` class
instances as the values. This field is used internally by the library and should not need
to be used directly unless developing an update for the EXIFData library.

* `field` (`Field`) – The `field` property is used internally by the library to associate
a registered metadata model field against the namespace. The property expects a `Field`
class instances as its value. This field is used internally by the library and should not
need to be used directly unless developing an update for the EXIFData library.

* `value` (`Value`) - The `value` property is used internally by the library to associate
assigned metadata model namespace field values with the namespace. The property expects
a `Value` class instances as its value. The `Value` class instance must hold references
to the relevant `Metadata` model class instance and `Field` class instance so that the
value can be assigned to the correct field under the correct metadata model. The field
is used internally by the library and should not need to be used directly unless
developing an update for the EXIFData library.

#### Groupspace

The `Groupspace` class provides a structured method for grouping one or more namespaces
together to make assigning field values to those namespaces easier for certain uses. The
`Groupspace` class instances streamline support for aliasing the namespaces and are used
internally by the library and likely does not need to be used directly unless developing
an update for the EXIFData library.

The `Groupspace` class provides its own implementations of the standard library getter
and setter methods to support assigning field values to the relevant `Namespace` class
instance held by the `Groupspace` class instance.

The `Groupspace` class provides the following properties:

* `namespaces` (`list[Namespace]`) – The `namespaces` property provides access to the
list of namespaces associated with the `Groupspace` class instance.

* `metadata` (`Metadata`) – The `metadata` property provides access to get and set the
associated `Metadata` model class instance for the `Groupspace` class instance. This is
used when interacting with the underlying `Namespace` class instances so that they can
interface with the correct `Metadata` model class instance.

#### Field

The `Field` class provides a controlled method for holding information about metadata
model fields, including their identifier, name, label, definition, acceptable value data
types, acceptable value ranges, whether the field can hold multiple values or not, and
all other relevant field configuration information that is used both when decoding raw
metadata payloads and assembling encoded payloads as well as during value assignment.

The `Field` class provides the following methods:

* `value(value: object, metadata: Metadata = None)` – The `value()` method provides
support for assigning a value to the field against its associated namespace and metadata
model class instance. The `metadata` argument is optional, but can be used to override
the metadata model that the field value will be assigned to if needed.

The `Field` class provides the following properties:

* `namespace` (`Namespace`) – The `namespace` property provides access to the `Field`
class associated namespace.

* `identifier` (`str` | `int`) – The `identifier` property provides access to the
field's identifier.

* `name` (`str`) – The `name` property provides access to the field's name.

* `type` (`str` | `list[str]` | `tuple[str]` | `set[str]`) – The `type` property provides
access to the field's accepted data type or types as defined by the name of the accepted
data types.

* `structure` (`Structure` | `str`) – The `structure` property provides access to the
field's associated `Structure` class instance or structure name if one has been defined.

* `alias` (`str` | `list[str]`) – The `alias` property provides access to the field's
associated field name alias or aliases if any have been defined. The field name aliases
provide support for accessing fields via aliases as well as their assigned names.

* `pseudonym` (`str` | `list[str]` | `dict[str, str]`) – The `pseudonym` property
provides access to the registered pseudonyms for a field, these are names that are used
for the field in other software such as EXIFTool which helps support interoperability.

* `encoding` (`Encoding` | `str`) – The `encoding` property provides access to the value
encoding used the field, expressed as an `Encoding` enumeration class option or string.

* `unit` (`str`) – The `unit` property provides access to the name of the measurement
unit associated with the values held by the field.

* `tag` (`int`) – The `tag` property provides access to the field's associated tag
identifier value, such as the tag identifiers used to uniquely identify the fields in
the EXIF metadata and IPTC metadata models.

* `ordered` (`bool`) – The `ordered` property provides access to the `ordered` flag that
notes if the value held by the field should have its ordering preserved or not.

* `minimum` (`int` | `float`) – The `minimum` property provides access to the minimum
numeric value that can be held by the field, when the field has been configured to hold
a numeric value with a defined minimum.

* `maximum` (`int` | `float`) – The `maximum` property provides access to the maximum
numeric value that can be held by the field, when the field has been configured to hold
a numeric value with a defined maximum.

* `options` (`list[object]`) – The `options` property provides access to the list of
acceptable values that can be held by the field for fields that have such a list.

* `closed` (`bool`) – The `closed` property provides access to the `closed` flag which
notes whether a field must be assigned a value from a predefined (closed) list of options
or whether the field can be assigned a value from the list of options as well as others.

* `nullable` (`bool`) – The `nullable` property provides access to the `nullable` flag
which notes if the field can hold a null (`None`) value or not.

* `required` (`bool`) – The `required` property provides access to the `required` flag
which notes if the field holds a required value or not, where a value must be assigned
if the field is marked as being required.

* `readonly` (`bool`) – The `readonly` property provides access to the `readonly` flag
which notes if the field holds a read only value or not. Fields with read only values
can be used to access values parsed and decoded from embedded metadata payloads but the
field cannot change its value.

* `count` (`int` | `tuple[int]`) – The `count` property provides access to the number or
numbers values that the field must hold if a count has been specified. This property is
also used to hold the minimum and maximum lengths of string and bytes fields.

* `multiple` (`bool`) – The `multiple` property provides access to the `multiple` flag
which notes if the field supports holding more than one value or not.

* `combine` (`bool`) – The `combine` property provides access to the `combine` flag that
notes whether the values held by the field should be combined or not.

* `label` (`str`) – The `label` property provides access to the field's label if one has
been set in the model class' schema.

* `definition` (`str`) – The `definition` property provides access to the field's
descriptive definition if one has been set in the model class' schema.

* `related` (`Field` | `str`) – The `related` property provides access to a reference to
the field's related `Field` if one has been specified.

* `section` (`str`) – The `section` property provides access to the documentation section
reference for the metadata field, if one has been set in the model class' schema.

#### Value

The `Value` class provides the following methods:

* `validate()` (`bool`) – The `validate()` method provides support for validating the
value held by the `Value` subclass instance to determine if it is valid according to the
metadata model class' schema configuration.

* `decode(value: bytes, order: ByteOrder)` (`Value`) – The `decode()` method provides
support for decoding a raw binary encoded value extracted from the metadata payload into
its corresponding value which will be returned as a `Value` subclass instance.

* `encode(order: ByteOrder)` (`bytes`) – The `encode()` method provides support for
encoding the value held by the `Value` subclass instance into a form suitable for use as
part of the metadata model's encoded payload.

The `Value` class provides the following properties:

* `value` (`object`) – The `value` property provides access to the underlying value held
by the `Value` subclass instance.

* `encoding` (`Encoding`) – The `encoding` property provides access to the associated
encoding of the value field, expressed as an `Encoding` enumeration class option value.

* `field` (`Field` | `None`) – The `field` property provides access to the associated
instance of the `Field` class if one has been assigned.

* `metadata` (`Metadata` | `None`) – The `metadata` property provides access to the
associated instance of the `Metadata` class if one has been assigned.

#### Structure

The `Structure` class provides a controlled method for holding metadata model field
structure information extracted and assigned dynamically from the metadata model class'
schema configuration. The structure information is used internally by the library when
encoding metadata into its encoded form as defined by the associated metadata standard.

The `Structure` class provides the following properties:

* `id` (`str`) – The `id` property provides access to the structure's identifier.

* `identifier` (`str`) – The `identifier` property provides access to the structure's identifier.

* `name` (`str`) – The `name` property provides access to the structure's name.

* `type` (`str`) – The `id` property provides access to the structure's type name.

* `kind` (`str`) – The `id` property provides access to the structure's kind descriptor.

#### Type

The `Type` class enumeration class provides a controlled method for keeping track of the
registered field value types supported by each metadata model. The field value types are
registered by the metadata model classes dynamically when they are parsed with the types
being determined from the metadata model class' schema configuration.

<a id="file-formats"></a>
### Supported File Formats

The EXIFData library has been tested with a range of image file formats to determine the
accessibility of and ability to write embedded metadata, those file formats are listed
in the table below and with whether the file format supports reading or writing or both.
As the library currently relies upon PyVIPS for loading and saving image files, it may
be the case that additional file formats are found to work with the library, or support
may be added for additional file formats over time. The EXIFData library's ability to
support an image file format depends on the file format itself as there are myriad image
file formats and embedded metadata standards. Although EXIF, IPTC and XMP are considered
the most common, these standards are not supported by every image file format.

| File Format | EXIF Read | EXIF Write | IPTC Read | IPTC Write | XMP Read | XMP Write |
| ----------- | :-------: | :--------: | :-------: | :--------: | :------: | :-------: |
| JPEG        | No*       | Yes        | Yes       | Yes        | No*      | Yes       |
| TIFF        | No*       | Yes        | Yes       | Yes        | No*      | Yes       |
| PyramidTIFF | No*       | Yes        | Yes       | Yes        | No*      | Yes       |
| PNG         | *         | *          | *         | *          | *        | *         |
| HEIF        | *         | *          | *         | *          | *        | *         |

* EXIF and XMP read capability is in development and will be added in a future release.
* Support for other image file formats is currently in development.

### Disclaimer

While every effort has been made to ensure that the library works reliably with embedded
image metadata, you must ensure that all files are backed up before using the EXIFData
library with any files especially as the library is still in early development.

Furthermore, the library may not be able to read nor preserve all metadata field values
from an image file, especially if manufacturer specific or custom metadata model values
are present, so it is possible that loss of embedded metadata could occur if an image is
loaded into the library and is then overwritten if the file is saved to the same path.

Use of the library is entirely at your own risk and the authors bear no responsibility
for losses of any kind. By using the software you assume all such risk and liability.

THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.

### Credits & References

The EXIF, IPTC and XMP metadata model specifications were researched across various
sources. Please visit these valuable online resources to learn more about the metadata
model specifications and to support these world class organizations and their products:

 * EXIF Metadata Model & Fields
   * https://www.cipa.jp/e/index.html
   * https://www.loc.gov/preservation/digital/formats/fdd/fdd000146.shtml
   * https://exiftool.org/TagNames/EXIF.html
   * https://www.media.mit.edu/pia/Research/deepview/exif.html
   * https://exiv2.org/tags.html

 * IPTC Metadata Model & Fields
   * https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata
   * https://exiftool.org/TagNames/IPTC.html

 * XMP Metadata Model & Fields
   * https://www.adobe.com/products/xmp.html
   * https://exiftool.org/TagNames/XMP.html

### Copyright & License Information

Copyright © 2024–2025 Daniel Sissman; licensed under the MIT License.