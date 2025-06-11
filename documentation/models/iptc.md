# EXIFData: The IPTC Metadata Model

The IPTC (International Press Telecommunications Council) metadata model provides a
standardized set of metadata fields used to describe images, especially in journalism,
media, and digital asset management. It provides support for embedding descriptive,
administrative, and rights-related information within image files, including JPEG, TIFF
and PNG image file formats.

The key elements of metadata supported by the IPTC metadata model include:

* Describing the content of an image (e.g., caption and keywords)
* Identifying authors and copyright holders
* Managing usage rights and licensing
* Facilitating search and discovery

The main IPTC metadata categories include:

* Descriptive Metadata
    * Title / Headline
    * Caption / Description
    * Keywords
    * Subject and Category

* Administrative Metadata
    * Creator / Photographer
    * Credit / Source
    * Copyright Notice
    * Contact Info

* Image Management Metadata
    * Date Created
    * Job Identifier
    * Instructions (for image use or editing)

### IPTC Metadata Structure

IPTC metadata can be embedded using either the IPTC-IIM (Information Interchange Model)
model or the XMP (Extensible Metadata Platform) model. Modern image software often uses
XMP as an alternative to, or in addition to, the legacy IPTC-IIM format. Both formats
can coexist in the same image file as they are held in different EXIF Tags. The IPTC-IIM
metadata is held within the IPTC NAA tag (ID 33723) while XMP encoded IPTC metadata is
held within the XMP payload stored within the Adobe® Photoshop® APP13 marker segment.
IPTC metadata can also be held in the Adobe® Photoshop® Resources tag (ID 34377).

In summary, IPTC metadata may be held in either or both of the formats:

* IPTC-IIM (Information Interchange Model) – Is the legacy, binary encoded format used
primarily in JPEG and TIFF images.

* XMP (Extensible Metadata Platform) – Is the modern XML-based standard developed by
Adobe® which offers more flexibility; is easier to read and write than the legacy binary
encoded IPTC-IIM format; relaxes most field length limits of the legacy format; and is
Unicode compliant.

The EXIFData library provides support for reading and writing IPTC fields as IPTC-IIM as
well as via the XMP. To work with IPTC metadata using the IPTC-IIM model, use the `IPTC`
metadata model class, and to work with IPTC metadata using the XMP model, use the `XMP`
metadata model class and its `iptc_core` and `iptc_extended` namespaces, which for ease
of use have both been aliased under the `iptc` namespace of the `XMP` metadata model.
See the documentation for the [**XMP**](./xmp.md) metadata model for more information on
the use of IPTC metadata fields via the `XMP` metadata model.

IPTC metadata encoded in the IPTC-IIM format is organized into a list of Records, with
tags storing the actual data values. The structure typical of EXIF-compatible image file
formats holding IPTC metadata is as follows, where IPTC metadata could be present in the
IPTC-IIM encoded metadata segment as well as the XMP metadata segment:

```
Image File (e.g. JPEG, TIFF, etc)
   └── Metadata Segments
         ├── EXIF Metadata
         ├── IPTC Metadata (IPTC-IIM encoded)
         │     ├── Object Name (Title)
         │     ├── Caption/Abstract
         │     ├── Keywords
         │     ├── Creator/By-line
         │     ├── Copyright Notice
         │     └── ...
         └── XMP Metadata (modern metadata wrapper for IPTC, EXIF, etc.)
```

As noted, IPTC metadata values in the IPTC-IIM model are held in IPTC Records which are
encoded in a binary format comprising of the following components:

| Component      | Description                                                     |
|----------------|-----------------------------------------------------------------|
| Fixed Marker   | One byte fixed marker value: `0x1C`                             |
| Record ID      | One byte record identifier value: `0xXX`                        |
| Data Set ID    | One byte data set identifier value: `0xXX`                      |
| Value Length   | Two or four bytes denoting the length of the data that follows  |
| Value          | Variable number of bytes of the encoded data                    |

