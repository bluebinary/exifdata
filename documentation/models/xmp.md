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

The EXIFData library provides support for reading and writing from the following XMP
fields within unless marked otherwise:

The XMP metadata model has fourteen namespaces which are documented below.

The XMP metadata model's 'basic' namespace offers ten fields which are detailed below:

### The `xmp:Label` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.basic.Label |
| ID | xmp:Label |
| Label | – |
| Name | Label |
| Definiton | A word or short phrase that identifies a resource as a member of a userdefined collection. NOTE: One anticipated usage is to organize resources in a file browser. |
| Pseudonym | exiftool: xmp:Label |
| Type | Text |

### The `xmp:CreateDate` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.basic.CreateDate |
| ID | xmp:CreateDate |
| Label | – |
| Name | CreateDate |
| Alias | CreationDate |
| Definiton | The date and time the resource was created. For a digital file, this need not match a file-system creation time. For a freshly created resource, it should be close to that time, modulo the time taken to write the file. Later file transfer, copying, and so on, can make the file-system time arbitrarily different. |
| Pseudonym | exiftool: xmp:CreateDate |
| Type | Date |

### The `xmp:CreatorTool` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.basic.CreatorTool |
| ID | xmp:CreatorTool |
| Label | – |
| Name | CreatorTool |
| Definiton | The name of the first known tool used to create the resource. |
| Pseudonym | exiftool: xmp:CreatorTool |
| Type | AgentName |

### The `xmp:Identifier` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.basic.Identifier |
| ID | xmp:Identifier |
| Label | – |
| Name | Identifier |
| Definiton | An unordered array of text strings that unambiguously identify the resource within a given context. An array item may be qualified with xmpidq:Scheme to denote the formal identification system to which that identifier conforms. NOTE: The xmp:Identifier property was added because dc:identifier has been defined in the original XMP specification as a single identifier instead of as an array, and changing dc:identifier to an array would break compatibility with existing XMP processors. |
| Multiple? | Yes |
| Ordered? | No |
| Pseudonym | exiftool: xmp:Identifier |
| Type | Text |

### The `xmp:MetadataDate` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.basic.MetadataDate |
| ID | xmp:MetadataDate |
| Label | – |
| Name | MetadataDate |
| Definiton | The date and time that any metadata for this resource was last changed. It should be the same as or more recent than xmp:ModifyDate. |
| Pseudonym | exiftool: xmp:MetadataDate |
| Type | Date |

### The `xmp:ModifyDate` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.basic.ModifyDate |
| ID | xmp:ModifyDate |
| Label | – |
| Name | ModifyDate |
| Alias | ModificationDate |
| Definiton | The date and time the resource was last modified. NOTE: The value of this property is not necessarily the same as the file’s system modification date because it is typically set before the file is saved. |
| Pseudonym | exiftool: xmp:ModifyDate |
| Type | Date |

### The `xmp:Rating` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.basic.Rating |
| ID | xmp:Rating |
| Label | – |
| Name | Rating |
| Definiton | A user-assigned rating for this file. The value shall be -1 or in the range [0..5], where -1 indicates “rejected” and 0 indicates “unrated”. If xmp:Rating is not present, a value of 0 should be assumed. NOTE: Anticipated usage is for a typical “star rating” UI, with the addition of a notion of rejection. |
| Options | -1, 0, 1, 2, 3, 4, 5 |
| Pseudonym | exiftool: xmp:Rating |
| Type | Real |

### The `xmp:BaseURL` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.basic.BaseURL |
| ID | xmp:BaseURL |
| Label | – |
| Name | BaseURL |
| Definiton | The base URL for relative URLs in the document content. If this document contains Internet links, and those links are relative, they are relative to this base URL. This property provides a standard way for embedded relative URLs to be interpreted by tools. Web authoring tools should set the value based on their notion of where URLs will be interpreted. |
| Pseudonym | exiftool: xmp:BaseURL |
| Type | URL |

### The `xmp:Nickname` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.basic.Nickname |
| ID | xmp:Nickname |
| Label | – |
| Name | Nickname |
| Definiton | A short informal name for the resource. |
| Pseudonym | exiftool: xmp:Nickname |
| Type | Text |

### The `xmp:Thumbnail` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.basic.Thumbnail |
| ID | xmp:Thumbnail |
| Label | – |
| Name | Thumbnail |
| Definiton | An alternative array of thumbnail images for a file, which can differ in characteristics such as size or image encoding. |
| Multiple? | Yes |
| Pseudonym | exiftool: xmp:Thumbnail |
| Type | Thumbnail |

The XMP metadata model's 'media_management' namespace offers sixteen fields which are detailed below:

### The `xmpMM:DerivedFrom` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.media_management.derivedFrom |
| ID | xmpMM:DerivedFrom |
| Label | – |
| Name | derivedFrom |
| Definiton | A reference to the original document from which this one is derived. It is a minimal reference; missing components can be assumed to be unchanged. For example, a new version might only need to specify the instance ID and version number of the previous version, or a rendition might only need to specify the instance ID and rendition class of the original. |
| Type | ResourceRef |

### The `xmpMM:DocumentID` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.media_management.documentID |
| ID | xmpMM:DocumentID |
| Label | – |
| Name | documentID |
| Definiton | The common identifier for all versions and renditions of a resource. It should be based on a UUID; Created once for new resources. Different renditions are expected to have different values for xmpMM:DocumentID. |
| Type | GUID |

### The `xmpMM:InstanceID` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.media_management.instanceID |
| ID | xmpMM:InstanceID |
| Label | – |
| Name | instanceID |
| Definiton | An identifier for a specific incarnation of a resource, updated each time a file is saved. It should be based on a UUID. |
| Type | GUID |

### The `xmpMM:OriginalDocumentID` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.media_management.originalDocumentID |
| ID | xmpMM:OriginalDocumentID |
| Label | – |
| Name | originalDocumentID |
| Definiton | The common identifier for the original resource from which the current resource is derived. For example, if you save a resource to a different format, then save that one to another format, each save operation should generate a new xmpMM:DocumentID that uniquely identifies the resource in that format, but should retain the ID of the source file here. It links a resource to its original source. |
| Type | GUID |

### The `xmpMM:RenditionClass` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.media_management.renditionClass |
| ID | xmpMM:RenditionClass |
| Label | – |
| Name | renditionClass |
| Definiton | The rendition class name for this resource. This property should be absent or set to default for a document version that is not a derived rendition. |
| Type | RenditionClass |

### The `xmpMM:RenditionParams` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.media_management.renditionParams |
| ID | xmpMM:RenditionParams |
| Label | – |
| Name | renditionParams |
| Definiton | Can be used to provide additional rendition parameters that are too complex or verbose to encode in xmpMM: RenditionClass. |
| Type | Text |

### The `xmpMM:History` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.media_management.history |
| ID | xmpMM:History |
| Label | – |
| Name | history |
| Definiton | An ordered array of high-level user actions that resulted in this resource. It is intended to give human readers a description of the steps taken to make the changes from the previous version to this one. The list should be at an abstract level; it is not intended to be an exhaustive keystroke or other detailed history. The description should be sufficient for metadata management, as well as for workflow enhancement. |
| Multiple? | Yes |
| Ordered? | Yes |
| Type | ResourceEvent |

### The `xmpMM:Ingredients` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.media_management.ingredients |
| ID | xmpMM:Ingredients |
| Label | – |
| Name | ingredients |
| Definiton | References to resources that were incorporated, by inclusion or reference, into this resource. |
| Multiple? | Yes |
| Ordered? | No |
| Type | ResourceRef |

### The `xmpMM:Pantry` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.media_management.pantry |
| ID | xmpMM:Pantry |
| Label | – |
| Name | pantry |
| Definiton | Each array item has a structure value with a potentially unique set of fields, containing extracted XMP from a component. Each field is a property from the XMP of a contained resource component, with all substructure preserved. Each pantry entry shall contain an xmpMM:InstanceID. Only one copy of the pantry entry for any given xmpMM:InstanceID shall be retained in the pantry. Nested pantry items shall be removed from the individual pantry item and promoted to the top level of the pantry. |
| Multiple? | Yes |
| Ordered? | No |
| Type | Struct |

### The `xmpMM:ManagedFrom` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.media_management.managedFrom |
| ID | xmpMM:ManagedFrom |
| Label | – |
| Name | managedFrom |
| Definiton | A reference to the document as it was prior to becoming managed. It is set when a managed document is introduced to an asset management system that does not currently own it. It may or may not include references to different management systems. |
| Type | ResourceRef |

### The `xmpMM:Manager` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.media_management.manager |
| ID | xmpMM:Manager |
| Label | – |
| Name | manager |
| Definiton | The name of the asset management system that manages this resource. Along with xmpMM: ManagerVariant, it tells applications which asset management system to contact concerning this document. |
| Type | AgentName |

### The `xmpMM:ManageTo` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.media_management.manageTo |
| ID | xmpMM:ManageTo |
| Label | – |
| Name | manageTo |
| Definiton | A URI identifying the managed resource to the asset management system; the presence of this property is the formal indication that this resource is managed. The form and content of this URI is private to the asset management system. |
| Type | URI |

### The `xmpMM:ManageUI` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.media_management.manageUI |
| ID | xmpMM:ManageUI |
| Label | – |
| Name | manageUI |
| Definiton | A URI that can be used to access information about the managed resource through a web browser. It might require a custom browser plug-in. |
| Type | URI |

### The `xmpMM:ManagerVariant` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.media_management.managerVariant |
| ID | xmpMM:ManagerVariant |
| Label | – |
| Name | managerVariant |
| Definiton | Specifies a particular variant of the asset management system. The format of this property is private to the specific asset management system. |
| Type | Text |

### The `xmpMM:VersionID` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.media_management.versionID |
| ID | xmpMM:VersionID |
| Label | – |
| Name | versionID |
| Definiton | The document version identifier for this resource. Each version of a document gets a new identifier, usually simply by incrementing integers 1, 2, 3 . . . and so on. Media management systems can have other conventions or support branching which requires a more complex scheme. |
| Type | Text |

### The `xmpMM:Versions` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.media_management.versions |
| ID | xmpMM:Versions |
| Label | – |
| Name | versions |
| Definiton | The version history associated with this resource. Entry 1 is the oldest known version for this document, entry[last()] is the most recent version. Typically, a media management system would fill in the version information in the metadata on check-in. It is not guaranteed that a complete history of versions from the first to this one will be present in the xmpMM:Versions property. Interior version information can be compressed or eliminated and the version history can be truncated at some point. |
| Multiple? | Yes |
| Ordered? | Yes |
| Type | Version |

The XMP metadata model's 'basic_job_ticket' namespace offers one field which are detailed below:

### The `xmpBJ:JobRef` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.basic_job_ticket.jobRef |
| ID | xmpBJ:JobRef |
| Label | – |
| Name | jobRef |
| Definiton | References an external job management file for a job process in which the document is being used. Use of job names is under user control. Typical use would be to identify all documents that are part of a particular job or contract. There are multiple values because there can be more than one job using a particular document at any time, and it can also be useful to keep historical information about what jobs a document was part of previously. |
| Multiple? | Yes |
| Ordered? | No |
| Type | Job |

The XMP metadata model's 'paged_text' namespace offers five fields which are detailed below:

### The `xmpTPg:Colorants` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.paged_text.colorants |
| ID | xmpTPg:Colorants |
| Label | – |
| Name | colorants |
| Definiton | An ordered array of colorants (swatches) that are used in the document (including any in contained documents). |
| Multiple? | Yes |
| Ordered? | Yes |
| Type | Colorants |

### The `xmpTPg:Fonts` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.paged_text.fonts |
| ID | xmpTPg:Fonts |
| Label | – |
| Name | fonts |
| Definiton | An unordered array of fonts that are used in the document (including any in contained documents). |
| Multiple? | Yes |
| Ordered? | No |
| Type | Font |

### The `xmpTPg:MaxPageSize` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.paged_text.maxPageSize |
| ID | xmpTPg:MaxPageSize |
| Label | – |
| Name | maxPageSize |
| Definiton | The size of the largest page in the document (including any in contained documents). |
| Type | Dimensions |

### The `xmpTPg:NPages` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.paged_text.nPages |
| ID | xmpTPg:NPages |
| Label | – |
| Name | nPages |
| Definiton | The number of pages in the document (including any in contained documents). |
| Type | Integer |

### The `xmpTPg:PlateNames` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.paged_text.plateNames |
| ID | xmpTPg:PlateNames |
| Label | – |
| Name | plateNames |
| Definiton | An ordered array of plate names that are needed to print the document (including any in contained documents). |
| Multiple? | Yes |
| Ordered? | Yes |
| Type | Text |

The XMP metadata model's 'dynamic_media' namespace offers 71 fields which are detailed below:

### The `xmpDM:absPeakAudioFilePath` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.absPeakAudioFilePath |
| ID | xmpDM:absPeakAudioFilePath |
| Label | – |
| Name | absPeakAudioFilePath |
| Definiton | The absolute path to the file’s peak audio file. If empty, no peak file exists. |
| Type | URI |

### The `xmpDM:album` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.album |
| ID | xmpDM:album |
| Label | – |
| Name | album |
| Definiton | The name of the album. |
| Type | Text |

### The `xmpDM:altTapeName` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.altTapeName |
| ID | xmpDM:altTapeName |
| Label | – |
| Name | altTapeName |
| Definiton | An alternative tape name, set via the project window or timecode dialog in Premiere. If an alternative name has been set and has not been reverted, that name is displayed. |
| Type | Text |

