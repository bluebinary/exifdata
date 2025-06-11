# EXIFData: The XMP Metadata Model

The XMP (Extensible Metadata Platform) is a standard developed by Adobe® for embedding
metadata into digital assets such as images, videos, and documents. It is designed to
standardize the creation, processing, and exchange of metadata across applications and
file formats.

XMP uses the RDF (Resource Description Framework) to represent metadata as a set of
property-value pairs which are organized into schemas. Each schema is a logical grouping
of related properties, such as Dublin Core as well as Adobe specific schemas. Metadata
is stored as XML, often embedded directly within a file (such as for JPEG, PDF, or TIFF)
or can be held in a sidecar file which is common with RAW file formats.

The XMP model supports:

* Extensibility: Custom schemas can be defined being RDF based any valid RDF schema can
be used with the properties and values being formatted correctly in the generated XML,
although support for custom schemas and any stored data is dependent upon support in
software for reading and writing these values.
* Interoperability: Facilitates metadata exchange between systems and applications.
* Synchronization: Helps maintain metadata consistency across file types and workflows.

XMP is widely used in content management, digital photography, publishing and archiving.

### XMP Metadata Structure

#### Foundation
XMP uses W3C's RDF (Resource Description Framework) expressed in XML syntax to describe
metadata. Metadata is expressed as triples: subject – predicate – object, for example:
"this painting" (the subject) – "has a title" (the predicate) – “Still Life with Roses”
(the object).

#### Namespaces and Schemas
Metadata properties are grouped into schemas, also known as namespaces. Common schemas
include:

 * Dublin Core (`dc`) – This includes standard properties like title, creator, subject,
 description.
 * XMP Basic (`xmp`) – Basic properties like creation date, modification date, and the
 authoring tool used.
 * Adobe (`photoshop`, `tiff`, etc) – These Adobe metadata schemas are commonly used to
 express technical image information such as width and height (via the `tiff:ImageWidth`
 and `tiff:ImageLength` fields respectively) as well as information such as copyright
 and credit line (via the `photoshop:Copyright` and `photoshop:Credit` fields
 respectively), along with many other values. 

The full listing of supported namespaces and fields can be found below in the
[**XMP Metadata Model Namespaces & Fields**](#namespaces-and-fields) section.

#### Embedding
The metadata is either:

* Embedded directly into supporting file formats (including JPEG, PDF and TIFF).
* Stored in sidecar files (usually `.xmp` files which are primarily used with RAW image
file formats).

#### Structure
Metadata entries are encapsulated within:

| XML Element         | Description                                          |
| ------------------- | :--------------------------------------------------- |
| `<x:xmpmeta>`       | Root container element for XMP.                      |
| `<rdf:RDF>`         | RDF container element.                               |
| `<rdf:Description>` | The core element containing the metadata properties. |

#### XMP Example

A simple example XMP metadata payload may look like the following:

```xml
<?xpacket begin="" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/">
  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <rdf:Description rdf:about=""  
                     xmlns:dc="http://purl.org/dc/elements/1.1/"
                     xmlns:xmp="http://ns.adobe.com/xap/1.0/"
                     xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/">
      <tiff:ImageWidth>9073</tiff:ImageWidth>
      <tiff:ImageLength>7134</tiff:ImageLength>
      <dc:title>
       <rdf:Alt>
          <rdf:li xml:lang="x-default">Still Life with Roses (1995); Sophie Haywell (Welsh)</rdf:li>
        </rdf:Alt>
      </dc:title>
    </rdf:Description>
  </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>
```

The `<?xpacket>` prolog if present in an XMP payload should always follow the standard
format including the `id` attribute with a fixed value of `W5M0MpCehiHzreSzNTczkc9d`
although it is not clear what the fixed `id` value means or indicates, but it if another
value is substituted some XMP parsers and toolkits will replace it with the standard
value when parsing and normalizing the provided XMP XML.

<a id="namespaces-and-fields"></a>
### XMP Metadata Model Namespaces & Fields

{{fields}}

### Credits & References

The XMP field information was researched from various sources including the Adobe® XMP
specification and EXIFTool documentation. Please visit these valuable online resources
to learn more about the XMP metadata model specification and to support these world
class organizations and their products:

 * https://www.adobe.com/products/xmp.html
 * https://exiftool.org/TagNames/XMP.html