The IPTC metadata tag Record ID and Data Set IDs are documented below in the
[**IPTC Metadata Model Namespaces & Fields**](#namespaces-and-fields) section.

⚠️ **Note**: If the length of bytes-encoded data is less than `0x8000` the value length
is encoded as two bytes; if it is longer, then the length is encoded as four bytes but
the four bytes are prefixed with a fixed marker value of two bytes – `0x80 0x04` – so
that the encoded length ultimately consists of six bytes.

<a id="namespaces-and-fields"></a>
### IPTC Metadata Model Namespaces & Fields

The EXIFData library provides support for reading and writing IPTC metadata model fields. The model provides seven namespaces.

The IPTC metadata model's `Envelope` namespace offers fourteen fields which are listed below along with a link to each field's technical information:

| Namespace  | Field Path | Field Name | Required? | Info |
|------------|------------|------------|:---------:|------|
| `Envelope` | `iptc.envelope.ModelVersion` | ModelVersion | Yes | [🔗](#iptc-envelope-modelversion) |
| `Envelope` | `iptc.envelope.Destination` | Destination | No | [🔗](#iptc-envelope-destination) |
| `Envelope` | `iptc.envelope.FileFormat` | FileFormat | Yes | [🔗](#iptc-envelope-fileformat) |
| `Envelope` | `iptc.envelope.FileVersion` | FileVersion | Yes | [🔗](#iptc-envelope-fileversion) |
| `Envelope` | `iptc.envelope.ServiceID` | ServiceID | Yes | [🔗](#iptc-envelope-serviceid) |
| `Envelope` | `iptc.envelope.EnvelopeNumber` | EnvelopeNumber | Yes | [🔗](#iptc-envelope-envelopenumber) |
| `Envelope` | `iptc.envelope.ProductID` | ProductID | No | [🔗](#iptc-envelope-productid) |
| `Envelope` | `iptc.envelope.EnvelopePriority` | EnvelopePriority | No | [🔗](#iptc-envelope-envelopepriority) |
| `Envelope` | `iptc.envelope.DateSent` | DateSent | Yes | [🔗](#iptc-envelope-datesent) |
| `Envelope` | `iptc.envelope.TimeSent` | TimeSent | No | [🔗](#iptc-envelope-timesent) |
| `Envelope` | `iptc.envelope.CharacterSet` | CharacterSet | No | [🔗](#iptc-envelope-characterset) |
| `Envelope` | `iptc.envelope.UNO` | UNO | No | [🔗](#iptc-envelope-uno) |
| `Envelope` | `iptc.envelope.ARMID` | ARMID | No | [🔗](#iptc-envelope-armid) |
| `Envelope` | `iptc.envelope.ARMVersion` | ARMVersion | No | [🔗](#iptc-envelope-armversion) |

The technical details of each field may be found below:

<a id="iptc-envelope-modelversion"></a>
### The `envelope:ModelVersion` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.envelope.ModelVersion` |
| ID | `envelope:ModelVersion` |
| Name | ModelVersion |
| Label | – |
| Tag ID | 0 |
| Minimum bytes | 2 |
| Maximum bytes | 2 |
| Definiton | A binary number identifying the version of the Information Interchange Model, Part I, utilised by the provider. Version numbers are assigned by IPTC and NAA organizations. |
| Repeatable? | No |
| Required? | Yes |
| Type | Short |

<a id="iptc-envelope-destination"></a>
### The `envelope:Destination` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.envelope.Destination` |
| ID | `envelope:Destination` |
| Name | Destination |
| Label | – |
| Tag ID | 5 |
| Minimum bytes | 0 |
| Maximum bytes | 1024 |
| Definiton | This DataSet is to accommodate some providers who require routing information above the appropriate OSI layers. |
| Repeatable? | Yes |
| Required? | No |
| Type | String |

<a id="iptc-envelope-fileformat"></a>
### The `envelope:FileFormat` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.envelope.FileFormat` |
| ID | `envelope:FileFormat` |
| Name | FileFormat |
| Label | – |
| Tag ID | 20 |
| Minimum bytes | 2 |
| Maximum bytes | 2 |
| Definiton | A binary number representing the file format. The file format must be registered with IPTC or NAA with a unique number assigned to it. The information is used to route the data to the appropriate system and to allow the receiving system to perform the appropriate actions there to. |
| Options | 0: No ObjectData; 1: IPTC-NAA Digital Newsphoto Parameter Record; 2: IPTC7901 Recommended Message Format; 3: Tagged Image File Format [.TIFF] (Adobe/Aldus Image Data); 4: Illustrator (Adobe Graphics Data); 5: AppleSingle (Apple Computer Inc); 6: NAA 89-3 (ANPA 1312); 7: MacBinary II; 8: IPTC Unstructured Character Oriented File Format (UCOFF); 9: United Press International ANPA 1312 variant; 10: United Press International Down-Load Message; 11: JPEG File Interchange (JFIF); 12: Photo-CD Image-Pac (Eastman Kodak); 13: Bit Mapped Graphics File [.BMP] (Microsoft); 14: Digital Audio File [.WAV] (Microsoft & Creative Labs); 15: Audio plus Moving Video [.AVI] (Microsoft); 16: PC DOS/Windows Executable Files [.COM][.EXE]; 17: Compressed Binary File [.ZIP] (PKWare Inc); 18: Audio Interchange File Format [.AIFF] (Apple Computer Inc); 19: RIFF Wave (Microsoft Corporation); 20: Freehand (Macromedia/Aldus); 21: Hypertext Markup Language [.HTML] (The Internet Society); 22: MPEG 2 Audio Layer 2 (Musicom), ISO/IEC; 23: MPEG 2 Audio Layer 3, ISO/IEC; 24: Portable Document File [.PDF] Adobe; 25: News Industry Text Format (NITF); 26: Tape Archive [.TAR]; 27: Tidningarnas Telegrambyra NITF version (TTNITF DTD); 28: Ritzaus Bureau NITF version (RBNITF DTD); 29: Corel Draw [.CDR] |
| Repeatable? | No |
| Required? | Yes |
| Type | Short |

<a id="iptc-envelope-fileversion"></a>
### The `envelope:FileVersion` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.envelope.FileVersion` |
| ID | `envelope:FileVersion` |
| Name | FileVersion |
| Label | – |
| Tag ID | 22 |
| Minimum bytes | 2 |
| Maximum bytes | 2 |
| Definiton | A binary number representing the particular version of the File Format specified by <FileFormat> tag. |
| Repeatable? | No |
| Required? | Yes |
| Type | Short |

<a id="iptc-envelope-serviceid"></a>
### The `envelope:ServiceID` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.envelope.ServiceID` |
| ID | `envelope:ServiceID` |
| Name | ServiceID |
| Label | – |
| Tag ID | 30 |
| Minimum bytes | 0 |
| Maximum bytes | 10 |
| Definiton | Identifies the provider and product. |
| Repeatable? | No |
| Required? | Yes |
| Type | String |

<a id="iptc-envelope-envelopenumber"></a>
### The `envelope:EnvelopeNumber` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.envelope.EnvelopeNumber` |
| ID | `envelope:EnvelopeNumber` |
| Name | EnvelopeNumber |
| Label | – |
| Tag ID | 40 |
| Minimum bytes | 8 |
| Maximum bytes | 8 |
| Definiton | The characters form a number that will be unique for the date specified in <DateSent> tag and for the Service Identifier specified by <ServiceIdentifier> tag. If identical envelope numbers appear with the same date and with the same Service Identifier, records 2-9 must be unchanged from the original. This is not intended to be a sequential serial number reception check. |
| Repeatable? | No |
| Required? | Yes |
| Type | String |

<a id="iptc-envelope-productid"></a>
### The `envelope:ProductID` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.envelope.ProductID` |
| ID | `envelope:ProductID` |
| Name | ProductID |
| Label | – |
| Tag ID | 50 |
| Minimum bytes | 0 |
| Maximum bytes | 32 |
| Definiton | Allows a provider to identify subsets of its overall service. Used to provide receiving organisation data on which to select, route, or otherwise handle data. |
| Repeatable? | Yes |
| Required? | No |
| Type | String |

<a id="iptc-envelope-envelopepriority"></a>
### The `envelope:EnvelopePriority` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.envelope.EnvelopePriority` |
| ID | `envelope:EnvelopePriority` |
| Name | EnvelopePriority |
| Label | – |
| Tag ID | 60 |
| Minimum bytes | 1 |
| Maximum bytes | 1 |
| Definiton | Specifies the envelope handling priority and not the editorial urgency (see <Urgency> tag). "1" indicates the most urgent, "5" the normal urgency, and "8" the least urgent copy. The numeral "9" indicates a User Defined Priority. The numeral "0" is reserved for future use. |
| Options | 0: 0 (reserved); 1: 1 (most urgent); 2: 2; 3: 3; 4: 4; 5: 5 (normal urgency); 6: 6; 7: 7; 8: 8 (least urgent); 9: 9 (user-defined priority) |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-envelope-datesent"></a>
### The `envelope:DateSent` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.envelope.DateSent` |
| ID | `envelope:DateSent` |
| Name | DateSent |
| Label | – |
| Tag ID | 70 |
| Minimum bytes | 8 |
| Maximum bytes | 8 |
| Definiton | Uses the format CCYYMMDD (century, year, month, day) as de-fined in ISO 8601 to indicate year, month and day the service sent the material. |
| Repeatable? | No |
| Required? | Yes |
| Type | Date |

<a id="iptc-envelope-timesent"></a>
### The `envelope:TimeSent` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.envelope.TimeSent` |
| ID | `envelope:TimeSent` |
| Name | TimeSent |
| Label | – |
| Tag ID | 80 |
| Minimum bytes | 11 |
| Maximum bytes | 11 |
| Definiton | Uses the format HHMMSS:HHMM where HHMMSS refers to local hour, minute and seconds and HHMM refers to hours and minutes ahead (+) or behind (-) Universal Coordinated Time as described in ISO 8601. This is the time the service sent the material. |
| Repeatable? | No |
| Required? | No |
| Type | Time |

<a id="iptc-envelope-characterset"></a>
### The `envelope:CharacterSet` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.envelope.CharacterSet` |
| ID | `envelope:CharacterSet` |
| Name | CharacterSet |
| Label | – |
| Tag ID | 90 |
| Minimum bytes | 0 |
| Maximum bytes | 32 |
| Definiton | This tag consisting of one or more control functions used for the announcement, invocation or designation of coded character sets. The control functions follow the ISO 2022 standard and may consist of the escape control character and one or more graphic characters. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-envelope-uno"></a>
### The `envelope:UNO` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.envelope.UNO` |
| ID | `envelope:UNO` |
| Name | UNO |
| Label | – |
| Tag ID | 100 |
| Minimum bytes | 14 |
| Maximum bytes | 80 |
| Definiton | This tag provide a globally unique identification for objects as specified in the IIM, independent of provider and for any media form. The provider must ensure the UNO is unique. Objects with the same UNO are identical. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-envelope-armid"></a>
### The `envelope:ARMID` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.envelope.ARMID` |
| ID | `envelope:ARMID` |
| Name | ARMID |
| Label | – |
| Tag ID | 120 |
| Minimum bytes | 2 |
| Maximum bytes | 2 |
| Definiton | The DataSet identifies the Abstract Relationship Method identifier (ARM) which is described in a document registered by the originator of the ARM with the IPTC and NAA organizations. |
| Repeatable? | No |
| Required? | No |
| Type | Short |

<a id="iptc-envelope-armversion"></a>
### The `envelope:ARMVersion` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.envelope.ARMVersion` |
| ID | `envelope:ARMVersion` |
| Name | ARMVersion |
| Label | – |
| Tag ID | 122 |
| Minimum bytes | 2 |
| Maximum bytes | 2 |
| Definiton | This tag consisting of a binary number representing the particular version of the ARM specified by tag 'ARMID'. |
| Repeatable? | No |
| Required? | No |
| Type | Short |


The IPTC metadata model's `Application` namespace offers 70 fields which are listed below along with a link to each field's technical information:

| Namespace  | Field Path | Field Name | Required? | Info |
|------------|------------|------------|:---------:|------|
| `Application` | `iptc.app.RecordVersion` | RecordVersion | Yes | [🔗](#iptc-application-recordversion) |
| `Application` | `iptc.app.ObjectType` | ObjectType | No | [🔗](#iptc-application-objecttype) |
| `Application` | `iptc.app.ObjectAttribute` | ObjectAttribute | No | [🔗](#iptc-application-objectattribute) |
| `Application` | `iptc.app.ObjectName` | ObjectName | No | [🔗](#iptc-application-objectname) |
| `Application` | `iptc.app.EditStatus` | EditStatus | No | [🔗](#iptc-application-editstatus) |
| `Application` | `iptc.app.EditorialUpdate` | EditorialUpdate | No | [🔗](#iptc-application-editorialupdate) |
| `Application` | `iptc.app.Urgency` | Urgency | No | [🔗](#iptc-application-urgency) |
| `Application` | `iptc.app.Subject` | Subject | No | [🔗](#iptc-application-subject) |
| `Application` | `iptc.app.Category` | Category | No | [🔗](#iptc-application-category) |
| `Application` | `iptc.app.SupplementalCategories` | SupplementalCategories | No | [🔗](#iptc-application-supplementalcategories) |
| `Application` | `iptc.app.FixtureID` | FixtureID | No | [🔗](#iptc-application-fixtureid) |
| `Application` | `iptc.app.Keywords` | Keywords | No | [🔗](#iptc-application-keywords) |
| `Application` | `iptc.app.LocationCode` | LocationCode | No | [🔗](#iptc-application-locationcode) |
| `Application` | `iptc.app.LocationName` | LocationName | No | [🔗](#iptc-application-locationname) |
| `Application` | `iptc.app.ReleaseDate` | ReleaseDate | No | [🔗](#iptc-application-releasedate) |
| `Application` | `iptc.app.ReleaseTime` | ReleaseTime | No | [🔗](#iptc-application-releasetime) |
| `Application` | `iptc.app.ExpirationDate` | ExpirationDate | No | [🔗](#iptc-application-expirationdate) |
| `Application` | `iptc.app.ExpirationTime` | ExpirationTime | No | [🔗](#iptc-application-expirationtime) |
| `Application` | `iptc.app.SpecialInstructions` | SpecialInstructions | No | [🔗](#iptc-application-specialinstructions) |
| `Application` | `iptc.app.ActionAdvised` | ActionAdvised | No | [🔗](#iptc-application-actionadvised) |
| `Application` | `iptc.app.ReferenceService` | ReferenceService | No | [🔗](#iptc-application-referenceservice) |
| `Application` | `iptc.app.ReferenceDate` | ReferenceDate | No | [🔗](#iptc-application-referencedate) |
| `Application` | `iptc.app.ReferenceNumber` | ReferenceNumber | No | [🔗](#iptc-application-referencenumber) |
| `Application` | `iptc.app.DateCreated` | DateCreated | No | [🔗](#iptc-application-datecreated) |
| `Application` | `iptc.app.TimeCreated` | TimeCreated | No | [🔗](#iptc-application-timecreated) |
| `Application` | `iptc.app.DigitizationDate` | DigitizationDate | No | [🔗](#iptc-application-digitizationdate) |
| `Application` | `iptc.app.DigitizationTime` | DigitizationTime | No | [🔗](#iptc-application-digitizationtime) |
| `Application` | `iptc.app.Program` | Program | No | [🔗](#iptc-application-program) |
| `Application` | `iptc.app.ProgramVersion` | ProgramVersion | No | [🔗](#iptc-application-programversion) |
| `Application` | `iptc.app.ObjectCycle` | ObjectCycle | No | [🔗](#iptc-application-objectcycle) |
| `Application` | `iptc.app.Byline` | Byline | No | [🔗](#iptc-application-byline) |
| `Application` | `iptc.app.BylineTitle` | BylineTitle | No | [🔗](#iptc-application-bylinetitle) |
| `Application` | `iptc.app.City` | City | No | [🔗](#iptc-application-city) |
| `Application` | `iptc.app.SubLocation` | SubLocation | No | [🔗](#iptc-application-sublocation) |
| `Application` | `iptc.app.ProvinceState` | ProvinceState | No | [🔗](#iptc-application-provincestate) |
| `Application` | `iptc.app.CountryCode` | CountryCode | No | [🔗](#iptc-application-countrycode) |
| `Application` | `iptc.app.CountryName` | CountryName | No | [🔗](#iptc-application-countryname) |
| `Application` | `iptc.app.TransmissionReference` | TransmissionReference | No | [🔗](#iptc-application-transmissionreference) |
| `Application` | `iptc.app.Headline` | Headline | No | [🔗](#iptc-application-headline) |
| `Application` | `iptc.app.Credit` | Credit | No | [🔗](#iptc-application-credit) |
| `Application` | `iptc.app.Source` | Source | No | [🔗](#iptc-application-source) |
| `Application` | `iptc.app.Copyright` | Copyright | No | [🔗](#iptc-application-copyright) |
| `Application` | `iptc.app.Contact` | Contact | No | [🔗](#iptc-application-contact) |
| `Application` | `iptc.app.Caption` | Caption | No | [🔗](#iptc-application-caption) |
| `Application` | `iptc.app.LocalCaption` | LocalCaption | No | [🔗](#iptc-application-localcaption) |
| `Application` | `iptc.app.Writer` | Writer | No | [🔗](#iptc-application-writer) |
| `Application` | `iptc.app.RasterizedCaption` | RasterizedCaption | No | [🔗](#iptc-application-rasterizedcaption) |
| `Application` | `iptc.app.ImageType` | ImageType | No | [🔗](#iptc-application-imagetype) |
| `Application` | `iptc.app.ImageOrientation` | ImageOrientation | No | [🔗](#iptc-application-imageorientation) |
| `Application` | `iptc.app.Language` | Language | No | [🔗](#iptc-application-language) |
| `Application` | `iptc.app.AudioType` | AudioType | No | [🔗](#iptc-application-audiotype) |
| `Application` | `iptc.app.AudioSamplingRate` | AudioSamplingRate | No | [🔗](#iptc-application-audiosamplingrate) |
| `Application` | `iptc.app.AudioSamplingResolution` | AudioSamplingResolution | No | [🔗](#iptc-application-audiosamplingresolution) |
| `Application` | `iptc.app.AudioDuration` | AudioDuration | No | [🔗](#iptc-application-audioduration) |
| `Application` | `iptc.app.AudioOutcue` | AudioOutcue | No | [🔗](#iptc-application-audiooutcue) |
| `Application` | `iptc.app.JobID` | JobID | No | [🔗](#iptc-application-jobid) |
| `Application` | `iptc.app.MasterDocumentID` | MasterDocumentID | No | [🔗](#iptc-application-masterdocumentid) |
| `Application` | `iptc.app.ShortDocumentID` | ShortDocumentID | No | [🔗](#iptc-application-shortdocumentid) |
| `Application` | `iptc.app.UniqueDocumentID` | UniqueDocumentID | No | [🔗](#iptc-application-uniquedocumentid) |
| `Application` | `iptc.app.OwnerID` | OwnerID | No | [🔗](#iptc-application-ownerid) |
| `Application` | `iptc.app.PreviewFormat` | PreviewFormat | No | [🔗](#iptc-application-previewformat) |
| `Application` | `iptc.app.PreviewVersion` | PreviewVersion | No | [🔗](#iptc-application-previewversion) |
| `Application` | `iptc.app.PreviewData` | PreviewData | No | [🔗](#iptc-application-previewdata) |
| `Application` | `iptc.app.Prefs` | Prefs | No | [🔗](#iptc-application-prefs) |
| `Application` | `iptc.app.ClassifyState` | ClassifyState | No | [🔗](#iptc-application-classifystate) |
| `Application` | `iptc.app.SimilarityIndex` | SimilarityIndex | No | [🔗](#iptc-application-similarityindex) |
| `Application` | `iptc.app.DocumentNotes` | DocumentNotes | No | [🔗](#iptc-application-documentnotes) |
| `Application` | `iptc.app.DocumentHistory` | DocumentHistory | No | [🔗](#iptc-application-documenthistory) |
| `Application` | `iptc.app.EXIFCameraInfo` | EXIFCameraInfo | No | [🔗](#iptc-application-exifcamerainfo) |
| `Application` | `iptc.app.CatalogSets` | CatalogSets | No | [🔗](#iptc-application-catalogsets) |

The technical details of each field may be found below:

<a id="iptc-application-recordversion"></a>
### The `application:RecordVersion` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.RecordVersion` |
| ID | `application:RecordVersion` |
| Name | RecordVersion |
| Label | – |
| Tag ID | 0 |
| Minimum bytes | 2 |
| Maximum bytes | 2 |
| Definiton | A binary number identifying the version of the Information Interchange Model, Part II, utilised by the provider. Version numbers are assigned by IPTC and NAA organizations. |
| Repeatable? | No |
| Required? | Yes |
| Type | Short |

<a id="iptc-application-objecttype"></a>
### The `application:ObjectType` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.ObjectType` |
| ID | `application:ObjectType` |
| Name | ObjectType |
| Label | – |
| Tag ID | 3 |
| Minimum bytes | 3 |
| Maximum bytes | 67 |
| Definiton | The Object Type is used to distinguish between different types of objects within the IIM. The first part is a number representing a language independent international reference to an Object Type followed by a colon separator. The second part, if used, is a text representation of the Object Type Number consisting of graphic characters plus spaces either in English or in the language of the service as indicated in tag <LanguageIdentifier>. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-objectattribute"></a>
### The `application:ObjectAttribute` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.ObjectAttribute` |
| ID | `application:ObjectAttribute` |
| Name | ObjectAttribute |
| Label | – |
| Tag ID | 4 |
| Minimum bytes | 4 |
| Maximum bytes | 68 |
| Definiton | The Object Attribute defines the nature of the object independent of the Subject. The first part is a number representing a language independent international reference to an Object Attribute followed by a colon separator. The second part, if used, is a text representation of the Object Attribute Number consisting of graphic characters plus spaces either in English, or in the language of the service as indicated in tag <LanguageIdentifier>. |
| Repeatable? | Yes |
| Required? | No |
| Type | String |

<a id="iptc-application-objectname"></a>
### The `application:ObjectName` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.ObjectName` |
| ID | `application:ObjectName` |
| Name | ObjectName |
| Label | – |
| Tag ID | 5 |
| Minimum bytes | 0 |
| Maximum bytes | 64 |
| Definiton | Used as a shorthand reference for the object. Changes to exist-ing data, such as updated stories or new crops on photos, should be identified in tag <EditStatus>. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-editstatus"></a>
### The `application:EditStatus` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.EditStatus` |
| ID | `application:EditStatus` |
| Name | EditStatus |
| Label | – |
| Tag ID | 7 |
| Minimum bytes | 0 |
| Maximum bytes | 64 |
| Definiton | Status of the object data, according to the practice of the provider. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-editorialupdate"></a>
### The `application:EditorialUpdate` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.EditorialUpdate` |
| ID | `application:EditorialUpdate` |
| Name | EditorialUpdate |
| Label | – |
| Tag ID | 8 |
| Minimum bytes | 2 |
| Maximum bytes | 2 |
| Definiton | Indicates the type of update that this object provides to a previous object. The link to the previous object is made using the tags <ARMIdentifier> and <ARMVersion>, according to the practices of the provider. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-urgency"></a>
### The `application:Urgency` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.Urgency` |
| ID | `application:Urgency` |
| Name | Urgency |
| Label | – |
| Tag ID | 10 |
| Minimum bytes | 1 |
| Maximum bytes | 1 |
| Definiton | Specifies the editorial urgency of content and not necessarily the envelope handling priority (see tag <EnvelopePriority>). The "1" is most urgent, "5" normal and "8" denotes the least-urgent copy. |
| Options | 0: 0 (reserved); 1: 1 (most urgent); 2: 2; 3: 3; 4: 4; 5: 5 (normal urgency); 6: 6; 7: 7; 8: 8 (least urgent); 9: 9 (user-defined priority) |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-subject"></a>
### The `application:Subject` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.Subject` |
| ID | `application:Subject` |
| Name | Subject |
| Label | – |
| Tag ID | 12 |
| Minimum bytes | 13 |
| Maximum bytes | 236 |
| Definiton | The Subject Reference is a structured definition of the subject matter. |
| Repeatable? | Yes |
| Required? | No |
| Type | String |

<a id="iptc-application-category"></a>
### The `application:Category` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.Category` |
| ID | `application:Category` |
| Name | Category |
| Label | – |
| Tag ID | 15 |
| Minimum bytes | 0 |
| Maximum bytes | 3 |
| Definiton | Identifies the subject of the object data in the opinion of the provider. A list of categories will be maintained by a regional registry, where available, otherwise by the provider. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-supplementalcategories"></a>
### The `application:SupplementalCategories` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.SupplementalCategories` |
| ID | `application:SupplementalCategories` |
| Name | SupplementalCategories |
| Label | – |
| Tag ID | 20 |
| Minimum bytes | 0 |
| Maximum bytes | 32 |
| Definiton | Supplemental categories further refine the subject of an object data. A supplemental category may include any of the recognised categories as used in tag 'Category'. Otherwise, selection of supplemental categories are left to the provider. |
| Repeatable? | Yes |
| Required? | No |
| Type | String |

<a id="iptc-application-fixtureid"></a>
### The `application:FixtureID` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.FixtureID` |
| ID | `application:FixtureID` |
| Name | FixtureID |
| Label | – |
| Tag ID | 22 |
| Minimum bytes | 0 |
| Maximum bytes | 32 |
| Definiton | Identifies object data that recurs often and predictably. Enables users to immediately find or recall such an object. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-keywords"></a>
### The `application:Keywords` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.Keywords` |
| ID | `application:Keywords` |
| Name | Keywords |
| Label | – |
| Tag ID | 25 |
| Minimum bytes | 0 |
| Maximum bytes | 64 |
| Definiton | Used to indicate specific information retrieval words. It is expected that a provider of various types of data that are related in subject matter uses the same keyword, enabling the receiving system or subsystems to search across all types of data for related material. |
| Repeatable? | Yes |
| Required? | No |
| Type | String |

<a id="iptc-application-locationcode"></a>
### The `application:LocationCode` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.LocationCode` |
| ID | `application:LocationCode` |
| Name | LocationCode |
| Label | – |
| Tag ID | 26 |
| Minimum bytes | 3 |
| Maximum bytes | 3 |
| Definiton | Indicates the code of a country/geographical location referenced by the content of the object. Where ISO has established an appropriate country code under ISO 3166, that code will be used. When ISO 3166 does not adequately provide for identification of a location or a country, e.g. ships at sea, space, IPTC will assign an appropriate three-character code under the provisions of ISO 3166 to avoid conflicts. |
| Repeatable? | Yes |
| Required? | No |
| Type | String |

<a id="iptc-application-locationname"></a>
### The `application:LocationName` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.LocationName` |
| ID | `application:LocationName` |
| Name | LocationName |
| Label | – |
| Tag ID | 27 |
| Minimum bytes | 0 |
| Maximum bytes | 64 |
| Definiton | Provides a full, publishable name of a country/geographical location referenced by the content of the object, according to guidelines of the provider. |
| Repeatable? | Yes |
| Required? | No |
| Type | String |

<a id="iptc-application-releasedate"></a>
### The `application:ReleaseDate` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.ReleaseDate` |
| ID | `application:ReleaseDate` |
| Name | ReleaseDate |
| Label | – |
| Tag ID | 30 |
| Minimum bytes | 8 |
| Maximum bytes | 8 |
| Definiton | Designates in the form CCYYMMDD the earliest date the provider intends the object to be used. Follows ISO 8601 standard. |
| Repeatable? | No |
| Required? | No |
| Type | Date |

<a id="iptc-application-releasetime"></a>
### The `application:ReleaseTime` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.ReleaseTime` |
| ID | `application:ReleaseTime` |
| Name | ReleaseTime |
| Label | – |
| Tag ID | 35 |
| Minimum bytes | 11 |
| Maximum bytes | 11 |
| Definiton | Designates in the form HHMMSS:HHMM the earliest time the provider intends the object to be used. Follows ISO 8601 standard. |
| Repeatable? | No |
| Required? | No |
| Type | Time |

<a id="iptc-application-expirationdate"></a>
### The `application:ExpirationDate` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.ExpirationDate` |
| ID | `application:ExpirationDate` |
| Name | ExpirationDate |
| Label | – |
| Tag ID | 37 |
| Minimum bytes | 8 |
| Maximum bytes | 8 |
| Definiton | Designates in the form CCYYMMDD the latest date the provider or owner intends the object data to be used. Follows ISO 8601 standard. |
| Repeatable? | No |
| Required? | No |
| Type | Date |

<a id="iptc-application-expirationtime"></a>
### The `application:ExpirationTime` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.ExpirationTime` |
| ID | `application:ExpirationTime` |
| Name | ExpirationTime |
| Label | – |
| Tag ID | 38 |
| Minimum bytes | 11 |
| Maximum bytes | 11 |
| Definiton | Designates in the form HHMMSS:HHMM the latest time the provider or owner intends the object data to be used. Follows ISO 8601 standard. |
| Repeatable? | No |
| Required? | No |
| Type | Time |

<a id="iptc-application-specialinstructions"></a>
### The `application:SpecialInstructions` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.SpecialInstructions` |
| ID | `application:SpecialInstructions` |
| Name | SpecialInstructions |
| Label | – |
| Tag ID | 40 |
| Minimum bytes | 0 |
| Maximum bytes | 256 |
| Definiton | Other editorial instructions concerning the use of the object data, such as embargoes and warnings. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-actionadvised"></a>
### The `application:ActionAdvised` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.ActionAdvised` |
| ID | `application:ActionAdvised` |
| Name | ActionAdvised |
| Label | – |
| Tag ID | 42 |
| Minimum bytes | 2 |
| Maximum bytes | 2 |
| Definiton | Indicates the type of action that this object provides to a previous object. The link to the previous object is made using tags <ARMIdentifier> and <ARMVersion>, according to the practices of the provider. |
| Options | 01: Object Kill; 02: Object Replace; 03: Object Append; 04: Object Reference |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-referenceservice"></a>
### The `application:ReferenceService` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.ReferenceService` |
| ID | `application:ReferenceService` |
| Name | ReferenceService |
| Label | – |
| Tag ID | 45 |
| Minimum bytes | 0 |
| Maximum bytes | 10 |
| Definiton | Identifies the Service Identifier of a prior envelope to which the current object refers. |
| Repeatable? | Yes |
| Required? | No |
| Type | String |

<a id="iptc-application-referencedate"></a>
### The `application:ReferenceDate` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.ReferenceDate` |
| ID | `application:ReferenceDate` |
| Name | ReferenceDate |
| Label | – |
| Tag ID | 47 |
| Minimum bytes | 8 |
| Maximum bytes | 8 |
| Definiton | Identifies the date of a prior envelope to which the current object refers. |
| Repeatable? | Yes |
| Required? | No |
| Type | Date |

<a id="iptc-application-referencenumber"></a>
### The `application:ReferenceNumber` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.ReferenceNumber` |
| ID | `application:ReferenceNumber` |
| Name | ReferenceNumber |
| Label | – |
| Tag ID | 50 |
| Minimum bytes | 8 |
| Maximum bytes | 8 |
| Definiton | Identifies the Envelope Number of a prior envelope to which the current object refers. |
| Repeatable? | Yes |
| Required? | No |
| Type | String |

<a id="iptc-application-datecreated"></a>
### The `application:DateCreated` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.DateCreated` |
| ID | `application:DateCreated` |
| Name | DateCreated |
| Label | – |
| Tag ID | 55 |
| Minimum bytes | 8 |
| Maximum bytes | 8 |
| Definiton | Represented in the form CCYYMMDD to designate the date the intellectual content of the object data was created rather than the date of the creation of the physical representation. Follows ISO 8601 standard. |
| Repeatable? | No |
| Required? | No |
| Type | Date |

<a id="iptc-application-timecreated"></a>
### The `application:TimeCreated` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.TimeCreated` |
| ID | `application:TimeCreated` |
| Name | TimeCreated |
| Label | – |
| Tag ID | 60 |
| Minimum bytes | 11 |
| Maximum bytes | 11 |
| Definiton | Represented in the form HHMMSS:HHMM to designate the time the intellectual content of the object data current source material was created rather than the creation of the physical representation. Follows ISO 8601 standard. |
| Repeatable? | No |
| Required? | No |
| Type | Time |

<a id="iptc-application-digitizationdate"></a>
### The `application:DigitizationDate` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.DigitizationDate` |
| ID | `application:DigitizationDate` |
| Name | DigitizationDate |
| Label | – |
| Tag ID | 62 |
| Minimum bytes | 8 |
| Maximum bytes | 8 |
| Definiton | Represented in the form CCYYMMDD to designate the date the digital representation of the object data was created. Follows ISO 8601 standard. |
| Repeatable? | No |
| Required? | No |
| Type | Date |

<a id="iptc-application-digitizationtime"></a>
### The `application:DigitizationTime` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.DigitizationTime` |
| ID | `application:DigitizationTime` |
| Name | DigitizationTime |
| Label | – |
| Tag ID | 63 |
| Minimum bytes | 11 |
| Maximum bytes | 11 |
| Definiton | Represented in the form HHMMSS:HHMM to designate the time the digital representation of the object data was created. Follows ISO 8601 standard. |
| Repeatable? | No |
| Required? | No |
| Type | Time |

<a id="iptc-application-program"></a>
### The `application:Program` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.Program` |
| ID | `application:Program` |
| Name | Program |
| Label | – |
| Tag ID | 65 |
| Minimum bytes | 0 |
| Maximum bytes | 32 |
| Definiton | Identifies the type of program used to originate the object data. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-programversion"></a>
### The `application:ProgramVersion` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.ProgramVersion` |
| ID | `application:ProgramVersion` |
| Name | ProgramVersion |
| Label | – |
| Tag ID | 70 |
| Minimum bytes | 0 |
| Maximum bytes | 10 |
| Definiton | Used to identify the version of the program mentioned in tag <Program>. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-objectcycle"></a>
### The `application:ObjectCycle` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.ObjectCycle` |
| ID | `application:ObjectCycle` |
| Name | ObjectCycle |
| Label | – |
| Tag ID | 75 |
| Minimum bytes | 1 |
| Maximum bytes | 1 |
| Definiton | Used to identify the editorial cycle of object data. |
| Options | a: Morning; b: Both Morning and Evening; p: Evening |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-byline"></a>
### The `application:Byline` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.Byline` |
| ID | `application:Byline` |
| Name | Byline |
| Label | – |
| Tag ID | 80 |
| Minimum bytes | 0 |
| Maximum bytes | 32 |
| Definiton | Contains name of the creator of the object data, e.g. writer, photographer or graphic artist. |
| Repeatable? | Yes |
| Required? | No |
| Type | String |

<a id="iptc-application-bylinetitle"></a>
### The `application:BylineTitle` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.BylineTitle` |
| ID | `application:BylineTitle` |
| Name | BylineTitle |
| Label | – |
| Tag ID | 85 |
| Minimum bytes | 0 |
| Maximum bytes | 32 |
| Definiton | A by-line title is the title of the creator or creators of an object data. Where used, a by-line title should follow the by-line it modifies. |
| Repeatable? | Yes |
| Required? | No |
| Type | String |

<a id="iptc-application-city"></a>
### The `application:City` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.City` |
| ID | `application:City` |
| Name | City |
| Label | – |
| Tag ID | 90 |
| Minimum bytes | 0 |
| Maximum bytes | 32 |
| Definiton | Identifies city of object data origin according to guidelines established by the provider. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-sublocation"></a>
### The `application:SubLocation` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.SubLocation` |
| ID | `application:SubLocation` |
| Name | SubLocation |
| Label | – |
| Tag ID | 92 |
| Minimum bytes | 0 |
| Maximum bytes | 32 |
| Definiton | Identifies the location within a city from which the object data originates, according to guidelines established by the provider. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-provincestate"></a>
### The `application:ProvinceState` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.ProvinceState` |
| ID | `application:ProvinceState` |
| Name | ProvinceState |
| Label | – |
| Tag ID | 95 |
| Minimum bytes | 0 |
| Maximum bytes | 32 |
| Definiton | Identifies Province/State of origin according to guidelines established by the provider. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-countrycode"></a>
### The `application:CountryCode` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.CountryCode` |
| ID | `application:CountryCode` |
| Name | CountryCode |
| Label | – |
| Tag ID | 100 |
| Minimum bytes | 3 |
| Maximum bytes | 3 |
| Definiton | Indicates the code of the country/primary location where the intellectual property of the object data was created, e.g. a photo was taken, an event occurred. Where ISO has established an appropriate country code under ISO 3166, that code will be used. When ISO 3166 does not adequately provide for identification of a location or a new country, e.g. ships at sea, space, IPTC will assign an appropriate three-character code under the provisions of ISO 3166 to avoid conflicts. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-countryname"></a>
### The `application:CountryName` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.CountryName` |
| ID | `application:CountryName` |
| Name | CountryName |
| Label | – |
| Tag ID | 101 |
| Minimum bytes | 0 |
| Maximum bytes | 64 |
| Definiton | Provides full, publishable, name of the country/primary location where the intellectual property of the object data was created, according to guidelines of the provider. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-transmissionreference"></a>
### The `application:TransmissionReference` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.TransmissionReference` |
| ID | `application:TransmissionReference` |
| Name | TransmissionReference |
| Label | – |
| Tag ID | 103 |
| Minimum bytes | 0 |
| Maximum bytes | 32 |
| Definiton | A code representing the location of original transmission according to practices of the provider. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-headline"></a>
### The `application:Headline` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.Headline` |
| ID | `application:Headline` |
| Name | Headline |
| Label | – |
| Tag ID | 105 |
| Minimum bytes | 0 |
| Maximum bytes | 256 |
| Definiton | A publishable entry providing a synopsis of the contents of the object data. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-credit"></a>
### The `application:Credit` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.Credit` |
| ID | `application:Credit` |
| Name | Credit |
| Label | – |
| Tag ID | 110 |
| Minimum bytes | 0 |
| Maximum bytes | 32 |
| Definiton | Identifies the provider of the object data, not necessarily the owner/creator. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-source"></a>
### The `application:Source` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.Source` |
| ID | `application:Source` |
| Name | Source |
| Label | – |
| Tag ID | 115 |
| Minimum bytes | 0 |
| Maximum bytes | 32 |
| Definiton | Identifies the original owner of the intellectual content of the object data. This could be an agency, a member of an agency or an individual. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-copyright"></a>
### The `application:Copyright` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.Copyright` |
| ID | `application:Copyright` |
| Name | Copyright |
| Label | – |
| Tag ID | 116 |
| Minimum bytes | 0 |
| Maximum bytes | 128 |
| Definiton | Contains any necessary copyright notice. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-contact"></a>
### The `application:Contact` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.Contact` |
| ID | `application:Contact` |
| Name | Contact |
| Label | – |
| Tag ID | 118 |
| Minimum bytes | 0 |
| Maximum bytes | 128 |
| Definiton | Identifies the person or organisation which can provide further background information on the object data. |
| Repeatable? | Yes |
| Required? | No |
| Type | String |

<a id="iptc-application-caption"></a>
### The `application:Caption` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.Caption` |
| ID | `application:Caption` |
| Name | Caption |
| Label | – |
| Tag ID | 120 |
| Minimum bytes | 0 |
| Maximum bytes | 2000 |
| Definiton | A textual description of the object data. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-localcaption"></a>
### The `application:LocalCaption` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.LocalCaption` |
| ID | `application:LocalCaption` |
| Name | LocalCaption |
| Label | – |
| Tag ID | 121 |
| Minimum bytes | 0 |
| Maximum bytes | 256 |
| Definiton | A localized textual description of the object data. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-writer"></a>
### The `application:Writer` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.Writer` |
| ID | `application:Writer` |
| Name | Writer |
| Label | – |
| Tag ID | 122 |
| Minimum bytes | 0 |
| Maximum bytes | 32 |
| Definiton | Identification of the name of the person involved in the writing, editing or correcting the object data or caption/abstract. |
| Repeatable? | Yes |
| Required? | No |
| Type | String |

<a id="iptc-application-rasterizedcaption"></a>
### The `application:RasterizedCaption` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.RasterizedCaption` |
| ID | `application:RasterizedCaption` |
| Name | RasterizedCaption |
| Label | – |
| Tag ID | 125 |
| Minimum bytes | 7360 |
| Maximum bytes | 7360 |
| Definiton | Contains the rasterized object data description and is used where characters that have not been coded are required for the caption. |
| Repeatable? | No |
| Required? | No |
| Type | Undefined |

<a id="iptc-application-imagetype"></a>
### The `application:ImageType` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.ImageType` |
| ID | `application:ImageType` |
| Name | ImageType |
| Label | – |
| Tag ID | 130 |
| Minimum bytes | 2 |
| Maximum bytes | 2 |
| Definiton | Indicates the color components of an image. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-imageorientation"></a>
### The `application:ImageOrientation` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.ImageOrientation` |
| ID | `application:ImageOrientation` |
| Name | ImageOrientation |
| Label | – |
| Tag ID | 131 |
| Minimum bytes | 1 |
| Maximum bytes | 1 |
| Definiton | Indicates the layout of an image. |
| Options | L: Landscape; P: Portrait; S: Square |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-language"></a>
### The `application:Language` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.Language` |
| ID | `application:Language` |
| Name | Language |
| Label | – |
| Tag ID | 135 |
| Minimum bytes | 2 |
| Maximum bytes | 3 |
| Definiton | Describes the major national language of the object, according to the 2-letter codes of ISO 639:1988. Does not define or imply any coded character set, but is used for internal routing, e.g. to various editorial desks. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-audiotype"></a>
### The `application:AudioType` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.AudioType` |
| ID | `application:AudioType` |
| Name | AudioType |
| Label | – |
| Tag ID | 150 |
| Minimum bytes | 2 |
| Maximum bytes | 2 |
| Definiton | Indicates the type of an audio content. |
| Options | 0T: Text Only; 1A: Mono Actuality; 1C: Mono Question and Answer Session; 1M: Mono Music; 1Q: Mono Response to a Question; 1R: Mono Raw Sound; 1S: Mono Scener; 1V: Mono Voicer; 1W: Mono Wrap; 2A: Stereo Actuality; 2C: Stereo Question and Answer Session; 2M: Stereo Music; 2Q: Stereo Response to a Question; 2R: Stereo Raw Sound; 2S: Stereo Scener; 2V: Stereo Voicer; 2W: Stereo Wrap |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-audiosamplingrate"></a>
### The `application:AudioSamplingRate` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.AudioSamplingRate` |
| ID | `application:AudioSamplingRate` |
| Name | AudioSamplingRate |
| Label | – |
| Tag ID | 151 |
| Minimum bytes | 6 |
| Maximum bytes | 6 |
| Definiton | Indicates the sampling rate in Hertz of an audio content. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-audiosamplingresolution"></a>
### The `application:AudioSamplingResolution` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.AudioSamplingResolution` |
| ID | `application:AudioSamplingResolution` |
| Name | AudioSamplingResolution |
| Label | – |
| Tag ID | 152 |
| Minimum bytes | 2 |
| Maximum bytes | 2 |
| Definiton | Indicates the sampling resolution of an audio content. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-audioduration"></a>
### The `application:AudioDuration` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.AudioDuration` |
| ID | `application:AudioDuration` |
| Name | AudioDuration |
| Label | – |
| Tag ID | 153 |
| Minimum bytes | 6 |
| Maximum bytes | 6 |
| Definiton | Indicates the duration of an audio content. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-audiooutcue"></a>
### The `application:AudioOutcue` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.AudioOutcue` |
| ID | `application:AudioOutcue` |
| Name | AudioOutcue |
| Label | – |
| Tag ID | 154 |
| Minimum bytes | 0 |
| Maximum bytes | 64 |
| Definiton | Identifies the content of the end of an audio object data, according to guidelines established by the provider. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-jobid"></a>
### The `application:JobID` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.JobID` |
| ID | `application:JobID` |
| Name | JobID |
| Label | – |
| Tag ID | 184 |
| Minimum bytes | 0 |
| Maximum bytes | 64 |
| Definiton | Job ID. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-masterdocumentid"></a>
### The `application:MasterDocumentID` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.MasterDocumentID` |
| ID | `application:MasterDocumentID` |
| Name | MasterDocumentID |
| Label | – |
| Tag ID | 185 |
| Minimum bytes | 0 |
| Maximum bytes | 256 |
| Definiton | Master Document ID. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-shortdocumentid"></a>
### The `application:ShortDocumentID` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.ShortDocumentID` |
| ID | `application:ShortDocumentID` |
| Name | ShortDocumentID |
| Label | – |
| Tag ID | 186 |
| Minimum bytes | 0 |
| Maximum bytes | 64 |
| Definiton | Short Document ID. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-uniquedocumentid"></a>
### The `application:UniqueDocumentID` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.UniqueDocumentID` |
| ID | `application:UniqueDocumentID` |
| Name | UniqueDocumentID |
| Label | – |
| Tag ID | 187 |
| Minimum bytes | 0 |
| Maximum bytes | 64 |
| Definiton | Unique Document ID. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-ownerid"></a>
### The `application:OwnerID` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.OwnerID` |
| ID | `application:OwnerID` |
| Name | OwnerID |
| Label | – |
| Tag ID | 188 |
| Minimum bytes | 0 |
| Maximum bytes | 64 |
| Definiton | Owner ID. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-previewformat"></a>
### The `application:PreviewFormat` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.PreviewFormat` |
| ID | `application:PreviewFormat` |
| Name | PreviewFormat |
| Label | – |
| Tag ID | 200 |
| Minimum bytes | 2 |
| Maximum bytes | 2 |
| Definiton | A binary number representing the file format of the object data preview. The file format must be registered with IPTC or NAA organizations with a unique number assigned to it. |
| Options | 0: No ObjectData; 1: IPTC-NAA Digital Newsphoto Parameter Record; 2: IPTC7901 Recommended Message Format; 3: Tagged Image File Format [.TIFF] (Adobe/Aldus Image Data); 4: Illustrator (Adobe Graphics Data); 5: AppleSingle (Apple Computer Inc); 6: NAA 89-3 (ANPA 1312); 7: MacBinary II; 8: IPTC Unstructured Character Oriented File Format (UCOFF); 9: United Press International ANPA 1312 variant; 10: United Press International Down-Load Message; 11: JPEG File Interchange (JFIF); 12: Photo-CD Image-Pac (Eastman Kodak); 13: Bit Mapped Graphics File [.BMP] (Microsoft); 14: Digital Audio File [.WAV] (Microsoft & Creative Labs); 15: Audio plus Moving Video [.AVI] (Microsoft); 16: PC DOS/Windows Executable Files [.COM][.EXE]; 17: Compressed Binary File [.ZIP] (PKWare Inc); 18: Audio Interchange File Format [.AIFF] (Apple Computer Inc); 19: RIFF Wave (Microsoft Corporation); 20: Freehand (Macromedia/Aldus); 21: Hypertext Markup Language [.HTML] (The Internet Society); 22: MPEG 2 Audio Layer 2 (Musicom), ISO/IEC; 23: MPEG 2 Audio Layer 3, ISO/IEC; 24: Portable Document File [.PDF] Adobe; 25: News Industry Text Format (NITF); 26: Tape Archive [.TAR]; 27: Tidningarnas Telegrambyra NITF version (TTNITF DTD); 28: Ritzaus Bureau NITF version (RBNITF DTD); 29: Corel Draw [.CDR] |
| Repeatable? | No |
| Required? | No |
| Type | Short |

<a id="iptc-application-previewversion"></a>
### The `application:PreviewVersion` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.PreviewVersion` |
| ID | `application:PreviewVersion` |
| Name | PreviewVersion |
| Label | – |
| Tag ID | 201 |
| Minimum bytes | 2 |
| Maximum bytes | 2 |
| Definiton | A binary number representing the particular version of the object data preview file format specified in tag <PreviewFormat>. |
| Repeatable? | No |
| Required? | No |
| Type | Short |

<a id="iptc-application-previewdata"></a>
### The `application:PreviewData` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.PreviewData` |
| ID | `application:PreviewData` |
| Name | PreviewData |
| Label | – |
| Tag ID | 202 |
| Minimum bytes | 0 |
| Maximum bytes | 256000 |
| Definiton | Binary image preview data. |
| Repeatable? | No |
| Required? | No |
| Type | Bytes |

<a id="iptc-application-prefs"></a>
### The `application:Prefs` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.Prefs` |
| ID | `application:Prefs` |
| Name | Prefs |
| Label | – |
| Tag ID | 221 |
| Minimum bytes | 0 |
| Maximum bytes | 64 |
| Definiton | PhotoMechanic Preferences. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-classifystate"></a>
### The `application:ClassifyState` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.ClassifyState` |
| ID | `application:ClassifyState` |
| Name | ClassifyState |
| Label | – |
| Tag ID | 225 |
| Minimum bytes | 0 |
| Maximum bytes | 64 |
| Definiton | Classify State. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-similarityindex"></a>
### The `application:SimilarityIndex` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.SimilarityIndex` |
| ID | `application:SimilarityIndex` |
| Name | SimilarityIndex |
| Label | – |
| Tag ID | 228 |
| Minimum bytes | 0 |
| Maximum bytes | 32 |
| Definiton | Similarity Index. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-documentnotes"></a>
### The `application:DocumentNotes` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.DocumentNotes` |
| ID | `application:DocumentNotes` |
| Name | DocumentNotes |
| Label | – |
| Tag ID | 230 |
| Minimum bytes | 0 |
| Maximum bytes | 1024 |
| Definiton | Document Notes. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-documenthistory"></a>
### The `application:DocumentHistory` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.DocumentHistory` |
| ID | `application:DocumentHistory` |
| Name | DocumentHistory |
| Label | – |
| Tag ID | 231 |
| Minimum bytes | 0 |
| Maximum bytes | 256 |
| Definiton | Document History. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-exifcamerainfo"></a>
### The `application:EXIFCameraInfo` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.EXIFCameraInfo` |
| ID | `application:EXIFCameraInfo` |
| Name | EXIFCameraInfo |
| Label | – |
| Tag ID | 232 |
| Minimum bytes | 0 |
| Maximum bytes | 4096 |
| Definiton | EXIF Camera Info. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-application-catalogsets"></a>
### The `application:CatalogSets` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.app.CatalogSets` |
| ID | `application:CatalogSets` |
| Name | CatalogSets |
| Label | – |
| Tag ID | 255 |
| Minimum bytes | 0 |
| Maximum bytes | 256 |
| Definiton | Catalog Sets. |
| Repeatable? | No |
| Required? | No |
| Type | String |


The IPTC metadata model's `News Photo Tags` namespace offers 26 fields which are listed below along with a link to each field's technical information:

| Namespace  | Field Path | Field Name | Required? | Info |
|------------|------------|------------|:---------:|------|
| `News Photo Tags` | `iptc.news.Version` | Version | No | [🔗](#iptc-news photo tags-version) |
| `News Photo Tags` | `iptc.news.IPTCPictureNumber` | IPTCPictureNumber | No | [🔗](#iptc-news photo tags-iptcpicturenumber) |
| `News Photo Tags` | `iptc.news.IPTCImageWidth` | IPTCImageWidth | No | [🔗](#iptc-news photo tags-iptcimagewidth) |
| `News Photo Tags` | `iptc.news.IPTCImageHeight` | IPTCImageHeight | No | [🔗](#iptc-news photo tags-iptcimageheight) |
| `News Photo Tags` | `iptc.news.IPTCPixelWidth` | IPTCPixelWidth | No | [🔗](#iptc-news photo tags-iptcpixelwidth) |
| `News Photo Tags` | `iptc.news.IPTCPixelHeight` | IPTCPixelHeight | No | [🔗](#iptc-news photo tags-iptcpixelheight) |
| `News Photo Tags` | `iptc.news.SupplementalType` | SupplementalType | No | [🔗](#iptc-news photo tags-supplementaltype) |
| `News Photo Tags` | `iptc.news.ColorRepresentation` | ColorRepresentation | No | [🔗](#iptc-news photo tags-colorrepresentation) |
| `News Photo Tags` | `iptc.news.InterchangeColorSpace` | InterchangeColorSpace | No | [🔗](#iptc-news photo tags-interchangecolorspace) |
| `News Photo Tags` | `iptc.news.ColorSequence` | ColorSequence | No | [🔗](#iptc-news photo tags-colorsequence) |
| `News Photo Tags` | `iptc.news.ICCProfile` | ICCProfile | No | [🔗](#iptc-news photo tags-iccprofile) |
| `News Photo Tags` | `iptc.news.ColorCalibrationMatrix` | ColorCalibrationMatrix | No | [🔗](#iptc-news photo tags-colorcalibrationmatrix) |
| `News Photo Tags` | `iptc.news.LookupTable` | LookupTable | No | [🔗](#iptc-news photo tags-lookuptable) |
| `News Photo Tags` | `iptc.news.NumIndexEntries` | NumIndexEntries | No | [🔗](#iptc-news photo tags-numindexentries) |
| `News Photo Tags` | `iptc.news.ColorPalette` | ColorPalette | No | [🔗](#iptc-news photo tags-colorpalette) |
| `News Photo Tags` | `iptc.news.IPTCBitsPerSample` | IPTCBitsPerSample | No | [🔗](#iptc-news photo tags-iptcbitspersample) |
| `News Photo Tags` | `iptc.news.SampleStructure` | SampleStructure | No | [🔗](#iptc-news photo tags-samplestructure) |
| `News Photo Tags` | `iptc.news.ScanningDirection` | ScanningDirection | No | [🔗](#iptc-news photo tags-scanningdirection) |
| `News Photo Tags` | `iptc.news.IPTCImageRotation` | IPTCImageRotation | No | [🔗](#iptc-news photo tags-iptcimagerotation) |
| `News Photo Tags` | `iptc.news.DataCompressionMethod` | DataCompressionMethod | No | [🔗](#iptc-news photo tags-datacompressionmethod) |
| `News Photo Tags` | `iptc.news.QuantizationMethod` | QuantizationMethod | No | [🔗](#iptc-news photo tags-quantizationmethod) |
| `News Photo Tags` | `iptc.news.EndPoints` | EndPoints | No | [🔗](#iptc-news photo tags-endpoints) |
| `News Photo Tags` | `iptc.news.ExcursionTolerance` | ExcursionTolerance | No | [🔗](#iptc-news photo tags-excursiontolerance) |
| `News Photo Tags` | `iptc.news.BitsPerComponent` | BitsPerComponent | No | [🔗](#iptc-news photo tags-bitspercomponent) |
| `News Photo Tags` | `iptc.news.MaximumDensityRange` | MaximumDensityRange | No | [🔗](#iptc-news photo tags-maximumdensityrange) |
| `News Photo Tags` | `iptc.news.GammaCompensatedValue` | GammaCompensatedValue | No | [🔗](#iptc-news photo tags-gammacompensatedvalue) |

The technical details of each field may be found below:

<a id="iptc-news photo tags-version"></a>
### The `newsPhoto:Version` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.news.Version` |
| ID | `newsPhoto:Version` |
| Name | Version |
| Label | Version |
| Tag ID | 0 |
| Minimum bytes | 2 |
| Maximum bytes | 2 |
| Definiton | Version. |
| Repeatable? | No |
| Required? | No |
| Type | Short |

<a id="iptc-news photo tags-iptcpicturenumber"></a>
### The `newsPhoto:IPTCPictureNumber` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.news.IPTCPictureNumber` |
| ID | `newsPhoto:IPTCPictureNumber` |
| Name | IPTCPictureNumber |
| Label | IPTC Picture Number |
| Tag ID | 10 |
| Minimum bytes | 16 |
| Maximum bytes | 16 |
| Definiton | IPTC Picture Number. |
| Repeatable? | No |
| Required? | No |
| Type | String |

<a id="iptc-news photo tags-iptcimagewidth"></a>
### The `newsPhoto:IPTCImageWidth` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.news.IPTCImageWidth` |
| ID | `newsPhoto:IPTCImageWidth` |
| Name | IPTCImageWidth |
| Label | IPTC Image Width |
| Tag ID | 20 |
| Minimum bytes | 2 |
| Maximum bytes | 2 |
| Definiton | IPTC Image Width. |
| Repeatable? | No |
| Required? | No |
| Type | Short |

<a id="iptc-news photo tags-iptcimageheight"></a>
### The `newsPhoto:IPTCImageHeight` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.news.IPTCImageHeight` |
| ID | `newsPhoto:IPTCImageHeight` |
| Name | IPTCImageHeight |
| Label | IPTC Image Height |
| Tag ID | 30 |
| Minimum bytes | 2 |
| Maximum bytes | 2 |
| Definiton | IPTC Image Height. |
| Repeatable? | No |
| Required? | No |
| Type | Short |

<a id="iptc-news photo tags-iptcpixelwidth"></a>
### The `newsPhoto:IPTCPixelWidth` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.news.IPTCPixelWidth` |
| ID | `newsPhoto:IPTCPixelWidth` |
| Name | IPTCPixelWidth |
| Label | IPTC Pixel Width |
| Tag ID | 40 |
| Minimum bytes | 2 |
| Maximum bytes | 2 |
| Definiton | IPTC Pixel Width. |
| Repeatable? | No |
| Required? | No |
| Type | Short |

<a id="iptc-news photo tags-iptcpixelheight"></a>
### The `newsPhoto:IPTCPixelHeight` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.news.IPTCPixelHeight` |
| ID | `newsPhoto:IPTCPixelHeight` |
| Name | IPTCPixelHeight |
| Label | IPTC Pixel Height |
| Tag ID | 50 |
| Minimum bytes | 2 |
| Maximum bytes | 2 |
| Definiton | IPTC Pixel Height. |
| Repeatable? | No |
| Required? | No |
| Type | Short |

<a id="iptc-news photo tags-supplementaltype"></a>
### The `newsPhoto:SupplementalType` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.news.SupplementalType` |
| ID | `newsPhoto:SupplementalType` |
| Name | SupplementalType |
| Label | Supplemental Type |
| Tag ID | 55 |
| Minimum bytes | 1 |
| Maximum bytes | 1 |
| Definiton | Supplemental Type. |
| Options | 0: Main Image; 1: Reduced Resolution Image; 2: Logo; 3: Rasterized Caption |
| Repeatable? | No |
| Required? | No |
| Type | UInt8 |

<a id="iptc-news photo tags-colorrepresentation"></a>
### The `newsPhoto:ColorRepresentation` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.news.ColorRepresentation` |
| ID | `newsPhoto:ColorRepresentation` |
| Name | ColorRepresentation |
| Label | Color Representation |
| Tag ID | 60 |
| Minimum bytes | 2 |
| Maximum bytes | 2 |
| Definiton | Color Representation. |
| Options | 0x000: No Image, Single Frame; 0x100: Monochrome, Single Frame; 0x300: 3 Components, Single Frame; 0x301: 3 Components, Frame Sequential in Multiple Objects; 0x302: 3 Components, Frame Sequential in One Object; 0x303: 3 Components, Line Sequential; 0x304: 3 Components, Pixel Sequential; 0x305: 3 Components, Special Interleaving; 0x400: 4 Components, Single Frame; 0x401: 4 Components, Frame Sequential in Multiple Objects; 0x402: 4 Components, Frame Sequential in One Object; 0x403: 4 Components, Line Sequential; 0x404: 4 Components, Pixel Sequential; 0x405: 4 Components, Special Interleaving |
| Repeatable? | No |
| Required? | No |
| Type | Short |

<a id="iptc-news photo tags-interchangecolorspace"></a>
### The `newsPhoto:InterchangeColorSpace` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.news.InterchangeColorSpace` |
| ID | `newsPhoto:InterchangeColorSpace` |
| Name | InterchangeColorSpace |
| Label | Interchange Color Space |
| Tag ID | 64 |
| Minimum bytes | 1 |
| Maximum bytes | 1 |
| Definiton | Interchange Color Space. |
| Options | 1: X,Y,Z CIE; 2: RGB SMPTE; 3: Y,U,V (K) (D65); 4: RGB Device Dependent; 5: CMY (K) Device Dependent; 6: Lab (K) CIE; 7: YCbCr; 8: sRGB |
| Repeatable? | No |
| Required? | No |
| Type | UInt8 |

<a id="iptc-news photo tags-colorsequence"></a>
### The `newsPhoto:ColorSequence` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.news.ColorSequence` |
| ID | `newsPhoto:ColorSequence` |
| Name | ColorSequence |
| Label | Color Sequence |
| Tag ID | 65 |
| Minimum bytes | 1 |
| Maximum bytes | 1 |
| Definiton | Color Sequence. |
| Repeatable? | No |
| Required? | No |
| Type | UInt8 |

<a id="iptc-news photo tags-iccprofile"></a>
### The `newsPhoto:ICCProfile` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.news.ICCProfile` |
| ID | `newsPhoto:ICCProfile` |
| Name | ICCProfile |
| Label | ICC Profile |
| Tag ID | 66 |
| Minimum bytes | – |
| Maximum bytes | – |
| Definiton | ICC Profile. |
| Read Only? | Yes |
| Repeatable? | No |
| Required? | No |
| Type | Undefined |

<a id="iptc-news photo tags-colorcalibrationmatrix"></a>
### The `newsPhoto:ColorCalibrationMatrix` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.news.ColorCalibrationMatrix` |
| ID | `newsPhoto:ColorCalibrationMatrix` |
| Name | ColorCalibrationMatrix |
| Label | Color Calibration Matrix |
| Tag ID | 70 |
| Minimum bytes | – |
| Maximum bytes | – |
| Definiton | Color Calibration Matrix. |
| Read Only? | Yes |
| Repeatable? | No |
| Required? | No |
| Type | Undefined |

<a id="iptc-news photo tags-lookuptable"></a>
### The `newsPhoto:LookupTable` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.news.LookupTable` |
| ID | `newsPhoto:LookupTable` |
| Name | LookupTable |
| Label | Lookup Table |
| Tag ID | 80 |
| Minimum bytes | – |
| Maximum bytes | – |
| Definiton | Lookup Table. |
| Read Only? | Yes |
| Repeatable? | No |
| Required? | No |
| Type | Undefined |

<a id="iptc-news photo tags-numindexentries"></a>
### The `newsPhoto:NumIndexEntries` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.news.NumIndexEntries` |
| ID | `newsPhoto:NumIndexEntries` |
| Name | NumIndexEntries |
| Label | Number of Index Entries |
| Tag ID | 84 |
| Minimum bytes | 2 |
| Maximum bytes | 2 |
| Definiton | Number of Index Entries. |
| Repeatable? | No |
| Required? | No |
| Type | Short |

<a id="iptc-news photo tags-colorpalette"></a>
### The `newsPhoto:ColorPalette` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.news.ColorPalette` |
| ID | `newsPhoto:ColorPalette` |
| Name | ColorPalette |
| Label | Color Palette |
| Tag ID | 85 |
| Minimum bytes | – |
| Maximum bytes | – |
| Definiton | Color Palette. |
| Repeatable? | No |
| Required? | No |
| Type | Undefined |

<a id="iptc-news photo tags-iptcbitspersample"></a>
### The `newsPhoto:IPTCBitsPerSample` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.news.IPTCBitsPerSample` |
| ID | `newsPhoto:IPTCBitsPerSample` |
| Name | IPTCBitsPerSample |
| Label | IPTC Bits Per Sample |
| Tag ID | 86 |
| Minimum bytes | 1 |
| Maximum bytes | 1 |
| Definiton | IPTC Bits Per Sample. |
| Repeatable? | No |
| Required? | No |
| Type | UInt8 |

<a id="iptc-news photo tags-samplestructure"></a>
### The `newsPhoto:SampleStructure` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.news.SampleStructure` |
| ID | `newsPhoto:SampleStructure` |
| Name | SampleStructure |
| Label | Sample Structure |
| Tag ID | 90 |
| Minimum bytes | 1 |
| Maximum bytes | 1 |
| Definiton | Sample Structure. |
| Options | 0: OrthogonalConstangSampling; 1: Orthogonal4-2-2Sampling; 2: CompressionDependent |
| Repeatable? | No |
| Required? | No |
| Type | UInt8 |

<a id="iptc-news photo tags-scanningdirection"></a>
### The `newsPhoto:ScanningDirection` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.news.ScanningDirection` |
| ID | `newsPhoto:ScanningDirection` |
| Name | ScanningDirection |
| Label | Scanning Direction |
| Tag ID | 100 |
| Minimum bytes | 1 |
| Maximum bytes | 1 |
| Definiton | Scanning Direction. |
| Options | 0: Left-Right, Top-Bottom; 1: Right-Left, Top-Bottom; 2: Left-Right, Bottom-Top; 3: Right-Left, Bottom-Top; 4: Top-Bottom, Left-Right; 5: Bottom-Top, Left-Right; 6: Top-Bottom, Right-Left; 7: Bottom-Top, Right-Left |
| Repeatable? | No |
| Required? | No |
| Type | UInt8 |

<a id="iptc-news photo tags-iptcimagerotation"></a>
### The `newsPhoto:IPTCImageRotation` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.news.IPTCImageRotation` |
| ID | `newsPhoto:IPTCImageRotation` |
| Name | IPTCImageRotation |
| Label | IPTC Image Rotation |
| Tag ID | 102 |
| Minimum bytes | 1 |
| Maximum bytes | 1 |
| Definiton | IPTC Image Rotation. |
| Options | 0: 0; 1: 90; 2: 180; 3: 270 |
| Repeatable? | No |
| Required? | No |
| Type | UInt8 |

<a id="iptc-news photo tags-datacompressionmethod"></a>
### The `newsPhoto:DataCompressionMethod` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.news.DataCompressionMethod` |
| ID | `newsPhoto:DataCompressionMethod` |
| Name | DataCompressionMethod |
| Label | Data Compression Method |
| Tag ID | 110 |
| Minimum bytes | 4 |
| Maximum bytes | 4 |
| Definiton | Data Compression Method. |
| Repeatable? | No |
| Required? | No |
| Type | Long |

<a id="iptc-news photo tags-quantizationmethod"></a>
### The `newsPhoto:QuantizationMethod` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.news.QuantizationMethod` |
| ID | `newsPhoto:QuantizationMethod` |
| Name | QuantizationMethod |
| Label | Quantization Method |
| Tag ID | 120 |
| Minimum bytes | 1 |
| Maximum bytes | 1 |
| Definiton | Quantization Method. |
| Options | 0: Linear Reflectance/Transmittance; 1: Linear Density; 2: IPTC Ref B; 3: Linear Dot Percent; 4: AP Domestic Analogue; 5: Compression Method Specific; 6: Color Space Specific; 7: Gamma Compensated |
| Repeatable? | No |
| Required? | No |
| Type | UInt8 |

<a id="iptc-news photo tags-endpoints"></a>
### The `newsPhoto:EndPoints` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.news.EndPoints` |
| ID | `newsPhoto:EndPoints` |
| Name | EndPoints |
| Label | End Points |
| Tag ID | 125 |
| Minimum bytes | – |
| Maximum bytes | – |
| Definiton | End Points. |
| Read Only? | Yes |
| Repeatable? | No |
| Required? | No |
| Type | Undefined |

<a id="iptc-news photo tags-excursiontolerance"></a>
### The `newsPhoto:ExcursionTolerance` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.news.ExcursionTolerance` |
| ID | `newsPhoto:ExcursionTolerance` |
| Name | ExcursionTolerance |
| Label | Excursion Tolerance |
| Tag ID | 125 |
| Minimum bytes | 1 |
| Maximum bytes | 1 |
| Definiton | Excursion Tolerance. |
| Options | 0: Not Allowed; 1: Allowed |
| Repeatable? | No |
| Required? | No |
| Type | UInt8 |

<a id="iptc-news photo tags-bitspercomponent"></a>
### The `newsPhoto:BitsPerComponent` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.news.BitsPerComponent` |
| ID | `newsPhoto:BitsPerComponent` |
| Name | BitsPerComponent |
| Label | Bits Per Component |
| Tag ID | 135 |
| Minimum bytes | 1 |
| Maximum bytes | 1 |
| Definiton | Bits Per Component. |
| Repeatable? | No |
| Required? | No |
| Type | UInt8 |

<a id="iptc-news photo tags-maximumdensityrange"></a>
### The `newsPhoto:MaximumDensityRange` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.news.MaximumDensityRange` |
| ID | `newsPhoto:MaximumDensityRange` |
| Name | MaximumDensityRange |
| Label | Maximum Density Range |
| Tag ID | 140 |
| Minimum bytes | 2 |
| Maximum bytes | 2 |
| Definiton | Maximum Density Range. |
| Repeatable? | No |
| Required? | No |
| Type | UInt16 |

<a id="iptc-news photo tags-gammacompensatedvalue"></a>
### The `newsPhoto:GammaCompensatedValue` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.news.GammaCompensatedValue` |
| ID | `newsPhoto:GammaCompensatedValue` |
| Name | GammaCompensatedValue |
| Label | Gamma Compensated Value |
| Tag ID | 145 |
| Minimum bytes | 2 |
| Maximum bytes | 2 |
| Definiton | Gamma Compensated Value. |
| Repeatable? | No |
| Required? | No |
| Type | UInt16 |


The IPTC metadata model's `Pre Object Data Tags` namespace offers four fields which are listed below along with a link to each field's technical information:

| Namespace  | Field Path | Field Name | Required? | Info |
|------------|------------|------------|:---------:|------|
| `Pre Object Data Tags` | `iptc.pre.SizeMode` | SizeMode | No | [🔗](#iptc-pre object data tags-sizemode) |
| `Pre Object Data Tags` | `iptc.pre.MaxSubfileSize` | MaxSubfileSize | No | [🔗](#iptc-pre object data tags-maxsubfilesize) |
| `Pre Object Data Tags` | `iptc.pre.ObjectSizeAnnounced` | ObjectSizeAnnounced | No | [🔗](#iptc-pre object data tags-objectsizeannounced) |
| `Pre Object Data Tags` | `iptc.pre.MaximumObjectSize` | MaximumObjectSize | No | [🔗](#iptc-pre object data tags-maximumobjectsize) |

The technical details of each field may be found below:

<a id="iptc-pre object data tags-sizemode"></a>
### The `preObjectData:SizeMode` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.pre.SizeMode` |
| ID | `preObjectData:SizeMode` |
| Name | SizeMode |
| Label | Size Mode |
| Tag ID | 10 |
| Minimum bytes | – |
| Maximum bytes | – |
| Definiton | Size Mode. |
| Read Only? | Yes |
| Repeatable? | No |
| Required? | No |
| Type | Undefined |

<a id="iptc-pre object data tags-maxsubfilesize"></a>
### The `preObjectData:MaxSubfileSize` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.pre.MaxSubfileSize` |
| ID | `preObjectData:MaxSubfileSize` |
| Name | MaxSubfileSize |
| Label | Max Subfile Size |
| Tag ID | 20 |
| Minimum bytes | – |
| Maximum bytes | – |
| Definiton | Max Subfile Size. |
| Read Only? | Yes |
| Repeatable? | No |
| Required? | No |
| Type | Undefined |

<a id="iptc-pre object data tags-objectsizeannounced"></a>
### The `preObjectData:ObjectSizeAnnounced` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.pre.ObjectSizeAnnounced` |
| ID | `preObjectData:ObjectSizeAnnounced` |
| Name | ObjectSizeAnnounced |
| Label | Object Size Announced |
| Tag ID | 90 |
| Minimum bytes | – |
| Maximum bytes | – |
| Definiton | Object Size Announced. |
| Read Only? | Yes |
| Repeatable? | No |
| Required? | No |
| Type | Undefined |

<a id="iptc-pre object data tags-maximumobjectsize"></a>
### The `preObjectData:MaximumObjectSize` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.pre.MaximumObjectSize` |
| ID | `preObjectData:MaximumObjectSize` |
| Name | MaximumObjectSize |
| Label | Maximum Object Size |
| Tag ID | 95 |
| Minimum bytes | – |
| Maximum bytes | – |
| Definiton | Maximum Object Size. |
| Read Only? | Yes |
| Repeatable? | No |
| Required? | No |
| Type | Undefined |


The IPTC metadata model's `Object Data Tags` namespace offers one field which is listed below along with a link to each field's technical information:

| Namespace  | Field Path | Field Name | Required? | Info |
|------------|------------|------------|:---------:|------|
| `Object Data Tags` | `iptc.object.SubFile` | SubFile | No | [🔗](#iptc-object data tags-subfile) |

The technical details of each field may be found below:

<a id="iptc-object data tags-subfile"></a>
### The `objectData:SubFile` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.object.SubFile` |
| ID | `objectData:SubFile` |
| Name | SubFile |
| Label | Sub File |
| Tag ID | 10 |
| Minimum bytes | – |
| Maximum bytes | – |
| Definiton | Sub File. |
| Read Only? | Yes |
| Repeatable? | No |
| Required? | No |
| Type | Undefined |


The IPTC metadata model's `Post Object Data Tags` namespace offers one field which is listed below along with a link to each field's technical information:

| Namespace  | Field Path | Field Name | Required? | Info |
|------------|------------|------------|:---------:|------|
| `Post Object Data Tags` | `iptc.post.ConfirmedObjectSize` | ConfirmedObjectSize | No | [🔗](#iptc-post object data tags-confirmedobjectsize) |

The technical details of each field may be found below:

<a id="iptc-post object data tags-confirmedobjectsize"></a>
### The `postObjectData:ConfirmedObjectSize` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `iptc.post.ConfirmedObjectSize` |
| ID | `postObjectData:ConfirmedObjectSize` |
| Name | ConfirmedObjectSize |
| Label | Confirmed Object Size |
| Tag ID | 10 |
| Minimum bytes | – |
| Maximum bytes | – |
| Definiton | Confirmed Object Size. |
| Read Only? | Yes |
| Repeatable? | No |
| Required? | No |
| Type | Undefined |


The IPTC metadata model's `FotoStation Tags` namespace does not currently offer any known fields.


### Credits & References

The IPTC field information was researched from various sources including from the IPTC
specification and EXIFTool documentation. Please visit these valuable online resources
to learn more about the IPTC metadata model specification and to support these world
class organizations and their products:

 * https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata
 * https://exiftool.org/TagNames/IPTC.html