### The `xmpDM:altTimecode` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.altTimecode |
| ID | xmpDM:altTimecode |
| Label | – |
| Name | altTimecode |
| Definiton | A timecode set by the user. When specified, it is used instead of the startTimecode. |
| Type | Timecode |

### The `xmpDM:artist` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.artist |
| ID | xmpDM:artist |
| Label | – |
| Name | artist |
| Definiton | The name of the artist or artists. |
| Type | Text |

### The `xmpDM:audioChannelType` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.audioChannelType |
| ID | xmpDM:audioChannelType |
| Label | – |
| Name | audioChannelType |
| Definiton | The audio channel type. One of: Mono, Stereo, 5.1, 7.1, 16 Channel, Other. |
| Options | Mono, Stereo, 5.1, 7.1, 16 Channel, Other |
| Type | Text |

### The `xmpDM:audioCompressor` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.audioCompressor |
| ID | xmpDM:audioCompressor |
| Label | – |
| Name | audioCompressor |
| Definiton | The audio compression used. For example, MP3. |
| Type | Text |

### The `xmpDM:audioSampleRate` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.audioSampleRate |
| ID | xmpDM:audioSampleRate |
| Label | – |
| Name | audioSampleRate |
| Definiton | The audio sample rate. Can be any value, but commonly 32000, 44100, or 48000. |
| Type | Integer |

### The `xmpDM:audioSampleType` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.audioSampleType |
| ID | xmpDM:audioSampleType |
| Label | – |
| Name | audioSampleType |
| Definiton | The audio sample type. One of: 8Int, 16Int, 24Int, 32Int, 32Float, Compressed, Packed,Other. |
| Options | 8Int, 16Int, 24Int, 32Int, 32Float, Compressed, Packed, Other |
| Type | Text |

### The `xmpDM:beatSpliceParams` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.beatSpliceParams |
| ID | xmpDM:beatSpliceParams |
| Label | – |
| Name | beatSpliceParams |
| Definiton | Additional parameters for Beat Splice stretch mode. |
| Type | BeatSpliceStretch |

### The `xmpDM:cameraAngle` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.cameraAngle |
| ID | xmpDM:cameraAngle |
| Label | – |
| Name | cameraAngle |
| Closed? | No |
| Definiton | The orientation of the camera to the subject in a static shot, from a fixed set of industry standard terminology. Predefined values include: Low Angle, Eye Level, High Angle, Overhead Shot, Birds Eye Shot, Dutch Angle, POV, Over the Shoulder, Reaction Shot. |
| Options | Low Angle, Eye Level, High Angle, Overhead Shot, Birds Eye Shot, Dutch Angle, POV, Over the Shoulder, Reaction Shot |
| Type | Text |

### The `xmpDM:cameraLabel` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.cameraLabel |
| ID | xmpDM:cameraLabel |
| Label | – |
| Name | cameraLabel |
| Definiton | A description of the camera used for a shoot. Can be any string, but is usually simply a number, for example '1', '2', or more explicitly 'Camera 1'. |
| Type | Text |

### The `xmpDM:cameraModel` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.cameraModel |
| ID | xmpDM:cameraModel |
| Label | – |
| Name | cameraModel |
| Definiton | The make and model of the camera used for a shoot. |
| Type | Text |

### The `xmpDM:cameraMove` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.cameraMove |
| ID | xmpDM:cameraMove |
| Label | – |
| Name | cameraMove |
| Closed? | No |
| Definiton | The movement of the camera during the shot, from a fixed set of industry standard terminology. Predefined values include: Aerial, Boom Up, Boom Down, Crane Up, Crane Down, Dolly In, Dolly Out, Pan Left, Pan Right, Pedestal Up, Pedestal Down, Tilt Up, Tilt Down, Tracking, Truck Left, Truck Right, Zoom In, Zoom Out. |
| Options | Aerial, Boom Up, Boom Down, Crane Up, Crane Down, Dolly In, Dolly Out, Pan Left, Pan Right, Pedestal Up, Pedestal Down, Tilt Up, Tilt Down, Tracking, Truck Left, Truck Right, Zoom In, Zoom Out |
| Type | Text |

### The `xmpDM:client` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.client |
| ID | xmpDM:client |
| Label | – |
| Name | client |
| Definiton | The client for the job of which this shot or take is a part. |
| Type | Text |

### The `xmpDM:comment` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.comment |
| ID | xmpDM:comment |
| Label | – |
| Name | comment |
| Definiton | A user’s comments. |
| Type | Text |

### The `xmpDM:composer` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.composer |
| ID | xmpDM:composer |
| Label | – |
| Name | composer |
| Definiton | The composer’s name. |
| Type | Text |

### The `xmpDM:contributedMedia` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.contributedMedia |
| ID | xmpDM:contributedMedia |
| Label | – |
| Name | contributedMedia |
| Definiton | An unordered list of all media used to create this media. |
| Multiple? | Yes |
| Ordered? | No |
| Type | Media |

### The `xmpDM:director` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.director |
| ID | xmpDM:director |
| Label | – |
| Name | director |
| Definiton | The director of the scene. |
| Type | Text |

### The `xmpDM:directorPhotography` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.directorPhotography |
| ID | xmpDM:directorPhotography |
| Label | – |
| Name | directorPhotography |
| Definiton | The director of photography for the scene. |
| Type | Text |

### The `xmpDM:duration` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.duration |
| ID | xmpDM:duration |
| Label | – |
| Name | duration |
| Definiton | The duration of the media file. |
| Type | Time |

### The `xmpDM:engineer` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.engineer |
| ID | xmpDM:engineer |
| Label | – |
| Name | engineer |
| Definiton | The engineer’s name. |
| Type | Text |

### The `xmpDM:fileDataRate` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.fileDataRate |
| ID | xmpDM:fileDataRate |
| Label | – |
| Name | fileDataRate |
| Definiton | The file data rate in megabytes per second. For example: '36/10' = 3.6 MB/sec. |
| Type | Rational |

### The `xmpDM:genre` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.genre |
| ID | xmpDM:genre |
| Label | – |
| Name | genre |
| Definiton | The name of the genre. |
| Type | Text |

### The `xmpDM:good` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.good |
| ID | xmpDM:good |
| Label | – |
| Name | good |
| Definiton | A checkbox for tracking whether a shot is a keeper. |
| Type | Boolean |

### The `xmpDM:instrument` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.instrument |
| ID | xmpDM:instrument |
| Label | – |
| Name | instrument |
| Definiton | The musical instrument. |
| Type | Text |

### The `xmpDM:introTime` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.introTime |
| ID | xmpDM:introTime |
| Label | – |
| Name | introTime |
| Definiton | The duration of lead time for queuing music. |
| Type | Time |

### The `xmpDM:key` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.key |
| ID | xmpDM:key |
| Label | – |
| Name | key |
| Definiton | The audio’s musical key. One of: C, C#, D, D#, E, F, F#, G, G#, A, A#, B. |
| Options | C, C#, D, D#, E, F, F#, G, G#, A, A#, B |
| Type | Text |

### The `xmpDM:logComment` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.logComment |
| ID | xmpDM:logComment |
| Label | – |
| Name | logComment |
| Definiton | User’s log comments. |
| Type | Text |

### The `xmpDM:loop` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.loop |
| ID | xmpDM:loop |
| Label | – |
| Name | loop |
| Definiton | When true, the clip can be looped seamlessly. |
| Type | Boolean |

### The `xmpDM:numberOfBeats` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.numberOfBeats |
| ID | xmpDM:numberOfBeats |
| Label | – |
| Name | numberOfBeats |
| Definiton | The total number of musical beats in a clip; for example, the beats-per-second times the duration in seconds. |
| Type | Real |

### The `xmpDM:markers` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.markers |
| ID | xmpDM:markers |
| Label | – |
| Name | markers |
| Definiton | An ordered list of markers. See also xmpDM:Tracks. |
| Multiple? | Yes |
| Ordered? | Yes |
| Type | Marker |

### The `xmpDM:outCue` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.outCue |
| ID | xmpDM:outCue |
| Label | – |
| Name | outCue |
| Definiton | The time at which to fade out. |
| Type | Time |

### The `xmpDM:projectName` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.projectName |
| ID | xmpDM:projectName |
| Label | – |
| Name | projectName |
| Definiton | The name of the project of which this file is a part. |
| Type | Text |

### The `xmpDM:projectRef` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.projectRef |
| ID | xmpDM:projectRef |
| Label | – |
| Name | projectRef |
| Definiton | A reference to the project of which this file is a part. |
| Type | ProjectLink |

### The `xmpDM:pullDown` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.pullDown |
| ID | xmpDM:pullDown |
| Label | – |
| Name | pullDown |
| Definiton | The sampling phase of film to be converted to video (pull-down). One of: WSSWW, SSWWW, SWWWS, WWWSS, WWSSW, WWWSW, WWSWW, WSWWW, SWWWW, WWWWS. |
| Options | WSSWW, SSWWW, SWWWS, WWWSS, WWSSW, WWWSW, WWSWW, WSWWW, SWWWW, WWWWS |
| Type | Text |

### The `xmpDM:relativePeakAudioFilePath` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.relativePeakAudioFilePath |
| ID | xmpDM:relativePeakAudioFilePath |
| Label | – |
| Name | relativePeakAudioFilePath |
| Definiton | The relative path to the file’s peak audio file. If empty, no peak file exists. |
| Type | URI |

### The `xmpDM:relativeTimestamp` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.relativeTimestamp |
| ID | xmpDM:relativeTimestamp |
| Label | – |
| Name | relativeTimestamp |
| Definiton | The start time of the media inside the audio project. |
| Type | Time |

### The `xmpDM:releaseDate` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.releaseDate |
| ID | xmpDM:releaseDate |
| Label | – |
| Name | releaseDate |
| Definiton | The date the title was released. |
| Type | Date |

### The `xmpDM:resampleParams` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.resampleParams |
| ID | xmpDM:resampleParams |
| Label | – |
| Name | resampleParams |
| Definiton | Additional parameters for Resample stretch mode. |
| Type | ResampleStretch |

### The `xmpDM:scaleType` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.scaleType |
| ID | xmpDM:scaleType |
| Label | – |
| Name | scaleType |
| Definiton | The musical scale used in the music. One of: Major, Minor, Both, Neither. Neither is most often used for instruments with no associated scale, such as drums. |
| Options | Major, Minor, Both, Neither |
| Type | Text |

### The `xmpDM:scene` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.scene |
| ID | xmpDM:scene |
| Label | – |
| Name | scene |
| Definiton | The name of the scene. |
| Type | Text |

### The `xmpDM:shotDate` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.shotDate |
| ID | xmpDM:shotDate |
| Label | – |
| Name | shotDate |
| Definiton | The date and time when the video was shot. |
| Type | Date |

### The `xmpDM:shotDay` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.shotDay |
| ID | xmpDM:shotDay |
| Label | – |
| Name | shotDay |
| Definiton | The day in a multiday shoot. For example: Day 2, Friday. |
| Type | Text |

### The `xmpDM:shotLocation` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.shotLocation |
| ID | xmpDM:shotLocation |
| Label | – |
| Name | shotLocation |
| Definiton | The name of the location where the video was shot. For example: 'Oktoberfest, Munich Germany'. For more accurate positioning, use the EXIF GPS values. |
| Type | Text |

### The `xmpDM:shotName` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.shotName |
| ID | xmpDM:shotName |
| Label | – |
| Name | shotName |
| Definiton | The name of the shot or take. |
| Type | Text |

### The `xmpDM:shotNumber` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.shotNumber |
| ID | xmpDM:shotNumber |
| Label | – |
| Name | shotNumber |
| Definiton | The position of the shot in a script or production, relative to other shots. For example: 1, 2, 1a, 1b, 1.1, 1.2. |
| Type | Text |

### The `xmpDM:shotSize` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.shotSize |
| ID | xmpDM:shotSize |
| Label | – |
| Name | shotSize |
| Definiton | The size or scale of the shot framing, from a fixed set of industry standard terminology. Predefined values include: ECU (extreme close-up), MCU (medium close-up), CU (close-up), MS (medium shot), WS (wide shot), MWS (medium wide shot), EWS (extreme wide shot). |
| Options | ECU, MCU, CU, MS, WS, MWS, EWS |
| Type | Text |

### The `xmpDM:speakerPlacement` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.speakerPlacement |
| ID | xmpDM:speakerPlacement |
| Label | – |
| Name | speakerPlacement |
| Definiton | A description of the speaker angles from centre front in degrees. For example: “Left = -30, Right = 30, Centre = 0, LFE = 45, Left Surround = -110, Right Surround = 110”. |
| Type | Text |

### The `xmpDM:startTimecode` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.startTimecode |
| ID | xmpDM:startTimecode |
| Label | – |
| Name | startTimecode |
| Definiton | The timecode of the first frame of video in the file, as obtained from the device control. |
| Type | Timecode |

### The `xmpDM:stretchMode` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.stretchMode |
| ID | xmpDM:stretchMode |
| Label | – |
| Name | stretchMode |
| Definiton | The audio stretch mode. One of: Fixed length, Time-Scale, Resample, Beat Splice, Hybrid. |
| Options | Fixed length, Time-Scale, Resample, Beat Splice, Hybrid |
| Type | Text |

### The `xmpDM:takeNumber` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.takeNumber |
| ID | xmpDM:takeNumber |
| Label | – |
| Name | takeNumber |
| Definiton | A numeric value indicating the absolute number of a take. |
| Type | Integer |

### The `xmpDM:tapeName` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.tapeName |
| ID | xmpDM:tapeName |
| Label | – |
| Name | tapeName |
| Definiton | The name of the tape from which the clip was captured, as set during the capture process. |
| Type | Text |

