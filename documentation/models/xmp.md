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

The EXIFData library provides support for writing XMP metadata model fields. The model provides fourteen namespaces.

The XMP metadata model's `basic` namespace offers ten fields which are listed below along with a link to each field's technical information:

| Namespace  | Field Path | Field Name | Required? | Info |
|------------|------------|------------|:---------:|------|
| `basic` | `xmp.basic.Label` | Label | No | [🔗](#xmp-basic-label) |
| `basic` | `xmp.basic.CreateDate` | CreateDate | No | [🔗](#xmp-basic-createdate) |
| `basic` | `xmp.basic.CreatorTool` | CreatorTool | No | [🔗](#xmp-basic-creatortool) |
| `basic` | `xmp.basic.Identifier` | Identifier | No | [🔗](#xmp-basic-identifier) |
| `basic` | `xmp.basic.MetadataDate` | MetadataDate | No | [🔗](#xmp-basic-metadatadate) |
| `basic` | `xmp.basic.ModifyDate` | ModifyDate | No | [🔗](#xmp-basic-modifydate) |
| `basic` | `xmp.basic.Rating` | Rating | No | [🔗](#xmp-basic-rating) |
| `basic` | `xmp.basic.BaseURL` | BaseURL | No | [🔗](#xmp-basic-baseurl) |
| `basic` | `xmp.basic.Nickname` | Nickname | No | [🔗](#xmp-basic-nickname) |
| `basic` | `xmp.basic.Thumbnail` | Thumbnail | No | [🔗](#xmp-basic-thumbnail) |

The technical details of each field may be found below:

<a id="xmp-basic-label"></a>
### The `xmp:Label` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.basic.Label` |
| ID | `xmp:Label` |
| Name | Label |
| Label | – |
| Definiton | A word or short phrase that identifies a resource as a member of a userdefined collection. NOTE: One anticipated usage is to organize resources in a file browser. |
| Pseudonym | exiftool: xmp:Label |
| Required? | No |
| Type | Text |

<a id="xmp-basic-createdate"></a>
### The `xmp:CreateDate` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.basic.CreateDate` |
| ID | `xmp:CreateDate` |
| Name | CreateDate |
| Label | – |
| Alias | CreationDate |
| Definiton | The date and time the resource was created. For a digital file, this need not match a file-system creation time. For a freshly created resource, it should be close to that time, modulo the time taken to write the file. Later file transfer, copying, and so on, can make the file-system time arbitrarily different. |
| Pseudonym | exiftool: xmp:CreateDate |
| Required? | No |
| Type | Date |

<a id="xmp-basic-creatortool"></a>
### The `xmp:CreatorTool` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.basic.CreatorTool` |
| ID | `xmp:CreatorTool` |
| Name | CreatorTool |
| Label | – |
| Definiton | The name of the first known tool used to create the resource. |
| Pseudonym | exiftool: xmp:CreatorTool |
| Required? | No |
| Type | AgentName |

<a id="xmp-basic-identifier"></a>
### The `xmp:Identifier` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.basic.Identifier` |
| ID | `xmp:Identifier` |
| Name | Identifier |
| Label | – |
| Definiton | An unordered array of text strings that unambiguously identify the resource within a given context. An array item may be qualified with xmpidq:Scheme to denote the formal identification system to which that identifier conforms. NOTE: The xmp:Identifier property was added because dc:identifier has been defined in the original XMP specification as a single identifier instead of as an array, and changing dc:identifier to an array would break compatibility with existing XMP processors. |
| Multiple? | Yes |
| Ordered? | No |
| Pseudonym | exiftool: xmp:Identifier |
| Required? | No |
| Type | Text |

<a id="xmp-basic-metadatadate"></a>
### The `xmp:MetadataDate` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.basic.MetadataDate` |
| ID | `xmp:MetadataDate` |
| Name | MetadataDate |
| Label | – |
| Definiton | The date and time that any metadata for this resource was last changed. It should be the same as or more recent than xmp:ModifyDate. |
| Pseudonym | exiftool: xmp:MetadataDate |
| Required? | No |
| Type | Date |

<a id="xmp-basic-modifydate"></a>
### The `xmp:ModifyDate` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.basic.ModifyDate` |
| ID | `xmp:ModifyDate` |
| Name | ModifyDate |
| Label | – |
| Alias | ModificationDate |
| Definiton | The date and time the resource was last modified. NOTE: The value of this property is not necessarily the same as the file’s system modification date because it is typically set before the file is saved. |
| Pseudonym | exiftool: xmp:ModifyDate |
| Required? | No |
| Type | Date |

<a id="xmp-basic-rating"></a>
### The `xmp:Rating` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.basic.Rating` |
| ID | `xmp:Rating` |
| Name | Rating |
| Label | – |
| Definiton | A user-assigned rating for this file. The value shall be -1 or in the range [0..5], where -1 indicates “rejected” and 0 indicates “unrated”. If xmp:Rating is not present, a value of 0 should be assumed. NOTE: Anticipated usage is for a typical “star rating” UI, with the addition of a notion of rejection. |
| Options | -1; 0; 1; 2; 3; 4; 5 |
| Pseudonym | exiftool: xmp:Rating |
| Required? | No |
| Type | Real |

<a id="xmp-basic-baseurl"></a>
### The `xmp:BaseURL` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.basic.BaseURL` |
| ID | `xmp:BaseURL` |
| Name | BaseURL |
| Label | – |
| Definiton | The base URL for relative URLs in the document content. If this document contains Internet links, and those links are relative, they are relative to this base URL. This property provides a standard way for embedded relative URLs to be interpreted by tools. Web authoring tools should set the value based on their notion of where URLs will be interpreted. |
| Pseudonym | exiftool: xmp:BaseURL |
| Required? | No |
| Type | URL |

<a id="xmp-basic-nickname"></a>
### The `xmp:Nickname` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.basic.Nickname` |
| ID | `xmp:Nickname` |
| Name | Nickname |
| Label | – |
| Definiton | A short informal name for the resource. |
| Pseudonym | exiftool: xmp:Nickname |
| Required? | No |
| Type | Text |

<a id="xmp-basic-thumbnail"></a>
### The `xmp:Thumbnail` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.basic.Thumbnail` |
| ID | `xmp:Thumbnail` |
| Name | Thumbnail |
| Label | – |
| Definiton | An alternative array of thumbnail images for a file, which can differ in characteristics such as size or image encoding. |
| Multiple? | Yes |
| Pseudonym | exiftool: xmp:Thumbnail |
| Required? | No |
| Type | Thumbnail |


The XMP metadata model's `media_management` namespace offers sixteen fields which are listed below along with a link to each field's technical information:

| Namespace  | Field Path | Field Name | Required? | Info |
|------------|------------|------------|:---------:|------|
| `media_management` | `xmp.media_management.derivedFrom` | derivedFrom | No | [🔗](#xmp-media_management-derivedfrom) |
| `media_management` | `xmp.media_management.documentID` | documentID | No | [🔗](#xmp-media_management-documentid) |
| `media_management` | `xmp.media_management.instanceID` | instanceID | No | [🔗](#xmp-media_management-instanceid) |
| `media_management` | `xmp.media_management.originalDocumentID` | originalDocumentID | No | [🔗](#xmp-media_management-originaldocumentid) |
| `media_management` | `xmp.media_management.renditionClass` | renditionClass | No | [🔗](#xmp-media_management-renditionclass) |
| `media_management` | `xmp.media_management.renditionParams` | renditionParams | No | [🔗](#xmp-media_management-renditionparams) |
| `media_management` | `xmp.media_management.history` | history | No | [🔗](#xmp-media_management-history) |
| `media_management` | `xmp.media_management.ingredients` | ingredients | No | [🔗](#xmp-media_management-ingredients) |
| `media_management` | `xmp.media_management.pantry` | pantry | No | [🔗](#xmp-media_management-pantry) |
| `media_management` | `xmp.media_management.managedFrom` | managedFrom | No | [🔗](#xmp-media_management-managedfrom) |
| `media_management` | `xmp.media_management.manager` | manager | No | [🔗](#xmp-media_management-manager) |
| `media_management` | `xmp.media_management.manageTo` | manageTo | No | [🔗](#xmp-media_management-manageto) |
| `media_management` | `xmp.media_management.manageUI` | manageUI | No | [🔗](#xmp-media_management-manageui) |
| `media_management` | `xmp.media_management.managerVariant` | managerVariant | No | [🔗](#xmp-media_management-managervariant) |
| `media_management` | `xmp.media_management.versionID` | versionID | No | [🔗](#xmp-media_management-versionid) |
| `media_management` | `xmp.media_management.versions` | versions | No | [🔗](#xmp-media_management-versions) |

The technical details of each field may be found below:

<a id="xmp-media_management-derivedfrom"></a>
### The `xmpMM:DerivedFrom` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.media_management.derivedFrom` |
| ID | `xmpMM:DerivedFrom` |
| Name | derivedFrom |
| Label | – |
| Definiton | A reference to the original document from which this one is derived. It is a minimal reference; missing components can be assumed to be unchanged. For example, a new version might only need to specify the instance ID and version number of the previous version, or a rendition might only need to specify the instance ID and rendition class of the original. |
| Required? | No |
| Type | ResourceRef |

<a id="xmp-media_management-documentid"></a>
### The `xmpMM:DocumentID` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.media_management.documentID` |
| ID | `xmpMM:DocumentID` |
| Name | documentID |
| Label | – |
| Definiton | The common identifier for all versions and renditions of a resource. It should be based on a UUID; Created once for new resources. Different renditions are expected to have different values for xmpMM:DocumentID. |
| Required? | No |
| Type | GUID |

<a id="xmp-media_management-instanceid"></a>
### The `xmpMM:InstanceID` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.media_management.instanceID` |
| ID | `xmpMM:InstanceID` |
| Name | instanceID |
| Label | – |
| Definiton | An identifier for a specific incarnation of a resource, updated each time a file is saved. It should be based on a UUID. |
| Required? | No |
| Type | GUID |

<a id="xmp-media_management-originaldocumentid"></a>
### The `xmpMM:OriginalDocumentID` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.media_management.originalDocumentID` |
| ID | `xmpMM:OriginalDocumentID` |
| Name | originalDocumentID |
| Label | – |
| Definiton | The common identifier for the original resource from which the current resource is derived. For example, if you save a resource to a different format, then save that one to another format, each save operation should generate a new xmpMM:DocumentID that uniquely identifies the resource in that format, but should retain the ID of the source file here. It links a resource to its original source. |
| Required? | No |
| Type | GUID |

<a id="xmp-media_management-renditionclass"></a>
### The `xmpMM:RenditionClass` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.media_management.renditionClass` |
| ID | `xmpMM:RenditionClass` |
| Name | renditionClass |
| Label | – |
| Definiton | The rendition class name for this resource. This property should be absent or set to default for a document version that is not a derived rendition. |
| Required? | No |
| Type | RenditionClass |

<a id="xmp-media_management-renditionparams"></a>
### The `xmpMM:RenditionParams` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.media_management.renditionParams` |
| ID | `xmpMM:RenditionParams` |
| Name | renditionParams |
| Label | – |
| Definiton | Can be used to provide additional rendition parameters that are too complex or verbose to encode in xmpMM: RenditionClass. |
| Required? | No |
| Type | Text |

<a id="xmp-media_management-history"></a>
### The `xmpMM:History` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.media_management.history` |
| ID | `xmpMM:History` |
| Name | history |
| Label | – |
| Definiton | An ordered array of high-level user actions that resulted in this resource. It is intended to give human readers a description of the steps taken to make the changes from the previous version to this one. The list should be at an abstract level; it is not intended to be an exhaustive keystroke or other detailed history. The description should be sufficient for metadata management, as well as for workflow enhancement. |
| Multiple? | Yes |
| Ordered? | Yes |
| Required? | No |
| Type | ResourceEvent |

<a id="xmp-media_management-ingredients"></a>
### The `xmpMM:Ingredients` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.media_management.ingredients` |
| ID | `xmpMM:Ingredients` |
| Name | ingredients |
| Label | – |
| Definiton | References to resources that were incorporated, by inclusion or reference, into this resource. |
| Multiple? | Yes |
| Ordered? | No |
| Required? | No |
| Type | ResourceRef |

<a id="xmp-media_management-pantry"></a>
### The `xmpMM:Pantry` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.media_management.pantry` |
| ID | `xmpMM:Pantry` |
| Name | pantry |
| Label | – |
| Definiton | Each array item has a structure value with a potentially unique set of fields, containing extracted XMP from a component. Each field is a property from the XMP of a contained resource component, with all substructure preserved. Each pantry entry shall contain an xmpMM:InstanceID. Only one copy of the pantry entry for any given xmpMM:InstanceID shall be retained in the pantry. Nested pantry items shall be removed from the individual pantry item and promoted to the top level of the pantry. |
| Multiple? | Yes |
| Ordered? | No |
| Required? | No |
| Type | Struct |

<a id="xmp-media_management-managedfrom"></a>
### The `xmpMM:ManagedFrom` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.media_management.managedFrom` |
| ID | `xmpMM:ManagedFrom` |
| Name | managedFrom |
| Label | – |
| Definiton | A reference to the document as it was prior to becoming managed. It is set when a managed document is introduced to an asset management system that does not currently own it. It may or may not include references to different management systems. |
| Required? | No |
| Type | ResourceRef |

<a id="xmp-media_management-manager"></a>
### The `xmpMM:Manager` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.media_management.manager` |
| ID | `xmpMM:Manager` |
| Name | manager |
| Label | – |
| Definiton | The name of the asset management system that manages this resource. Along with xmpMM: ManagerVariant, it tells applications which asset management system to contact concerning this document. |
| Required? | No |
| Type | AgentName |

<a id="xmp-media_management-manageto"></a>
### The `xmpMM:ManageTo` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.media_management.manageTo` |
| ID | `xmpMM:ManageTo` |
| Name | manageTo |
| Label | – |
| Definiton | A URI identifying the managed resource to the asset management system; the presence of this property is the formal indication that this resource is managed. The form and content of this URI is private to the asset management system. |
| Required? | No |
| Type | URI |

<a id="xmp-media_management-manageui"></a>
### The `xmpMM:ManageUI` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.media_management.manageUI` |
| ID | `xmpMM:ManageUI` |
| Name | manageUI |
| Label | – |
| Definiton | A URI that can be used to access information about the managed resource through a web browser. It might require a custom browser plug-in. |
| Required? | No |
| Type | URI |

<a id="xmp-media_management-managervariant"></a>
### The `xmpMM:ManagerVariant` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.media_management.managerVariant` |
| ID | `xmpMM:ManagerVariant` |
| Name | managerVariant |
| Label | – |
| Definiton | Specifies a particular variant of the asset management system. The format of this property is private to the specific asset management system. |
| Required? | No |
| Type | Text |

<a id="xmp-media_management-versionid"></a>
### The `xmpMM:VersionID` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.media_management.versionID` |
| ID | `xmpMM:VersionID` |
| Name | versionID |
| Label | – |
| Definiton | The document version identifier for this resource. Each version of a document gets a new identifier, usually simply by incrementing integers 1, 2, 3 . . . and so on. Media management systems can have other conventions or support branching which requires a more complex scheme. |
| Required? | No |
| Type | Text |

<a id="xmp-media_management-versions"></a>
### The `xmpMM:Versions` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.media_management.versions` |
| ID | `xmpMM:Versions` |
| Name | versions |
| Label | – |
| Definiton | The version history associated with this resource. Entry 1 is the oldest known version for this document, entry[last()] is the most recent version. Typically, a media management system would fill in the version information in the metadata on check-in. It is not guaranteed that a complete history of versions from the first to this one will be present in the xmpMM:Versions property. Interior version information can be compressed or eliminated and the version history can be truncated at some point. |
| Multiple? | Yes |
| Ordered? | Yes |
| Required? | No |
| Type | Version |


The XMP metadata model's `basic_job_ticket` namespace offers one field which is listed below along with a link to each field's technical information:

| Namespace  | Field Path | Field Name | Required? | Info |
|------------|------------|------------|:---------:|------|
| `basic_job_ticket` | `xmp.basic_job_ticket.jobRef` | jobRef | No | [🔗](#xmp-basic_job_ticket-jobref) |

The technical details of each field may be found below:

<a id="xmp-basic_job_ticket-jobref"></a>
### The `xmpBJ:JobRef` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.basic_job_ticket.jobRef` |
| ID | `xmpBJ:JobRef` |
| Name | jobRef |
| Label | – |
| Definiton | References an external job management file for a job process in which the document is being used. Use of job names is under user control. Typical use would be to identify all documents that are part of a particular job or contract. There are multiple values because there can be more than one job using a particular document at any time, and it can also be useful to keep historical information about what jobs a document was part of previously. |
| Multiple? | Yes |
| Ordered? | No |
| Required? | No |
| Type | Job |


The XMP metadata model's `paged_text` namespace offers five fields which are listed below along with a link to each field's technical information:

| Namespace  | Field Path | Field Name | Required? | Info |
|------------|------------|------------|:---------:|------|
| `paged_text` | `xmp.paged_text.colorants` | colorants | No | [🔗](#xmp-paged_text-colorants) |
| `paged_text` | `xmp.paged_text.fonts` | fonts | No | [🔗](#xmp-paged_text-fonts) |
| `paged_text` | `xmp.paged_text.maxPageSize` | maxPageSize | No | [🔗](#xmp-paged_text-maxpagesize) |
| `paged_text` | `xmp.paged_text.nPages` | nPages | No | [🔗](#xmp-paged_text-npages) |
| `paged_text` | `xmp.paged_text.plateNames` | plateNames | No | [🔗](#xmp-paged_text-platenames) |

The technical details of each field may be found below:

<a id="xmp-paged_text-colorants"></a>
### The `xmpTPg:Colorants` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.paged_text.colorants` |
| ID | `xmpTPg:Colorants` |
| Name | colorants |
| Label | – |
| Definiton | An ordered array of colorants (swatches) that are used in the document (including any in contained documents). |
| Multiple? | Yes |
| Ordered? | Yes |
| Required? | No |
| Type | Colorants |

<a id="xmp-paged_text-fonts"></a>
### The `xmpTPg:Fonts` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.paged_text.fonts` |
| ID | `xmpTPg:Fonts` |
| Name | fonts |
| Label | – |
| Definiton | An unordered array of fonts that are used in the document (including any in contained documents). |
| Multiple? | Yes |
| Ordered? | No |
| Required? | No |
| Type | Font |

<a id="xmp-paged_text-maxpagesize"></a>
### The `xmpTPg:MaxPageSize` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.paged_text.maxPageSize` |
| ID | `xmpTPg:MaxPageSize` |
| Name | maxPageSize |
| Label | – |
| Definiton | The size of the largest page in the document (including any in contained documents). |
| Required? | No |
| Type | Dimensions |

<a id="xmp-paged_text-npages"></a>
### The `xmpTPg:NPages` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.paged_text.nPages` |
| ID | `xmpTPg:NPages` |
| Name | nPages |
| Label | – |
| Definiton | The number of pages in the document (including any in contained documents). |
| Required? | No |
| Type | Integer |

<a id="xmp-paged_text-platenames"></a>
### The `xmpTPg:PlateNames` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.paged_text.plateNames` |
| ID | `xmpTPg:PlateNames` |
| Name | plateNames |
| Label | – |
| Definiton | An ordered array of plate names that are needed to print the document (including any in contained documents). |
| Multiple? | Yes |
| Ordered? | Yes |
| Required? | No |
| Type | Text |


The XMP metadata model's `dynamic_media` namespace offers 71 fields which are listed below along with a link to each field's technical information:

| Namespace  | Field Path | Field Name | Required? | Info |
|------------|------------|------------|:---------:|------|
| `dynamic_media` | `xmp.dynamic_media.absPeakAudioFilePath` | absPeakAudioFilePath | No | [🔗](#xmp-dynamic_media-abspeakaudiofilepath) |
| `dynamic_media` | `xmp.dynamic_media.album` | album | No | [🔗](#xmp-dynamic_media-album) |
| `dynamic_media` | `xmp.dynamic_media.altTapeName` | altTapeName | No | [🔗](#xmp-dynamic_media-alttapename) |
| `dynamic_media` | `xmp.dynamic_media.altTimecode` | altTimecode | No | [🔗](#xmp-dynamic_media-alttimecode) |
| `dynamic_media` | `xmp.dynamic_media.artist` | artist | No | [🔗](#xmp-dynamic_media-artist) |
| `dynamic_media` | `xmp.dynamic_media.audioChannelType` | audioChannelType | No | [🔗](#xmp-dynamic_media-audiochanneltype) |
| `dynamic_media` | `xmp.dynamic_media.audioCompressor` | audioCompressor | No | [🔗](#xmp-dynamic_media-audiocompressor) |
| `dynamic_media` | `xmp.dynamic_media.audioSampleRate` | audioSampleRate | No | [🔗](#xmp-dynamic_media-audiosamplerate) |
| `dynamic_media` | `xmp.dynamic_media.audioSampleType` | audioSampleType | No | [🔗](#xmp-dynamic_media-audiosampletype) |
| `dynamic_media` | `xmp.dynamic_media.beatSpliceParams` | beatSpliceParams | No | [🔗](#xmp-dynamic_media-beatspliceparams) |
| `dynamic_media` | `xmp.dynamic_media.cameraAngle` | cameraAngle | No | [🔗](#xmp-dynamic_media-cameraangle) |
| `dynamic_media` | `xmp.dynamic_media.cameraLabel` | cameraLabel | No | [🔗](#xmp-dynamic_media-cameralabel) |
| `dynamic_media` | `xmp.dynamic_media.cameraModel` | cameraModel | No | [🔗](#xmp-dynamic_media-cameramodel) |
| `dynamic_media` | `xmp.dynamic_media.cameraMove` | cameraMove | No | [🔗](#xmp-dynamic_media-cameramove) |
| `dynamic_media` | `xmp.dynamic_media.client` | client | No | [🔗](#xmp-dynamic_media-client) |
| `dynamic_media` | `xmp.dynamic_media.comment` | comment | No | [🔗](#xmp-dynamic_media-comment) |
| `dynamic_media` | `xmp.dynamic_media.composer` | composer | No | [🔗](#xmp-dynamic_media-composer) |
| `dynamic_media` | `xmp.dynamic_media.contributedMedia` | contributedMedia | No | [🔗](#xmp-dynamic_media-contributedmedia) |
| `dynamic_media` | `xmp.dynamic_media.director` | director | No | [🔗](#xmp-dynamic_media-director) |
| `dynamic_media` | `xmp.dynamic_media.directorPhotography` | directorPhotography | No | [🔗](#xmp-dynamic_media-directorphotography) |
| `dynamic_media` | `xmp.dynamic_media.duration` | duration | No | [🔗](#xmp-dynamic_media-duration) |
| `dynamic_media` | `xmp.dynamic_media.engineer` | engineer | No | [🔗](#xmp-dynamic_media-engineer) |
| `dynamic_media` | `xmp.dynamic_media.fileDataRate` | fileDataRate | No | [🔗](#xmp-dynamic_media-filedatarate) |
| `dynamic_media` | `xmp.dynamic_media.genre` | genre | No | [🔗](#xmp-dynamic_media-genre) |
| `dynamic_media` | `xmp.dynamic_media.good` | good | No | [🔗](#xmp-dynamic_media-good) |
| `dynamic_media` | `xmp.dynamic_media.instrument` | instrument | No | [🔗](#xmp-dynamic_media-instrument) |
| `dynamic_media` | `xmp.dynamic_media.introTime` | introTime | No | [🔗](#xmp-dynamic_media-introtime) |
| `dynamic_media` | `xmp.dynamic_media.key` | key | No | [🔗](#xmp-dynamic_media-key) |
| `dynamic_media` | `xmp.dynamic_media.logComment` | logComment | No | [🔗](#xmp-dynamic_media-logcomment) |
| `dynamic_media` | `xmp.dynamic_media.loop` | loop | No | [🔗](#xmp-dynamic_media-loop) |
| `dynamic_media` | `xmp.dynamic_media.numberOfBeats` | numberOfBeats | No | [🔗](#xmp-dynamic_media-numberofbeats) |
| `dynamic_media` | `xmp.dynamic_media.markers` | markers | No | [🔗](#xmp-dynamic_media-markers) |
| `dynamic_media` | `xmp.dynamic_media.outCue` | outCue | No | [🔗](#xmp-dynamic_media-outcue) |
| `dynamic_media` | `xmp.dynamic_media.projectName` | projectName | No | [🔗](#xmp-dynamic_media-projectname) |
| `dynamic_media` | `xmp.dynamic_media.projectRef` | projectRef | No | [🔗](#xmp-dynamic_media-projectref) |
| `dynamic_media` | `xmp.dynamic_media.pullDown` | pullDown | No | [🔗](#xmp-dynamic_media-pulldown) |
| `dynamic_media` | `xmp.dynamic_media.relativePeakAudioFilePath` | relativePeakAudioFilePath | No | [🔗](#xmp-dynamic_media-relativepeakaudiofilepath) |
| `dynamic_media` | `xmp.dynamic_media.relativeTimestamp` | relativeTimestamp | No | [🔗](#xmp-dynamic_media-relativetimestamp) |
| `dynamic_media` | `xmp.dynamic_media.releaseDate` | releaseDate | No | [🔗](#xmp-dynamic_media-releasedate) |
| `dynamic_media` | `xmp.dynamic_media.resampleParams` | resampleParams | No | [🔗](#xmp-dynamic_media-resampleparams) |
| `dynamic_media` | `xmp.dynamic_media.scaleType` | scaleType | No | [🔗](#xmp-dynamic_media-scaletype) |
| `dynamic_media` | `xmp.dynamic_media.scene` | scene | No | [🔗](#xmp-dynamic_media-scene) |
| `dynamic_media` | `xmp.dynamic_media.shotDate` | shotDate | No | [🔗](#xmp-dynamic_media-shotdate) |
| `dynamic_media` | `xmp.dynamic_media.shotDay` | shotDay | No | [🔗](#xmp-dynamic_media-shotday) |
| `dynamic_media` | `xmp.dynamic_media.shotLocation` | shotLocation | No | [🔗](#xmp-dynamic_media-shotlocation) |
| `dynamic_media` | `xmp.dynamic_media.shotName` | shotName | No | [🔗](#xmp-dynamic_media-shotname) |
| `dynamic_media` | `xmp.dynamic_media.shotNumber` | shotNumber | No | [🔗](#xmp-dynamic_media-shotnumber) |
| `dynamic_media` | `xmp.dynamic_media.shotSize` | shotSize | No | [🔗](#xmp-dynamic_media-shotsize) |
| `dynamic_media` | `xmp.dynamic_media.speakerPlacement` | speakerPlacement | No | [🔗](#xmp-dynamic_media-speakerplacement) |
| `dynamic_media` | `xmp.dynamic_media.startTimecode` | startTimecode | No | [🔗](#xmp-dynamic_media-starttimecode) |
| `dynamic_media` | `xmp.dynamic_media.stretchMode` | stretchMode | No | [🔗](#xmp-dynamic_media-stretchmode) |
| `dynamic_media` | `xmp.dynamic_media.takeNumber` | takeNumber | No | [🔗](#xmp-dynamic_media-takenumber) |
| `dynamic_media` | `xmp.dynamic_media.tapeName` | tapeName | No | [🔗](#xmp-dynamic_media-tapename) |
| `dynamic_media` | `xmp.dynamic_media.tempo` | tempo | No | [🔗](#xmp-dynamic_media-tempo) |
| `dynamic_media` | `xmp.dynamic_media.timeScaleParams` | timeScaleParams | No | [🔗](#xmp-dynamic_media-timescaleparams) |
| `dynamic_media` | `xmp.dynamic_media.timeSignature` | timeSignature | No | [🔗](#xmp-dynamic_media-timesignature) |
| `dynamic_media` | `xmp.dynamic_media.trackNumber` | trackNumber | No | [🔗](#xmp-dynamic_media-tracknumber) |
| `dynamic_media` | `xmp.dynamic_media.tracks` | tracks | No | [🔗](#xmp-dynamic_media-tracks) |
| `dynamic_media` | `xmp.dynamic_media.videoAlphaMode` | videoAlphaMode | No | [🔗](#xmp-dynamic_media-videoalphamode) |
| `dynamic_media` | `xmp.dynamic_media.videoAlphaPremultipleColor` | videoAlphaPremultipleColor | No | [🔗](#xmp-dynamic_media-videoalphapremultiplecolor) |
| `dynamic_media` | `xmp.dynamic_media.videoAlphaUnityIsTransparent` | videoAlphaUnityIsTransparent | No | [🔗](#xmp-dynamic_media-videoalphaunityistransparent) |
| `dynamic_media` | `xmp.dynamic_media.videoColorSpace` | videoColorSpace | No | [🔗](#xmp-dynamic_media-videocolorspace) |
| `dynamic_media` | `xmp.dynamic_media.videoCompressor` | videoCompressor | No | [🔗](#xmp-dynamic_media-videocompressor) |
| `dynamic_media` | `xmp.dynamic_media.videoFieldOrder` | videoFieldOrder | No | [🔗](#xmp-dynamic_media-videofieldorder) |
| `dynamic_media` | `xmp.dynamic_media.videoFrameRate` | videoFrameRate | No | [🔗](#xmp-dynamic_media-videoframerate) |
| `dynamic_media` | `xmp.dynamic_media.videoFrameSize` | videoFrameSize | No | [🔗](#xmp-dynamic_media-videoframesize) |
| `dynamic_media` | `xmp.dynamic_media.videoPixelAspectRatio` | videoPixelAspectRatio | No | [🔗](#xmp-dynamic_media-videopixelaspectratio) |
| `dynamic_media` | `xmp.dynamic_media.videoPixelDepth` | videoPixelDepth | No | [🔗](#xmp-dynamic_media-videopixeldepth) |
| `dynamic_media` | `xmp.dynamic_media.partOfCompilation` | partOfCompilation | No | [🔗](#xmp-dynamic_media-partofcompilation) |
| `dynamic_media` | `xmp.dynamic_media.lyrics` | lyrics | No | [🔗](#xmp-dynamic_media-lyrics) |
| `dynamic_media` | `xmp.dynamic_media.discNumber` | discNumber | No | [🔗](#xmp-dynamic_media-discnumber) |

The technical details of each field may be found below:

<a id="xmp-dynamic_media-abspeakaudiofilepath"></a>
### The `xmpDM:absPeakAudioFilePath` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.absPeakAudioFilePath` |
| ID | `xmpDM:absPeakAudioFilePath` |
| Name | absPeakAudioFilePath |
| Label | – |
| Definiton | The absolute path to the file’s peak audio file. If empty, no peak file exists. |
| Required? | No |
| Type | URI |

<a id="xmp-dynamic_media-album"></a>
### The `xmpDM:album` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.album` |
| ID | `xmpDM:album` |
| Name | album |
| Label | – |
| Definiton | The name of the album. |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-alttapename"></a>
### The `xmpDM:altTapeName` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.altTapeName` |
| ID | `xmpDM:altTapeName` |
| Name | altTapeName |
| Label | – |
| Definiton | An alternative tape name, set via the project window or timecode dialog in Premiere. If an alternative name has been set and has not been reverted, that name is displayed. |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-alttimecode"></a>
### The `xmpDM:altTimecode` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.altTimecode` |
| ID | `xmpDM:altTimecode` |
| Name | altTimecode |
| Label | – |
| Definiton | A timecode set by the user. When specified, it is used instead of the startTimecode. |
| Required? | No |
| Type | Timecode |

<a id="xmp-dynamic_media-artist"></a>
### The `xmpDM:artist` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.artist` |
| ID | `xmpDM:artist` |
| Name | artist |
| Label | – |
| Definiton | The name of the artist or artists. |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-audiochanneltype"></a>
### The `xmpDM:audioChannelType` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.audioChannelType` |
| ID | `xmpDM:audioChannelType` |
| Name | audioChannelType |
| Label | – |
| Definiton | The audio channel type. One of: Mono, Stereo, 5.1, 7.1, 16 Channel, Other. |
| Options | Mono; Stereo; 5.1; 7.1; 16 Channel; Other |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-audiocompressor"></a>
### The `xmpDM:audioCompressor` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.audioCompressor` |
| ID | `xmpDM:audioCompressor` |
| Name | audioCompressor |
| Label | – |
| Definiton | The audio compression used. For example, MP3. |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-audiosamplerate"></a>
### The `xmpDM:audioSampleRate` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.audioSampleRate` |
| ID | `xmpDM:audioSampleRate` |
| Name | audioSampleRate |
| Label | – |
| Definiton | The audio sample rate. Can be any value, but commonly 32000, 44100, or 48000. |
| Required? | No |
| Type | Integer |

<a id="xmp-dynamic_media-audiosampletype"></a>
### The `xmpDM:audioSampleType` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.audioSampleType` |
| ID | `xmpDM:audioSampleType` |
| Name | audioSampleType |
| Label | – |
| Definiton | The audio sample type. One of: 8Int, 16Int, 24Int, 32Int, 32Float, Compressed, Packed,Other. |
| Options | 8Int; 16Int; 24Int; 32Int; 32Float; Compressed; Packed; Other |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-beatspliceparams"></a>
### The `xmpDM:beatSpliceParams` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.beatSpliceParams` |
| ID | `xmpDM:beatSpliceParams` |
| Name | beatSpliceParams |
| Label | – |
| Definiton | Additional parameters for Beat Splice stretch mode. |
| Required? | No |
| Type | BeatSpliceStretch |

<a id="xmp-dynamic_media-cameraangle"></a>
### The `xmpDM:cameraAngle` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.cameraAngle` |
| ID | `xmpDM:cameraAngle` |
| Name | cameraAngle |
| Label | – |
| Closed? | No |
| Definiton | The orientation of the camera to the subject in a static shot, from a fixed set of industry standard terminology. Predefined values include: Low Angle, Eye Level, High Angle, Overhead Shot, Birds Eye Shot, Dutch Angle, POV, Over the Shoulder, Reaction Shot. |
| Options | Low Angle; Eye Level; High Angle; Overhead Shot; Birds Eye Shot; Dutch Angle; POV; Over the Shoulder; Reaction Shot |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-cameralabel"></a>
### The `xmpDM:cameraLabel` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.cameraLabel` |
| ID | `xmpDM:cameraLabel` |
| Name | cameraLabel |
| Label | – |
| Definiton | A description of the camera used for a shoot. Can be any string, but is usually simply a number, for example '1', '2', or more explicitly 'Camera 1'. |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-cameramodel"></a>
### The `xmpDM:cameraModel` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.cameraModel` |
| ID | `xmpDM:cameraModel` |
| Name | cameraModel |
| Label | – |
| Definiton | The make and model of the camera used for a shoot. |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-cameramove"></a>
### The `xmpDM:cameraMove` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.cameraMove` |
| ID | `xmpDM:cameraMove` |
| Name | cameraMove |
| Label | – |
| Closed? | No |
| Definiton | The movement of the camera during the shot, from a fixed set of industry standard terminology. Predefined values include: Aerial, Boom Up, Boom Down, Crane Up, Crane Down, Dolly In, Dolly Out, Pan Left, Pan Right, Pedestal Up, Pedestal Down, Tilt Up, Tilt Down, Tracking, Truck Left, Truck Right, Zoom In, Zoom Out. |
| Options | Aerial; Boom Up; Boom Down; Crane Up; Crane Down; Dolly In; Dolly Out; Pan Left; Pan Right; Pedestal Up; Pedestal Down; Tilt Up; Tilt Down; Tracking; Truck Left; Truck Right; Zoom In; Zoom Out |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-client"></a>
### The `xmpDM:client` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.client` |
| ID | `xmpDM:client` |
| Name | client |
| Label | – |
| Definiton | The client for the job of which this shot or take is a part. |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-comment"></a>
### The `xmpDM:comment` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.comment` |
| ID | `xmpDM:comment` |
| Name | comment |
| Label | – |
| Definiton | A user’s comments. |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-composer"></a>
### The `xmpDM:composer` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.composer` |
| ID | `xmpDM:composer` |
| Name | composer |
| Label | – |
| Definiton | The composer’s name. |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-contributedmedia"></a>
### The `xmpDM:contributedMedia` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.contributedMedia` |
| ID | `xmpDM:contributedMedia` |
| Name | contributedMedia |
| Label | – |
| Definiton | An unordered list of all media used to create this media. |
| Multiple? | Yes |
| Ordered? | No |
| Required? | No |
| Type | Media |

<a id="xmp-dynamic_media-director"></a>
### The `xmpDM:director` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.director` |
| ID | `xmpDM:director` |
| Name | director |
| Label | – |
| Definiton | The director of the scene. |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-directorphotography"></a>
### The `xmpDM:directorPhotography` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.directorPhotography` |
| ID | `xmpDM:directorPhotography` |
| Name | directorPhotography |
| Label | – |
| Definiton | The director of photography for the scene. |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-duration"></a>
### The `xmpDM:duration` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.duration` |
| ID | `xmpDM:duration` |
| Name | duration |
| Label | – |
| Definiton | The duration of the media file. |
| Required? | No |
| Type | Time |

<a id="xmp-dynamic_media-engineer"></a>
### The `xmpDM:engineer` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.engineer` |
| ID | `xmpDM:engineer` |
| Name | engineer |
| Label | – |
| Definiton | The engineer’s name. |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-filedatarate"></a>
### The `xmpDM:fileDataRate` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.fileDataRate` |
| ID | `xmpDM:fileDataRate` |
| Name | fileDataRate |
| Label | – |
| Definiton | The file data rate in megabytes per second. For example: '36/10' = 3.6 MB/sec. |
| Required? | No |
| Type | Rational |

<a id="xmp-dynamic_media-genre"></a>
### The `xmpDM:genre` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.genre` |
| ID | `xmpDM:genre` |
| Name | genre |
| Label | – |
| Definiton | The name of the genre. |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-good"></a>
### The `xmpDM:good` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.good` |
| ID | `xmpDM:good` |
| Name | good |
| Label | – |
| Definiton | A checkbox for tracking whether a shot is a keeper. |
| Required? | No |
| Type | Boolean |

<a id="xmp-dynamic_media-instrument"></a>
### The `xmpDM:instrument` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.instrument` |
| ID | `xmpDM:instrument` |
| Name | instrument |
| Label | – |
| Definiton | The musical instrument. |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-introtime"></a>
### The `xmpDM:introTime` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.introTime` |
| ID | `xmpDM:introTime` |
| Name | introTime |
| Label | – |
| Definiton | The duration of lead time for queuing music. |
| Required? | No |
| Type | Time |

<a id="xmp-dynamic_media-key"></a>
### The `xmpDM:key` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.key` |
| ID | `xmpDM:key` |
| Name | key |
| Label | – |
| Definiton | The audio’s musical key. One of: C, C#, D, D#, E, F, F#, G, G#, A, A#, B. |
| Options | C; C#; D; D#; E; F; F#; G; G#; A; A#; B |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-logcomment"></a>
### The `xmpDM:logComment` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.logComment` |
| ID | `xmpDM:logComment` |
| Name | logComment |
| Label | – |
| Definiton | User’s log comments. |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-loop"></a>
### The `xmpDM:loop` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.loop` |
| ID | `xmpDM:loop` |
| Name | loop |
| Label | – |
| Definiton | When true, the clip can be looped seamlessly. |
| Required? | No |
| Type | Boolean |

<a id="xmp-dynamic_media-numberofbeats"></a>
### The `xmpDM:numberOfBeats` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.numberOfBeats` |
| ID | `xmpDM:numberOfBeats` |
| Name | numberOfBeats |
| Label | – |
| Definiton | The total number of musical beats in a clip; for example, the beats-per-second times the duration in seconds. |
| Required? | No |
| Type | Real |

<a id="xmp-dynamic_media-markers"></a>
### The `xmpDM:markers` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.markers` |
| ID | `xmpDM:markers` |
| Name | markers |
| Label | – |
| Definiton | An ordered list of markers. See also xmpDM:Tracks. |
| Multiple? | Yes |
| Ordered? | Yes |
| Required? | No |
| Type | Marker |

<a id="xmp-dynamic_media-outcue"></a>
### The `xmpDM:outCue` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.outCue` |
| ID | `xmpDM:outCue` |
| Name | outCue |
| Label | – |
| Definiton | The time at which to fade out. |
| Required? | No |
| Type | Time |

<a id="xmp-dynamic_media-projectname"></a>
### The `xmpDM:projectName` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.projectName` |
| ID | `xmpDM:projectName` |
| Name | projectName |
| Label | – |
| Definiton | The name of the project of which this file is a part. |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-projectref"></a>
### The `xmpDM:projectRef` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.projectRef` |
| ID | `xmpDM:projectRef` |
| Name | projectRef |
| Label | – |
| Definiton | A reference to the project of which this file is a part. |
| Required? | No |
| Type | ProjectLink |

<a id="xmp-dynamic_media-pulldown"></a>
### The `xmpDM:pullDown` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.pullDown` |
| ID | `xmpDM:pullDown` |
| Name | pullDown |
| Label | – |
| Definiton | The sampling phase of film to be converted to video (pull-down). One of: WSSWW, SSWWW, SWWWS, WWWSS, WWSSW, WWWSW, WWSWW, WSWWW, SWWWW, WWWWS. |
| Options | WSSWW; SSWWW; SWWWS; WWWSS; WWSSW; WWWSW; WWSWW; WSWWW; SWWWW; WWWWS |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-relativepeakaudiofilepath"></a>
### The `xmpDM:relativePeakAudioFilePath` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.relativePeakAudioFilePath` |
| ID | `xmpDM:relativePeakAudioFilePath` |
| Name | relativePeakAudioFilePath |
| Label | – |
| Definiton | The relative path to the file’s peak audio file. If empty, no peak file exists. |
| Required? | No |
| Type | URI |

<a id="xmp-dynamic_media-relativetimestamp"></a>
### The `xmpDM:relativeTimestamp` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.relativeTimestamp` |
| ID | `xmpDM:relativeTimestamp` |
| Name | relativeTimestamp |
| Label | – |
| Definiton | The start time of the media inside the audio project. |
| Required? | No |
| Type | Time |

<a id="xmp-dynamic_media-releasedate"></a>
### The `xmpDM:releaseDate` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.releaseDate` |
| ID | `xmpDM:releaseDate` |
| Name | releaseDate |
| Label | – |
| Definiton | The date the title was released. |
| Required? | No |
| Type | Date |

<a id="xmp-dynamic_media-resampleparams"></a>
### The `xmpDM:resampleParams` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.resampleParams` |
| ID | `xmpDM:resampleParams` |
| Name | resampleParams |
| Label | – |
| Definiton | Additional parameters for Resample stretch mode. |
| Required? | No |
| Type | ResampleStretch |

<a id="xmp-dynamic_media-scaletype"></a>
### The `xmpDM:scaleType` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.scaleType` |
| ID | `xmpDM:scaleType` |
| Name | scaleType |
| Label | – |
| Definiton | The musical scale used in the music. One of: Major, Minor, Both, Neither. Neither is most often used for instruments with no associated scale, such as drums. |
| Options | Major; Minor; Both; Neither |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-scene"></a>
### The `xmpDM:scene` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.scene` |
| ID | `xmpDM:scene` |
| Name | scene |
| Label | – |
| Definiton | The name of the scene. |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-shotdate"></a>
### The `xmpDM:shotDate` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.shotDate` |
| ID | `xmpDM:shotDate` |
| Name | shotDate |
| Label | – |
| Definiton | The date and time when the video was shot. |
| Required? | No |
| Type | Date |

<a id="xmp-dynamic_media-shotday"></a>
### The `xmpDM:shotDay` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.shotDay` |
| ID | `xmpDM:shotDay` |
| Name | shotDay |
| Label | – |
| Definiton | The day in a multiday shoot. For example: Day 2, Friday. |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-shotlocation"></a>
### The `xmpDM:shotLocation` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.shotLocation` |
| ID | `xmpDM:shotLocation` |
| Name | shotLocation |
| Label | – |
| Definiton | The name of the location where the video was shot. For example: 'Oktoberfest, Munich Germany'. For more accurate positioning, use the EXIF GPS values. |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-shotname"></a>
### The `xmpDM:shotName` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.shotName` |
| ID | `xmpDM:shotName` |
| Name | shotName |
| Label | – |
| Definiton | The name of the shot or take. |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-shotnumber"></a>
### The `xmpDM:shotNumber` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.shotNumber` |
| ID | `xmpDM:shotNumber` |
| Name | shotNumber |
| Label | – |
| Definiton | The position of the shot in a script or production, relative to other shots. For example: 1, 2, 1a, 1b, 1.1, 1.2. |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-shotsize"></a>
### The `xmpDM:shotSize` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.shotSize` |
| ID | `xmpDM:shotSize` |
| Name | shotSize |
| Label | – |
| Definiton | The size or scale of the shot framing, from a fixed set of industry standard terminology. Predefined values include: ECU (extreme close-up), MCU (medium close-up), CU (close-up), MS (medium shot), WS (wide shot), MWS (medium wide shot), EWS (extreme wide shot). |
| Options | ECU; MCU; CU; MS; WS; MWS; EWS |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-speakerplacement"></a>
### The `xmpDM:speakerPlacement` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.speakerPlacement` |
| ID | `xmpDM:speakerPlacement` |
| Name | speakerPlacement |
| Label | – |
| Definiton | A description of the speaker angles from centre front in degrees. For example: “Left = -30, Right = 30, Centre = 0, LFE = 45, Left Surround = -110, Right Surround = 110”. |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-starttimecode"></a>
### The `xmpDM:startTimecode` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.startTimecode` |
| ID | `xmpDM:startTimecode` |
| Name | startTimecode |
| Label | – |
| Definiton | The timecode of the first frame of video in the file, as obtained from the device control. |
| Required? | No |
| Type | Timecode |

<a id="xmp-dynamic_media-stretchmode"></a>
### The `xmpDM:stretchMode` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.stretchMode` |
| ID | `xmpDM:stretchMode` |
| Name | stretchMode |
| Label | – |
| Definiton | The audio stretch mode. One of: Fixed length, Time-Scale, Resample, Beat Splice, Hybrid. |
| Options | Fixed length; Time-Scale; Resample; Beat Splice; Hybrid |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-takenumber"></a>
### The `xmpDM:takeNumber` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.takeNumber` |
| ID | `xmpDM:takeNumber` |
| Name | takeNumber |
| Label | – |
| Definiton | A numeric value indicating the absolute number of a take. |
| Required? | No |
| Type | Integer |

<a id="xmp-dynamic_media-tapename"></a>
### The `xmpDM:tapeName` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.tapeName` |
| ID | `xmpDM:tapeName` |
| Name | tapeName |
| Label | – |
| Definiton | The name of the tape from which the clip was captured, as set during the capture process. |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-tempo"></a>
### The `xmpDM:tempo` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.tempo` |
| ID | `xmpDM:tempo` |
| Name | tempo |
| Label | – |
| Definiton | The audio’s tempo. |
| Required? | No |
| Type | Real |

<a id="xmp-dynamic_media-timescaleparams"></a>
### The `xmpDM:timeScaleParams` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.timeScaleParams` |
| ID | `xmpDM:timeScaleParams` |
| Name | timeScaleParams |
| Label | – |
| Definiton | Additional parameters for Time-Scale stretch mode. |
| Required? | No |
| Type | TimeScaleStretch |

<a id="xmp-dynamic_media-timesignature"></a>
### The `xmpDM:timeSignature` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.timeSignature` |
| ID | `xmpDM:timeSignature` |
| Name | timeSignature |
| Label | – |
| Definiton | The time signature of the music. One of: 2/4, 3/4, 4/4, 5/4, 7/4, 6/8, 9/8, 12/8, other. |
| Options | 2/4; 3/4; 4/4; 5/4; 7/4; 6/8; 9/8; 12/8; other |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-tracknumber"></a>
### The `xmpDM:trackNumber` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.trackNumber` |
| ID | `xmpDM:trackNumber` |
| Name | trackNumber |
| Label | – |
| Definiton | A numeric value indicating the order of the audio file within its original recording. |
| Required? | No |
| Type | Integer |

<a id="xmp-dynamic_media-tracks"></a>
### The `xmpDM:Tracks` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.tracks` |
| ID | `xmpDM:Tracks` |
| Name | tracks |
| Label | – |
| Definiton | An unordered list of tracks. A track is a named set of markers, which can specify a frame rate for all markers in the set. See also xmpDM:markers. |
| Multiple? | Yes |
| Ordered? | No |
| Required? | No |
| Type | Track |

<a id="xmp-dynamic_media-videoalphamode"></a>
### The `xmpDM:videoAlphaMode` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.videoAlphaMode` |
| ID | `xmpDM:videoAlphaMode` |
| Name | videoAlphaMode |
| Label | – |
| Definiton | The alpha mode. One of: straight, pre-multiplied, or none. |
| Options | straight; pre-multiplied; none |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-videoalphapremultiplecolor"></a>
### The `xmpDM:videoAlphaPremultipleColor` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.videoAlphaPremultipleColor` |
| ID | `xmpDM:videoAlphaPremultipleColor` |
| Name | videoAlphaPremultipleColor |
| Label | – |
| Definiton | A colour in CMYK or RGB to be used as the premultiple colour when alpha mode is premultiplied. |
| Required? | No |
| Type | Colorants |

<a id="xmp-dynamic_media-videoalphaunityistransparent"></a>
### The `xmpDM:videoAlphaUnityIsTransparent` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.videoAlphaUnityIsTransparent` |
| ID | `xmpDM:videoAlphaUnityIsTransparent` |
| Name | videoAlphaUnityIsTransparent |
| Label | – |
| Definiton | When true, unity is clear, when false, it is opaque. |
| Required? | No |
| Type | Boolean |

<a id="xmp-dynamic_media-videocolorspace"></a>
### The `xmpDM:videoColorSpace` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.videoColorSpace` |
| ID | `xmpDM:videoColorSpace` |
| Name | videoColorSpace |
| Label | – |
| Definiton | The colour space. One of: sRGB (used by Photoshop), CCIR-601 (used for NTSC), CCIR-709 (used for HD). |
| Options | sRGB; CCIR-601; CCIR-709 |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-videocompressor"></a>
### The `xmpDM:videoCompressor` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.videoCompressor` |
| ID | `xmpDM:videoCompressor` |
| Name | videoCompressor |
| Label | – |
| Definiton | Video compression used. For example, jpeg. |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-videofieldorder"></a>
### The `xmpDM:videoFieldOrder` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.videoFieldOrder` |
| ID | `xmpDM:videoFieldOrder` |
| Name | videoFieldOrder |
| Label | – |
| Definiton | The field order for video. One of: Upper, Lower, Progressive. |
| Options | Upper; Lower; Progressive |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-videoframerate"></a>
### The `xmpDM:videoFrameRate` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.videoFrameRate` |
| ID | `xmpDM:videoFrameRate` |
| Name | videoFrameRate |
| Label | – |
| Closed? | No |
| Definiton | The video frame rate. Predefined values include: 24, NTSC, PAL. |
| Options | 24; NTSC; PAL |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-videoframesize"></a>
### The `xmpDM:videoFrameSize` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.videoFrameSize` |
| ID | `xmpDM:videoFrameSize` |
| Name | videoFrameSize |
| Label | – |
| Definiton | The frame size. For example: w:720, h: 480, unit:pixels. |
| Required? | No |
| Type | Dimensions |

<a id="xmp-dynamic_media-videopixelaspectratio"></a>
### The `xmpDM:videoPixelAspectRatio` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.videoPixelAspectRatio` |
| ID | `xmpDM:videoPixelAspectRatio` |
| Name | videoPixelAspectRatio |
| Label | – |
| Definiton | The aspect ratio, expressed as wd/ht. For example: “648/720” = 0.9. |
| Required? | No |
| Type | Rational |

<a id="xmp-dynamic_media-videopixeldepth"></a>
### The `xmpDM:videoPixelDepth` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.videoPixelDepth` |
| ID | `xmpDM:videoPixelDepth` |
| Name | videoPixelDepth |
| Label | – |
| Definiton | The size in bits of each colour component of a pixel. Standard Windows 32-bit pixels have 8 bits per component. One of: 8Int, 16Int, 24Int, 32Int, 32Float, Other. |
| Options | 8Int; 16Int; 24Int; 32Int; 32Float; Other |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-partofcompilation"></a>
### The `xmpDM:partOfCompilation` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.partOfCompilation` |
| ID | `xmpDM:partOfCompilation` |
| Name | partOfCompilation |
| Label | – |
| Definiton | Part of compilation. |
| Required? | No |
| Type | Boolean |

<a id="xmp-dynamic_media-lyrics"></a>
### The `xmpDM:lyrics` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.lyrics` |
| ID | `xmpDM:lyrics` |
| Name | lyrics |
| Label | – |
| Definiton | Lyrics text. No association with timecode. |
| Required? | No |
| Type | Text |

<a id="xmp-dynamic_media-discnumber"></a>
### The `xmpDM:discNumber` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dynamic_media.discNumber` |
| ID | `xmpDM:discNumber` |
| Name | discNumber |
| Label | – |
| Definiton | If in a multi-disc set, might contain total number of discs. For example: 2/3. |
| Required? | No |
| Type | Text |


The XMP metadata model's `rights_management` namespace offers five fields which are listed below along with a link to each field's technical information:

| Namespace  | Field Path | Field Name | Required? | Info |
|------------|------------|------------|:---------:|------|
| `rights_management` | `xmp.rights.Certificate` | Certificate | No | [🔗](#xmp-rights_management-certificate) |
| `rights_management` | `xmp.rights.Marked` | Marked | No | [🔗](#xmp-rights_management-marked) |
| `rights_management` | `xmp.rights.Owner` | Owner | No | [🔗](#xmp-rights_management-owner) |
| `rights_management` | `xmp.rights.UsageTerms` | UsageTerms | No | [🔗](#xmp-rights_management-usageterms) |
| `rights_management` | `xmp.rights.WebStatement` | WebStatement | No | [🔗](#xmp-rights_management-webstatement) |

The technical details of each field may be found below:

<a id="xmp-rights_management-certificate"></a>
### The `xmpRights:Certificate` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.rights.Certificate` |
| ID | `xmpRights:Certificate` |
| Name | Certificate |
| Label | – |
| Definiton | A web URL for a rights management certificate. NOTE: This is a normal (non-URI) simple value because of historical usage. |
| Pseudonym | exiftool: xmpRights:Certificate |
| Required? | No |
| Type | Text |

<a id="xmp-rights_management-marked"></a>
### The `xmpRights:Marked` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.rights.Marked` |
| ID | `xmpRights:Marked` |
| Name | Marked |
| Label | – |
| Definiton | When true, indicates that this is a rights-managed resource. When false, indicates that this is a public-domain resource. Omit if the state is unknown. |
| Nullable? | No |
| Pseudonym | exiftool: xmpRights:Marked |
| Required? | No |
| Type | Boolean |

<a id="xmp-rights_management-owner"></a>
### The `xmpRights:Owner` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.rights.Owner` |
| ID | `xmpRights:Owner` |
| Name | Owner |
| Label | – |
| Definiton | A list of legal owners of the resource. |
| Multiple? | Yes |
| Ordered? | No |
| Pseudonym | exiftool: xmpRights:Owner |
| Required? | No |
| Type | ProperName |

<a id="xmp-rights_management-usageterms"></a>
### The `xmpRights:UsageTerms` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.rights.UsageTerms` |
| ID | `xmpRights:UsageTerms` |
| Name | UsageTerms |
| Label | – |
| Combine? | Yes |
| Definiton | A collection of text instructions on how a resource can be legally used, given in a variety of languages. |
| Pseudonym | exiftool: xmpRights:UsageTerms |
| Required? | No |
| Type | LanguageAlternative |

<a id="xmp-rights_management-webstatement"></a>
### The `xmpRights:WebStatement` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.rights.WebStatement` |
| ID | `xmpRights:WebStatement` |
| Name | WebStatement |
| Label | – |
| Definiton | A Web URL for a statement of the ownership and usage rights for this resource. NOTE: This is a normal (non-URI) simple value because of historical usage. |
| Pseudonym | exiftool: xmpRights:WebStatement |
| Required? | No |
| Type | Text |


The XMP metadata model's `adobe_pdf` namespace offers four fields which are listed below along with a link to each field's technical information:

| Namespace  | Field Path | Field Name | Required? | Info |
|------------|------------|------------|:---------:|------|
| `adobe_pdf` | `xmp.adobe_pdf.keywords` | keywords | No | [🔗](#xmp-adobe_pdf-keywords) |
| `adobe_pdf` | `xmp.adobe_pdf.PDFVersion` | PDFVersion | No | [🔗](#xmp-adobe_pdf-pdfversion) |
| `adobe_pdf` | `xmp.adobe_pdf.producer` | producer | No | [🔗](#xmp-adobe_pdf-producer) |
| `adobe_pdf` | `xmp.adobe_pdf.trapped` | trapped | No | [🔗](#xmp-adobe_pdf-trapped) |

The technical details of each field may be found below:

<a id="xmp-adobe_pdf-keywords"></a>
### The `pdf:Keywords` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.adobe_pdf.keywords` |
| ID | `pdf:Keywords` |
| Name | keywords |
| Label | – |
| Definiton | Keywords. |
| Required? | No |
| Type | Text |

<a id="xmp-adobe_pdf-pdfversion"></a>
### The `pdf:PDFVersion` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.adobe_pdf.PDFVersion` |
| ID | `pdf:PDFVersion` |
| Name | PDFVersion |
| Label | – |
| Definiton | The PDF file version (for example: 1.0, 1.3, and so on). |
| Required? | No |
| Type | Text |

<a id="xmp-adobe_pdf-producer"></a>
### The `pdf:Producer` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.adobe_pdf.producer` |
| ID | `pdf:Producer` |
| Name | producer |
| Label | – |
| Definiton | The name of the tool that created the PDF document. |
| Required? | No |
| Type | AgentName |

<a id="xmp-adobe_pdf-trapped"></a>
### The `pdf:Trapped` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.adobe_pdf.trapped` |
| ID | `pdf:Trapped` |
| Name | trapped |
| Label | – |
| Definiton | True when the document has been trapped. |
| Required? | No |
| Type | Boolean |


The XMP metadata model's `photoshop` namespace offers nineteen fields which are listed below along with a link to each field's technical information:

| Namespace  | Field Path | Field Name | Required? | Info |
|------------|------------|------------|:---------:|------|
| `photoshop` | `xmp.photoshop.colorMode` | colorMode | No | [🔗](#xmp-photoshop-colormode) |
| `photoshop` | `xmp.photoshop.documentAncestors` | documentAncestors | No | [🔗](#xmp-photoshop-documentancestors) |
| `photoshop` | `xmp.photoshop.history` | history | No | [🔗](#xmp-photoshop-history) |
| `photoshop` | `xmp.photoshop.ICCProfile` | ICCProfile | No | [🔗](#xmp-photoshop-iccprofile) |
| `photoshop` | `xmp.photoshop.textLayers` | textLayers | No | [🔗](#xmp-photoshop-textlayers) |
| `photoshop` | `xmp.photoshop.authorsPosition` | authorsPosition | No | [🔗](#xmp-photoshop-authorsposition) |
| `photoshop` | `xmp.photoshop.captionWriter` | captionWriter | No | [🔗](#xmp-photoshop-captionwriter) |
| `photoshop` | `xmp.photoshop.category` | category | No | [🔗](#xmp-photoshop-category) |
| `photoshop` | `xmp.photoshop.city` | city | No | [🔗](#xmp-photoshop-city) |
| `photoshop` | `xmp.photoshop.country` | country | No | [🔗](#xmp-photoshop-country) |
| `photoshop` | `xmp.photoshop.credit` | credit | No | [🔗](#xmp-photoshop-credit) |
| `photoshop` | `xmp.photoshop.dateCreated` | dateCreated | No | [🔗](#xmp-photoshop-datecreated) |
| `photoshop` | `xmp.photoshop.headline` | headline | No | [🔗](#xmp-photoshop-headline) |
| `photoshop` | `xmp.photoshop.instructions` | instructions | No | [🔗](#xmp-photoshop-instructions) |
| `photoshop` | `xmp.photoshop.source` | source | No | [🔗](#xmp-photoshop-source) |
| `photoshop` | `xmp.photoshop.state` | state | No | [🔗](#xmp-photoshop-state) |
| `photoshop` | `xmp.photoshop.supplementalCategories` | supplementalCategories | No | [🔗](#xmp-photoshop-supplementalcategories) |
| `photoshop` | `xmp.photoshop.transmissionReference` | transmissionReference | No | [🔗](#xmp-photoshop-transmissionreference) |
| `photoshop` | `xmp.photoshop.urgency` | urgency | No | [🔗](#xmp-photoshop-urgency) |

The technical details of each field may be found below:

<a id="xmp-photoshop-colormode"></a>
### The `photoshop:ColorMode` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.photoshop.colorMode` |
| ID | `photoshop:ColorMode` |
| Name | colorMode |
| Label | – |
| Definiton | The colour mode. One of: 0 = Bitmap , 1 = Gray scale, 2 = Indexed colour, 3 = RGB colour, 4 = CMYK colour, 7 = Multi-channel, 8 = Duotone, 9 = LAB colour. |
| Options | 0; 1; 2; 3; 4; 7; 8; 9 |
| Required? | No |
| Type | Integer |

<a id="xmp-photoshop-documentancestors"></a>
### The `photoshop:DocumentAncestors` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.photoshop.documentAncestors` |
| ID | `photoshop:DocumentAncestors` |
| Name | documentAncestors |
| Label | – |
| Definiton | If the source document for a copy-and-paste or place operation has a document ID, that ID is added to this list in the destination document's XMP. |
| Multiple? | Yes |
| Ordered? | No |
| Required? | No |
| Type | Ancestor |

<a id="xmp-photoshop-history"></a>
### The `photoshop:History` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.photoshop.history` |
| ID | `photoshop:History` |
| Name | history |
| Label | – |
| Definiton | The history that appears in the FileInfo panel, if activated in the application preferences. |
| Required? | No |
| Type | Text |

<a id="xmp-photoshop-iccprofile"></a>
### The `photoshop:ICCProfile` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.photoshop.ICCProfile` |
| ID | `photoshop:ICCProfile` |
| Name | ICCProfile |
| Label | – |
| Definiton | The colour profile, such as AppleRGB, AdobeRGB1998. |
| Required? | No |
| Type | Text |

<a id="xmp-photoshop-textlayers"></a>
### The `photoshop:TextLayers` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.photoshop.textLayers` |
| ID | `photoshop:TextLayers` |
| Name | textLayers |
| Label | – |
| Definiton | If a document has text layers, this property caches the text for each layer. |
| Multiple? | Yes |
| Ordered? | Yes |
| Required? | No |
| Type | Layer |

<a id="xmp-photoshop-authorsposition"></a>
### The `photoshop:AuthorsPosition` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.photoshop.authorsPosition` |
| ID | `photoshop:AuthorsPosition` |
| Name | authorsPosition |
| Label | – |
| Definiton | By-line title. |
| Required? | No |
| Type | Text |

<a id="xmp-photoshop-captionwriter"></a>
### The `photoshop:CaptionWriter` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.photoshop.captionWriter` |
| ID | `photoshop:CaptionWriter` |
| Name | captionWriter |
| Label | – |
| Definiton | Writer/editor. |
| Required? | No |
| Type | ProperName |

<a id="xmp-photoshop-category"></a>
### The `photoshop:Category` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.photoshop.category` |
| ID | `photoshop:Category` |
| Name | category |
| Label | – |
| Count/Length | 3 |
| Definiton | Category. Limited to 3 7-bit ASCII characters. |
| Encoding | ASCII |
| Required? | No |
| Type | Text |

<a id="xmp-photoshop-city"></a>
### The `photoshop:City` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.photoshop.city` |
| ID | `photoshop:City` |
| Name | city |
| Label | – |
| Definiton | City. |
| Required? | No |
| Type | Text |

<a id="xmp-photoshop-country"></a>
### The `photoshop:Country` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.photoshop.country` |
| ID | `photoshop:Country` |
| Name | country |
| Label | – |
| Definiton | Country/primary location. |
| Required? | No |
| Type | Text |

<a id="xmp-photoshop-credit"></a>
### The `photoshop:Credit` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.photoshop.credit` |
| ID | `photoshop:Credit` |
| Name | credit |
| Label | – |
| Definiton | Credit. |
| Pseudonym | exiftool: photoshop:Credit |
| Required? | No |
| Type | Text |

<a id="xmp-photoshop-datecreated"></a>
### The `photoshop:DateCreated` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.photoshop.dateCreated` |
| ID | `photoshop:DateCreated` |
| Name | dateCreated |
| Label | – |
| Definiton | The date the intellectual content of the document was created, rather than the creation date of the physical representation. |
| Required? | No |
| Type | Date |

<a id="xmp-photoshop-headline"></a>
### The `photoshop:Headline` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.photoshop.headline` |
| ID | `photoshop:Headline` |
| Name | headline |
| Label | – |
| Definiton | Headline. |
| Required? | No |
| Type | Text |

<a id="xmp-photoshop-instructions"></a>
### The `photoshop:Instructions` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.photoshop.instructions` |
| ID | `photoshop:Instructions` |
| Name | instructions |
| Label | – |
| Definiton | Special instructions. |
| Required? | No |
| Type | Text |

<a id="xmp-photoshop-source"></a>
### The `photoshop:Source` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.photoshop.source` |
| ID | `photoshop:Source` |
| Name | source |
| Label | – |
| Definiton | Source. |
| Pseudonym | exiftool: photoshop:Source |
| Required? | No |
| Type | Text |

<a id="xmp-photoshop-state"></a>
### The `photoshop:State` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.photoshop.state` |
| ID | `photoshop:State` |
| Name | state |
| Label | – |
| Definiton | Province/state. |
| Required? | No |
| Type | Text |

<a id="xmp-photoshop-supplementalcategories"></a>
### The `photoshop:SupplementalCategories` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.photoshop.supplementalCategories` |
| ID | `photoshop:SupplementalCategories` |
| Name | supplementalCategories |
| Label | – |
| Definiton | Supplemental category. |
| Multiple? | Yes |
| Ordered? | No |
| Required? | No |
| Type | Text |

<a id="xmp-photoshop-transmissionreference"></a>
### The `photoshop:TransmissionReference` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.photoshop.transmissionReference` |
| ID | `photoshop:TransmissionReference` |
| Name | transmissionReference |
| Label | – |
| Definiton | Original transmission reference. |
| Required? | No |
| Type | Text |

<a id="xmp-photoshop-urgency"></a>
### The `photoshop:Urgency` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.photoshop.urgency` |
| ID | `photoshop:Urgency` |
| Name | urgency |
| Label | – |
| Definiton | Urgency. Valid range is 1-8. |
| Maximum Value | 8 |
| Minimum Value | 1 |
| Required? | No |
| Type | Integer |


The XMP metadata model's `camera_raw` namespace offers 41 fields which are listed below along with a link to each field's technical information:

| Namespace  | Field Path | Field Name | Required? | Info |
|------------|------------|------------|:---------:|------|
| `camera_raw` | `xmp.camera_raw.autoBrightness` | autoBrightness | No | [🔗](#xmp-camera_raw-autobrightness) |
| `camera_raw` | `xmp.camera_raw.autoContrast` | autoContrast | No | [🔗](#xmp-camera_raw-autocontrast) |
| `camera_raw` | `xmp.camera_raw.autoExposure` | autoExposure | No | [🔗](#xmp-camera_raw-autoexposure) |
| `camera_raw` | `xmp.camera_raw.autoShadows` | autoShadows | No | [🔗](#xmp-camera_raw-autoshadows) |
| `camera_raw` | `xmp.camera_raw.blueHue` | blueHue | No | [🔗](#xmp-camera_raw-bluehue) |
| `camera_raw` | `xmp.camera_raw.blueSaturation` | blueSaturation | No | [🔗](#xmp-camera_raw-bluesaturation) |
| `camera_raw` | `xmp.camera_raw.brightness` | brightness | No | [🔗](#xmp-camera_raw-brightness) |
| `camera_raw` | `xmp.camera_raw.cameraProfile` | cameraProfile | No | [🔗](#xmp-camera_raw-cameraprofile) |
| `camera_raw` | `xmp.camera_raw.chromaticAberrationB` | chromaticAberrationB | No | [🔗](#xmp-camera_raw-chromaticaberrationb) |
| `camera_raw` | `xmp.camera_raw.chromaticAberrationR` | chromaticAberrationR | No | [🔗](#xmp-camera_raw-chromaticaberrationr) |
| `camera_raw` | `xmp.camera_raw.colorNoiseReduction` | colorNoiseReduction | No | [🔗](#xmp-camera_raw-colornoisereduction) |
| `camera_raw` | `xmp.camera_raw.contrast` | contrast | No | [🔗](#xmp-camera_raw-contrast) |
| `camera_raw` | `xmp.camera_raw.cropTop` | cropTop | No | [🔗](#xmp-camera_raw-croptop) |
| `camera_raw` | `xmp.camera_raw.cropLeft` | cropLeft | No | [🔗](#xmp-camera_raw-cropleft) |
| `camera_raw` | `xmp.camera_raw.cropBottom` | cropBottom | No | [🔗](#xmp-camera_raw-cropbottom) |
| `camera_raw` | `xmp.camera_raw.cropRight` | cropRight | No | [🔗](#xmp-camera_raw-cropright) |
| `camera_raw` | `xmp.camera_raw.cropAngle` | cropAngle | No | [🔗](#xmp-camera_raw-cropangle) |
| `camera_raw` | `xmp.camera_raw.cropWidth` | cropWidth | No | [🔗](#xmp-camera_raw-cropwidth) |
| `camera_raw` | `xmp.camera_raw.cropHeight` | cropHeight | No | [🔗](#xmp-camera_raw-cropheight) |
| `camera_raw` | `xmp.camera_raw.cropUnits` | cropUnits | No | [🔗](#xmp-camera_raw-cropunits) |
| `camera_raw` | `xmp.camera_raw.exposure` | exposure | No | [🔗](#xmp-camera_raw-exposure) |
| `camera_raw` | `xmp.camera_raw.greenHue` | greenHue | No | [🔗](#xmp-camera_raw-greenhue) |
| `camera_raw` | `xmp.camera_raw.greenSaturation` | greenSaturation | No | [🔗](#xmp-camera_raw-greensaturation) |
| `camera_raw` | `xmp.camera_raw.hasCrop` | hasCrop | No | [🔗](#xmp-camera_raw-hascrop) |
| `camera_raw` | `xmp.camera_raw.hasSettings` | hasSettings | No | [🔗](#xmp-camera_raw-hassettings) |
| `camera_raw` | `xmp.camera_raw.luminanceSmoothing` | luminanceSmoothing | No | [🔗](#xmp-camera_raw-luminancesmoothing) |
| `camera_raw` | `xmp.camera_raw.rawFileName` | rawFileName | No | [🔗](#xmp-camera_raw-rawfilename) |
| `camera_raw` | `xmp.camera_raw.redHue` | redHue | No | [🔗](#xmp-camera_raw-redhue) |
| `camera_raw` | `xmp.camera_raw.redSaturation` | redSaturation | No | [🔗](#xmp-camera_raw-redsaturation) |
| `camera_raw` | `xmp.camera_raw.saturation` | saturation | No | [🔗](#xmp-camera_raw-saturation) |
| `camera_raw` | `xmp.camera_raw.shadows` | shadows | No | [🔗](#xmp-camera_raw-shadows) |
| `camera_raw` | `xmp.camera_raw.shadowTint` | shadowTint | No | [🔗](#xmp-camera_raw-shadowtint) |
| `camera_raw` | `xmp.camera_raw.sharpness` | sharpness | No | [🔗](#xmp-camera_raw-sharpness) |
| `camera_raw` | `xmp.camera_raw.temperature` | temperature | No | [🔗](#xmp-camera_raw-temperature) |
| `camera_raw` | `xmp.camera_raw.tint` | tint | No | [🔗](#xmp-camera_raw-tint) |
| `camera_raw` | `xmp.camera_raw.toneCurve` | toneCurve | No | [🔗](#xmp-camera_raw-tonecurve) |
| `camera_raw` | `xmp.camera_raw.toneCurveName` | toneCurveName | No | [🔗](#xmp-camera_raw-tonecurvename) |
| `camera_raw` | `xmp.camera_raw.version` | version | No | [🔗](#xmp-camera_raw-version) |
| `camera_raw` | `xmp.camera_raw.vignetteAmount` | vignetteAmount | No | [🔗](#xmp-camera_raw-vignetteamount) |
| `camera_raw` | `xmp.camera_raw.vignetteMidpoint` | vignetteMidpoint | No | [🔗](#xmp-camera_raw-vignettemidpoint) |
| `camera_raw` | `xmp.camera_raw.whiteBalance` | whiteBalance | No | [🔗](#xmp-camera_raw-whitebalance) |

The technical details of each field may be found below:

<a id="xmp-camera_raw-autobrightness"></a>
### The `crs:AutoBrightness` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.autoBrightness` |
| ID | `crs:AutoBrightness` |
| Name | autoBrightness |
| Label | – |
| Definiton | When true, brightness is automatically adjusted. |
| Required? | No |
| Type | Boolean |

<a id="xmp-camera_raw-autocontrast"></a>
### The `crs:AutoContrast` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.autoContrast` |
| ID | `crs:AutoContrast` |
| Name | autoContrast |
| Label | – |
| Definiton | When true, contrast is automatically adjusted. |
| Required? | No |
| Type | Boolean |

<a id="xmp-camera_raw-autoexposure"></a>
### The `crs:AutoExposure` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.autoExposure` |
| ID | `crs:AutoExposure` |
| Name | autoExposure |
| Label | – |
| Definiton | When true, exposure is automatically adjusted. |
| Required? | No |
| Type | Boolean |

<a id="xmp-camera_raw-autoshadows"></a>
### The `crs:AutoShadows` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.autoShadows` |
| ID | `crs:AutoShadows` |
| Name | autoShadows |
| Label | – |
| Definiton | When true, shadows are automatically adjusted. |
| Required? | No |
| Type | Boolean |

<a id="xmp-camera_raw-bluehue"></a>
### The `crs:BlueHue` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.blueHue` |
| ID | `crs:BlueHue` |
| Name | blueHue |
| Label | – |
| Definiton | Blue Hue setting. Range -100 to +100. |
| Maximum Value | 100 |
| Minimum Value | -100 |
| Required? | No |
| Type | Integer |

<a id="xmp-camera_raw-bluesaturation"></a>
### The `crs:BlueSaturation` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.blueSaturation` |
| ID | `crs:BlueSaturation` |
| Name | blueSaturation |
| Label | – |
| Definiton | Blue Saturation setting. Range -100 to +100. |
| Maximum Value | 100 |
| Minimum Value | -100 |
| Required? | No |
| Type | Integer |

<a id="xmp-camera_raw-brightness"></a>
### The `crs:Brightness` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.brightness` |
| ID | `crs:Brightness` |
| Name | brightness |
| Label | – |
| Definiton | Brightness setting. Range 0 to 150. |
| Maximum Value | 150 |
| Minimum Value | 0 |
| Required? | No |
| Type | Integer |

<a id="xmp-camera_raw-cameraprofile"></a>
### The `crs:CameraProfile` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.cameraProfile` |
| ID | `crs:CameraProfile` |
| Name | cameraProfile |
| Label | – |
| Definiton | Camera Profile setting. |
| Required? | No |
| Type | Text |

<a id="xmp-camera_raw-chromaticaberrationb"></a>
### The `crs:ChromaticAberrationB` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.chromaticAberrationB` |
| ID | `crs:ChromaticAberrationB` |
| Name | chromaticAberrationB |
| Label | – |
| Definiton | Chomatic Aberration, Fix Blue/Yellow Fringe setting. Range -100 to +100. |
| Maximum Value | 100 |
| Minimum Value | -100 |
| Required? | No |
| Type | Integer |

<a id="xmp-camera_raw-chromaticaberrationr"></a>
### The `crs:ChromaticAberrationR` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.chromaticAberrationR` |
| ID | `crs:ChromaticAberrationR` |
| Name | chromaticAberrationR |
| Label | – |
| Definiton | Chomatic Aberration, Fix Red/Cyan Fringe setting. Range -100 to +100. |
| Maximum Value | 100 |
| Minimum Value | -100 |
| Required? | No |
| Type | Integer |

<a id="xmp-camera_raw-colornoisereduction"></a>
### The `crs:ColorNoiseReduction` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.colorNoiseReduction` |
| ID | `crs:ColorNoiseReduction` |
| Name | colorNoiseReduction |
| Label | – |
| Definiton | Color Noise Reducton setting. Range 0 to 100. |
| Maximum Value | 100 |
| Minimum Value | 0 |
| Required? | No |
| Type | Integer |

<a id="xmp-camera_raw-contrast"></a>
### The `crs:Contrast` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.contrast` |
| ID | `crs:Contrast` |
| Name | contrast |
| Label | – |
| Definiton | Contrast setting. Range -50 to 100. |
| Maximum Value | 100 |
| Minimum Value | -50 |
| Required? | No |
| Type | Integer |

<a id="xmp-camera_raw-croptop"></a>
### The `crs:CropTop` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.cropTop` |
| ID | `crs:CropTop` |
| Name | cropTop |
| Label | – |
| Definiton | When Has Crop is true, top of crop rectangle. |
| Required? | No |
| Type | Real |

<a id="xmp-camera_raw-cropleft"></a>
### The `crs:CropLeft` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.cropLeft` |
| ID | `crs:CropLeft` |
| Name | cropLeft |
| Label | – |
| Definiton | When Has Crop is true, left of crop rectangle. |
| Required? | No |
| Type | Real |

<a id="xmp-camera_raw-cropbottom"></a>
### The `crs:CropBottom` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.cropBottom` |
| ID | `crs:CropBottom` |
| Name | cropBottom |
| Label | – |
| Definiton | When Has Crop is true, bottom of crop rectangle. |
| Required? | No |
| Type | Real |

<a id="xmp-camera_raw-cropright"></a>
### The `crs:CropRight` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.cropRight` |
| ID | `crs:CropRight` |
| Name | cropRight |
| Label | – |
| Definiton | When Has Crop is true, right of crop rectangle. |
| Required? | No |
| Type | Real |

<a id="xmp-camera_raw-cropangle"></a>
### The `crs:CropAngle` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.cropAngle` |
| ID | `crs:CropAngle` |
| Name | cropAngle |
| Label | – |
| Definiton | When Has Crop is true, angle of crop rectangle. |
| Required? | No |
| Type | Real |

<a id="xmp-camera_raw-cropwidth"></a>
### The `crs:CropWidth` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.cropWidth` |
| ID | `crs:CropWidth` |
| Name | cropWidth |
| Label | – |
| Definiton | Width of resulting cropped image in CropUnits units. |
| Required? | No |
| Type | Real |

<a id="xmp-camera_raw-cropheight"></a>
### The `crs:CropHeight` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.cropHeight` |
| ID | `crs:CropHeight` |
| Name | cropHeight |
| Label | – |
| Definiton | Height of resulting cropped image in CropUnits units. |
| Required? | No |
| Type | Real |

<a id="xmp-camera_raw-cropunits"></a>
### The `crs:CropUnits` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.cropUnits` |
| ID | `crs:CropUnits` |
| Name | cropUnits |
| Label | – |
| Definiton | Units for Crop Width and Crop Height. One of: 0=pixels 1=inches 2=cm. |
| Options | 0; 1; 2 |
| Required? | No |
| Type | Integer |

<a id="xmp-camera_raw-exposure"></a>
### The `crs:Exposure` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.exposure` |
| ID | `crs:Exposure` |
| Name | exposure |
| Label | – |
| Definiton | Exposure setting. Range -4.0 to +4.0. |
| Maximum Value | 4.0 |
| Minimum Value | -4.0 |
| Required? | No |
| Type | Real |

<a id="xmp-camera_raw-greenhue"></a>
### The `crs:GreenHue` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.greenHue` |
| ID | `crs:GreenHue` |
| Name | greenHue |
| Label | – |
| Definiton | Green Hue setting. Range -100 to +100. |
| Maximum Value | 100 |
| Minimum Value | -100 |
| Required? | No |
| Type | Integer |

<a id="xmp-camera_raw-greensaturation"></a>
### The `crs:GreenSaturation` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.greenSaturation` |
| ID | `crs:GreenSaturation` |
| Name | greenSaturation |
| Label | – |
| Definiton | Green Saturation setting. Range -100 to +100. |
| Maximum Value | 100 |
| Minimum Value | -100 |
| Required? | No |
| Type | Integer |

<a id="xmp-camera_raw-hascrop"></a>
### The `crs:HasCrop` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.hasCrop` |
| ID | `crs:HasCrop` |
| Name | hasCrop |
| Label | – |
| Definiton | When true, image has a cropping rectangle. |
| Required? | No |
| Type | Boolean |

<a id="xmp-camera_raw-hassettings"></a>
### The `crs:HasSettings` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.hasSettings` |
| ID | `crs:HasSettings` |
| Name | hasSettings |
| Label | – |
| Definiton | When true, non-default camera raw settings. |
| Required? | No |
| Type | Boolean |

<a id="xmp-camera_raw-luminancesmoothing"></a>
### The `crs:LuminanceSmoothing` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.luminanceSmoothing` |
| ID | `crs:LuminanceSmoothing` |
| Name | luminanceSmoothing |
| Label | – |
| Definiton | Luminance Smoothing setting. Range 0 to +100. |
| Maximum Value | 100 |
| Minimum Value | 0 |
| Required? | No |
| Type | Integer |

<a id="xmp-camera_raw-rawfilename"></a>
### The `crs:RawFileName` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.rawFileName` |
| ID | `crs:RawFileName` |
| Name | rawFileName |
| Label | – |
| Definiton | File name for raw file (not a complete path). |
| Required? | No |
| Type | Text |

<a id="xmp-camera_raw-redhue"></a>
### The `crs:RedHue` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.redHue` |
| ID | `crs:RedHue` |
| Name | redHue |
| Label | – |
| Definiton | Red Hue setting. Range -100 to +100. |
| Maximum Value | 100 |
| Minimum Value | -100 |
| Required? | No |
| Type | Integer |

<a id="xmp-camera_raw-redsaturation"></a>
### The `crs:RedSaturation` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.redSaturation` |
| ID | `crs:RedSaturation` |
| Name | redSaturation |
| Label | – |
| Definiton | Red Saturation setting. Range -100 to +100. |
| Maximum Value | 100 |
| Minimum Value | -100 |
| Required? | No |
| Type | Integer |

<a id="xmp-camera_raw-saturation"></a>
### The `crs:Saturation` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.saturation` |
| ID | `crs:Saturation` |
| Name | saturation |
| Label | – |
| Definiton | Saturation setting. Range -100 to +100. |
| Maximum Value | 100 |
| Minimum Value | -100 |
| Required? | No |
| Type | Integer |

<a id="xmp-camera_raw-shadows"></a>
### The `crs:Shadows` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.shadows` |
| ID | `crs:Shadows` |
| Name | shadows |
| Label | – |
| Definiton | Shadows setting. Range 0 to +100. |
| Maximum Value | 100 |
| Minimum Value | 0 |
| Required? | No |
| Type | Integer |

<a id="xmp-camera_raw-shadowtint"></a>
### The `crs:ShadowTint` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.shadowTint` |
| ID | `crs:ShadowTint` |
| Name | shadowTint |
| Label | – |
| Definiton | Shadow Tint setting. Range -100 to 100. |
| Maximum Value | 100 |
| Minimum Value | -100 |
| Required? | No |
| Type | Integer |

<a id="xmp-camera_raw-sharpness"></a>
### The `crs:Sharpness` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.sharpness` |
| ID | `crs:Sharpness` |
| Name | sharpness |
| Label | – |
| Definiton | Sharpness setting. Range 0 to 100. |
| Maximum Value | 100 |
| Minimum Value | 0 |
| Required? | No |
| Type | Integer |

<a id="xmp-camera_raw-temperature"></a>
### The `crs:Temperature` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.temperature` |
| ID | `crs:Temperature` |
| Name | temperature |
| Label | – |
| Definiton | Temperature setting. Range 2000 to 50000. |
| Maximum Value | 50000 |
| Minimum Value | 2000 |
| Required? | No |
| Type | Integer |

<a id="xmp-camera_raw-tint"></a>
### The `crs:Tint` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.tint` |
| ID | `crs:Tint` |
| Name | tint |
| Label | – |
| Definiton | Tint setting. Range -150 to 150. |
| Maximum Value | 150 |
| Minimum Value | -150 |
| Required? | No |
| Type | Integer |

<a id="xmp-camera_raw-tonecurve"></a>
### The `crs:ToneCurve` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.toneCurve` |
| ID | `crs:ToneCurve` |
| Name | toneCurve |
| Label | – |
| Definiton | Array of points (Integer, Integer) defining a tone curve. |
| Multiple? | Yes |
| Ordered? | Yes |
| Required? | No |
| Type | Integer |

<a id="xmp-camera_raw-tonecurvename"></a>
### The `crs:ToneCurveName` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.toneCurveName` |
| ID | `crs:ToneCurveName` |
| Name | toneCurveName |
| Label | – |
| Closed? | No |
| Definiton | The name of the Tone Curve described by ToneCurve. One of: Linear , Medium Contrast , Strong Contrast, Custom, or a user-defined preset name. |
| Options | Linear; Medium Contrast; Strong Contrast; Custom |
| Required? | No |
| Type | Text |

<a id="xmp-camera_raw-version"></a>
### The `crs:Version` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.version` |
| ID | `crs:Version` |
| Name | version |
| Label | – |
| Definiton | Version of Camera Raw plugin. |
| Required? | No |
| Type | Text |

<a id="xmp-camera_raw-vignetteamount"></a>
### The `crs:VignetteAmount` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.vignetteAmount` |
| ID | `crs:VignetteAmount` |
| Name | vignetteAmount |
| Label | – |
| Definiton | Vignetting Amount setting. Range -100 to 100. |
| Maximum Value | 100 |
| Minimum Value | -100 |
| Required? | No |
| Type | Integer |

<a id="xmp-camera_raw-vignettemidpoint"></a>
### The `crs:VignetteMidpoint` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.vignetteMidpoint` |
| ID | `crs:VignetteMidpoint` |
| Name | vignetteMidpoint |
| Label | – |
| Definiton | Vignetting Midpoint setting. Range 0 to 100. |
| Maximum Value | 100 |
| Minimum Value | 0 |
| Required? | No |
| Type | Integer |

<a id="xmp-camera_raw-whitebalance"></a>
### The `crs:WhiteBalance` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.camera_raw.whiteBalance` |
| ID | `crs:WhiteBalance` |
| Name | whiteBalance |
| Label | – |
| Definiton | White Balance setting. One of: As Shot, Auto, Daylight, Cloudy, Shade, Tungsten, Fluorescent, Flash, Custom. |
| Options | As Shot; Auto; Daylight; Cloudy; Shade; Tungsten; Fluorescent; Flash; Custom |
| Required? | No |
| Type | Text |


The XMP metadata model's `exif` namespace offers 77 fields which are listed below along with a link to each field's technical information:

| Namespace  | Field Path | Field Name | Required? | Info |
|------------|------------|------------|:---------:|------|
| `exif` | `xmp.exif.apertureValue` | apertureValue | No | [🔗](#xmp-exif-aperturevalue) |
| `exif` | `xmp.exif.brightnessValue` | brightnessValue | No | [🔗](#xmp-exif-brightnessvalue) |
| `exif` | `xmp.exif.CFAPattern` | CFAPattern | No | [🔗](#xmp-exif-cfapattern) |
| `exif` | `xmp.exif.colorSpace` | colorSpace | No | [🔗](#xmp-exif-colorspace) |
| `exif` | `xmp.exif.compressedBitsPerPixel` | compressedBitsPerPixel | No | [🔗](#xmp-exif-compressedbitsperpixel) |
| `exif` | `xmp.exif.contrast` | contrast | No | [🔗](#xmp-exif-contrast) |
| `exif` | `xmp.exif.customRendered` | customRendered | No | [🔗](#xmp-exif-customrendered) |
| `exif` | `xmp.exif.dateTimeDigitized` | dateTimeDigitized | No | [🔗](#xmp-exif-datetimedigitized) |
| `exif` | `xmp.exif.dateTimeOriginal` | dateTimeOriginal | No | [🔗](#xmp-exif-datetimeoriginal) |
| `exif` | `xmp.exif.deviceSettingDescription` | deviceSettingDescription | No | [🔗](#xmp-exif-devicesettingdescription) |
| `exif` | `xmp.exif.digitalZoomRatio` | digitalZoomRatio | No | [🔗](#xmp-exif-digitalzoomratio) |
| `exif` | `xmp.exif.exifVersion` | exifVersion | No | [🔗](#xmp-exif-exifversion) |
| `exif` | `xmp.exif.exposureBiasValue` | exposureBiasValue | No | [🔗](#xmp-exif-exposurebiasvalue) |
| `exif` | `xmp.exif.exposureIndex` | exposureIndex | No | [🔗](#xmp-exif-exposureindex) |
| `exif` | `xmp.exif.exposureMode` | exposureMode | No | [🔗](#xmp-exif-exposuremode) |
| `exif` | `xmp.exif.exposureProgram` | exposureProgram | No | [🔗](#xmp-exif-exposureprogram) |
| `exif` | `xmp.exif.exposureTime` | exposureTime | No | [🔗](#xmp-exif-exposuretime) |
| `exif` | `xmp.exif.fileSource` | fileSource | No | [🔗](#xmp-exif-filesource) |
| `exif` | `xmp.exif.flash` | flash | No | [🔗](#xmp-exif-flash) |
| `exif` | `xmp.exif.flashEnergy` | flashEnergy | No | [🔗](#xmp-exif-flashenergy) |
| `exif` | `xmp.exif.flashpixVersion` | flashpixVersion | No | [🔗](#xmp-exif-flashpixversion) |
| `exif` | `xmp.exif.FNumber` | FNumber | No | [🔗](#xmp-exif-fnumber) |
| `exif` | `xmp.exif.focalLength` | focalLength | No | [🔗](#xmp-exif-focallength) |
| `exif` | `xmp.exif.FocalLengthIn35mmFilm` | FocalLengthIn35mmFilm | No | [🔗](#xmp-exif-focallengthin35mmfilm) |
| `exif` | `xmp.exif.focalPlaneResolutionUnit` | focalPlaneResolutionUnit | No | [🔗](#xmp-exif-focalplaneresolutionunit) |
| `exif` | `xmp.exif.focalPlaneXResolution` | focalPlaneXResolution | No | [🔗](#xmp-exif-focalplanexresolution) |
| `exif` | `xmp.exif.focalPlaneYResolution` | focalPlaneYResolution | No | [🔗](#xmp-exif-focalplaneyresolution) |
| `exif` | `xmp.exif.gainControl` | gainControl | No | [🔗](#xmp-exif-gaincontrol) |
| `exif` | `xmp.exif.imageUniqueID` | imageUniqueID | No | [🔗](#xmp-exif-imageuniqueid) |
| `exif` | `xmp.exif.ISOSpeedRatings` | ISOSpeedRatings | No | [🔗](#xmp-exif-isospeedratings) |
| `exif` | `xmp.exif.lightSource` | lightSource | No | [🔗](#xmp-exif-lightsource) |
| `exif` | `xmp.exif.maxApertureValue` | maxApertureValue | No | [🔗](#xmp-exif-maxaperturevalue) |
| `exif` | `xmp.exif.meteringMode` | meteringMode | No | [🔗](#xmp-exif-meteringmode) |
| `exif` | `xmp.exif.OECF` | OECF | No | [🔗](#xmp-exif-oecf) |
| `exif` | `xmp.exif.pixelXDimension` | pixelXDimension | No | [🔗](#xmp-exif-pixelxdimension) |
| `exif` | `xmp.exif.pixelYDimension` | pixelYDimension | No | [🔗](#xmp-exif-pixelydimension) |
| `exif` | `xmp.exif.relatedSoundFile` | relatedSoundFile | No | [🔗](#xmp-exif-relatedsoundfile) |
| `exif` | `xmp.exif.saturation` | saturation | No | [🔗](#xmp-exif-saturation) |
| `exif` | `xmp.exif.sceneCaptureType` | sceneCaptureType | No | [🔗](#xmp-exif-scenecapturetype) |
| `exif` | `xmp.exif.sceneType` | sceneType | No | [🔗](#xmp-exif-scenetype) |
| `exif` | `xmp.exif.sensingMethod` | sensingMethod | No | [🔗](#xmp-exif-sensingmethod) |
| `exif` | `xmp.exif.sharpness` | sharpness | No | [🔗](#xmp-exif-sharpness) |
| `exif` | `xmp.exif.shutterSpeedValue` | shutterSpeedValue | No | [🔗](#xmp-exif-shutterspeedvalue) |
| `exif` | `xmp.exif.spatialFrequencyResponse` | spatialFrequencyResponse | No | [🔗](#xmp-exif-spatialfrequencyresponse) |
| `exif` | `xmp.exif.spectralSensitivity` | spectralSensitivity | No | [🔗](#xmp-exif-spectralsensitivity) |
| `exif` | `xmp.exif.subjectArea` | subjectArea | No | [🔗](#xmp-exif-subjectarea) |
| `exif` | `xmp.exif.subjectDistance` | subjectDistance | No | [🔗](#xmp-exif-subjectdistance) |
| `exif` | `xmp.exif.subjectDistanceRange` | subjectDistanceRange | No | [🔗](#xmp-exif-subjectdistancerange) |
| `exif` | `xmp.exif.subjectLocation` | subjectLocation | No | [🔗](#xmp-exif-subjectlocation) |
| `exif` | `xmp.exif.userComment` | userComment | No | [🔗](#xmp-exif-usercomment) |
| `exif` | `xmp.exif.whiteBalance` | whiteBalance | No | [🔗](#xmp-exif-whitebalance) |
| `exif` | `xmp.exif.GPSAltitude` | GPSAltitude | No | [🔗](#xmp-exif-gpsaltitude) |
| `exif` | `xmp.exif.GPSAltitudeRef` | GPSAltitudeRef | No | [🔗](#xmp-exif-gpsaltituderef) |
| `exif` | `xmp.exif.GPSAreaInformation` | GPSAreaInformation | No | [🔗](#xmp-exif-gpsareainformation) |
| `exif` | `xmp.exif.GPSDestBearing` | GPSDestBearing | No | [🔗](#xmp-exif-gpsdestbearing) |
| `exif` | `xmp.exif.GPSDestBearingRef` | GPSDestBearingRef | No | [🔗](#xmp-exif-gpsdestbearingref) |
| `exif` | `xmp.exif.GPSDestDistance` | GPSDestDistance | No | [🔗](#xmp-exif-gpsdestdistance) |
| `exif` | `xmp.exif.GPSDestDistanceRef` | GPSDestDistanceRef | No | [🔗](#xmp-exif-gpsdestdistanceref) |
| `exif` | `xmp.exif.GPSDestLatitude` | GPSDestLatitude | No | [🔗](#xmp-exif-gpsdestlatitude) |
| `exif` | `xmp.exif.GPSDestLongitude` | GPSDestLongitude | No | [🔗](#xmp-exif-gpsdestlongitude) |
| `exif` | `xmp.exif.GPSDifferential` | GPSDifferential | No | [🔗](#xmp-exif-gpsdifferential) |
| `exif` | `xmp.exif.GPSDOP` | GPSDOP | No | [🔗](#xmp-exif-gpsdop) |
| `exif` | `xmp.exif.GPSImgDirection` | GPSImgDirection | No | [🔗](#xmp-exif-gpsimgdirection) |
| `exif` | `xmp.exif.GPSImgDirectionRef` | GPSImgDirectionRef | No | [🔗](#xmp-exif-gpsimgdirectionref) |
| `exif` | `xmp.exif.GPSLatitude` | GPSLatitude | No | [🔗](#xmp-exif-gpslatitude) |
| `exif` | `xmp.exif.GPSLongitude` | GPSLongitude | No | [🔗](#xmp-exif-gpslongitude) |
| `exif` | `xmp.exif.GPSMapDatum` | GPSMapDatum | No | [🔗](#xmp-exif-gpsmapdatum) |
| `exif` | `xmp.exif.GPSMeasureMode` | GPSMeasureMode | No | [🔗](#xmp-exif-gpsmeasuremode) |
| `exif` | `xmp.exif.GPSProcessingMethod` | GPSProcessingMethod | No | [🔗](#xmp-exif-gpsprocessingmethod) |
| `exif` | `xmp.exif.GPSSatellites` | GPSSatellites | No | [🔗](#xmp-exif-gpssatellites) |
| `exif` | `xmp.exif.GPSSpeed` | GPSSpeed | No | [🔗](#xmp-exif-gpsspeed) |
| `exif` | `xmp.exif.GPSSpeedRef` | GPSSpeedRef | No | [🔗](#xmp-exif-gpsspeedref) |
| `exif` | `xmp.exif.GPSStatus` | GPSStatus | No | [🔗](#xmp-exif-gpsstatus) |
| `exif` | `xmp.exif.GPSTimeStamp` | GPSTimeStamp | No | [🔗](#xmp-exif-gpstimestamp) |
| `exif` | `xmp.exif.GPSTrack` | GPSTrack | No | [🔗](#xmp-exif-gpstrack) |
| `exif` | `xmp.exif.GPSTrackRef` | GPSTrackRef | No | [🔗](#xmp-exif-gpstrackref) |
| `exif` | `xmp.exif.GPSVersionID` | GPSVersionID | No | [🔗](#xmp-exif-gpsversionid) |

The technical details of each field may be found below:

<a id="xmp-exif-aperturevalue"></a>
### The `exif:ApertureValue` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.apertureValue` |
| ID | `exif:ApertureValue` |
| Name | apertureValue |
| Label | – |
| Definiton | EXIF tag 37378, 0x9202. Lens aperture, unit is APEX. |
| Required? | No |
| Tag | 37378 |
| Type | Rational |
| Unit | APEX |

<a id="xmp-exif-brightnessvalue"></a>
### The `exif:BrightnessValue` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.brightnessValue` |
| ID | `exif:BrightnessValue` |
| Name | brightnessValue |
| Label | – |
| Definiton | EXIF tag 37379, 0x9203. Brightness, unit is APEX. |
| Required? | No |
| Tag | 37379 |
| Type | Rational |
| Unit | APEX |

<a id="xmp-exif-cfapattern"></a>
### The `exif:CFAPattern` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.CFAPattern` |
| ID | `exif:CFAPattern` |
| Name | CFAPattern |
| Label | – |
| Definiton | EXIF tag 41730, 0xA302. Color filter array geometric pattern of the image sense. |
| Required? | No |
| Tag | 41730 |
| Type | CFAPattern |

<a id="xmp-exif-colorspace"></a>
### The `exif:ColorSpace` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.colorSpace` |
| ID | `exif:ColorSpace` |
| Name | colorSpace |
| Label | – |
| Definiton | EXIF tag 40961, 0xA001. Color space information: 1 = sRGB, 65535 = uncalibrated. |
| Options | 1; 65535 |
| Required? | No |
| Tag | 40961 |
| Type | Integer |

<a id="xmp-exif-compressedbitsperpixel"></a>
### The `exif:CompressedBitsPerPixel` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.compressedBitsPerPixel` |
| ID | `exif:CompressedBitsPerPixel` |
| Name | compressedBitsPerPixel |
| Label | – |
| Definiton | EXIF tag 37122, 0x9102. Compression mode used for a compressed image is indicated in unit bits per pixel. |
| Required? | No |
| Tag | 37122 |
| Type | Rational |

<a id="xmp-exif-contrast"></a>
### The `exif:Contrast` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.contrast` |
| ID | `exif:Contrast` |
| Name | contrast |
| Label | – |
| Definiton | EXIF tag 41992, 0xA408. Indicates the direction of contrast processing applied by the camera: 0 = Normal, 1 = Soft, 2 = Hard. |
| Options | 0; 1; 2 |
| Required? | No |
| Tag | 41992 |
| Type | Integer |

<a id="xmp-exif-customrendered"></a>
### The `exif:CustomRendered` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.customRendered` |
| ID | `exif:CustomRendered` |
| Name | customRendered |
| Label | – |
| Definiton | EXIF tag 41985, 0xA401. Indicates the use of special processing on image data: 0 = Normal process, 1 = Custom process. |
| Options | 0; 1 |
| Required? | No |
| Tag | 41985 |
| Type | Integer |

<a id="xmp-exif-datetimedigitized"></a>
### The `exif:DateTimeDigitized` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.dateTimeDigitized` |
| ID | `exif:DateTimeDigitized` |
| Name | dateTimeDigitized |
| Label | – |
| Definiton | EXIF tag 36868, 0x9004 (primary) and 37522, 0x9292 (subseconds). Date and time when image was stored as digital data, can be the same as DateTimeOriginal if originally stored in digital form. Stored in ISO 8601 format. Includes the EXIF SubSecTimeDigitized data. This value is used in XMP as xmp:CreateDate. |
| Related Field | exif:SubSecTimeDigitized |
| Required? | No |
| Tag | 36868 |
| Type | Date |

<a id="xmp-exif-datetimeoriginal"></a>
### The `exif:DateTimeOriginal` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.dateTimeOriginal` |
| ID | `exif:DateTimeOriginal` |
| Name | dateTimeOriginal |
| Label | – |
| Definiton | EXIF tags 36867, 0x9003 (primary) and 37521, 0x9291 (subseconds). Date and time when original image was generated, in ISO 8601 format. Includes the EXIF SubSecTimeOriginal data. Note that Exif date-time values have no time zone information. |
| Related Field | exif:SubSecTimeOriginal |
| Required? | No |
| Tag | 36867 |
| Type | Date |

<a id="xmp-exif-devicesettingdescription"></a>
### The `exif:DeviceSettingDescription` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.deviceSettingDescription` |
| ID | `exif:DeviceSettingDescription` |
| Name | deviceSettingDescription |
| Label | – |
| Definiton | EXIF tag 41995, 0xA40B. Indicates information on the picture-taking conditions of a particular camera model. |
| Required? | No |
| Tag | 41995 |
| Type | DeviceSettings |

<a id="xmp-exif-digitalzoomratio"></a>
### The `exif:DigitalZoomRatio` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.digitalZoomRatio` |
| ID | `exif:DigitalZoomRatio` |
| Name | digitalZoomRatio |
| Label | – |
| Definiton | EXIF tag 41988, 0xA404. Indicates the digital zoom ratio when the image was shot. |
| Required? | No |
| Tag | 41988 |
| Type | Rational |

<a id="xmp-exif-exifversion"></a>
### The `exif:ExifVersion` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.exifVersion` |
| ID | `exif:ExifVersion` |
| Name | exifVersion |
| Label | – |
| Definiton | EXIF tag 36864, 0x9000. EXIF version number. |
| Required? | No |
| Tag | 36864 |
| Type | Text |

<a id="xmp-exif-exposurebiasvalue"></a>
### The `exif:ExposureBiasValue` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.exposureBiasValue` |
| ID | `exif:ExposureBiasValue` |
| Name | exposureBiasValue |
| Label | – |
| Definiton | EXIF tag 37380, 0x9204. Exposure bias, unit is APEX. |
| Required? | No |
| Tag | 37380 |
| Type | Rational |
| Unit | APEX |

<a id="xmp-exif-exposureindex"></a>
### The `exif:ExposureIndex` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.exposureIndex` |
| ID | `exif:ExposureIndex` |
| Name | exposureIndex |
| Label | – |
| Definiton | EXIF tag 41493, 0xA215. Exposure index of input device. |
| Required? | No |
| Tag | 41493 |
| Type | Rational |

<a id="xmp-exif-exposuremode"></a>
### The `exif:ExposureMode` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.exposureMode` |
| ID | `exif:ExposureMode` |
| Name | exposureMode |
| Label | – |
| Definiton | EXIF tag 41986, 0xA402. Indicates the exposure mode set when the image was shot: 0 = Auto exposure, 1 = Manual exposure, 2 = Auto bracket. |
| Options | 0; 1; 2 |
| Required? | No |
| Tag | 41986 |
| Type | Integer |

<a id="xmp-exif-exposureprogram"></a>
### The `exif:ExposureProgram` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.exposureProgram` |
| ID | `exif:ExposureProgram` |
| Name | exposureProgram |
| Label | – |
| Definiton | EXIF tag 34850, 0x8822. Class of program used for exposure: 0 = not defined, 1 = Manual, 2 = Normal program, 3 = Aperture priority, 4 = Shutter priority, 5 = Creative program, 6 = Action program, 7 = Portrait mode, 8 = Landscape mode. |
| Options | 0; 1; 2; 3; 4; 5; 6; 7; 8 |
| Required? | No |
| Tag | 34850 |
| Type | Integer |

<a id="xmp-exif-exposuretime"></a>
### The `exif:ExposureTime` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.exposureTime` |
| ID | `exif:ExposureTime` |
| Name | exposureTime |
| Label | – |
| Definiton | EXIF tag 33434, 0x829A. Exposure time in seconds. |
| Required? | No |
| Tag | 33434 |
| Type | Rational |

<a id="xmp-exif-filesource"></a>
### The `exif:FileSource` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.fileSource` |
| ID | `exif:FileSource` |
| Name | fileSource |
| Label | – |
| Definiton | EXIF tag 41728, 0xA300. Indicates image source: 3 (DSC) is the only choice. |
| Options | 3 |
| Required? | No |
| Tag | 41728 |
| Type | Integer |

<a id="xmp-exif-flash"></a>
### The `exif:Flash` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.flash` |
| ID | `exif:Flash` |
| Name | flash |
| Label | – |
| Definiton | EXIF tag 37385, 0x9209. Strobe light (flash) source data. |
| Required? | No |
| Tag | 37385 |
| Type | Flash |

<a id="xmp-exif-flashenergy"></a>
### The `exif:FlashEnergy` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.flashEnergy` |
| ID | `exif:FlashEnergy` |
| Name | flashEnergy |
| Label | – |
| Definiton | EXIF tag 41483, 0xA20B. Strobe energy during image capture. |
| Required? | No |
| Tag | 41483 |
| Type | Rational |

<a id="xmp-exif-flashpixversion"></a>
### The `exif:FlashpixVersion` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.flashpixVersion` |
| ID | `exif:FlashpixVersion` |
| Name | flashpixVersion |
| Label | – |
| Definiton | EXIF tag 40960, 0xA000. Version of FlashPix. |
| Required? | No |
| Tag | 40960 |
| Type | Text |

<a id="xmp-exif-fnumber"></a>
### The `exif:FNumber` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.FNumber` |
| ID | `exif:FNumber` |
| Name | FNumber |
| Label | – |
| Definiton | EXIF tag 33437, 0x829D. F number. |
| Required? | No |
| Tag | 33437 |
| Type | Rational |

<a id="xmp-exif-focallength"></a>
### The `exif:FocalLength` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.focalLength` |
| ID | `exif:FocalLength` |
| Name | focalLength |
| Label | – |
| Definiton | EXIF tag 37386, 0x920A. Focal length of the lens, in millimeters. |
| Required? | No |
| Tag | 37386 |
| Type | Rational |
| Unit | mm |

<a id="xmp-exif-focallengthin35mmfilm"></a>
### The `exif:FocalLengthIn35mmFilm` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.FocalLengthIn35mmFilm` |
| ID | `exif:FocalLengthIn35mmFilm` |
| Name | FocalLengthIn35mmFilm |
| Label | – |
| Definiton | EXIF tag 41989, 0xA405. Indicates the equivalent focal length assuming a 35mm film camera, in mm. A value of 0 means the focal length is unknown. Note that this tag differs from the FocalLength tag. |
| Required? | No |
| Tag | 41989 |
| Type | Integer |
| Unit | mm |

<a id="xmp-exif-focalplaneresolutionunit"></a>
### The `exif:FocalPlaneResolutionUnit` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.focalPlaneResolutionUnit` |
| ID | `exif:FocalPlaneResolutionUnit` |
| Name | focalPlaneResolutionUnit |
| Label | – |
| Definiton | EXIF tag 41488, 0xA210. Unit used for FocalPlaneXResolution and FocalPlaneYResolution. 2 = inches, 3 = centimeters. |
| Options | 2; 3 |
| Required? | No |
| Tag | 41488 |
| Type | Integer |

<a id="xmp-exif-focalplanexresolution"></a>
### The `exif:FocalPlaneXResolution` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.focalPlaneXResolution` |
| ID | `exif:FocalPlaneXResolution` |
| Name | focalPlaneXResolution |
| Label | – |
| Definiton | EXIF tag 41486, 0xA20E. Horizontal focal resolution, measured pixels per unit. |
| Required? | No |
| Tag | 41486 |
| Type | Rational |
| Unit | pixels |

<a id="xmp-exif-focalplaneyresolution"></a>
### The `exif:FocalPlaneYResolution` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.focalPlaneYResolution` |
| ID | `exif:FocalPlaneYResolution` |
| Name | focalPlaneYResolution |
| Label | – |
| Definiton | EXIF tag 41487, 0xA20F. Vertical focal resolution, measured in pixels per unit. |
| Required? | No |
| Tag | 41487 |
| Type | Rational |
| Unit | pixels |

<a id="xmp-exif-gaincontrol"></a>
### The `exif:GainControl` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.gainControl` |
| ID | `exif:GainControl` |
| Name | gainControl |
| Label | – |
| Definiton | EXIF tag 41991, 0xA407. Indicates the degree of overall image gain adjustment: 0 = None, 1 = Low gain up, 2 = High gain up, 3 = Low gain down, 4 = High gain down. |
| Options | 0; 1; 2; 3; 4 |
| Required? | No |
| Tag | 41991 |
| Type | Integer |

<a id="xmp-exif-imageuniqueid"></a>
### The `exif:ImageUniqueID` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.imageUniqueID` |
| ID | `exif:ImageUniqueID` |
| Name | imageUniqueID |
| Label | – |
| Definiton | EXIF tag 42016, 0xA420. An identifier assigned uniquely to each image. It is recorded as a 32 character ASCII string, equivalent to hexadecimal notation and 128-bit fixed length. |
| Required? | No |
| Tag | 42016 |
| Type | Text |

<a id="xmp-exif-isospeedratings"></a>
### The `exif:ISOSpeedRatings` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.ISOSpeedRatings` |
| ID | `exif:ISOSpeedRatings` |
| Name | ISOSpeedRatings |
| Label | – |
| Definiton | EXIF tag 34855, 0x8827. ISO Speed and ISO Latitude of the input device as specified in ISO 12232. A native Exif ISO value of exactly 65535 indicates an ISO value of above 64K, which cannot be stored in the native Exif Tag 34855. The real value should be stored in the XMP. |
| Multiple? | Yes |
| Ordered? | Yes |
| Required? | No |
| Tag | 34855 |
| Type | Integer |

<a id="xmp-exif-lightsource"></a>
### The `exif:LightSource` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.lightSource` |
| ID | `exif:LightSource` |
| Name | lightSource |
| Label | – |
| Definiton | EXIF tag 37384, 0x9208. Light source: 0 = unknown, 1 = Daylight, 2 = Fluorescent, 3 = Tungsten, 4 = Flash, 9 = Fine weather, 10 = Cloudy weather, 11 = Shade, 12 = Daylight fluorescent (D 5700 – 7100K), 13 = Day white fluorescent (N 4600 – 5400K), 14 = Cool white fluorescent (W 3900 – 4500K), 15 = White fluorescent (WW 3200 – 3700K), 17 = Standard light A, 18 = Standard light B, 19 = Standard light C, 20 = D55, 21 = D65, 22 = D75, 23 = D50, 24 = ISO studio tungsten, 255 = other. |
| Options | 0; 1; 2; 3; 4; 9; 10; 11; 12; 13; 14; 15; 17; 18; 19; 20; 21; 22; 23; 24; 255 |
| Required? | No |
| Tag | 37384 |
| Type | Integer |

<a id="xmp-exif-maxaperturevalue"></a>
### The `exif:MaxApertureValue` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.maxApertureValue` |
| ID | `exif:MaxApertureValue` |
| Name | maxApertureValue |
| Label | – |
| Definiton | EXIF tag 37381, 0x9205. Smallest F number of lens, in APEX. |
| Required? | No |
| Tag | 37381 |
| Type | Rational |
| Unit | APEX |

<a id="xmp-exif-meteringmode"></a>
### The `exif:MeteringMode` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.meteringMode` |
| ID | `exif:MeteringMode` |
| Name | meteringMode |
| Label | – |
| Definiton | EXIF tag 37383, 0x9207. Metering mode: 0 = unknown, 1 = Average, 2 = CenterWeightedAverage, 3 = Spot, 4 = MultiSpot, 5 = Pattern, 6 = Partial, 255 = other. |
| Options | 0; 1; 2; 3; 4; 5; 6; 255 |
| Required? | No |
| Tag | 37383 |
| Type | Integer |

<a id="xmp-exif-oecf"></a>
### The `exif:OECF` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.OECF` |
| ID | `exif:OECF` |
| Name | OECF |
| Label | – |
| Definiton | EXIF tag 34856, 0x8828. Opto-Electoric Conversion Function as specified in ISO 14524. |
| Required? | No |
| Tag | 34856 |
| Type | OECFSFR |

<a id="xmp-exif-pixelxdimension"></a>
### The `exif:PixelXDimension` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.pixelXDimension` |
| ID | `exif:PixelXDimension` |
| Name | pixelXDimension |
| Label | – |
| Definiton | EXIF tag 40962, 0xA002. Valid image width, in pixels. |
| Required? | No |
| Tag | 40962 |
| Type | Integer |
| Unit | pixels |

<a id="xmp-exif-pixelydimension"></a>
### The `exif:PixelYDimension` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.pixelYDimension` |
| ID | `exif:PixelYDimension` |
| Name | pixelYDimension |
| Label | – |
| Definiton | EXIF tag 40963, 0xA003. Valid image height, in pixels. |
| Required? | No |
| Tag | 40963 |
| Type | Integer |
| Unit | pixels |

<a id="xmp-exif-relatedsoundfile"></a>
### The `exif:RelatedSoundFile` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.relatedSoundFile` |
| ID | `exif:RelatedSoundFile` |
| Name | relatedSoundFile |
| Label | – |
| Definiton | EXIF tag 40964, 0xA004. An 8.3 file name for the related sound file. |
| Required? | No |
| Tag | 40964 |
| Type | Text |

<a id="xmp-exif-saturation"></a>
### The `exif:Saturation` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.saturation` |
| ID | `exif:Saturation` |
| Name | saturation |
| Label | – |
| Definiton | EXIF tag 41993, 0xA409. Indicates the direction of saturation processing applied by the camera: 0 = Normal, 1 = Low saturation, 2 = High saturation. |
| Options | 0; 1; 2 |
| Required? | No |
| Tag | 40964 |
| Type | Integer |

<a id="xmp-exif-scenecapturetype"></a>
### The `exif:SceneCaptureType` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.sceneCaptureType` |
| ID | `exif:SceneCaptureType` |
| Name | sceneCaptureType |
| Label | – |
| Definiton | EXIF tag 41990, 0xA406. Indicates the type of scene that was shot: 0 = Standard, 1 = Landscape, 2 = Portrait, 3 = Night scene. |
| Options | 0; 1; 2; 3 |
| Required? | No |
| Tag | 41990 |
| Type | Integer |

<a id="xmp-exif-scenetype"></a>
### The `exif:SceneType` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.sceneType` |
| ID | `exif:SceneType` |
| Name | sceneType |
| Label | – |
| Definiton | EXIF tag 41729, 0xA301. Indicates the type of scene: 1 (directly photographed image) is the only choice. |
| Options | 1 |
| Required? | No |
| Tag | 41729 |
| Type | Integer |

<a id="xmp-exif-sensingmethod"></a>
### The `exif:SensingMethod` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.sensingMethod` |
| ID | `exif:SensingMethod` |
| Name | sensingMethod |
| Label | – |
| Definiton | EXIF tag 41495, 0xA217. Image sensor type on input device: 1 = Not defined, 2 = One-chip colour area sensor, 3 = Two-chip colour area sensor, 4 = Three-chip colour area sensor, 5 = Colour sequential area sensor, 7 = Trilinear sensor, 8 = Colour sequential linear sensor. |
| Options | 1; 2; 3; 4; 5; 7; 8 |
| Required? | No |
| Tag | 41495 |
| Type | Integer |

<a id="xmp-exif-sharpness"></a>
### The `exif:Sharpness` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.sharpness` |
| ID | `exif:Sharpness` |
| Name | sharpness |
| Label | – |
| Definiton | EXIF tag 41994, 0xA40A. Indicates the direction of sharpness processing applied by the camera: 0 = Normal, 1 = Soft, 2 = Hard. |
| Options | 0; 1; 2 |
| Required? | No |
| Tag | 41994 |
| Type | Integer |

<a id="xmp-exif-shutterspeedvalue"></a>
### The `exif:ShutterSpeedValue` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.shutterSpeedValue` |
| ID | `exif:ShutterSpeedValue` |
| Name | shutterSpeedValue |
| Label | – |
| Definiton | EXIF tag 37377, 0x9201. Shutter speed, unit is APEX. See Annex C of the EXIF specification. |
| Required? | No |
| Tag | 37377 |
| Type | Rational |

<a id="xmp-exif-spatialfrequencyresponse"></a>
### The `exif:SpatialFrequencyResponse` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.spatialFrequencyResponse` |
| ID | `exif:SpatialFrequencyResponse` |
| Name | spatialFrequencyResponse |
| Label | – |
| Definiton | EXIF tag 41484, 0xA20C. Input device spatial frequency table and SFR values as specified in ISO 12233. |
| Required? | No |
| Tag | 41484 |
| Type | OECFSFR |

<a id="xmp-exif-spectralsensitivity"></a>
### The `exif:SpectralSensitivity` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.spectralSensitivity` |
| ID | `exif:SpectralSensitivity` |
| Name | spectralSensitivity |
| Label | – |
| Definiton | EXIF tag 34852, 0x8824. Spectral sensitivity of each channel. |
| Required? | No |
| Tag | 34852 |
| Type | Text |

<a id="xmp-exif-subjectarea"></a>
### The `exif:SubjectArea` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.subjectArea` |
| ID | `exif:SubjectArea` |
| Name | subjectArea |
| Label | – |
| Definiton | EXIF tag 37396, 0x9214. The location and area of the main subject in the overall scene. |
| Multiple? | Yes |
| Ordered? | Yes |
| Required? | No |
| Tag | 37396 |
| Type | Integer |

<a id="xmp-exif-subjectdistance"></a>
### The `exif:SubjectDistance` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.subjectDistance` |
| ID | `exif:SubjectDistance` |
| Name | subjectDistance |
| Label | – |
| Definiton | EXIF tag 37382, 0x9206. Distance to subject, in meters. |
| Required? | No |
| Tag | 37382 |
| Type | Rational |
| Unit | meters |

<a id="xmp-exif-subjectdistancerange"></a>
### The `exif:SubjectDistanceRange` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.subjectDistanceRange` |
| ID | `exif:SubjectDistanceRange` |
| Name | subjectDistanceRange |
| Label | – |
| Definiton | EXIF tag 41996, 0xA40C. Indicates the distance to the subject: 0 = Unknown, 1 = Macro, 2 = Close view, 3 = Distant view. |
| Options | 0; 1; 2; 3 |
| Required? | No |
| Tag | 41996 |
| Type | Integer |

<a id="xmp-exif-subjectlocation"></a>
### The `exif:SubjectLocation` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.subjectLocation` |
| ID | `exif:SubjectLocation` |
| Name | subjectLocation |
| Label | – |
| Definiton | EXIF tag 41492, 0xA214. Location of the main subject of the scene. The first value is the horizontal pixel and the second value is the vertical pixel at which the main subject appears. |
| Multiple? | Yes |
| Ordered? | Yes |
| Required? | No |
| Tag | 41492 |
| Type | Integer |

<a id="xmp-exif-usercomment"></a>
### The `exif:UserComment` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.userComment` |
| ID | `exif:UserComment` |
| Name | userComment |
| Label | – |
| Combine? | Yes |
| Definiton | EXIF tag 37510, 0x9286. Comments from user. |
| Required? | No |
| Tag | 37510 |
| Type | LanguageAlternative |

<a id="xmp-exif-whitebalance"></a>
### The `exif:WhiteBalance` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.whiteBalance` |
| ID | `exif:WhiteBalance` |
| Name | whiteBalance |
| Label | – |
| Definiton | EXIF tag 41987, 0xA403. Indicates the white balance mode set when the image was shot: 0 = Auto white balance, 1 = Manual white balance. |
| Options | 0; 1 |
| Required? | No |
| Tag | 41987 |
| Type | Integer |

<a id="xmp-exif-gpsaltitude"></a>
### The `exif:GPSAltitude` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.GPSAltitude` |
| ID | `exif:GPSAltitude` |
| Name | GPSAltitude |
| Label | – |
| Definiton | GPS tag 6, 0x06. Indicates altitude in meters. |
| Required? | No |
| Tag | 6 |
| Type | Rational |
| Unit | meters |

<a id="xmp-exif-gpsaltituderef"></a>
### The `exif:GPSAltitudeRef` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.GPSAltitudeRef` |
| ID | `exif:GPSAltitudeRef` |
| Name | GPSAltitudeRef |
| Label | – |
| Definiton | GPS tag 5, 0x5. Indicates whether the altitude is above or below sea level: 0 = Above sea level, 1 = Below sea level. |
| Options | 0; 1 |
| Required? | No |
| Tag | 5 |
| Type | Integer |

<a id="xmp-exif-gpsareainformation"></a>
### The `exif:GPSAreaInformation` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.GPSAreaInformation` |
| ID | `exif:GPSAreaInformation` |
| Name | GPSAreaInformation |
| Label | – |
| Definiton | GPS tag 28, 0x1C. A character string recording the name of the GPS area. |
| Required? | No |
| Tag | 28 |
| Type | Text |

<a id="xmp-exif-gpsdestbearing"></a>
### The `exif:GPSDestBearing` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.GPSDestBearing` |
| ID | `exif:GPSDestBearing` |
| Name | GPSDestBearing |
| Label | – |
| Definiton | GPS tag 24, 0x18. Destination bearing, values from 0 to 359.99. |
| Maximum Value | 359.99 |
| Minimum Value | 0 |
| Required? | No |
| Tag | 24 |
| Type | Rational |

<a id="xmp-exif-gpsdestbearingref"></a>
### The `exif:GPSDestBearingRef` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.GPSDestBearingRef` |
| ID | `exif:GPSDestBearingRef` |
| Name | GPSDestBearingRef |
| Label | – |
| Definiton | GPS tag 23, 0x17. Reference for movement direction: T = true direction, M = magnetic direction. |
| Options | T; M |
| Required? | No |
| Tag | 23 |
| Type | Text |

<a id="xmp-exif-gpsdestdistance"></a>
### The `exif:GPSDestDistance` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.GPSDestDistance` |
| ID | `exif:GPSDestDistance` |
| Name | GPSDestDistance |
| Label | – |
| Definiton | GPS tag 26, 0x1A. Distance to destination. |
| Required? | No |
| Tag | 26 |
| Type | Rational |

<a id="xmp-exif-gpsdestdistanceref"></a>
### The `exif:GPSDestDistanceRef` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.GPSDestDistanceRef` |
| ID | `exif:GPSDestDistanceRef` |
| Name | GPSDestDistanceRef |
| Label | – |
| Definiton | GPS tag 25, 0x19. Units used for speed measurement: "K" = kilometers, "M" = miles, "N" = knots. |
| Options | K; MN |
| Required? | No |
| Tag | 25 |
| Type | Text |

<a id="xmp-exif-gpsdestlatitude"></a>
### The `exif:GPSDestLatitude` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.GPSDestLatitude` |
| ID | `exif:GPSDestLatitude` |
| Name | GPSDestLatitude |
| Label | – |
| Definiton | GPS tag 20, 0x14 (position) and 19, 0x13 (North/South). Indicates destination latitude. |
| Required? | No |
| Tag | 20 |
| Type | Text |

<a id="xmp-exif-gpsdestlongitude"></a>
### The `exif:GPSDestLongitude` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.GPSDestLongitude` |
| ID | `exif:GPSDestLongitude` |
| Name | GPSDestLongitude |
| Label | – |
| Definiton | GPS tag 22, 0x16 (position) and 21, 0x15 (East/West). Indicates destination longitude. |
| Required? | No |
| Tag | 22 |
| Type | Text |

<a id="xmp-exif-gpsdifferential"></a>
### The `exif:GPSDifferential` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.GPSDifferential` |
| ID | `exif:GPSDifferential` |
| Name | GPSDifferential |
| Label | – |
| Definiton | GPS tag 30, 0x1E. Indicates whether differential correction is applied to the GPS receiver: 0 = Without correction, 1 = Correction applied. |
| Options | 0; 1 |
| Required? | No |
| Tag | 30 |
| Type | Integer |

<a id="xmp-exif-gpsdop"></a>
### The `exif:GPSDOP` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.GPSDOP` |
| ID | `exif:GPSDOP` |
| Name | GPSDOP |
| Label | – |
| Definiton | GPS tag 11, 0x0B. Degree of precision for GPS data. |
| Required? | No |
| Tag | 11 |
| Type | Rational |

<a id="xmp-exif-gpsimgdirection"></a>
### The `exif:GPSImgDirection` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.GPSImgDirection` |
| ID | `exif:GPSImgDirection` |
| Name | GPSImgDirection |
| Label | – |
| Definiton | GPS tag 17, 0x11. Direction of image when captured, values range from 0 to 359.99. |
| Maximum Value | 359.99 |
| Minimum Value | 0 |
| Required? | No |
| Tag | 17 |
| Type | Rational |

<a id="xmp-exif-gpsimgdirectionref"></a>
### The `exif:GPSImgDirectionRef` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.GPSImgDirectionRef` |
| ID | `exif:GPSImgDirectionRef` |
| Name | GPSImgDirectionRef |
| Label | – |
| Definiton | GPS tag 16, 0x10. Reference for movement direction: "T" = true direction, "M" = magnetic direction. |
| Options | T; M |
| Required? | No |
| Tag | 16 |
| Type | Text |

<a id="xmp-exif-gpslatitude"></a>
### The `exif:GPSLatitude` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.GPSLatitude` |
| ID | `exif:GPSLatitude` |
| Name | GPSLatitude |
| Label | – |
| Definiton | GPS tag 2, 0x02 (position) and 1, 0x01 (North/South). Indicates latitude. |
| Required? | No |
| Tag | 2 |
| Type | Text |

<a id="xmp-exif-gpslongitude"></a>
### The `exif:GPSLongitude` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.GPSLongitude` |
| ID | `exif:GPSLongitude` |
| Name | GPSLongitude |
| Label | – |
| Definiton | GPS tag 4, 0x04 (position) and 3, 0x03 (East/West). Indicates longitude. |
| Required? | No |
| Tag | 4 |
| Type | Text |

<a id="xmp-exif-gpsmapdatum"></a>
### The `exif:GPSMapDatum` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.GPSMapDatum` |
| ID | `exif:GPSMapDatum` |
| Name | GPSMapDatum |
| Label | – |
| Definiton | GPS tag 18, 0x12. Geodetic survey data. |
| Required? | No |
| Tag | 18 |
| Type | Text |

<a id="xmp-exif-gpsmeasuremode"></a>
### The `exif:GPSMeasureMode` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.GPSMeasureMode` |
| ID | `exif:GPSMeasureMode` |
| Name | GPSMeasureMode |
| Label | – |
| Definiton | GPS tag 10, 0x0A. GPS measurement mode, Text type: "2" = two-dimensional measurement, "3" = three-dimensional measurement. |
| Options | 2; 3 |
| Required? | No |
| Tag | 10 |
| Type | Text |

<a id="xmp-exif-gpsprocessingmethod"></a>
### The `exif:GPSProcessingMethod` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.GPSProcessingMethod` |
| ID | `exif:GPSProcessingMethod` |
| Name | GPSProcessingMethod |
| Label | – |
| Definiton | GPS tag 27, 0x1B. A character string recording the name of the method used for location finding. |
| Required? | No |
| Tag | 27 |
| Type | Text |

<a id="xmp-exif-gpssatellites"></a>
### The `exif:GPSSatellites` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.GPSSatellites` |
| ID | `exif:GPSSatellites` |
| Name | GPSSatellites |
| Label | – |
| Definiton | GPS tag 8, 0x08. Satellite information, format is unspecified. |
| Required? | No |
| Tag | 8 |
| Type | Text |

<a id="xmp-exif-gpsspeed"></a>
### The `exif:GPSSpeed` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.GPSSpeed` |
| ID | `exif:GPSSpeed` |
| Name | GPSSpeed |
| Label | – |
| Definiton | GPS tag 13, 0x0D. Speed of GPS receiver movement. |
| Required? | No |
| Tag | 13 |
| Type | Rational |

<a id="xmp-exif-gpsspeedref"></a>
### The `exif:GPSSpeedRef` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.GPSSpeedRef` |
| ID | `exif:GPSSpeedRef` |
| Name | GPSSpeedRef |
| Label | – |
| Definiton | GPS tag 12, 0x0C. Units used for speed measurement: "K" = kilometers per hour, "M" = miles per hour, "N" = knots. |
| Options | K; M; N |
| Required? | No |
| Tag | 12 |
| Type | Text |

<a id="xmp-exif-gpsstatus"></a>
### The `exif:GPSStatus` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.GPSStatus` |
| ID | `exif:GPSStatus` |
| Name | GPSStatus |
| Label | – |
| Definiton | GPS tag 9, 0x09. Status of GPS receiver at image creation time: "A" = measurement in progress, "V" = measurement is interoperability. |
| Options | A; V |
| Required? | No |
| Tag | 9 |
| Type | Text |

<a id="xmp-exif-gpstimestamp"></a>
### The `exif:GPSTimeStamp` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.GPSTimeStamp` |
| ID | `exif:GPSTimeStamp` |
| Name | GPSTimeStamp |
| Label | – |
| Definiton | GPS tag 29 (date), 0x1D, and, and GPS tag 7 (time), 0x07. Time stamp of GPS data, in Coordinated Universal Time. NOTE: The GPSDateStamp tag is new in EXIF 2.2. The GPS timestamp in EXIF 2.1 does not include a date. If not present, the date component for the XMP should be taken from exif:DateTimeOriginal, or if that is also lacking from exif:DateTimeDigitized. If no date is available, do not write exif:GPSTimeStamp to XMP. |
| Required? | No |
| Tag | 29 |
| Type | Date |

<a id="xmp-exif-gpstrack"></a>
### The `exif:GPSTrack` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.GPSTrack` |
| ID | `exif:GPSTrack` |
| Name | GPSTrack |
| Label | – |
| Definiton | GPS tag 15, 0x0F. Direction of GPS movement, values range from 0 to 359.99. |
| Maximum Value | 359.99 |
| Minimum Value | 0 |
| Required? | No |
| Tag | 15 |
| Type | Rational |

<a id="xmp-exif-gpstrackref"></a>
### The `exif:GPSTrackRef` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.GPSTrackRef` |
| ID | `exif:GPSTrackRef` |
| Name | GPSTrackRef |
| Label | – |
| Definiton | GPS tag 14, 0x0E. Reference for movement direction: "T" = true direction, "M" = magnetic direction. |
| Options | T; M |
| Required? | No |
| Tag | 14 |
| Type | Text |

<a id="xmp-exif-gpsversionid"></a>
### The `exif:GPSVersionID` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.exif.GPSVersionID` |
| ID | `exif:GPSVersionID` |
| Name | GPSVersionID |
| Label | – |
| Definiton | GPS tag 0, 0x00. A decimal encoding of each of the four EXIF bytes with period separators. The current value is "2.3.0.0". |
| Required? | No |
| Tag | 0 |
| Type | Text |


The XMP metadata model's `tiff` namespace offers 25 fields which are listed below along with a link to each field's technical information:

| Namespace  | Field Path | Field Name | Required? | Info |
|------------|------------|------------|:---------:|------|
| `tiff` | `xmp.tiff.artist` | artist | No | [🔗](#xmp-tiff-artist) |
| `tiff` | `xmp.tiff.bitsPerSample` | bitsPerSample | No | [🔗](#xmp-tiff-bitspersample) |
| `tiff` | `xmp.tiff.compression` | compression | No | [🔗](#xmp-tiff-compression) |
| `tiff` | `xmp.tiff.Copyright` | Copyright | No | [🔗](#xmp-tiff-copyright) |
| `tiff` | `xmp.tiff.DateTime` | DateTime | No | [🔗](#xmp-tiff-datetime) |
| `tiff` | `xmp.tiff.ImageDescription` | ImageDescription | No | [🔗](#xmp-tiff-imagedescription) |
| `tiff` | `xmp.tiff.ImageLength` | ImageLength | No | [🔗](#xmp-tiff-imagelength) |
| `tiff` | `xmp.tiff.ImageWidth` | ImageWidth | No | [🔗](#xmp-tiff-imagewidth) |
| `tiff` | `xmp.tiff.Make` | Make | No | [🔗](#xmp-tiff-make) |
| `tiff` | `xmp.tiff.Model` | Model | No | [🔗](#xmp-tiff-model) |
| `tiff` | `xmp.tiff.Orientation` | Orientation | No | [🔗](#xmp-tiff-orientation) |
| `tiff` | `xmp.tiff.photometricInterpretation` | photometricInterpretation | No | [🔗](#xmp-tiff-photometricinterpretation) |
| `tiff` | `xmp.tiff.planarConfiguration` | planarConfiguration | No | [🔗](#xmp-tiff-planarconfiguration) |
| `tiff` | `xmp.tiff.primaryChromaticities` | primaryChromaticities | No | [🔗](#xmp-tiff-primarychromaticities) |
| `tiff` | `xmp.tiff.referenceBlackWhite` | referenceBlackWhite | No | [🔗](#xmp-tiff-referenceblackwhite) |
| `tiff` | `xmp.tiff.resolutionUnit` | resolutionUnit | No | [🔗](#xmp-tiff-resolutionunit) |
| `tiff` | `xmp.tiff.samplesPerPixel` | samplesPerPixel | No | [🔗](#xmp-tiff-samplesperpixel) |
| `tiff` | `xmp.tiff.software` | software | No | [🔗](#xmp-tiff-software) |
| `tiff` | `xmp.tiff.transferFunction` | transferFunction | No | [🔗](#xmp-tiff-transferfunction) |
| `tiff` | `xmp.tiff.whitePoint` | whitePoint | No | [🔗](#xmp-tiff-whitepoint) |
| `tiff` | `xmp.tiff.XResolution` | XResolution | No | [🔗](#xmp-tiff-xresolution) |
| `tiff` | `xmp.tiff.YResolution` | YResolution | No | [🔗](#xmp-tiff-yresolution) |
| `tiff` | `xmp.tiff.YCbCrCoefficients` | YCbCrCoefficients | No | [🔗](#xmp-tiff-ycbcrcoefficients) |
| `tiff` | `xmp.tiff.YCbCrPositioning` | YCbCrPositioning | No | [🔗](#xmp-tiff-ycbcrpositioning) |
| `tiff` | `xmp.tiff.YCbCrSubSampling` | YCbCrSubSampling | No | [🔗](#xmp-tiff-ycbcrsubsampling) |

The technical details of each field may be found below:

<a id="xmp-tiff-artist"></a>
### The `tiff:Artist` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.tiff.artist` |
| ID | `tiff:Artist` |
| Name | artist |
| Label | – |
| Definiton | Camera owner, photographer or image creator. NOTE: This property is stored in XMP as the first item in the dc:creator array. |
| Required? | No |
| Type | ProperName |

<a id="xmp-tiff-bitspersample"></a>
### The `tiff:BitsPerSample` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.tiff.bitsPerSample` |
| ID | `tiff:BitsPerSample` |
| Name | bitsPerSample |
| Label | – |
| Definiton | Number of bits per component in each channel. |
| Multiple? | Yes |
| Ordered? | Yes |
| Required? | No |
| Type | Integer |

<a id="xmp-tiff-compression"></a>
### The `tiff:Compression` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.tiff.compression` |
| ID | `tiff:Compression` |
| Name | compression |
| Label | – |
| Definiton | Compression scheme. 1 = Uncompressed , 6 = JPEG. |
| Options | 1; 6 |
| Required? | No |
| Type | Integer |

<a id="xmp-tiff-copyright"></a>
### The `tiff:Copyright` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.tiff.Copyright` |
| ID | `tiff:Copyright` |
| Name | Copyright |
| Label | – |
| Combine? | Yes |
| Definiton | Copyright information as an ASCII string. NOTE: This property is stored in XMP as dc:rights. |
| Pseudonym | exiftool: Copyright |
| Required? | No |
| Type | LanguageAlternative |

<a id="xmp-tiff-datetime"></a>
### The `tiff:DateTime` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.tiff.DateTime` |
| ID | `tiff:DateTime` |
| Name | DateTime |
| Label | – |
| Definiton | Date and time when the file was last modified (no time zone in EXIF), stored in ISO 8601 format, not the original EXIF format. This property includes the value for the EXIF SubSecTime(37520, 0x9290) attribute. NOTE: This property is stored in XMP as xmp:ModifyDate. |
| Required? | No |
| Type | Date |

<a id="xmp-tiff-imagedescription"></a>
### The `tiff:ImageDescription` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.tiff.ImageDescription` |
| ID | `tiff:ImageDescription` |
| Name | ImageDescription |
| Label | – |
| Combine? | Yes |
| Definiton | The title of the image as an ASCII string. NOTE: This property is stored in XMP as dc:description. |
| Required? | No |
| Type | LanguageAlternative |

<a id="xmp-tiff-imagelength"></a>
### The `tiff:ImageLength` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.tiff.ImageLength` |
| ID | `tiff:ImageLength` |
| Name | ImageLength |
| Label | – |
| Alias | ImageHeight |
| Definiton | Image height in pixels. |
| Required? | No |
| Type | Integer |
| Unit | pixels |

<a id="xmp-tiff-imagewidth"></a>
### The `tiff:ImageWidth` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.tiff.ImageWidth` |
| ID | `tiff:ImageWidth` |
| Name | ImageWidth |
| Label | – |
| Definiton | Image width in pixels. |
| Required? | No |
| Type | Integer |
| Unit | pixels |

<a id="xmp-tiff-make"></a>
### The `tiff:Make` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.tiff.Make` |
| ID | `tiff:Make` |
| Name | Make |
| Label | – |
| Definiton | Manufacturer of recording equipment as an ASCII string. |
| Encoding | ASCII |
| Required? | No |
| Type | ProperName |

<a id="xmp-tiff-model"></a>
### The `tiff:Model` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.tiff.Model` |
| ID | `tiff:Model` |
| Name | Model |
| Label | – |
| Definiton | Model name or number of equipment as an ASCII string. |
| Encoding | ASCII |
| Required? | No |
| Type | ProperName |

<a id="xmp-tiff-orientation"></a>
### The `tiff:Orientation` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.tiff.Orientation` |
| ID | `tiff:Orientation` |
| Name | Orientation |
| Label | – |
| Definiton | Orientation: 1 = 0th row at the top, 0th column at left, 2 = 0th row at the top, 0th column at right, 3 = 0th row at the bottom, 0th column at right, 4 = 0th row at the bottom, 0th column at left, 5 = 0th row at the left, 0th column at top, 6 = 0th row at the right, 0th column at top, 7 = 0th row at the right, 0th column at bottom, 8 = 0th row at the left, 0th column at bottom. |
| Options | 1; 2; 3; 4; 5; 6; 7; 8 |
| Required? | No |
| Type | Integer |

<a id="xmp-tiff-photometricinterpretation"></a>
### The `tiff:PhotometricInterpretation` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.tiff.photometricInterpretation` |
| ID | `tiff:PhotometricInterpretation` |
| Name | photometricInterpretation |
| Label | – |
| Definiton | Pixel Composition: 2 = RGB, 6 = YCbCr. |
| Options | 2; 6 |
| Required? | No |
| Type | Integer |

<a id="xmp-tiff-planarconfiguration"></a>
### The `tiff:PlanarConfiguration` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.tiff.planarConfiguration` |
| ID | `tiff:PlanarConfiguration` |
| Name | planarConfiguration |
| Label | – |
| Definiton | Data layout: 1 = chunky, 2 = planar. |
| Options | 1; 2 |
| Required? | No |
| Type | Integer |

<a id="xmp-tiff-primarychromaticities"></a>
### The `tiff:PrimaryChromaticities` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.tiff.primaryChromaticities` |
| ID | `tiff:PrimaryChromaticities` |
| Name | primaryChromaticities |
| Label | – |
| Definiton | Chromaticity of the three primary colors. |
| Multiple? | Yes |
| Ordered? | Yes |
| Required? | No |
| Type | Rational |

<a id="xmp-tiff-referenceblackwhite"></a>
### The `tiff:ReferenceBlackWhite` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.tiff.referenceBlackWhite` |
| ID | `tiff:ReferenceBlackWhite` |
| Name | referenceBlackWhite |
| Label | – |
| Definiton | Reference black and white point values. |
| Multiple? | Yes |
| Ordered? | Yes |
| Required? | No |
| Type | Rational |

<a id="xmp-tiff-resolutionunit"></a>
### The `tiff:ResolutionUnit` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.tiff.resolutionUnit` |
| ID | `tiff:ResolutionUnit` |
| Name | resolutionUnit |
| Label | – |
| Definiton | Unit used for XResolution and YResolution. Value is one of 2 = Inches, 3 = Centimeters. |
| Options | 2; 3 |
| Required? | No |
| Type | Integer |

<a id="xmp-tiff-samplesperpixel"></a>
### The `tiff:SamplesPerPixel` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.tiff.samplesPerPixel` |
| ID | `tiff:SamplesPerPixel` |
| Name | samplesPerPixel |
| Label | – |
| Definiton | Number of components per pixel. |
| Required? | No |
| Type | Integer |

<a id="xmp-tiff-software"></a>
### The `tiff:Software` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.tiff.software` |
| ID | `tiff:Software` |
| Name | software |
| Label | – |
| Definiton | Software or firmware used to generate image. NOTE: This property is stored in XMP as xmp:CreatorTool. |
| Required? | No |
| Type | AgentName |

<a id="xmp-tiff-transferfunction"></a>
### The `tiff:TransferFunction` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.tiff.transferFunction` |
| ID | `tiff:TransferFunction` |
| Name | transferFunction |
| Label | – |
| Count/Length | 768 |
| Definiton | Transfer function for image described in tabular style with 3 * 256 entries. |
| Multiple? | Yes |
| Ordered? | Yes |
| Required? | No |
| Type | Integer |

<a id="xmp-tiff-whitepoint"></a>
### The `tiff:WhitePoint` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.tiff.whitePoint` |
| ID | `tiff:WhitePoint` |
| Name | whitePoint |
| Label | – |
| Definiton | Chromaticity of white point. |
| Multiple? | Yes |
| Ordered? | Yes |
| Required? | No |
| Type | Rational |

<a id="xmp-tiff-xresolution"></a>
### The `tiff:XResolution` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.tiff.XResolution` |
| ID | `tiff:XResolution` |
| Name | XResolution |
| Label | – |
| Definiton | Horizontal resolution in pixels per unit. |
| Required? | No |
| Type | Rational |

<a id="xmp-tiff-yresolution"></a>
### The `tiff:YResolution` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.tiff.YResolution` |
| ID | `tiff:YResolution` |
| Name | YResolution |
| Label | – |
| Definiton | Vertical resolution in pixels per unit. |
| Required? | No |
| Type | Rational |

<a id="xmp-tiff-ycbcrcoefficients"></a>
### The `tiff:YCbCrCoefficients` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.tiff.YCbCrCoefficients` |
| ID | `tiff:YCbCrCoefficients` |
| Name | YCbCrCoefficients |
| Label | – |
| Definiton | Matrix coefficients for RGB to YCbCr transformation. |
| Multiple? | Yes |
| Ordered? | Yes |
| Required? | No |
| Type | Rational |

<a id="xmp-tiff-ycbcrpositioning"></a>
### The `tiff:YCbCrPositioning` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.tiff.YCbCrPositioning` |
| ID | `tiff:YCbCrPositioning` |
| Name | YCbCrPositioning |
| Label | – |
| Definiton | Position of chrominance vs. luminance components: 1 = centered, 2 = co-sited. |
| Options | 1; 2 |
| Required? | No |
| Type | Integer |

<a id="xmp-tiff-ycbcrsubsampling"></a>
### The `tiff:YCbCrSubSampling` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.tiff.YCbCrSubSampling` |
| ID | `tiff:YCbCrSubSampling` |
| Name | YCbCrSubSampling |
| Label | – |
| Definiton | Sampling ratio of chrominance components: [2,1] = YCbCr4:2:2, [2,2] = YCbCr4:2:0. |
| Multiple? | Yes |
| Ordered? | Yes |
| Required? | No |
| Type | Integer |


The XMP metadata model's `dc` namespace offers fifteen fields which are listed below along with a link to each field's technical information:

| Namespace  | Field Path | Field Name | Required? | Info |
|------------|------------|------------|:---------:|------|
| `dc` | `xmp.dc.Contributor` | Contributor | No | [🔗](#xmp-dc-contributor) |
| `dc` | `xmp.dc.Coverage` | Coverage | No | [🔗](#xmp-dc-coverage) |
| `dc` | `xmp.dc.Creator` | Creator | No | [🔗](#xmp-dc-creator) |
| `dc` | `xmp.dc.date` | date | No | [🔗](#xmp-dc-date) |
| `dc` | `xmp.dc.Description` | Description | No | [🔗](#xmp-dc-description) |
| `dc` | `xmp.dc.Format` | Format | No | [🔗](#xmp-dc-format) |
| `dc` | `xmp.dc.Identifier` | Identifier | No | [🔗](#xmp-dc-identifier) |
| `dc` | `xmp.dc.Language` | Language | No | [🔗](#xmp-dc-language) |
| `dc` | `xmp.dc.Publisher` | Publisher | No | [🔗](#xmp-dc-publisher) |
| `dc` | `xmp.dc.Relation` | Relation | No | [🔗](#xmp-dc-relation) |
| `dc` | `xmp.dc.Rights` | Rights | No | [🔗](#xmp-dc-rights) |
| `dc` | `xmp.dc.Source` | Source | No | [🔗](#xmp-dc-source) |
| `dc` | `xmp.dc.Subject` | Subject | No | [🔗](#xmp-dc-subject) |
| `dc` | `xmp.dc.Title` | Title | No | [🔗](#xmp-dc-title) |
| `dc` | `xmp.dc.Type` | Type | No | [🔗](#xmp-dc-type) |

The technical details of each field may be found below:

<a id="xmp-dc-contributor"></a>
### The `dc:contributor` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dc.Contributor` |
| ID | `dc:contributor` |
| Name | Contributor |
| Label | – |
| Definiton | DCMI definition: An entity responsible for making contributions to the resource. DCMI comment: Examples of a contributor include a person, an organization, or a service. Typically, the name of a contributor should be used to indicate the entity. XMP addition: XMP usage is a list of contributors. These contributors should not include those listed in dc:creator. |
| Multiple? | Yes |
| Ordered? | No |
| Pseudonym | exiftool: -XMP-dc:Contributor |
| Required? | No |
| Type | ProperName |

<a id="xmp-dc-coverage"></a>
### The `dc:coverage` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dc.Coverage` |
| ID | `dc:coverage` |
| Name | Coverage |
| Label | – |
| Definiton | DCMI definition: The spatial or temporal topic of the resource, the spatial applicability of the resource, or the jurisdiction under which the resource is relevant. XMP addition: XMP usage is the extent or scope of the resource. |
| Pseudonym | exiftool: -XMP-dc:Coverage |
| Required? | No |
| Type | Text |

<a id="xmp-dc-creator"></a>
### The `dc:creator` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dc.Creator` |
| ID | `dc:creator` |
| Name | Creator |
| Label | – |
| Definiton | DCMI definition: An entity primarily responsible for making the resource. DCMI comment: Examples of a creator include a person, an organization, or a service. Typically, the name of a creator should be used to indicate the entity. XMP addition: XMP usage is a list of creators. Entities should be listed in order of decreasing precedence, if such order is significant. |
| Multiple? | Yes |
| Ordered? | Yes |
| Pseudonym | exiftool: -XMP-dc:Creator |
| Required? | No |
| Type | ProperName |

<a id="xmp-dc-date"></a>
### The `dc:date` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dc.date` |
| ID | `dc:date` |
| Name | date |
| Label | – |
| Definiton | DCMI definition: A point or period of time associated with an event in the life cycle of the resource. |
| Multiple? | Yes |
| Ordered? | Yes |
| Pseudonym | exiftool: -XMP-dc:Date |
| Required? | No |
| Type | Date |

<a id="xmp-dc-description"></a>
### The `dc:description` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dc.Description` |
| ID | `dc:description` |
| Name | Description |
| Label | – |
| Combine? | Yes |
| Definiton | DCMI definition: An account of the resource. XMP addition: XMP usage is a list of textual descriptions of the content of the resource, given in various languages. |
| Pseudonym | exiftool: -XMP-dc:Description |
| Required? | No |
| Type | LanguageAlternative |

<a id="xmp-dc-format"></a>
### The `dc:format` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dc.Format` |
| ID | `dc:format` |
| Name | Format |
| Label | – |
| Definiton | DCMI definition: The file format, physical medium, or dimensions of the resource. DCMI comment: Examples of dimensions include size and duration. Recommended best practice is to use a controlled vocabulary such as the list of Internet Media Types [MIME]. XMP addition: XMP usage is a MIME type. Dimensions would be stored using a media-specific property, beyond the scope of this document. |
| Pseudonym | exiftool: -XMP-dc:Format |
| Required? | No |
| Type | MIMEType |

<a id="xmp-dc-identifier"></a>
### The `dc:identifier` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dc.Identifier` |
| ID | `dc:identifier` |
| Name | Identifier |
| Label | – |
| Definiton | DCMI definition: An unambiguous reference to the resource within a given context. DCMI comment: Recommended best practice is to identify the resource by means of a string conforming to a formal identification system. |
| Pseudonym | exiftool: -XMP-dc:Identifier |
| Required? | No |
| Type | Text |

<a id="xmp-dc-language"></a>
### The `dc:language` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dc.Language` |
| ID | `dc:language` |
| Name | Language |
| Label | – |
| Definiton | DCMI definition: A language of the resource. XMP addition: XMP usage is a list of languages used in the content of the resource. |
| Multiple? | Yes |
| Ordered? | No |
| Pseudonym | exiftool: -XMP-dc:Language |
| Required? | No |
| Type | Locale |

<a id="xmp-dc-publisher"></a>
### The `dc:publisher` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dc.Publisher` |
| ID | `dc:publisher` |
| Name | Publisher |
| Label | – |
| Definiton | DCMI definition: An entity responsible for making the resource available. DCMI comment: Examples of a publisher include a person, an organization, or a service. Typically, the name of a publisher should be used to indicate the entity. XMP addition: XMP usage is a list of publishers. |
| Multiple? | Yes |
| Ordered? | No |
| Pseudonym | exiftool: -XMP-dc:Publisher |
| Required? | No |
| Type | ProperName |

<a id="xmp-dc-relation"></a>
### The `dc:relation` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dc.Relation` |
| ID | `dc:relation` |
| Name | Relation |
| Label | – |
| Definiton | DCMI definition: A related resource.DCMI comment: Recommended best practice is to identify the related resource by means of a string conforming to a formal identification system. XMP addition: XMP usage is a list of related resources. |
| Multiple? | Yes |
| Ordered? | No |
| Pseudonym | exiftool: -XMP-dc:Relation |
| Required? | No |
| Type | Text |

<a id="xmp-dc-rights"></a>
### The `dc:rights` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dc.Rights` |
| ID | `dc:rights` |
| Name | Rights |
| Label | – |
| Combine? | Yes |
| Definiton | DCMI definition: Information about rights held in and over the resource. DCMI comment: Typically, rights information includes a statement about various property rights associated with the resource, including intellectual property rights. XMP addition: XMP usage is a list of informal rights statements, given in various languages. |
| Pseudonym | exiftool: -XMP-dc:Rights |
| Required? | No |
| Type | LanguageAlternative |

<a id="xmp-dc-source"></a>
### The `dc:source` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dc.Source` |
| ID | `dc:source` |
| Name | Source |
| Label | – |
| Definiton | DCMI definition: A related resource from which the described resource is derived. DCMI comment: The described resource may be derived from the related resource in whole or in part. Recommended best practice is to identify the related resource by means of a string conforming to a formal identification system. |
| Pseudonym | exiftool: -XMP-dc:Source |
| Required? | No |
| Type | Text |

<a id="xmp-dc-subject"></a>
### The `dc:subject` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dc.Subject` |
| ID | `dc:subject` |
| Name | Subject |
| Label | – |
| Definiton | DCMI definition: The topic of the resource.DCMI comment: Typically, the subject will be represented using keywords, key phrases, or classification codes. Recommended best practice is to use a controlled vocabulary. To describe the spatial or temporal topic of the resource, use the dc:coverage element. XMP addition: XMP usage is a list of descriptive phrases or keywords that specify the content of the resource. |
| Multiple? | Yes |
| Ordered? | No |
| Pseudonym | exiftool: -XMP-dc:Subject |
| Required? | No |
| Type | Text |

<a id="xmp-dc-title"></a>
### The `dc:title` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dc.Title` |
| ID | `dc:title` |
| Name | Title |
| Label | – |
| Combine? | Yes |
| Definiton | DCMI definition: A name given to the resource. DCMI comment: Typically, a title will be a name by which the resource is formally known. XMP addition: XMP usage is a title or name, given in various languages. |
| Pseudonym | exiftool: -XMP-dc:Title |
| Required? | No |
| Type | LanguageAlternative |

<a id="xmp-dc-type"></a>
### The `dc:type` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.dc.Type` |
| ID | `dc:type` |
| Name | Type |
| Label | – |
| Definiton | DCMI definition: The nature or genre of the resource. DCMI comment: Recommended best practice is to use a controlled vocabulary such as the DCMI Type Vocabulary [DCMITYPE]. To describe the file format, physical medium, or dimensions of the resource, use the dc:format element. XMP addition: See the dc:format entry for clarification of the XMP usage of that element. |
| Multiple? | Yes |
| Ordered? | No |
| Pseudonym | exiftool: -XMP-dc:Type |
| Required? | No |
| Type | Text |


The XMP metadata model's `iptc_core` namespace offers thirteen fields which are listed below along with a link to each field's technical information:

| Namespace  | Field Path | Field Name | Required? | Info |
|------------|------------|------------|:---------:|------|
| `iptc_core` | `xmp.iptc.creatorContactInfo` | creatorContactInfo | No | [🔗](#xmp-iptc_core-creatorcontactinfo) |
| `iptc_core` | `xmp.iptc.CreatorContactAddress` | CreatorContactAddress | No | [🔗](#xmp-iptc_core-creatorcontactaddress) |
| `iptc_core` | `xmp.iptc.CreatorContactCity` | CreatorContactCity | No | [🔗](#xmp-iptc_core-creatorcontactcity) |
| `iptc_core` | `xmp.iptc.CreatorContactCountry` | CreatorContactCountry | No | [🔗](#xmp-iptc_core-creatorcontactcountry) |
| `iptc_core` | `xmp.iptc.CreatorContactPostalCode` | CreatorContactPostalCode | No | [🔗](#xmp-iptc_core-creatorcontactpostalcode) |
| `iptc_core` | `xmp.iptc.CreatorContactRegion` | CreatorContactRegion | No | [🔗](#xmp-iptc_core-creatorcontactregion) |
| `iptc_core` | `xmp.iptc.CreatorContactWorkEmail` | CreatorContactWorkEmail | No | [🔗](#xmp-iptc_core-creatorcontactworkemail) |
| `iptc_core` | `xmp.iptc.CreatorContactWorkURL` | CreatorContactWorkURL | No | [🔗](#xmp-iptc_core-creatorcontactworkurl) |
| `iptc_core` | `xmp.iptc.intellectualGenre` | intellectualGenre | No | [🔗](#xmp-iptc_core-intellectualgenre) |
| `iptc_core` | `xmp.iptc.scene` | scene | No | [🔗](#xmp-iptc_core-scene) |
| `iptc_core` | `xmp.iptc.location` | location | No | [🔗](#xmp-iptc_core-location) |
| `iptc_core` | `xmp.iptc.countryCode` | countryCode | No | [🔗](#xmp-iptc_core-countrycode) |
| `iptc_core` | `xmp.iptc.subjectCode` | subjectCode | No | [🔗](#xmp-iptc_core-subjectcode) |

The technical details of each field may be found below:

<a id="xmp-iptc_core-creatorcontactinfo"></a>
### The `Iptc4xmpCore:CreatorContactInfo` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.iptc.creatorContactInfo` |
| ID | `Iptc4xmpCore:CreatorContactInfo` |
| Name | creatorContactInfo |
| Label | – |
| Definiton | The creator contact information provides all necessary information to get in contact with the creator of this news object and comprises a set of sub-properties for proper addressing. |
| Pseudonym | exiftool: XMP-iptcCore:CreatorContactInfo |
| Required? | No |
| Structure | Iptc4xmpCore:CreatorContactInfo |
| Type | ContactInfo |

<a id="xmp-iptc_core-creatorcontactaddress"></a>
### The `Iptc4xmpCore:CiAdrExtadr` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.iptc.CreatorContactAddress` |
| ID | `Iptc4xmpCore:CiAdrExtadr` |
| Name | CreatorContactAddress |
| Label | – |
| Definiton | – |
| Pseudonym | exiftool: CreatorAddress |
| Required? | No |
| Structure | Iptc4xmpCore:CreatorContactInfo |
| Type | Text |

<a id="xmp-iptc_core-creatorcontactcity"></a>
### The `Iptc4xmpCore:CiAdrCity` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.iptc.CreatorContactCity` |
| ID | `Iptc4xmpCore:CiAdrCity` |
| Name | CreatorContactCity |
| Label | – |
| Definiton | – |
| Pseudonym | exiftool: CreatorCity |
| Required? | No |
| Structure | Iptc4xmpCore:CreatorContactInfo |
| Type | Text |

<a id="xmp-iptc_core-creatorcontactcountry"></a>
### The `Iptc4xmpCore:CiAdrCtry` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.iptc.CreatorContactCountry` |
| ID | `Iptc4xmpCore:CiAdrCtry` |
| Name | CreatorContactCountry |
| Label | – |
| Definiton | – |
| Pseudonym | exiftool: CreatorCountry |
| Required? | No |
| Structure | Iptc4xmpCore:CreatorContactInfo |
| Type | Text |

<a id="xmp-iptc_core-creatorcontactpostalcode"></a>
### The `Iptc4xmpCore:CiAdrPcode` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.iptc.CreatorContactPostalCode` |
| ID | `Iptc4xmpCore:CiAdrPcode` |
| Name | CreatorContactPostalCode |
| Label | – |
| Definiton | – |
| Pseudonym | exiftool: CreatorPostalCode |
| Required? | No |
| Structure | Iptc4xmpCore:CreatorContactInfo |
| Type | Text |

<a id="xmp-iptc_core-creatorcontactregion"></a>
### The `Iptc4xmpCore:CiAdrRegion` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.iptc.CreatorContactRegion` |
| ID | `Iptc4xmpCore:CiAdrRegion` |
| Name | CreatorContactRegion |
| Label | – |
| Definiton | – |
| Pseudonym | exiftool: CreatorRegion |
| Required? | No |
| Structure | Iptc4xmpCore:CreatorContactInfo |
| Type | Text |

<a id="xmp-iptc_core-creatorcontactworkemail"></a>
### The `Iptc4xmpCore:CiEmailWork` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.iptc.CreatorContactWorkEmail` |
| ID | `Iptc4xmpCore:CiEmailWork` |
| Name | CreatorContactWorkEmail |
| Label | – |
| Definiton | – |
| Pseudonym | exiftool: CreatorWorkEmail |
| Required? | No |
| Structure | Iptc4xmpCore:CreatorContactInfo |
| Type | Text |

<a id="xmp-iptc_core-creatorcontactworkurl"></a>
### The `Iptc4xmpCore:CiUrlWork` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.iptc.CreatorContactWorkURL` |
| ID | `Iptc4xmpCore:CiUrlWork` |
| Name | CreatorContactWorkURL |
| Label | – |
| Definiton | – |
| Pseudonym | exiftool: CreatorWorkURL |
| Required? | No |
| Structure | Iptc4xmpCore:CreatorContactInfo |
| Type | URL |

<a id="xmp-iptc_core-intellectualgenre"></a>
### The `Iptc4xmpCore:IntellectualGenre` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.iptc.intellectualGenre` |
| ID | `Iptc4xmpCore:IntellectualGenre` |
| Name | intellectualGenre |
| Label | – |
| Definiton | Describes the nature, intellectual or journalistic characteristic of a news object, not specifically its content. |
| Required? | No |
| Type | Text |

<a id="xmp-iptc_core-scene"></a>
### The `Iptc4xmpCore:Scene` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.iptc.scene` |
| ID | `Iptc4xmpCore:Scene` |
| Name | scene |
| Label | – |
| Definiton | Describes the scene of a photo content. Specifies one ore more terms from the IPTC Scene-NewsCodes. Each Scene is represented as a string of 6 digits in an unordered list. |
| Multiple? | Yes |
| Ordered? | No |
| Required? | No |
| Type | Text |

<a id="xmp-iptc_core-location"></a>
### The `Iptc4xmpCore:Location` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.iptc.location` |
| ID | `Iptc4xmpCore:Location` |
| Name | location |
| Label | – |
| Definiton | Name of a location the content is focussing on -- either the location shown in visual media or referenced by text or audio media. This location name could either be the name of a sublocation to a city or the name of a well known location or (natural) monument outside a city. In the sense of a sublocation to a city this element is at the fourth level of a top-down geographical hierarchy. |
| Required? | No |
| Type | Text |

<a id="xmp-iptc_core-countrycode"></a>
### The `Iptc4xmpCore:CountryCode` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.iptc.countryCode` |
| ID | `Iptc4xmpCore:CountryCode` |
| Name | countryCode |
| Label | – |
| Definiton | Code of the country the content is focussing on -- either the country shown in visual media or referenced in text or audio media. This element is at the top/first level of a top-down geographical hierarchy. The code should be taken from ISO 3166 two or three letter code. The full name of a country should go to the "Country" element. |
| Required? | No |
| Type | Locale |

<a id="xmp-iptc_core-subjectcode"></a>
### The `Iptc4xmpCore:SubjectCode` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.iptc.subjectCode` |
| ID | `Iptc4xmpCore:SubjectCode` |
| Name | subjectCode |
| Label | – |
| Definiton | Specifies one or more Subjects from the IPTC Subject-NewsCodes taxonomy to categorize the content. Each Subject is represented as a string of 8 digits in an unordered list. |
| Multiple? | Yes |
| Ordered? | No |
| Required? | No |
| Type | Text |


The XMP metadata model's `iptc_extended` namespace offers seventeen fields which are listed below along with a link to each field's technical information:

| Namespace  | Field Path | Field Name | Required? | Info |
|------------|------------|------------|:---------:|------|
| `iptc_extended` | `xmp.iptc.AOCircaDateCreated` | AOCircaDateCreated | No | [🔗](#xmp-iptc_extended-aocircadatecreated) |
| `iptc_extended` | `xmp.iptc.AOContentDescription` | AOContentDescription | No | [🔗](#xmp-iptc_extended-aocontentdescription) |
| `iptc_extended` | `xmp.iptc.AOContributionDescription` | AOContributionDescription | No | [🔗](#xmp-iptc_extended-aocontributiondescription) |
| `iptc_extended` | `xmp.iptc.AOCopyrightNotice` | AOCopyrightNotice | No | [🔗](#xmp-iptc_extended-aocopyrightnotice) |
| `iptc_extended` | `xmp.iptc.AOCreator` | AOCreator | No | [🔗](#xmp-iptc_extended-aocreator) |
| `iptc_extended` | `xmp.iptc.AOCreatorID` | AOCreatorID | No | [🔗](#xmp-iptc_extended-aocreatorid) |
| `iptc_extended` | `xmp.iptc.AOCurrentCopyrightOwnerID` | AOCurrentCopyrightOwnerID | No | [🔗](#xmp-iptc_extended-aocurrentcopyrightownerid) |
| `iptc_extended` | `xmp.iptc.AOCurrentCopyrightOwnerName` | AOCurrentCopyrightOwnerName | No | [🔗](#xmp-iptc_extended-aocurrentcopyrightownername) |
| `iptc_extended` | `xmp.iptc.AOCurrentLicensorID` | AOCurrentLicensorID | No | [🔗](#xmp-iptc_extended-aocurrentlicensorid) |
| `iptc_extended` | `xmp.iptc.AOCurrentLicensorName` | AOCurrentLicensorName | No | [🔗](#xmp-iptc_extended-aocurrentlicensorname) |
| `iptc_extended` | `xmp.iptc.AODateCreated` | AODateCreated | No | [🔗](#xmp-iptc_extended-aodatecreated) |
| `iptc_extended` | `xmp.iptc.AOPhysicalDescription` | AOPhysicalDescription | No | [🔗](#xmp-iptc_extended-aophysicaldescription) |
| `iptc_extended` | `xmp.iptc.AOSource` | AOSource | No | [🔗](#xmp-iptc_extended-aosource) |
| `iptc_extended` | `xmp.iptc.AOSourceInvNo` | AOSourceInvNo | No | [🔗](#xmp-iptc_extended-aosourceinvno) |
| `iptc_extended` | `xmp.iptc.AOSourceInvURL` | AOSourceInvURL | No | [🔗](#xmp-iptc_extended-aosourceinvurl) |
| `iptc_extended` | `xmp.iptc.AOStylePeriod` | AOStylePeriod | No | [🔗](#xmp-iptc_extended-aostyleperiod) |
| `iptc_extended` | `xmp.iptc.AOTitle` | AOTitle | No | [🔗](#xmp-iptc_extended-aotitle) |

The technical details of each field may be found below:

<a id="xmp-iptc_extended-aocircadatecreated"></a>
### The `Iptc4xmpExt:AOCircaDateCreated` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.iptc.AOCircaDateCreated` |
| ID | `Iptc4xmpExt:AOCircaDateCreated` |
| Name | AOCircaDateCreated |
| Label | – |
| Alias | ArtworkOrObjectCircaDateCreated; ArtworkCircaDateCreated; ObjectCircaDateCreated |
| Definiton | Approximate date or range of dates associated with the creation and production of an artwork or object or its components. |
| Pseudonym | exiftool: ArtworkCircaDateCreated |
| Required? | No |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | Text |

<a id="xmp-iptc_extended-aocontentdescription"></a>
### The `Iptc4xmpExt:AOContentDescription` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.iptc.AOContentDescription` |
| ID | `Iptc4xmpExt:AOContentDescription` |
| Name | AOContentDescription |
| Label | – |
| Alias | ArtworkOrObjectContentDescription; ArtworkContentDescription; ObjectContentDescription |
| Definiton | A textual description of the content depicted in the artwork or object. |
| Pseudonym | exiftool: ArtworkContentDescription |
| Required? | No |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | Text |

<a id="xmp-iptc_extended-aocontributiondescription"></a>
### The `Iptc4xmpExt:AOContributionDescription` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.iptc.AOContributionDescription` |
| ID | `Iptc4xmpExt:AOContributionDescription` |
| Name | AOContributionDescription |
| Label | – |
| Alias | ArtworkOrObjectContributionDescription; ArtworkContributionDescription; ObjectContributionDescription |
| Definiton | A textual description about a contribution made to an artwork or an object. |
| Required? | No |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | Text |

<a id="xmp-iptc_extended-aocopyrightnotice"></a>
### The `Iptc4xmpExt:AOCopyrightNotice` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.iptc.AOCopyrightNotice` |
| ID | `Iptc4xmpExt:AOCopyrightNotice` |
| Name | AOCopyrightNotice |
| Label | – |
| Alias | ArtworkOrObjectCopyrightNotice; ArtworkCopyrightNotice; ObjectCopyrightNotice |
| Definiton | Contains any necessary copyright notice for claiming the intellectual property for artwork or an object in the image and should identify the current owner of the copyright of this work with associated intellectual property rights. |
| Pseudonym | exiftool: ArtworkCopyrightNotice |
| Required? | No |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | Text |

<a id="xmp-iptc_extended-aocreator"></a>
### The `Iptc4xmpExt:AOCreator` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.iptc.AOCreator` |
| ID | `Iptc4xmpExt:AOCreator` |
| Name | AOCreator |
| Label | – |
| Alias | ArtworkOrObjectCreator; ArtworkCreator; ObjectCreator |
| Definiton | Contains the name of the artist who has created artwork or an object in the image. In cases where the artist could or should not be identified the name of a company or organisation may be appropriate. |
| Pseudonym | exiftool: ArtworkCreator |
| Required? | No |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | Text |

<a id="xmp-iptc_extended-aocreatorid"></a>
### The `Iptc4xmpExt:AOCreatorID` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.iptc.AOCreatorID` |
| ID | `Iptc4xmpExt:AOCreatorID` |
| Name | AOCreatorID |
| Label | – |
| Alias | ArtworkOrObjectCreatorID; ArtworkCreatorID; ObjectCreatorID |
| Definiton | Globally unique identifier for the creator of artwork or object. |
| Pseudonym | exiftool: ArtworkCreatorID |
| Required? | No |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | Text |

<a id="xmp-iptc_extended-aocurrentcopyrightownerid"></a>
### The `Iptc4xmpExt:AOCurrentCopyrightOwnerID` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.iptc.AOCurrentCopyrightOwnerID` |
| ID | `Iptc4xmpExt:AOCurrentCopyrightOwnerID` |
| Name | AOCurrentCopyrightOwnerID |
| Label | – |
| Alias | ArtworkOrObjectCopyrightOwnerID; ArtworkCopyrightOwnerID; ObjectCopyrightOwnerID |
| Definiton | Globally unique identifier for the current owner of the copyright of the artwork or object. |
| Pseudonym | exiftool: ArtworkCopyrightOwnerID |
| Required? | No |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | Text |

<a id="xmp-iptc_extended-aocurrentcopyrightownername"></a>
### The `Iptc4xmpExt:AOCurrentCopyrightOwnerName` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.iptc.AOCurrentCopyrightOwnerName` |
| ID | `Iptc4xmpExt:AOCurrentCopyrightOwnerName` |
| Name | AOCurrentCopyrightOwnerName |
| Label | – |
| Alias | ArtworkOrObjectCopyrightOwnerName; ArtworkCopyrightOwnerName; ObjectCopyrightOwnerName |
| Definiton | Name of the current owner of the copyright of the artwork or object. |
| Pseudonym | exiftool: ArtworkCopyrightOwnerName |
| Required? | No |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | Text |

<a id="xmp-iptc_extended-aocurrentlicensorid"></a>
### The `Iptc4xmpExt:AOCurrentLicensorID` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.iptc.AOCurrentLicensorID` |
| ID | `Iptc4xmpExt:AOCurrentLicensorID` |
| Name | AOCurrentLicensorID |
| Label | – |
| Alias | ArtworkOrObjectCurrentLicensorID; ArtworkCurrentLicensorID; ObjectCurrentLicensorID |
| Definiton | Globally unique identifier for the current licensor of the artwork or object. |
| Pseudonym | exiftool: ArtworkCurrentLicensorID |
| Required? | No |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | Text |

<a id="xmp-iptc_extended-aocurrentlicensorname"></a>
### The `Iptc4xmpExt:AOCurrentLicensorName` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.iptc.AOCurrentLicensorName` |
| ID | `Iptc4xmpExt:AOCurrentLicensorName` |
| Name | AOCurrentLicensorName |
| Label | – |
| Alias | ArtworkOrObjectCurrentLicensorName; ArtworkCurrentLicensorName; ObjectCurrentLicensorName |
| Definiton | Name of the current licensor of the artwork or object. |
| Pseudonym | exiftool: ArtworkCurrentLicensorName |
| Required? | No |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | Text |

<a id="xmp-iptc_extended-aodatecreated"></a>
### The `Iptc4xmpExt:AODateCreated` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.iptc.AODateCreated` |
| ID | `Iptc4xmpExt:AODateCreated` |
| Name | AODateCreated |
| Label | – |
| Alias | ArtworkOrObjectDateCreated; ArtworkDateCreated; ObjectDateCreated |
| Definiton | Designates the date and optionally the time the artwork or object in the image was created. This relates to artwork or objects with associated intellectual property rights. |
| Pseudonym | exiftool: ArtworkDateCreated |
| Required? | No |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | DateTime |

<a id="xmp-iptc_extended-aophysicaldescription"></a>
### The `Iptc4xmpExt:AOPhysicalDescription` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.iptc.AOPhysicalDescription` |
| ID | `Iptc4xmpExt:AOPhysicalDescription` |
| Name | AOPhysicalDescription |
| Label | – |
| Alias | ArtworkOrObjectPhysicalDescription; ArtworkPhysicalDescription; ObjectPhysicalDescription |
| Definiton | A textual description of the physical characteristics of the artwork or object, without reference to the content depicted. |
| Pseudonym | exiftool: ArtworkPhysicalDescription |
| Required? | No |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | Text |

<a id="xmp-iptc_extended-aosource"></a>
### The `Iptc4xmpExt:AOSource` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.iptc.AOSource` |
| ID | `Iptc4xmpExt:AOSource` |
| Name | AOSource |
| Label | – |
| Alias | ArtworkOrObjectSource; ArtworkSource; ObjectSource |
| Definiton | The organisation or body holding and registering the artwork or object in the image for inventory purposes. |
| Pseudonym | exiftool: ArtworkSource |
| Required? | No |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | Text |

<a id="xmp-iptc_extended-aosourceinvno"></a>
### The `Iptc4xmpExt:AOSourceInvNo` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.iptc.AOSourceInvNo` |
| ID | `Iptc4xmpExt:AOSourceInvNo` |
| Name | AOSourceInvNo |
| Label | – |
| Alias | ArtworkOrObjectSourceInventoryNo; ArtworkSourceInventoryNo; ObjectSourceInventoryNo |
| Definiton | The inventory number issued by the organisation or body holding and registering the artwork or object in the image. |
| Pseudonym | exiftool: ArtworkSourceInventoryNo |
| Required? | No |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | Text |

<a id="xmp-iptc_extended-aosourceinvurl"></a>
### The `Iptc4xmpExt:AOSourceInvURL` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.iptc.AOSourceInvURL` |
| ID | `Iptc4xmpExt:AOSourceInvURL` |
| Name | AOSourceInvURL |
| Label | – |
| Alias | ArtworkOrObjectSourceInventoryURL; ArtworkSourceInventoryURL; ObjectSourceInventoryURL |
| Definiton | URL reference to the metadata record of the inventory maintained by the Source. |
| Pseudonym | exiftool: ArtworkSourceInvURL |
| Required? | No |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | URL |

<a id="xmp-iptc_extended-aostyleperiod"></a>
### The `Iptc4xmpExt:AOStylePeriod` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.iptc.AOStylePeriod` |
| ID | `Iptc4xmpExt:AOStylePeriod` |
| Name | AOStylePeriod |
| Label | – |
| Alias | ArtworkOrObjectStylePeriod; ArtworkStylePeriod; ObjectStylePeriod |
| Definiton | The style, historical or artistic period, movement, group, or school whose characteristics are represented in the artwork or object. |
| Pseudonym | exiftool: ArtworkStylePeriod |
| Required? | No |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | Text |

<a id="xmp-iptc_extended-aotitle"></a>
### The `Iptc4xmpExt:AOTitle` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `xmp.iptc.AOTitle` |
| ID | `Iptc4xmpExt:AOTitle` |
| Name | AOTitle |
| Label | – |
| Alias | ArtworkOrObjectTitle; ArtworkTitle; ObjectTitle |
| Definiton | A reference for the artwork or object in the image. |
| Pseudonym | exiftool: ArtworkTitle |
| Required? | No |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | Text |



### Credits & References

The XMP field information was researched from various sources including the Adobe® XMP
specification and EXIFTool documentation. Please visit these valuable online resources
to learn more about the XMP metadata model specification and to support these world
class organizations and their products:

 * https://www.adobe.com/products/xmp.html
 * https://exiftool.org/TagNames/XMP.html