### The `xmpDM:tempo` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.tempo |
| ID | xmpDM:tempo |
| Label | – |
| Name | tempo |
| Definiton | The audio’s tempo. |
| Type | Real |

### The `xmpDM:timeScaleParams` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.timeScaleParams |
| ID | xmpDM:timeScaleParams |
| Label | – |
| Name | timeScaleParams |
| Definiton | Additional parameters for Time-Scale stretch mode. |
| Type | TimeScaleStretch |

### The `xmpDM:timeSignature` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.timeSignature |
| ID | xmpDM:timeSignature |
| Label | – |
| Name | timeSignature |
| Definiton | The time signature of the music. One of: 2/4, 3/4, 4/4, 5/4, 7/4, 6/8, 9/8, 12/8, other. |
| Options | 2/4, 3/4, 4/4, 5/4, 7/4, 6/8, 9/8, 12/8, other |
| Type | Text |

### The `xmpDM:trackNumber` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.trackNumber |
| ID | xmpDM:trackNumber |
| Label | – |
| Name | trackNumber |
| Definiton | A numeric value indicating the order of the audio file within its original recording. |
| Type | Integer |

### The `xmpDM:Tracks` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.tracks |
| ID | xmpDM:Tracks |
| Label | – |
| Name | tracks |
| Definiton | An unordered list of tracks. A track is a named set of markers, which can specify a frame rate for all markers in the set. See also xmpDM:markers. |
| Multiple? | Yes |
| Ordered? | No |
| Type | Track |

### The `xmpDM:videoAlphaMode` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.videoAlphaMode |
| ID | xmpDM:videoAlphaMode |
| Label | – |
| Name | videoAlphaMode |
| Definiton | The alpha mode. One of: straight, pre-multiplied, or none. |
| Options | straight, pre-multiplied, none |
| Type | Text |

### The `xmpDM:videoAlphaPremultipleColor` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.videoAlphaPremultipleColor |
| ID | xmpDM:videoAlphaPremultipleColor |
| Label | – |
| Name | videoAlphaPremultipleColor |
| Definiton | A colour in CMYK or RGB to be used as the premultiple colour when alpha mode is premultiplied. |
| Type | Colorants |

### The `xmpDM:videoAlphaUnityIsTransparent` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.videoAlphaUnityIsTransparent |
| ID | xmpDM:videoAlphaUnityIsTransparent |
| Label | – |
| Name | videoAlphaUnityIsTransparent |
| Definiton | When true, unity is clear, when false, it is opaque. |
| Type | Boolean |

### The `xmpDM:videoColorSpace` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.videoColorSpace |
| ID | xmpDM:videoColorSpace |
| Label | – |
| Name | videoColorSpace |
| Definiton | The colour space. One of: sRGB (used by Photoshop), CCIR-601 (used for NTSC), CCIR-709 (used for HD). |
| Options | sRGB, CCIR-601, CCIR-709 |
| Type | Text |

### The `xmpDM:videoCompressor` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.videoCompressor |
| ID | xmpDM:videoCompressor |
| Label | – |
| Name | videoCompressor |
| Definiton | Video compression used. For example, jpeg. |
| Type | Text |

### The `xmpDM:videoFieldOrder` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.videoFieldOrder |
| ID | xmpDM:videoFieldOrder |
| Label | – |
| Name | videoFieldOrder |
| Definiton | The field order for video. One of: Upper, Lower, Progressive. |
| Options | Upper, Lower, Progressive |
| Type | Text |

### The `xmpDM:videoFrameRate` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.videoFrameRate |
| ID | xmpDM:videoFrameRate |
| Label | – |
| Name | videoFrameRate |
| Closed? | No |
| Definiton | The video frame rate. Predefined values include: 24, NTSC, PAL. |
| Options | 24, NTSC, PAL |
| Type | Text |

### The `xmpDM:videoFrameSize` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.videoFrameSize |
| ID | xmpDM:videoFrameSize |
| Label | – |
| Name | videoFrameSize |
| Definiton | The frame size. For example: w:720, h: 480, unit:pixels. |
| Type | Dimensions |

### The `xmpDM:videoPixelAspectRatio` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.videoPixelAspectRatio |
| ID | xmpDM:videoPixelAspectRatio |
| Label | – |
| Name | videoPixelAspectRatio |
| Definiton | The aspect ratio, expressed as wd/ht. For example: “648/720” = 0.9. |
| Type | Rational |

### The `xmpDM:videoPixelDepth` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.videoPixelDepth |
| ID | xmpDM:videoPixelDepth |
| Label | – |
| Name | videoPixelDepth |
| Definiton | The size in bits of each colour component of a pixel. Standard Windows 32-bit pixels have 8 bits per component. One of: 8Int, 16Int, 24Int, 32Int, 32Float, Other. |
| Options | 8Int, 16Int, 24Int, 32Int, 32Float, Other |
| Type | Text |

### The `xmpDM:partOfCompilation` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.partOfCompilation |
| ID | xmpDM:partOfCompilation |
| Label | – |
| Name | partOfCompilation |
| Definiton | Part of compilation. |
| Type | Boolean |

### The `xmpDM:lyrics` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.lyrics |
| ID | xmpDM:lyrics |
| Label | – |
| Name | lyrics |
| Definiton | Lyrics text. No association with timecode. |
| Type | Text |

### The `xmpDM:discNumber` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dynamic_media.discNumber |
| ID | xmpDM:discNumber |
| Label | – |
| Name | discNumber |
| Definiton | If in a multi-disc set, might contain total number of discs. For example: 2/3. |
| Type | Text |

The XMP metadata model's 'rights_management' namespace offers five fields which are detailed below:

### The `xmpRights:Certificate` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.rights.Certificate |
| ID | xmpRights:Certificate |
| Label | – |
| Name | Certificate |
| Definiton | A web URL for a rights management certificate. NOTE: This is a normal (non-URI) simple value because of historical usage. |
| Pseudonym | exiftool: xmpRights:Certificate |
| Type | Text |

### The `xmpRights:Marked` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.rights.Marked |
| ID | xmpRights:Marked |
| Label | – |
| Name | Marked |
| Definiton | When true, indicates that this is a rights-managed resource. When false, indicates that this is a public-domain resource. Omit if the state is unknown. |
| Nullable? | No |
| Pseudonym | exiftool: xmpRights:Marked |
| Type | Boolean |

### The `xmpRights:Owner` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.rights.Owner |
| ID | xmpRights:Owner |
| Label | – |
| Name | Owner |
| Definiton | A list of legal owners of the resource. |
| Multiple? | Yes |
| Ordered? | No |
| Pseudonym | exiftool: xmpRights:Owner |
| Type | ProperName |

### The `xmpRights:UsageTerms` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.rights.UsageTerms |
| ID | xmpRights:UsageTerms |
| Label | – |
| Name | UsageTerms |
| Combine? | Yes |
| Definiton | A collection of text instructions on how a resource can be legally used, given in a variety of languages. |
| Pseudonym | exiftool: xmpRights:UsageTerms |
| Type | LanguageAlternative |

### The `xmpRights:WebStatement` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.rights.WebStatement |
| ID | xmpRights:WebStatement |
| Label | – |
| Name | WebStatement |
| Definiton | A Web URL for a statement of the ownership and usage rights for this resource. NOTE: This is a normal (non-URI) simple value because of historical usage. |
| Pseudonym | exiftool: xmpRights:WebStatement |
| Type | Text |

The XMP metadata model's 'adobe_pdf' namespace offers four fields which are detailed below:

### The `pdf:Keywords` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.adobe_pdf.keywords |
| ID | pdf:Keywords |
| Label | – |
| Name | keywords |
| Definiton | Keywords. |
| Type | Text |

### The `pdf:PDFVersion` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.adobe_pdf.PDFVersion |
| ID | pdf:PDFVersion |
| Label | – |
| Name | PDFVersion |
| Definiton | The PDF file version (for example: 1.0, 1.3, and so on). |
| Type | Text |

### The `pdf:Producer` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.adobe_pdf.producer |
| ID | pdf:Producer |
| Label | – |
| Name | producer |
| Definiton | The name of the tool that created the PDF document. |
| Type | AgentName |

### The `pdf:Trapped` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.adobe_pdf.trapped |
| ID | pdf:Trapped |
| Label | – |
| Name | trapped |
| Definiton | True when the document has been trapped. |
| Type | Boolean |

The XMP metadata model's 'photoshop' namespace offers nineteen fields which are detailed below:

### The `photoshop:ColorMode` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.photoshop.colorMode |
| ID | photoshop:ColorMode |
| Label | – |
| Name | colorMode |
| Definiton | The colour mode. One of: 0 = Bitmap , 1 = Gray scale, 2 = Indexed colour, 3 = RGB colour, 4 = CMYK colour, 7 = Multi-channel, 8 = Duotone, 9 = LAB colour. |
| Options | 0, 1, 2, 3, 4, 7, 8, 9 |
| Type | Integer |

### The `photoshop:DocumentAncestors` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.photoshop.documentAncestors |
| ID | photoshop:DocumentAncestors |
| Label | – |
| Name | documentAncestors |
| Definiton | If the source document for a copy-and-paste or place operation has a document ID, that ID is added to this list in the destination document's XMP. |
| Multiple? | Yes |
| Ordered? | No |
| Type | Ancestor |

### The `photoshop:History` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.photoshop.history |
| ID | photoshop:History |
| Label | – |
| Name | history |
| Definiton | The history that appears in the FileInfo panel, if activated in the application preferences. |
| Type | Text |

### The `photoshop:ICCProfile` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.photoshop.ICCProfile |
| ID | photoshop:ICCProfile |
| Label | – |
| Name | ICCProfile |
| Definiton | The colour profile, such as AppleRGB, AdobeRGB1998. |
| Type | Text |

### The `photoshop:TextLayers` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.photoshop.textLayers |
| ID | photoshop:TextLayers |
| Label | – |
| Name | textLayers |
| Definiton | If a document has text layers, this property caches the text for each layer. |
| Multiple? | Yes |
| Ordered? | Yes |
| Type | Layer |

### The `photoshop:AuthorsPosition` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.photoshop.authorsPosition |
| ID | photoshop:AuthorsPosition |
| Label | – |
| Name | authorsPosition |
| Definiton | By-line title. |
| Type | Text |

### The `photoshop:CaptionWriter` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.photoshop.captionWriter |
| ID | photoshop:CaptionWriter |
| Label | – |
| Name | captionWriter |
| Definiton | Writer/editor. |
| Type | ProperName |

### The `photoshop:Category` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.photoshop.category |
| ID | photoshop:Category |
| Label | – |
| Name | category |
| Count/Length | 3 |
| Definiton | Category. Limited to 3 7-bit ASCII characters. |
| Encoding | ASCII |
| Type | Text |

### The `photoshop:City` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.photoshop.city |
| ID | photoshop:City |
| Label | – |
| Name | city |
| Definiton | City. |
| Type | Text |

### The `photoshop:Country` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.photoshop.country |
| ID | photoshop:Country |
| Label | – |
| Name | country |
| Definiton | Country/primary location. |
| Type | Text |

### The `photoshop:Credit` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.photoshop.credit |
| ID | photoshop:Credit |
| Label | – |
| Name | credit |
| Definiton | Credit. |
| Pseudonym | exiftool: photoshop:Credit |
| Type | Text |

### The `photoshop:DateCreated` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.photoshop.dateCreated |
| ID | photoshop:DateCreated |
| Label | – |
| Name | dateCreated |
| Definiton | The date the intellectual content of the document was created, rather than the creation date of the physical representation. |
| Type | Date |

### The `photoshop:Headline` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.photoshop.headline |
| ID | photoshop:Headline |
| Label | – |
| Name | headline |
| Definiton | Headline. |
| Type | Text |

### The `photoshop:Instructions` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.photoshop.instructions |
| ID | photoshop:Instructions |
| Label | – |
| Name | instructions |
| Definiton | Special instructions. |
| Type | Text |

### The `photoshop:Source` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.photoshop.source |
| ID | photoshop:Source |
| Label | – |
| Name | source |
| Definiton | Source. |
| Pseudonym | exiftool: photoshop:Source |
| Type | Text |

### The `photoshop:State` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.photoshop.state |
| ID | photoshop:State |
| Label | – |
| Name | state |
| Definiton | Province/state. |
| Type | Text |

### The `photoshop:SupplementalCategories` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.photoshop.supplementalCategories |
| ID | photoshop:SupplementalCategories |
| Label | – |
| Name | supplementalCategories |
| Definiton | Supplemental category. |
| Multiple? | Yes |
| Ordered? | No |
| Type | Text |

### The `photoshop:TransmissionReference` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.photoshop.transmissionReference |
| ID | photoshop:TransmissionReference |
| Label | – |
| Name | transmissionReference |
| Definiton | Original transmission reference. |
| Type | Text |

### The `photoshop:Urgency` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.photoshop.urgency |
| ID | photoshop:Urgency |
| Label | – |
| Name | urgency |
| Definiton | Urgency. Valid range is 1-8. |
| Maximum Value | 8 |
| Minimum Value | 1 |
| Type | Integer |

The XMP metadata model's 'camera_raw' namespace offers 41 fields which are detailed below:

### The `crs:AutoBrightness` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.autoBrightness |
| ID | crs:AutoBrightness |
| Label | – |
| Name | autoBrightness |
| Definiton | When true, brightness is automatically adjusted. |
| Type | Boolean |

### The `crs:AutoContrast` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.autoContrast |
| ID | crs:AutoContrast |
| Label | – |
| Name | autoContrast |
| Definiton | When true, contrast is automatically adjusted. |
| Type | Boolean |

### The `crs:AutoExposure` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.autoExposure |
| ID | crs:AutoExposure |
| Label | – |
| Name | autoExposure |
| Definiton | When true, exposure is automatically adjusted. |
| Type | Boolean |

### The `crs:AutoShadows` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.autoShadows |
| ID | crs:AutoShadows |
| Label | – |
| Name | autoShadows |
| Definiton | When true, shadows are automatically adjusted. |
| Type | Boolean |

### The `crs:BlueHue` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.blueHue |
| ID | crs:BlueHue |
| Label | – |
| Name | blueHue |
| Definiton | Blue Hue setting. Range -100 to +100. |
| Maximum Value | 100 |
| Minimum Value | -100 |
| Type | Integer |

### The `crs:BlueSaturation` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.blueSaturation |
| ID | crs:BlueSaturation |
| Label | – |
| Name | blueSaturation |
| Definiton | Blue Saturation setting. Range -100 to +100. |
| Maximum Value | 100 |
| Minimum Value | -100 |
| Type | Integer |

### The `crs:Brightness` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.brightness |
| ID | crs:Brightness |
| Label | – |
| Name | brightness |
| Definiton | Brightness setting. Range 0 to 150. |
| Maximum Value | 150 |
| Minimum Value | 0 |
| Type | Integer |

### The `crs:CameraProfile` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.cameraProfile |
| ID | crs:CameraProfile |
| Label | – |
| Name | cameraProfile |
| Definiton | Camera Profile setting. |
| Type | Text |

### The `crs:ChromaticAberrationB` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.chromaticAberrationB |
| ID | crs:ChromaticAberrationB |
| Label | – |
| Name | chromaticAberrationB |
| Definiton | Chomatic Aberration, Fix Blue/Yellow Fringe setting. Range -100 to +100. |
| Maximum Value | 100 |
| Minimum Value | -100 |
| Type | Integer |

### The `crs:ChromaticAberrationR` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.chromaticAberrationR |
| ID | crs:ChromaticAberrationR |
| Label | – |
| Name | chromaticAberrationR |
| Definiton | Chomatic Aberration, Fix Red/Cyan Fringe setting. Range -100 to +100. |
| Maximum Value | 100 |
| Minimum Value | -100 |
| Type | Integer |

### The `crs:ColorNoiseReduction` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.colorNoiseReduction |
| ID | crs:ColorNoiseReduction |
| Label | – |
| Name | colorNoiseReduction |
| Definiton | Color Noise Reducton setting. Range 0 to 100. |
| Maximum Value | 100 |
| Minimum Value | 0 |
| Type | Integer |

### The `crs:Contrast` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.contrast |
| ID | crs:Contrast |
| Label | – |
| Name | contrast |
| Definiton | Contrast setting. Range -50 to 100. |
| Maximum Value | 100 |
| Minimum Value | -50 |
| Type | Integer |

### The `crs:CropTop` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.cropTop |
| ID | crs:CropTop |
| Label | – |
| Name | cropTop |
| Definiton | When Has Crop is true, top of crop rectangle. |
| Type | Real |

### The `crs:CropLeft` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.cropLeft |
| ID | crs:CropLeft |
| Label | – |
| Name | cropLeft |
| Definiton | When Has Crop is true, left of crop rectangle. |
| Type | Real |

### The `crs:CropBottom` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.cropBottom |
| ID | crs:CropBottom |
| Label | – |
| Name | cropBottom |
| Definiton | When Has Crop is true, bottom of crop rectangle. |
| Type | Real |

### The `crs:CropRight` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.cropRight |
| ID | crs:CropRight |
| Label | – |
| Name | cropRight |
| Definiton | When Has Crop is true, right of crop rectangle. |
| Type | Real |

### The `crs:CropAngle` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.cropAngle |
| ID | crs:CropAngle |
| Label | – |
| Name | cropAngle |
| Definiton | When Has Crop is true, angle of crop rectangle. |
| Type | Real |

### The `crs:CropWidth` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.cropWidth |
| ID | crs:CropWidth |
| Label | – |
| Name | cropWidth |
| Definiton | Width of resulting cropped image in CropUnits units. |
| Type | Real |

### The `crs:CropHeight` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.cropHeight |
| ID | crs:CropHeight |
| Label | – |
| Name | cropHeight |
| Definiton | Height of resulting cropped image in CropUnits units. |
| Type | Real |

### The `crs:CropUnits` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.cropUnits |
| ID | crs:CropUnits |
| Label | – |
| Name | cropUnits |
| Definiton | Units for Crop Width and Crop Height. One of: 0=pixels 1=inches 2=cm. |
| Options | 0, 1, 2 |
| Type | Integer |

### The `crs:Exposure` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.exposure |
| ID | crs:Exposure |
| Label | – |
| Name | exposure |
| Definiton | Exposure setting. Range -4.0 to +4.0. |
| Maximum Value | 4.0 |
| Minimum Value | -4.0 |
| Type | Real |

### The `crs:GreenHue` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.greenHue |
| ID | crs:GreenHue |
| Label | – |
| Name | greenHue |
| Definiton | Green Hue setting. Range -100 to +100. |
| Maximum Value | 100 |
| Minimum Value | -100 |
| Type | Integer |

### The `crs:GreenSaturation` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.greenSaturation |
| ID | crs:GreenSaturation |
| Label | – |
| Name | greenSaturation |
| Definiton | Green Saturation setting. Range -100 to +100. |
| Maximum Value | 100 |
| Minimum Value | -100 |
| Type | Integer |

### The `crs:HasCrop` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.hasCrop |
| ID | crs:HasCrop |
| Label | – |
| Name | hasCrop |
| Definiton | When true, image has a cropping rectangle. |
| Type | Boolean |

### The `crs:HasSettings` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.hasSettings |
| ID | crs:HasSettings |
| Label | – |
| Name | hasSettings |
| Definiton | When true, non-default camera raw settings. |
| Type | Boolean |

### The `crs:LuminanceSmoothing` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.luminanceSmoothing |
| ID | crs:LuminanceSmoothing |
| Label | – |
| Name | luminanceSmoothing |
| Definiton | Luminance Smoothing setting. Range 0 to +100. |
| Maximum Value | 100 |
| Minimum Value | 0 |
| Type | Integer |

### The `crs:RawFileName` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.rawFileName |
| ID | crs:RawFileName |
| Label | – |
| Name | rawFileName |
| Definiton | File name for raw file (not a complete path). |
| Type | Text |

### The `crs:RedHue` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.redHue |
| ID | crs:RedHue |
| Label | – |
| Name | redHue |
| Definiton | Red Hue setting. Range -100 to +100. |
| Maximum Value | 100 |
| Minimum Value | -100 |
| Type | Integer |

### The `crs:RedSaturation` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.redSaturation |
| ID | crs:RedSaturation |
| Label | – |
| Name | redSaturation |
| Definiton | Red Saturation setting. Range -100 to +100. |
| Maximum Value | 100 |
| Minimum Value | -100 |
| Type | Integer |

### The `crs:Saturation` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.saturation |
| ID | crs:Saturation |
| Label | – |
| Name | saturation |
| Definiton | Saturation setting. Range -100 to +100. |
| Maximum Value | 100 |
| Minimum Value | -100 |
| Type | Integer |

### The `crs:Shadows` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.shadows |
| ID | crs:Shadows |
| Label | – |
| Name | shadows |
| Definiton | Shadows setting. Range 0 to +100. |
| Maximum Value | 100 |
| Minimum Value | 0 |
| Type | Integer |

### The `crs:ShadowTint` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.shadowTint |
| ID | crs:ShadowTint |
| Label | – |
| Name | shadowTint |
| Definiton | Shadow Tint setting. Range -100 to 100. |
| Maximum Value | 100 |
| Minimum Value | -100 |
| Type | Integer |

### The `crs:Sharpness` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.sharpness |
| ID | crs:Sharpness |
| Label | – |
| Name | sharpness |
| Definiton | Sharpness setting. Range 0 to 100. |
| Maximum Value | 100 |
| Minimum Value | 0 |
| Type | Integer |

### The `crs:Temperature` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.temperature |
| ID | crs:Temperature |
| Label | – |
| Name | temperature |
| Definiton | Temperature setting. Range 2000 to 50000. |
| Maximum Value | 50000 |
| Minimum Value | 2000 |
| Type | Integer |

### The `crs:Tint` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.tint |
| ID | crs:Tint |
| Label | – |
| Name | tint |
| Definiton | Tint setting. Range -150 to 150. |
| Maximum Value | 150 |
| Minimum Value | -150 |
| Type | Integer |

### The `crs:ToneCurve` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.toneCurve |
| ID | crs:ToneCurve |
| Label | – |
| Name | toneCurve |
| Definiton | Array of points (Integer, Integer) defining a tone curve. |
| Multiple? | Yes |
| Ordered? | Yes |
| Type | Integer |

### The `crs:ToneCurveName` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.toneCurveName |
| ID | crs:ToneCurveName |
| Label | – |
| Name | toneCurveName |
| Closed? | No |
| Definiton | The name of the Tone Curve described by ToneCurve. One of: Linear , Medium Contrast , Strong Contrast, Custom, or a user-defined preset name. |
| Options | Linear, Medium Contrast, Strong Contrast, Custom |
| Type | Text |

### The `crs:Version` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.version |
| ID | crs:Version |
| Label | – |
| Name | version |
| Definiton | Version of Camera Raw plugin. |
| Type | Text |

### The `crs:VignetteAmount` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.vignetteAmount |
| ID | crs:VignetteAmount |
| Label | – |
| Name | vignetteAmount |
| Definiton | Vignetting Amount setting. Range -100 to 100. |
| Maximum Value | 100 |
| Minimum Value | -100 |
| Type | Integer |

### The `crs:VignetteMidpoint` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.vignetteMidpoint |
| ID | crs:VignetteMidpoint |
| Label | – |
| Name | vignetteMidpoint |
| Definiton | Vignetting Midpoint setting. Range 0 to 100. |
| Maximum Value | 100 |
| Minimum Value | 0 |
| Type | Integer |

### The `crs:WhiteBalance` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.camera_raw.whiteBalance |
| ID | crs:WhiteBalance |
| Label | – |
| Name | whiteBalance |
| Definiton | White Balance setting. One of: As Shot, Auto, Daylight, Cloudy, Shade, Tungsten, Fluorescent, Flash, Custom. |
| Options | As Shot, Auto, Daylight, Cloudy, Shade, Tungsten, Fluorescent, Flash, Custom |
| Type | Text |

The XMP metadata model's 'exif' namespace offers 77 fields which are detailed below:

### The `exif:ApertureValue` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.apertureValue |
| ID | exif:ApertureValue |
| Label | – |
| Name | apertureValue |
| Definiton | EXIF tag 37378, 0x9202. Lens aperture, unit is APEX. |
| Tag | 37378 |
| Type | Rational |
| Unit | APEX |

### The `exif:BrightnessValue` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.brightnessValue |
| ID | exif:BrightnessValue |
| Label | – |
| Name | brightnessValue |
| Definiton | EXIF tag 37379, 0x9203. Brightness, unit is APEX. |
| Tag | 37379 |
| Type | Rational |
| Unit | APEX |

### The `exif:CFAPattern` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.CFAPattern |
| ID | exif:CFAPattern |
| Label | – |
| Name | CFAPattern |
| Definiton | EXIF tag 41730, 0xA302. Color filter array geometric pattern of the image sense. |
| Tag | 41730 |
| Type | CFAPattern |

### The `exif:ColorSpace` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.colorSpace |
| ID | exif:ColorSpace |
| Label | – |
| Name | colorSpace |
| Definiton | EXIF tag 40961, 0xA001. Color space information: 1 = sRGB, 65535 = uncalibrated. |
| Options | 1, 65535 |
| Tag | 40961 |
| Type | Integer |

### The `exif:CompressedBitsPerPixel` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.compressedBitsPerPixel |
| ID | exif:CompressedBitsPerPixel |
| Label | – |
| Name | compressedBitsPerPixel |
| Definiton | EXIF tag 37122, 0x9102. Compression mode used for a compressed image is indicated in unit bits per pixel. |
| Tag | 37122 |
| Type | Rational |

### The `exif:Contrast` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.contrast |
| ID | exif:Contrast |
| Label | – |
| Name | contrast |
| Definiton | EXIF tag 41992, 0xA408. Indicates the direction of contrast processing applied by the camera: 0 = Normal, 1 = Soft, 2 = Hard. |
| Options | 0, 1, 2 |
| Tag | 41992 |
| Type | Integer |

### The `exif:CustomRendered` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.customRendered |
| ID | exif:CustomRendered |
| Label | – |
| Name | customRendered |
| Definiton | EXIF tag 41985, 0xA401. Indicates the use of special processing on image data: 0 = Normal process, 1 = Custom process. |
| Options | 0, 1 |
| Tag | 41985 |
| Type | Integer |

### The `exif:DateTimeDigitized` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.dateTimeDigitized |
| ID | exif:DateTimeDigitized |
| Label | – |
| Name | dateTimeDigitized |
| Definiton | EXIF tag 36868, 0x9004 (primary) and 37522, 0x9292 (subseconds). Date and time when image was stored as digital data, can be the same as DateTimeOriginal if originally stored in digital form. Stored in ISO 8601 format. Includes the EXIF SubSecTimeDigitized data. This value is used in XMP as xmp:CreateDate. |
| Related Field | exif:SubSecTimeDigitized |
| Tag | 36868 |
| Type | Date |

### The `exif:DateTimeOriginal` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.dateTimeOriginal |
| ID | exif:DateTimeOriginal |
| Label | – |
| Name | dateTimeOriginal |
| Definiton | EXIF tags 36867, 0x9003 (primary) and 37521, 0x9291 (subseconds). Date and time when original image was generated, in ISO 8601 format. Includes the EXIF SubSecTimeOriginal data. Note that Exif date-time values have no time zone information. |
| Related Field | exif:SubSecTimeOriginal |
| Tag | 36867 |
| Type | Date |

### The `exif:DeviceSettingDescription` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.deviceSettingDescription |
| ID | exif:DeviceSettingDescription |
| Label | – |
| Name | deviceSettingDescription |
| Definiton | EXIF tag 41995, 0xA40B. Indicates information on the picture-taking conditions of a particular camera model. |
| Tag | 41995 |
| Type | DeviceSettings |

### The `exif:DigitalZoomRatio` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.digitalZoomRatio |
| ID | exif:DigitalZoomRatio |
| Label | – |
| Name | digitalZoomRatio |
| Definiton | EXIF tag 41988, 0xA404. Indicates the digital zoom ratio when the image was shot. |
| Tag | 41988 |
| Type | Rational |

### The `exif:ExifVersion` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.exifVersion |
| ID | exif:ExifVersion |
| Label | – |
| Name | exifVersion |
| Definiton | EXIF tag 36864, 0x9000. EXIF version number. |
| Tag | 36864 |
| Type | Text |

### The `exif:ExposureBiasValue` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.exposureBiasValue |
| ID | exif:ExposureBiasValue |
| Label | – |
| Name | exposureBiasValue |
| Definiton | EXIF tag 37380, 0x9204. Exposure bias, unit is APEX. |
| Tag | 37380 |
| Type | Rational |
| Unit | APEX |

### The `exif:ExposureIndex` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.exposureIndex |
| ID | exif:ExposureIndex |
| Label | – |
| Name | exposureIndex |
| Definiton | EXIF tag 41493, 0xA215. Exposure index of input device. |
| Tag | 41493 |
| Type | Rational |

### The `exif:ExposureMode` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.exposureMode |
| ID | exif:ExposureMode |
| Label | – |
| Name | exposureMode |
| Definiton | EXIF tag 41986, 0xA402. Indicates the exposure mode set when the image was shot: 0 = Auto exposure, 1 = Manual exposure, 2 = Auto bracket. |
| Options | 0, 1, 2 |
| Tag | 41986 |
| Type | Integer |

### The `exif:ExposureProgram` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.exposureProgram |
| ID | exif:ExposureProgram |
| Label | – |
| Name | exposureProgram |
| Definiton | EXIF tag 34850, 0x8822. Class of program used for exposure: 0 = not defined, 1 = Manual, 2 = Normal program, 3 = Aperture priority, 4 = Shutter priority, 5 = Creative program, 6 = Action program, 7 = Portrait mode, 8 = Landscape mode. |
| Options | 0, 1, 2, 3, 4, 5, 6, 7, 8 |
| Tag | 34850 |
| Type | Integer |

### The `exif:ExposureTime` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.exposureTime |
| ID | exif:ExposureTime |
| Label | – |
| Name | exposureTime |
| Definiton | EXIF tag 33434, 0x829A. Exposure time in seconds. |
| Tag | 33434 |
| Type | Rational |

### The `exif:FileSource` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.fileSource |
| ID | exif:FileSource |
| Label | – |
| Name | fileSource |
| Definiton | EXIF tag 41728, 0xA300. Indicates image source: 3 (DSC) is the only choice. |
| Options | 3 |
| Tag | 41728 |
| Type | Integer |

### The `exif:Flash` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.flash |
| ID | exif:Flash |
| Label | – |
| Name | flash |
| Definiton | EXIF tag 37385, 0x9209. Strobe light (flash) source data. |
| Tag | 37385 |
| Type | Flash |

### The `exif:FlashEnergy` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.flashEnergy |
| ID | exif:FlashEnergy |
| Label | – |
| Name | flashEnergy |
| Definiton | EXIF tag 41483, 0xA20B. Strobe energy during image capture. |
| Tag | 41483 |
| Type | Rational |

### The `exif:FlashpixVersion` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.flashpixVersion |
| ID | exif:FlashpixVersion |
| Label | – |
| Name | flashpixVersion |
| Definiton | EXIF tag 40960, 0xA000. Version of FlashPix. |
| Tag | 40960 |
| Type | Text |

### The `exif:FNumber` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.FNumber |
| ID | exif:FNumber |
| Label | – |
| Name | FNumber |
| Definiton | EXIF tag 33437, 0x829D. F number. |
| Tag | 33437 |
| Type | Rational |

### The `exif:FocalLength` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.focalLength |
| ID | exif:FocalLength |
| Label | – |
| Name | focalLength |
| Definiton | EXIF tag 37386, 0x920A. Focal length of the lens, in millimeters. |
| Tag | 37386 |
| Type | Rational |
| Unit | mm |

### The `exif:FocalLengthIn35mmFilm` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.FocalLengthIn35mmFilm |
| ID | exif:FocalLengthIn35mmFilm |
| Label | – |
| Name | FocalLengthIn35mmFilm |
| Definiton | EXIF tag 41989, 0xA405. Indicates the equivalent focal length assuming a 35mm film camera, in mm. A value of 0 means the focal length is unknown. Note that this tag differs from the FocalLength tag. |
| Tag | 41989 |
| Type | Integer |
| Unit | mm |

### The `exif:FocalPlaneResolutionUnit` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.focalPlaneResolutionUnit |
| ID | exif:FocalPlaneResolutionUnit |
| Label | – |
| Name | focalPlaneResolutionUnit |
| Definiton | EXIF tag 41488, 0xA210. Unit used for FocalPlaneXResolution and FocalPlaneYResolution. 2 = inches, 3 = centimeters. |
| Options | 2, 3 |
| Tag | 41488 |
| Type | Integer |

### The `exif:FocalPlaneXResolution` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.focalPlaneXResolution |
| ID | exif:FocalPlaneXResolution |
| Label | – |
| Name | focalPlaneXResolution |
| Definiton | EXIF tag 41486, 0xA20E. Horizontal focal resolution, measured pixels per unit. |
| Tag | 41486 |
| Type | Rational |
| Unit | pixels |

### The `exif:FocalPlaneYResolution` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.focalPlaneYResolution |
| ID | exif:FocalPlaneYResolution |
| Label | – |
| Name | focalPlaneYResolution |
| Definiton | EXIF tag 41487, 0xA20F. Vertical focal resolution, measured in pixels per unit. |
| Tag | 41487 |
| Type | Rational |
| Unit | pixels |

### The `exif:GainControl` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.gainControl |
| ID | exif:GainControl |
| Label | – |
| Name | gainControl |
| Definiton | EXIF tag 41991, 0xA407. Indicates the degree of overall image gain adjustment: 0 = None, 1 = Low gain up, 2 = High gain up, 3 = Low gain down, 4 = High gain down. |
| Options | 0, 1, 2, 3, 4 |
| Tag | 41991 |
| Type | Integer |

### The `exif:ImageUniqueID` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.imageUniqueID |
| ID | exif:ImageUniqueID |
| Label | – |
| Name | imageUniqueID |
| Definiton | EXIF tag 42016, 0xA420. An identifier assigned uniquely to each image. It is recorded as a 32 character ASCII string, equivalent to hexadecimal notation and 128-bit fixed length. |
| Tag | 42016 |
| Type | Text |

### The `exif:ISOSpeedRatings` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.ISOSpeedRatings |
| ID | exif:ISOSpeedRatings |
| Label | – |
| Name | ISOSpeedRatings |
| Definiton | EXIF tag 34855, 0x8827. ISO Speed and ISO Latitude of the input device as specified in ISO 12232. A native Exif ISO value of exactly 65535 indicates an ISO value of above 64K, which cannot be stored in the native Exif Tag 34855. The real value should be stored in the XMP. |
| Multiple? | Yes |
| Ordered? | Yes |
| Tag | 34855 |
| Type | Integer |

### The `exif:LightSource` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.lightSource |
| ID | exif:LightSource |
| Label | – |
| Name | lightSource |
| Definiton | EXIF tag 37384, 0x9208. Light source: 0 = unknown, 1 = Daylight, 2 = Fluorescent, 3 = Tungsten, 4 = Flash, 9 = Fine weather, 10 = Cloudy weather, 11 = Shade, 12 = Daylight fluorescent (D 5700 – 7100K), 13 = Day white fluorescent (N 4600 – 5400K), 14 = Cool white fluorescent (W 3900 – 4500K), 15 = White fluorescent (WW 3200 – 3700K), 17 = Standard light A, 18 = Standard light B, 19 = Standard light C, 20 = D55, 21 = D65, 22 = D75, 23 = D50, 24 = ISO studio tungsten, 255 = other. |
| Options | 0, 1, 2, 3, 4, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 255 |
| Tag | 37384 |
| Type | Integer |

### The `exif:MaxApertureValue` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.maxApertureValue |
| ID | exif:MaxApertureValue |
| Label | – |
| Name | maxApertureValue |
| Definiton | EXIF tag 37381, 0x9205. Smallest F number of lens, in APEX. |
| Tag | 37381 |
| Type | Rational |
| Unit | APEX |

### The `exif:MeteringMode` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.meteringMode |
| ID | exif:MeteringMode |
| Label | – |
| Name | meteringMode |
| Definiton | EXIF tag 37383, 0x9207. Metering mode: 0 = unknown, 1 = Average, 2 = CenterWeightedAverage, 3 = Spot, 4 = MultiSpot, 5 = Pattern, 6 = Partial, 255 = other. |
| Options | 0, 1, 2, 3, 4, 5, 6, 255 |
| Tag | 37383 |
| Type | Integer |

### The `exif:OECF` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.OECF |
| ID | exif:OECF |
| Label | – |
| Name | OECF |
| Definiton | EXIF tag 34856, 0x8828. Opto-Electoric Conversion Function as specified in ISO 14524. |
| Tag | 34856 |
| Type | OECFSFR |

### The `exif:PixelXDimension` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.pixelXDimension |
| ID | exif:PixelXDimension |
| Label | – |
| Name | pixelXDimension |
| Definiton | EXIF tag 40962, 0xA002. Valid image width, in pixels. |
| Tag | 40962 |
| Type | Integer |
| Unit | pixels |

### The `exif:PixelYDimension` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.pixelYDimension |
| ID | exif:PixelYDimension |
| Label | – |
| Name | pixelYDimension |
| Definiton | EXIF tag 40963, 0xA003. Valid image height, in pixels. |
| Tag | 40963 |
| Type | Integer |
| Unit | pixels |

### The `exif:RelatedSoundFile` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.relatedSoundFile |
| ID | exif:RelatedSoundFile |
| Label | – |
| Name | relatedSoundFile |
| Definiton | EXIF tag 40964, 0xA004. An 8.3 file name for the related sound file. |
| Tag | 40964 |
| Type | Text |

### The `exif:Saturation` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.saturation |
| ID | exif:Saturation |
| Label | – |
| Name | saturation |
| Definiton | EXIF tag 41993, 0xA409. Indicates the direction of saturation processing applied by the camera: 0 = Normal, 1 = Low saturation, 2 = High saturation. |
| Options | 0, 1, 2 |
| Tag | 40964 |
| Type | Integer |

### The `exif:SceneCaptureType` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.sceneCaptureType |
| ID | exif:SceneCaptureType |
| Label | – |
| Name | sceneCaptureType |
| Definiton | EXIF tag 41990, 0xA406. Indicates the type of scene that was shot: 0 = Standard, 1 = Landscape, 2 = Portrait, 3 = Night scene. |
| Options | 0, 1, 2, 3 |
| Tag | 41990 |
| Type | Integer |

### The `exif:SceneType` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.sceneType |
| ID | exif:SceneType |
| Label | – |
| Name | sceneType |
| Definiton | EXIF tag 41729, 0xA301. Indicates the type of scene: 1 (directly photographed image) is the only choice. |
| Options | 1 |
| Tag | 41729 |
| Type | Integer |

### The `exif:SensingMethod` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.sensingMethod |
| ID | exif:SensingMethod |
| Label | – |
| Name | sensingMethod |
| Definiton | EXIF tag 41495, 0xA217. Image sensor type on input device: 1 = Not defined, 2 = One-chip colour area sensor, 3 = Two-chip colour area sensor, 4 = Three-chip colour area sensor, 5 = Colour sequential area sensor, 7 = Trilinear sensor, 8 = Colour sequential linear sensor. |
| Options | 1, 2, 3, 4, 5, 7, 8 |
| Tag | 41495 |
| Type | Integer |

### The `exif:Sharpness` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.sharpness |
| ID | exif:Sharpness |
| Label | – |
| Name | sharpness |
| Definiton | EXIF tag 41994, 0xA40A. Indicates the direction of sharpness processing applied by the camera: 0 = Normal, 1 = Soft, 2 = Hard. |
| Options | 0, 1, 2 |
| Tag | 41994 |
| Type | Integer |

### The `exif:ShutterSpeedValue` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.shutterSpeedValue |
| ID | exif:ShutterSpeedValue |
| Label | – |
| Name | shutterSpeedValue |
| Definiton | EXIF tag 37377, 0x9201. Shutter speed, unit is APEX. See Annex C of the EXIF specification. |
| Tag | 37377 |
| Type | Rational |

### The `exif:SpatialFrequencyResponse` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.spatialFrequencyResponse |
| ID | exif:SpatialFrequencyResponse |
| Label | – |
| Name | spatialFrequencyResponse |
| Definiton | EXIF tag 41484, 0xA20C. Input device spatial frequency table and SFR values as specified in ISO 12233. |
| Tag | 41484 |
| Type | OECFSFR |

### The `exif:SpectralSensitivity` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.spectralSensitivity |
| ID | exif:SpectralSensitivity |
| Label | – |
| Name | spectralSensitivity |
| Definiton | EXIF tag 34852, 0x8824. Spectral sensitivity of each channel. |
| Tag | 34852 |
| Type | Text |

### The `exif:SubjectArea` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.subjectArea |
| ID | exif:SubjectArea |
| Label | – |
| Name | subjectArea |
| Definiton | EXIF tag 37396, 0x9214. The location and area of the main subject in the overall scene. |
| Multiple? | Yes |
| Ordered? | Yes |
| Tag | 37396 |
| Type | Integer |

### The `exif:SubjectDistance` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.subjectDistance |
| ID | exif:SubjectDistance |
| Label | – |
| Name | subjectDistance |
| Definiton | EXIF tag 37382, 0x9206. Distance to subject, in meters. |
| Tag | 37382 |
| Type | Rational |
| Unit | meters |

### The `exif:SubjectDistanceRange` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.subjectDistanceRange |
| ID | exif:SubjectDistanceRange |
| Label | – |
| Name | subjectDistanceRange |
| Definiton | EXIF tag 41996, 0xA40C. Indicates the distance to the subject: 0 = Unknown, 1 = Macro, 2 = Close view, 3 = Distant view. |
| Options | 0, 1, 2, 3 |
| Tag | 41996 |
| Type | Integer |

### The `exif:SubjectLocation` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.subjectLocation |
| ID | exif:SubjectLocation |
| Label | – |
| Name | subjectLocation |
| Definiton | EXIF tag 41492, 0xA214. Location of the main subject of the scene. The first value is the horizontal pixel and the second value is the vertical pixel at which the main subject appears. |
| Multiple? | Yes |
| Ordered? | Yes |
| Tag | 41492 |
| Type | Integer |

### The `exif:UserComment` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.userComment |
| ID | exif:UserComment |
| Label | – |
| Name | userComment |
| Combine? | Yes |
| Definiton | EXIF tag 37510, 0x9286. Comments from user. |
| Tag | 37510 |
| Type | LanguageAlternative |

### The `exif:WhiteBalance` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.whiteBalance |
| ID | exif:WhiteBalance |
| Label | – |
| Name | whiteBalance |
| Definiton | EXIF tag 41987, 0xA403. Indicates the white balance mode set when the image was shot: 0 = Auto white balance, 1 = Manual white balance. |
| Options | 0, 1 |
| Tag | 41987 |
| Type | Integer |

### The `exif:GPSAltitude` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.GPSAltitude |
| ID | exif:GPSAltitude |
| Label | – |
| Name | GPSAltitude |
| Definiton | GPS tag 6, 0x06. Indicates altitude in meters. |
| Tag | 6 |
| Type | Rational |
| Unit | meters |

### The `exif:GPSAltitudeRef` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.GPSAltitudeRef |
| ID | exif:GPSAltitudeRef |
| Label | – |
| Name | GPSAltitudeRef |
| Definiton | GPS tag 5, 0x5. Indicates whether the altitude is above or below sea level: 0 = Above sea level, 1 = Below sea level. |
| Options | 0, 1 |
| Tag | 5 |
| Type | Integer |

### The `exif:GPSAreaInformation` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.GPSAreaInformation |
| ID | exif:GPSAreaInformation |
| Label | – |
| Name | GPSAreaInformation |
| Definiton | GPS tag 28, 0x1C. A character string recording the name of the GPS area. |
| Tag | 28 |
| Type | Text |

### The `exif:GPSDestBearing` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.GPSDestBearing |
| ID | exif:GPSDestBearing |
| Label | – |
| Name | GPSDestBearing |
| Definiton | GPS tag 24, 0x18. Destination bearing, values from 0 to 359.99. |
| Maximum Value | 359.99 |
| Minimum Value | 0 |
| Tag | 24 |
| Type | Rational |

### The `exif:GPSDestBearingRef` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.GPSDestBearingRef |
| ID | exif:GPSDestBearingRef |
| Label | – |
| Name | GPSDestBearingRef |
| Definiton | GPS tag 23, 0x17. Reference for movement direction: T = true direction, M = magnetic direction. |
| Options | T, M |
| Tag | 23 |
| Type | Text |

### The `exif:GPSDestDistance` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.GPSDestDistance |
| ID | exif:GPSDestDistance |
| Label | – |
| Name | GPSDestDistance |
| Definiton | GPS tag 26, 0x1A. Distance to destination. |
| Tag | 26 |
| Type | Rational |

### The `exif:GPSDestDistanceRef` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.GPSDestDistanceRef |
| ID | exif:GPSDestDistanceRef |
| Label | – |
| Name | GPSDestDistanceRef |
| Definiton | GPS tag 25, 0x19. Units used for speed measurement: "K" = kilometers, "M" = miles, "N" = knots. |
| Options | K, MN |
| Tag | 25 |
| Type | Text |

### The `exif:GPSDestLatitude` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.GPSDestLatitude |
| ID | exif:GPSDestLatitude |
| Label | – |
| Name | GPSDestLatitude |
| Definiton | GPS tag 20, 0x14 (position) and 19, 0x13 (North/South). Indicates destination latitude. |
| Tag | 20 |
| Type | Text |

### The `exif:GPSDestLongitude` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.GPSDestLongitude |
| ID | exif:GPSDestLongitude |
| Label | – |
| Name | GPSDestLongitude |
| Definiton | GPS tag 22, 0x16 (position) and 21, 0x15 (East/West). Indicates destination longitude. |
| Tag | 22 |
| Type | Text |

### The `exif:GPSDifferential` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.GPSDifferential |
| ID | exif:GPSDifferential |
| Label | – |
| Name | GPSDifferential |
| Definiton | GPS tag 30, 0x1E. Indicates whether differential correction is applied to the GPS receiver: 0 = Without correction, 1 = Correction applied. |
| Options | 0, 1 |
| Tag | 30 |
| Type | Integer |

### The `exif:GPSDOP` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.GPSDOP |
| ID | exif:GPSDOP |
| Label | – |
| Name | GPSDOP |
| Definiton | GPS tag 11, 0x0B. Degree of precision for GPS data. |
| Tag | 11 |
| Type | Rational |

### The `exif:GPSImgDirection` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.GPSImgDirection |
| ID | exif:GPSImgDirection |
| Label | – |
| Name | GPSImgDirection |
| Definiton | GPS tag 17, 0x11. Direction of image when captured, values range from 0 to 359.99. |
| Maximum Value | 359.99 |
| Minimum Value | 0 |
| Tag | 17 |
| Type | Rational |

### The `exif:GPSImgDirectionRef` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.GPSImgDirectionRef |
| ID | exif:GPSImgDirectionRef |
| Label | – |
| Name | GPSImgDirectionRef |
| Definiton | GPS tag 16, 0x10. Reference for movement direction: "T" = true direction, "M" = magnetic direction. |
| Options | T, M |
| Tag | 16 |
| Type | Text |

### The `exif:GPSLatitude` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.GPSLatitude |
| ID | exif:GPSLatitude |
| Label | – |
| Name | GPSLatitude |
| Definiton | GPS tag 2, 0x02 (position) and 1, 0x01 (North/South). Indicates latitude. |
| Tag | 2 |
| Type | Text |

### The `exif:GPSLongitude` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.GPSLongitude |
| ID | exif:GPSLongitude |
| Label | – |
| Name | GPSLongitude |
| Definiton | GPS tag 4, 0x04 (position) and 3, 0x03 (East/West). Indicates longitude. |
| Tag | 4 |
| Type | Text |

### The `exif:GPSMapDatum` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.GPSMapDatum |
| ID | exif:GPSMapDatum |
| Label | – |
| Name | GPSMapDatum |
| Definiton | GPS tag 18, 0x12. Geodetic survey data. |
| Tag | 18 |
| Type | Text |

### The `exif:GPSMeasureMode` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.GPSMeasureMode |
| ID | exif:GPSMeasureMode |
| Label | – |
| Name | GPSMeasureMode |
| Definiton | GPS tag 10, 0x0A. GPS measurement mode, Text type: "2" = two-dimensional measurement, "3" = three-dimensional measurement. |
| Options | 2, 3 |
| Tag | 10 |
| Type | Text |

### The `exif:GPSProcessingMethod` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.GPSProcessingMethod |
| ID | exif:GPSProcessingMethod |
| Label | – |
| Name | GPSProcessingMethod |
| Definiton | GPS tag 27, 0x1B. A character string recording the name of the method used for location finding. |
| Tag | 27 |
| Type | Text |

### The `exif:GPSSatellites` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.GPSSatellites |
| ID | exif:GPSSatellites |
| Label | – |
| Name | GPSSatellites |
| Definiton | GPS tag 8, 0x08. Satellite information, format is unspecified. |
| Tag | 8 |
| Type | Text |

### The `exif:GPSSpeed` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.GPSSpeed |
| ID | exif:GPSSpeed |
| Label | – |
| Name | GPSSpeed |
| Definiton | GPS tag 13, 0x0D. Speed of GPS receiver movement. |
| Tag | 13 |
| Type | Rational |

### The `exif:GPSSpeedRef` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.GPSSpeedRef |
| ID | exif:GPSSpeedRef |
| Label | – |
| Name | GPSSpeedRef |
| Definiton | GPS tag 12, 0x0C. Units used for speed measurement: "K" = kilometers per hour, "M" = miles per hour, "N" = knots. |
| Options | K, M, N |
| Tag | 12 |
| Type | Text |

### The `exif:GPSStatus` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.GPSStatus |
| ID | exif:GPSStatus |
| Label | – |
| Name | GPSStatus |
| Definiton | GPS tag 9, 0x09. Status of GPS receiver at image creation time: "A" = measurement in progress, "V" = measurement is interoperability. |
| Options | A, V |
| Tag | 9 |
| Type | Text |

### The `exif:GPSTimeStamp` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.GPSTimeStamp |
| ID | exif:GPSTimeStamp |
| Label | – |
| Name | GPSTimeStamp |
| Definiton | GPS tag 29 (date), 0x1D, and, and GPS tag 7 (time), 0x07. Time stamp of GPS data, in Coordinated Universal Time. NOTE: The GPSDateStamp tag is new in EXIF 2.2. The GPS timestamp in EXIF 2.1 does not include a date. If not present, the date component for the XMP should be taken from exif:DateTimeOriginal, or if that is also lacking from exif:DateTimeDigitized. If no date is available, do not write exif:GPSTimeStamp to XMP. |
| Tag | 29 |
| Type | Date |

### The `exif:GPSTrack` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.GPSTrack |
| ID | exif:GPSTrack |
| Label | – |
| Name | GPSTrack |
| Definiton | GPS tag 15, 0x0F. Direction of GPS movement, values range from 0 to 359.99. |
| Maximum Value | 359.99 |
| Minimum Value | 0 |
| Tag | 15 |
| Type | Rational |

### The `exif:GPSTrackRef` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.GPSTrackRef |
| ID | exif:GPSTrackRef |
| Label | – |
| Name | GPSTrackRef |
| Definiton | GPS tag 14, 0x0E. Reference for movement direction: "T" = true direction, "M" = magnetic direction. |
| Options | T, M |
| Tag | 14 |
| Type | Text |

### The `exif:GPSVersionID` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.exif.GPSVersionID |
| ID | exif:GPSVersionID |
| Label | – |
| Name | GPSVersionID |
| Definiton | GPS tag 0, 0x00. A decimal encoding of each of the four EXIF bytes with period separators. The current value is "2.3.0.0". |
| Tag | 0 |
| Type | Text |

The XMP metadata model's 'tiff' namespace offers 25 fields which are detailed below:

### The `tiff:Artist` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.tiff.artist |
| ID | tiff:Artist |
| Label | – |
| Name | artist |
| Definiton | Camera owner, photographer or image creator. NOTE: This property is stored in XMP as the first item in the dc:creator array. |
| Type | ProperName |

### The `tiff:BitsPerSample` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.tiff.bitsPerSample |
| ID | tiff:BitsPerSample |
| Label | – |
| Name | bitsPerSample |
| Definiton | Number of bits per component in each channel. |
| Multiple? | Yes |
| Ordered? | Yes |
| Type | Integer |

### The `tiff:Compression` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.tiff.compression |
| ID | tiff:Compression |
| Label | – |
| Name | compression |
| Definiton | Compression scheme. 1 = Uncompressed , 6 = JPEG. |
| Options | 1, 6 |
| Type | Integer |

### The `tiff:Copyright` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.tiff.Copyright |
| ID | tiff:Copyright |
| Label | – |
| Name | Copyright |
| Combine? | Yes |
| Definiton | Copyright information as an ASCII string. NOTE: This property is stored in XMP as dc:rights. |
| Pseudonym | exiftool: Copyright |
| Type | LanguageAlternative |

### The `tiff:DateTime` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.tiff.DateTime |
| ID | tiff:DateTime |
| Label | – |
| Name | DateTime |
| Definiton | Date and time when the file was last modified (no time zone in EXIF), stored in ISO 8601 format, not the original EXIF format. This property includes the value for the EXIF SubSecTime(37520, 0x9290) attribute. NOTE: This property is stored in XMP as xmp:ModifyDate. |
| Type | Date |

### The `tiff:ImageDescription` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.tiff.ImageDescription |
| ID | tiff:ImageDescription |
| Label | – |
| Name | ImageDescription |
| Combine? | Yes |
| Definiton | The title of the image as an ASCII string. NOTE: This property is stored in XMP as dc:description. |
| Type | LanguageAlternative |

### The `tiff:ImageLength` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.tiff.ImageLength |
| ID | tiff:ImageLength |
| Label | – |
| Name | ImageLength |
| Alias | ImageHeight |
| Definiton | Image height in pixels. |
| Type | Integer |
| Unit | pixels |

### The `tiff:ImageWidth` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.tiff.ImageWidth |
| ID | tiff:ImageWidth |
| Label | – |
| Name | ImageWidth |
| Definiton | Image width in pixels. |
| Type | Integer |
| Unit | pixels |

### The `tiff:Make` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.tiff.Make |
| ID | tiff:Make |
| Label | – |
| Name | Make |
| Definiton | Manufacturer of recording equipment as an ASCII string. |
| Encoding | ASCII |
| Type | ProperName |

### The `tiff:Model` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.tiff.Model |
| ID | tiff:Model |
| Label | – |
| Name | Model |
| Definiton | Model name or number of equipment as an ASCII string. |
| Encoding | ASCII |
| Type | ProperName |

### The `tiff:Orientation` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.tiff.Orientation |
| ID | tiff:Orientation |
| Label | – |
| Name | Orientation |
| Definiton | Orientation: 1 = 0th row at the top, 0th column at left, 2 = 0th row at the top, 0th column at right, 3 = 0th row at the bottom, 0th column at right, 4 = 0th row at the bottom, 0th column at left, 5 = 0th row at the left, 0th column at top, 6 = 0th row at the right, 0th column at top, 7 = 0th row at the right, 0th column at bottom, 8 = 0th row at the left, 0th column at bottom. |
| Options | 1, 2, 3, 4, 5, 6, 7, 8 |
| Type | Integer |

### The `tiff:PhotometricInterpretation` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.tiff.photometricInterpretation |
| ID | tiff:PhotometricInterpretation |
| Label | – |
| Name | photometricInterpretation |
| Definiton | Pixel Composition: 2 = RGB, 6 = YCbCr. |
| Options | 2, 6 |
| Type | Integer |

### The `tiff:PlanarConfiguration` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.tiff.planarConfiguration |
| ID | tiff:PlanarConfiguration |
| Label | – |
| Name | planarConfiguration |
| Definiton | Data layout: 1 = chunky, 2 = planar. |
| Options | 1, 2 |
| Type | Integer |

### The `tiff:PrimaryChromaticities` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.tiff.primaryChromaticities |
| ID | tiff:PrimaryChromaticities |
| Label | – |
| Name | primaryChromaticities |
| Definiton | Chromaticity of the three primary colors. |
| Multiple? | Yes |
| Ordered? | Yes |
| Type | Rational |

### The `tiff:ReferenceBlackWhite` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.tiff.referenceBlackWhite |
| ID | tiff:ReferenceBlackWhite |
| Label | – |
| Name | referenceBlackWhite |
| Definiton | Reference black and white point values. |
| Multiple? | Yes |
| Ordered? | Yes |
| Type | Rational |

### The `tiff:ResolutionUnit` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.tiff.resolutionUnit |
| ID | tiff:ResolutionUnit |
| Label | – |
| Name | resolutionUnit |
| Definiton | Unit used for XResolution and YResolution. Value is one of 2 = Inches, 3 = Centimeters. |
| Options | 2, 3 |
| Type | Integer |

### The `tiff:SamplesPerPixel` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.tiff.samplesPerPixel |
| ID | tiff:SamplesPerPixel |
| Label | – |
| Name | samplesPerPixel |
| Definiton | Number of components per pixel. |
| Type | Integer |

### The `tiff:Software` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.tiff.software |
| ID | tiff:Software |
| Label | – |
| Name | software |
| Definiton | Software or firmware used to generate image. NOTE: This property is stored in XMP as xmp:CreatorTool. |
| Type | AgentName |

### The `tiff:TransferFunction` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.tiff.transferFunction |
| ID | tiff:TransferFunction |
| Label | – |
| Name | transferFunction |
| Count/Length | 768 |
| Definiton | Transfer function for image described in tabular style with 3 * 256 entries. |
| Multiple? | Yes |
| Ordered? | Yes |
| Type | Integer |

### The `tiff:WhitePoint` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.tiff.whitePoint |
| ID | tiff:WhitePoint |
| Label | – |
| Name | whitePoint |
| Definiton | Chromaticity of white point. |
| Multiple? | Yes |
| Ordered? | Yes |
| Type | Rational |

### The `tiff:XResolution` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.tiff.XResolution |
| ID | tiff:XResolution |
| Label | – |
| Name | XResolution |
| Definiton | Horizontal resolution in pixels per unit. |
| Type | Rational |

### The `tiff:YResolution` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.tiff.YResolution |
| ID | tiff:YResolution |
| Label | – |
| Name | YResolution |
| Definiton | Vertical resolution in pixels per unit. |
| Type | Rational |

### The `tiff:YCbCrCoefficients` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.tiff.YCbCrCoefficients |
| ID | tiff:YCbCrCoefficients |
| Label | – |
| Name | YCbCrCoefficients |
| Definiton | Matrix coefficients for RGB to YCbCr transformation. |
| Multiple? | Yes |
| Ordered? | Yes |
| Type | Rational |

### The `tiff:YCbCrPositioning` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.tiff.YCbCrPositioning |
| ID | tiff:YCbCrPositioning |
| Label | – |
| Name | YCbCrPositioning |
| Definiton | Position of chrominance vs. luminance components: 1 = centered, 2 = co-sited. |
| Options | 1, 2 |
| Type | Integer |

### The `tiff:YCbCrSubSampling` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.tiff.YCbCrSubSampling |
| ID | tiff:YCbCrSubSampling |
| Label | – |
| Name | YCbCrSubSampling |
| Definiton | Sampling ratio of chrominance components: [2,1] = YCbCr4:2:2, [2,2] = YCbCr4:2:0. |
| Multiple? | Yes |
| Ordered? | Yes |
| Type | Integer |

The XMP metadata model's 'dc' namespace offers fifteen fields which are detailed below:

### The `dc:contributor` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dc.Contributor |
| ID | dc:contributor |
| Label | – |
| Name | Contributor |
| Definiton | DCMI definition: An entity responsible for making contributions to the resource. DCMI comment: Examples of a contributor include a person, an organization, or a service. Typically, the name of a contributor should be used to indicate the entity. XMP addition: XMP usage is a list of contributors. These contributors should not include those listed in dc:creator. |
| Multiple? | Yes |
| Ordered? | No |
| Pseudonym | exiftool: -XMP-dc:Contributor |
| Type | ProperName |

### The `dc:coverage` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dc.Coverage |
| ID | dc:coverage |
| Label | – |
| Name | Coverage |
| Definiton | DCMI definition: The spatial or temporal topic of the resource, the spatial applicability of the resource, or the jurisdiction under which the resource is relevant. XMP addition: XMP usage is the extent or scope of the resource. |
| Pseudonym | exiftool: -XMP-dc:Coverage |
| Type | Text |

### The `dc:creator` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dc.Creator |
| ID | dc:creator |
| Label | – |
| Name | Creator |
| Definiton | DCMI definition: An entity primarily responsible for making the resource. DCMI comment: Examples of a creator include a person, an organization, or a service. Typically, the name of a creator should be used to indicate the entity. XMP addition: XMP usage is a list of creators. Entities should be listed in order of decreasing precedence, if such order is significant. |
| Multiple? | Yes |
| Ordered? | Yes |
| Pseudonym | exiftool: -XMP-dc:Creator |
| Type | ProperName |

### The `dc:date` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dc.date |
| ID | dc:date |
| Label | – |
| Name | date |
| Definiton | DCMI definition: A point or period of time associated with an event in the life cycle of the resource. |
| Multiple? | Yes |
| Ordered? | Yes |
| Pseudonym | exiftool: -XMP-dc:Date |
| Type | Date |

### The `dc:description` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dc.Description |
| ID | dc:description |
| Label | – |
| Name | Description |
| Combine? | Yes |
| Definiton | DCMI definition: An account of the resource. XMP addition: XMP usage is a list of textual descriptions of the content of the resource, given in various languages. |
| Pseudonym | exiftool: -XMP-dc:Description |
| Type | LanguageAlternative |

### The `dc:format` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dc.Format |
| ID | dc:format |
| Label | – |
| Name | Format |
| Definiton | DCMI definition: The file format, physical medium, or dimensions of the resource. DCMI comment: Examples of dimensions include size and duration. Recommended best practice is to use a controlled vocabulary such as the list of Internet Media Types [MIME]. XMP addition: XMP usage is a MIME type. Dimensions would be stored using a media-specific property, beyond the scope of this document. |
| Pseudonym | exiftool: -XMP-dc:Format |
| Type | MIMEType |

### The `dc:identifier` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dc.Identifier |
| ID | dc:identifier |
| Label | – |
| Name | Identifier |
| Definiton | DCMI definition: An unambiguous reference to the resource within a given context. DCMI comment: Recommended best practice is to identify the resource by means of a string conforming to a formal identification system. |
| Pseudonym | exiftool: -XMP-dc:Identifier |
| Type | Text |

### The `dc:language` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dc.Language |
| ID | dc:language |
| Label | – |
| Name | Language |
| Definiton | DCMI definition: A language of the resource. XMP addition: XMP usage is a list of languages used in the content of the resource. |
| Multiple? | Yes |
| Ordered? | No |
| Pseudonym | exiftool: -XMP-dc:Language |
| Type | Locale |

### The `dc:publisher` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dc.Publisher |
| ID | dc:publisher |
| Label | – |
| Name | Publisher |
| Definiton | DCMI definition: An entity responsible for making the resource available. DCMI comment: Examples of a publisher include a person, an organization, or a service. Typically, the name of a publisher should be used to indicate the entity. XMP addition: XMP usage is a list of publishers. |
| Multiple? | Yes |
| Ordered? | No |
| Pseudonym | exiftool: -XMP-dc:Publisher |
| Type | ProperName |

### The `dc:relation` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dc.Relation |
| ID | dc:relation |
| Label | – |
| Name | Relation |
| Definiton | DCMI definition: A related resource.DCMI comment: Recommended best practice is to identify the related resource by means of a string conforming to a formal identification system. XMP addition: XMP usage is a list of related resources. |
| Multiple? | Yes |
| Ordered? | No |
| Pseudonym | exiftool: -XMP-dc:Relation |
| Type | Text |

### The `dc:rights` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dc.Rights |
| ID | dc:rights |
| Label | – |
| Name | Rights |
| Combine? | Yes |
| Definiton | DCMI definition: Information about rights held in and over the resource. DCMI comment: Typically, rights information includes a statement about various property rights associated with the resource, including intellectual property rights. XMP addition: XMP usage is a list of informal rights statements, given in various languages. |
| Pseudonym | exiftool: -XMP-dc:Rights |
| Type | LanguageAlternative |

### The `dc:source` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dc.Source |
| ID | dc:source |
| Label | – |
| Name | Source |
| Definiton | DCMI definition: A related resource from which the described resource is derived. DCMI comment: The described resource may be derived from the related resource in whole or in part. Recommended best practice is to identify the related resource by means of a string conforming to a formal identification system. |
| Pseudonym | exiftool: -XMP-dc:Source |
| Type | Text |

### The `dc:subject` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dc.Subject |
| ID | dc:subject |
| Label | – |
| Name | Subject |
| Definiton | DCMI definition: The topic of the resource.DCMI comment: Typically, the subject will be represented using keywords, key phrases, or classification codes. Recommended best practice is to use a controlled vocabulary. To describe the spatial or temporal topic of the resource, use the dc:coverage element. XMP addition: XMP usage is a list of descriptive phrases or keywords that specify the content of the resource. |
| Multiple? | Yes |
| Ordered? | No |
| Pseudonym | exiftool: -XMP-dc:Subject |
| Type | Text |

### The `dc:title` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dc.Title |
| ID | dc:title |
| Label | – |
| Name | Title |
| Combine? | Yes |
| Definiton | DCMI definition: A name given to the resource. DCMI comment: Typically, a title will be a name by which the resource is formally known. XMP addition: XMP usage is a title or name, given in various languages. |
| Pseudonym | exiftool: -XMP-dc:Title |
| Type | LanguageAlternative |

### The `dc:type` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.dc.Type |
| ID | dc:type |
| Label | – |
| Name | Type |
| Definiton | DCMI definition: The nature or genre of the resource. DCMI comment: Recommended best practice is to use a controlled vocabulary such as the DCMI Type Vocabulary [DCMITYPE]. To describe the file format, physical medium, or dimensions of the resource, use the dc:format element. XMP addition: See the dc:format entry for clarification of the XMP usage of that element. |
| Multiple? | Yes |
| Ordered? | No |
| Pseudonym | exiftool: -XMP-dc:Type |
| Type | Text |

The XMP metadata model's 'iptc_core' namespace offers thirteen fields which are detailed below:

### The `Iptc4xmpCore:CreatorContactInfo` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.iptc.creatorContactInfo |
| ID | Iptc4xmpCore:CreatorContactInfo |
| Label | – |
| Name | creatorContactInfo |
| Definiton | The creator contact information provides all necessary information to get in contact with the creator of this news object and comprises a set of sub-properties for proper addressing. |
| Pseudonym | exiftool: XMP-iptcCore:CreatorContactInfo |
| Structure | Iptc4xmpCore:CreatorContactInfo |
| Type | ContactInfo |

### The `Iptc4xmpCore:CiAdrExtadr` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.iptc.CreatorContactAddress |
| ID | Iptc4xmpCore:CiAdrExtadr |
| Label | – |
| Name | CreatorContactAddress |
| Definiton | – |
| Pseudonym | exiftool: CreatorAddress |
| Structure | Iptc4xmpCore:CreatorContactInfo |
| Type | Text |

### The `Iptc4xmpCore:CiAdrCity` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.iptc.CreatorContactCity |
| ID | Iptc4xmpCore:CiAdrCity |
| Label | – |
| Name | CreatorContactCity |
| Definiton | – |
| Pseudonym | exiftool: CreatorCity |
| Structure | Iptc4xmpCore:CreatorContactInfo |
| Type | Text |

### The `Iptc4xmpCore:CiAdrCtry` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.iptc.CreatorContactCountry |
| ID | Iptc4xmpCore:CiAdrCtry |
| Label | – |
| Name | CreatorContactCountry |
| Definiton | – |
| Pseudonym | exiftool: CreatorCountry |
| Structure | Iptc4xmpCore:CreatorContactInfo |
| Type | Text |

### The `Iptc4xmpCore:CiAdrPcode` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.iptc.CreatorContactPostalCode |
| ID | Iptc4xmpCore:CiAdrPcode |
| Label | – |
| Name | CreatorContactPostalCode |
| Definiton | – |
| Pseudonym | exiftool: CreatorPostalCode |
| Structure | Iptc4xmpCore:CreatorContactInfo |
| Type | Text |

### The `Iptc4xmpCore:CiAdrRegion` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.iptc.CreatorContactRegion |
| ID | Iptc4xmpCore:CiAdrRegion |
| Label | – |
| Name | CreatorContactRegion |
| Definiton | – |
| Pseudonym | exiftool: CreatorRegion |
| Structure | Iptc4xmpCore:CreatorContactInfo |
| Type | Text |

### The `Iptc4xmpCore:CiEmailWork` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.iptc.CreatorContactWorkEmail |
| ID | Iptc4xmpCore:CiEmailWork |
| Label | – |
| Name | CreatorContactWorkEmail |
| Definiton | – |
| Pseudonym | exiftool: CreatorWorkEmail |
| Structure | Iptc4xmpCore:CreatorContactInfo |
| Type | Text |

### The `Iptc4xmpCore:CiUrlWork` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.iptc.CreatorContactWorkURL |
| ID | Iptc4xmpCore:CiUrlWork |
| Label | – |
| Name | CreatorContactWorkURL |
| Definiton | – |
| Pseudonym | exiftool: CreatorWorkURL |
| Structure | Iptc4xmpCore:CreatorContactInfo |
| Type | URL |

### The `Iptc4xmpCore:IntellectualGenre` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.iptc.intellectualGenre |
| ID | Iptc4xmpCore:IntellectualGenre |
| Label | – |
| Name | intellectualGenre |
| Definiton | Describes the nature, intellectual or journalistic characteristic of a news object, not specifically its content. |
| Type | Text |

### The `Iptc4xmpCore:Scene` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.iptc.scene |
| ID | Iptc4xmpCore:Scene |
| Label | – |
| Name | scene |
| Definiton | Describes the scene of a photo content. Specifies one ore more terms from the IPTC Scene-NewsCodes. Each Scene is represented as a string of 6 digits in an unordered list. |
| Multiple? | Yes |
| Ordered? | No |
| Type | Text |

### The `Iptc4xmpCore:Location` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.iptc.location |
| ID | Iptc4xmpCore:Location |
| Label | – |
| Name | location |
| Definiton | Name of a location the content is focussing on -- either the location shown in visual media or referenced by text or audio media. This location name could either be the name of a sublocation to a city or the name of a well known location or (natural) monument outside a city. In the sense of a sublocation to a city this element is at the fourth level of a top-down geographical hierarchy. |
| Type | Text |

### The `Iptc4xmpCore:CountryCode` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.iptc.countryCode |
| ID | Iptc4xmpCore:CountryCode |
| Label | – |
| Name | countryCode |
| Definiton | Code of the country the content is focussing on -- either the country shown in visual media or referenced in text or audio media. This element is at the top/first level of a top-down geographical hierarchy. The code should be taken from ISO 3166 two or three letter code. The full name of a country should go to the "Country" element. |
| Type | Locale |

### The `Iptc4xmpCore:SubjectCode` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.iptc.subjectCode |
| ID | Iptc4xmpCore:SubjectCode |
| Label | – |
| Name | subjectCode |
| Definiton | Specifies one or more Subjects from the IPTC Subject-NewsCodes taxonomy to categorize the content. Each Subject is represented as a string of 8 digits in an unordered list. |
| Multiple? | Yes |
| Ordered? | No |
| Type | Text |

The XMP metadata model's 'iptc_extended' namespace offers seventeen fields which are detailed below:

### The `Iptc4xmpExt:AOCircaDateCreated` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.iptc.AOCircaDateCreated |
| ID | Iptc4xmpExt:AOCircaDateCreated |
| Label | – |
| Name | AOCircaDateCreated |
| Alias | ArtworkOrObjectCircaDateCreated, ArtworkCircaDateCreated, ObjectCircaDateCreated |
| Definiton | Approximate date or range of dates associated with the creation and production of an artwork or object or its components. |
| Pseudonym | exiftool: ArtworkCircaDateCreated |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | Text |

### The `Iptc4xmpExt:AOContentDescription` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.iptc.AOContentDescription |
| ID | Iptc4xmpExt:AOContentDescription |
| Label | – |
| Name | AOContentDescription |
| Alias | ArtworkOrObjectContentDescription, ArtworkContentDescription, ObjectContentDescription |
| Definiton | A textual description of the content depicted in the artwork or object. |
| Pseudonym | exiftool: ArtworkContentDescription |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | Text |

### The `Iptc4xmpExt:AOContributionDescription` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.iptc.AOContributionDescription |
| ID | Iptc4xmpExt:AOContributionDescription |
| Label | – |
| Name | AOContributionDescription |
| Alias | ArtworkOrObjectContributionDescription, ArtworkContributionDescription, ObjectContributionDescription |
| Definiton | A textual description about a contribution made to an artwork or an object. |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | Text |

### The `Iptc4xmpExt:AOCopyrightNotice` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.iptc.AOCopyrightNotice |
| ID | Iptc4xmpExt:AOCopyrightNotice |
| Label | – |
| Name | AOCopyrightNotice |
| Alias | ArtworkOrObjectCopyrightNotice, ArtworkCopyrightNotice, ObjectCopyrightNotice |
| Definiton | Contains any necessary copyright notice for claiming the intellectual property for artwork or an object in the image and should identify the current owner of the copyright of this work with associated intellectual property rights. |
| Pseudonym | exiftool: ArtworkCopyrightNotice |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | Text |

### The `Iptc4xmpExt:AOCreator` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.iptc.AOCreator |
| ID | Iptc4xmpExt:AOCreator |
| Label | – |
| Name | AOCreator |
| Alias | ArtworkOrObjectCreator, ArtworkCreator, ObjectCreator |
| Definiton | Contains the name of the artist who has created artwork or an object in the image. In cases where the artist could or should not be identified the name of a company or organisation may be appropriate. |
| Pseudonym | exiftool: ArtworkCreator |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | Text |

### The `Iptc4xmpExt:AOCreatorID` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.iptc.AOCreatorID |
| ID | Iptc4xmpExt:AOCreatorID |
| Label | – |
| Name | AOCreatorID |
| Alias | ArtworkOrObjectCreatorID, ArtworkCreatorID, ObjectCreatorID |
| Definiton | Globally unique identifier for the creator of artwork or object. |
| Pseudonym | exiftool: ArtworkCreatorID |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | Text |

### The `Iptc4xmpExt:AOCurrentCopyrightOwnerID` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.iptc.AOCurrentCopyrightOwnerID |
| ID | Iptc4xmpExt:AOCurrentCopyrightOwnerID |
| Label | – |
| Name | AOCurrentCopyrightOwnerID |
| Alias | ArtworkOrObjectCopyrightOwnerID, ArtworkCopyrightOwnerID, ObjectCopyrightOwnerID |
| Definiton | Globally unique identifier for the current owner of the copyright of the artwork or object. |
| Pseudonym | exiftool: ArtworkCopyrightOwnerID |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | Text |

### The `Iptc4xmpExt:AOCurrentCopyrightOwnerName` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.iptc.AOCurrentCopyrightOwnerName |
| ID | Iptc4xmpExt:AOCurrentCopyrightOwnerName |
| Label | – |
| Name | AOCurrentCopyrightOwnerName |
| Alias | ArtworkOrObjectCopyrightOwnerName, ArtworkCopyrightOwnerName, ObjectCopyrightOwnerName |
| Definiton | Name of the current owner of the copyright of the artwork or object. |
| Pseudonym | exiftool: ArtworkCopyrightOwnerName |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | Text |

### The `Iptc4xmpExt:AOCurrentLicensorID` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.iptc.AOCurrentLicensorID |
| ID | Iptc4xmpExt:AOCurrentLicensorID |
| Label | – |
| Name | AOCurrentLicensorID |
| Alias | ArtworkOrObjectCurrentLicensorID, ArtworkCurrentLicensorID, ObjectCurrentLicensorID |
| Definiton | Globally unique identifier for the current licensor of the artwork or object. |
| Pseudonym | exiftool: ArtworkCurrentLicensorID |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | Text |

### The `Iptc4xmpExt:AOCurrentLicensorName` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.iptc.AOCurrentLicensorName |
| ID | Iptc4xmpExt:AOCurrentLicensorName |
| Label | – |
| Name | AOCurrentLicensorName |
| Alias | ArtworkOrObjectCurrentLicensorName, ArtworkCurrentLicensorName, ObjectCurrentLicensorName |
| Definiton | Name of the current licensor of the artwork or object. |
| Pseudonym | exiftool: ArtworkCurrentLicensorName |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | Text |

### The `Iptc4xmpExt:AODateCreated` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.iptc.AODateCreated |
| ID | Iptc4xmpExt:AODateCreated |
| Label | – |
| Name | AODateCreated |
| Alias | ArtworkOrObjectDateCreated, ArtworkDateCreated, ObjectDateCreated |
| Definiton | Designates the date and optionally the time the artwork or object in the image was created. This relates to artwork or objects with associated intellectual property rights. |
| Pseudonym | exiftool: ArtworkDateCreated |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | DateTime |

### The `Iptc4xmpExt:AOPhysicalDescription` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.iptc.AOPhysicalDescription |
| ID | Iptc4xmpExt:AOPhysicalDescription |
| Label | – |
| Name | AOPhysicalDescription |
| Alias | ArtworkOrObjectPhysicalDescription, ArtworkPhysicalDescription, ObjectPhysicalDescription |
| Definiton | A textual description of the physical characteristics of the artwork or object, without reference to the content depicted. |
| Pseudonym | exiftool: ArtworkPhysicalDescription |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | Text |

### The `Iptc4xmpExt:AOSource` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.iptc.AOSource |
| ID | Iptc4xmpExt:AOSource |
| Label | – |
| Name | AOSource |
| Alias | ArtworkOrObjectSource, ArtworkSource, ObjectSource |
| Definiton | The organisation or body holding and registering the artwork or object in the image for inventory purposes. |
| Pseudonym | exiftool: ArtworkSource |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | Text |

### The `Iptc4xmpExt:AOSourceInvNo` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.iptc.AOSourceInvNo |
| ID | Iptc4xmpExt:AOSourceInvNo |
| Label | – |
| Name | AOSourceInvNo |
| Alias | ArtworkOrObjectSourceInventoryNo, ArtworkSourceInventoryNo, ObjectSourceInventoryNo |
| Definiton | The inventory number issued by the organisation or body holding and registering the artwork or object in the image. |
| Pseudonym | exiftool: ArtworkSourceInventoryNo |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | Text |

### The `Iptc4xmpExt:AOSourceInvURL` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.iptc.AOSourceInvURL |
| ID | Iptc4xmpExt:AOSourceInvURL |
| Label | – |
| Name | AOSourceInvURL |
| Alias | ArtworkOrObjectSourceInventoryURL, ArtworkSourceInventoryURL, ObjectSourceInventoryURL |
| Definiton | URL reference to the metadata record of the inventory maintained by the Source. |
| Pseudonym | exiftool: ArtworkSourceInvURL |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | URL |

### The `Iptc4xmpExt:AOStylePeriod` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.iptc.AOStylePeriod |
| ID | Iptc4xmpExt:AOStylePeriod |
| Label | – |
| Name | AOStylePeriod |
| Alias | ArtworkOrObjectStylePeriod, ArtworkStylePeriod, ObjectStylePeriod |
| Definiton | The style, historical or artistic period, movement, group, or school whose characteristics are represented in the artwork or object. |
| Pseudonym | exiftool: ArtworkStylePeriod |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | Text |

### The `Iptc4xmpExt:AOTitle` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | xmp.iptc.AOTitle |
| ID | Iptc4xmpExt:AOTitle |
| Label | – |
| Name | AOTitle |
| Alias | ArtworkOrObjectTitle, ArtworkTitle, ObjectTitle |
| Definiton | A reference for the artwork or object in the image. |
| Pseudonym | exiftool: ArtworkTitle |
| Structure | Iptc4xmpExt:ArtworkOrObject |
| Type | Text |


### Credits & References

The XMP field information was researched from various sources including the Adobe® XMP
specification and EXIFTool documentation. Please visit these valuable online resources
to learn more about the XMP metadata model specification and to support these world
class organizations and their products:

 * https://www.adobe.com/products/xmp.html
 * https://exiftool.org/TagNames/XMP.html
