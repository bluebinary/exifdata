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

The EXIFData library provides support for reading and writing from the following IPTC
fields within the IPTC-IIM model unless marked otherwise:

The IPTC metadata model has seven namespaces which are documented below.

The IPTC metadata model's 'Envelope' namespace offers fourteen fields which are detailed below:

### The `envelope:ModelVersion` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.envelope.ModelVersion |
| Maximum bytes | 2 |
| Minimum bytes | 2 |
| ID | envelope:ModelVersion |
| Label | – |
| Name | ModelVersion |
| Tag ID | 0 |
| Definiton | A binary number identifying the version of the Information Interchange Model, Part I, utilised by the provider. Version numbers are assigned by IPTC and NAA organizations. |
| Repeatable? | No |
| Required? | Yes |
| Type | Short |

### The `envelope:Destination` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.envelope.Destination |
| Maximum bytes | 1024 |
| Minimum bytes | 0 |
| ID | envelope:Destination |
| Label | – |
| Name | Destination |
| Tag ID | 5 |
| Definiton | This DataSet is to accommodate some providers who require routing information above the appropriate OSI layers. |
| Repeatable? | Yes |
| Required? | No |
| Type | String |

### The `envelope:FileFormat` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.envelope.FileFormat |
| Maximum bytes | 2 |
| Minimum bytes | 2 |
| ID | envelope:FileFormat |
| Label | – |
| Name | FileFormat |
| Tag ID | 20 |
| Definiton | A binary number representing the file format. The file format must be registered with IPTC or NAA with a unique number assigned to it. The information is used to route the data to the appropriate system and to allow the receiving system to perform the appropriate actions there to. |
| Options | 0: No ObjectData, 1: IPTC-NAA Digital Newsphoto Parameter Record, 2: IPTC7901 Recommended Message Format, 3: Tagged Image File Format [.TIFF] (Adobe/Aldus Image Data), 4: Illustrator (Adobe Graphics Data), 5: AppleSingle (Apple Computer Inc), 6: NAA 89-3 (ANPA 1312), 7: MacBinary II, 8: IPTC Unstructured Character Oriented File Format (UCOFF), 9: United Press International ANPA 1312 variant, 10: United Press International Down-Load Message, 11: JPEG File Interchange (JFIF), 12: Photo-CD Image-Pac (Eastman Kodak), 13: Bit Mapped Graphics File [.BMP] (Microsoft), 14: Digital Audio File [.WAV] (Microsoft & Creative Labs), 15: Audio plus Moving Video [.AVI] (Microsoft), 16: PC DOS/Windows Executable Files [.COM][.EXE], 17: Compressed Binary File [.ZIP] (PKWare Inc), 18: Audio Interchange File Format [.AIFF] (Apple Computer Inc), 19: RIFF Wave (Microsoft Corporation), 20: Freehand (Macromedia/Aldus), 21: Hypertext Markup Language [.HTML] (The Internet Society), 22: MPEG 2 Audio Layer 2 (Musicom), ISO/IEC, 23: MPEG 2 Audio Layer 3, ISO/IEC, 24: Portable Document File [.PDF] Adobe, 25: News Industry Text Format (NITF), 26: Tape Archive [.TAR], 27: Tidningarnas Telegrambyra NITF version (TTNITF DTD), 28: Ritzaus Bureau NITF version (RBNITF DTD), 29: Corel Draw [.CDR] |
| Repeatable? | No |
| Required? | Yes |
| Type | Short |

### The `envelope:FileVersion` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.envelope.FileVersion |
| Maximum bytes | 2 |
| Minimum bytes | 2 |
| ID | envelope:FileVersion |
| Label | – |
| Name | FileVersion |
| Tag ID | 22 |
| Definiton | A binary number representing the particular version of the File Format specified by <FileFormat> tag. |
| Repeatable? | No |
| Required? | Yes |
| Type | Short |

### The `envelope:ServiceID` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.envelope.ServiceID |
| Maximum bytes | 10 |
| Minimum bytes | 0 |
| ID | envelope:ServiceID |
| Label | – |
| Name | ServiceID |
| Tag ID | 30 |
| Definiton | Identifies the provider and product. |
| Repeatable? | No |
| Required? | Yes |
| Type | String |

### The `envelope:EnvelopeNumber` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.envelope.EnvelopeNumber |
| Maximum bytes | 8 |
| Minimum bytes | 8 |
| ID | envelope:EnvelopeNumber |
| Label | – |
| Name | EnvelopeNumber |
| Tag ID | 40 |
| Definiton | The characters form a number that will be unique for the date specified in <DateSent> tag and for the Service Identifier specified by <ServiceIdentifier> tag. If identical envelope numbers appear with the same date and with the same Service Identifier, records 2-9 must be unchanged from the original. This is not intended to be a sequential serial number reception check. |
| Repeatable? | No |
| Required? | Yes |
| Type | String |

### The `envelope:ProductID` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.envelope.ProductID |
| Maximum bytes | 32 |
| Minimum bytes | 0 |
| ID | envelope:ProductID |
| Label | – |
| Name | ProductID |
| Tag ID | 50 |
| Definiton | Allows a provider to identify subsets of its overall service. Used to provide receiving organisation data on which to select, route, or otherwise handle data. |
| Repeatable? | Yes |
| Required? | No |
| Type | String |

### The `envelope:EnvelopePriority` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.envelope.EnvelopePriority |
| Maximum bytes | 1 |
| Minimum bytes | 1 |
| ID | envelope:EnvelopePriority |
| Label | – |
| Name | EnvelopePriority |
| Tag ID | 60 |
| Definiton | Specifies the envelope handling priority and not the editorial urgency (see <Urgency> tag). "1" indicates the most urgent, "5" the normal urgency, and "8" the least urgent copy. The numeral "9" indicates a User Defined Priority. The numeral "0" is reserved for future use. |
| Options | 0: 0 (reserved), 1: 1 (most urgent), 2: 2, 3: 3, 4: 4, 5: 5 (normal urgency), 6: 6, 7: 7, 8: 8 (least urgent), 9: 9 (user-defined priority) |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `envelope:DateSent` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.envelope.DateSent |
| Maximum bytes | 8 |
| Minimum bytes | 8 |
| ID | envelope:DateSent |
| Label | – |
| Name | DateSent |
| Tag ID | 70 |
| Definiton | Uses the format CCYYMMDD (century, year, month, day) as de-fined in ISO 8601 to indicate year, month and day the service sent the material. |
| Repeatable? | No |
| Required? | Yes |
| Type | Date |

### The `envelope:TimeSent` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.envelope.TimeSent |
| Maximum bytes | 11 |
| Minimum bytes | 11 |
| ID | envelope:TimeSent |
| Label | – |
| Name | TimeSent |
| Tag ID | 80 |
| Definiton | Uses the format HHMMSS:HHMM where HHMMSS refers to local hour, minute and seconds and HHMM refers to hours and minutes ahead (+) or behind (-) Universal Coordinated Time as described in ISO 8601. This is the time the service sent the material. |
| Repeatable? | No |
| Required? | No |
| Type | Time |

### The `envelope:CharacterSet` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.envelope.CharacterSet |
| Maximum bytes | 32 |
| Minimum bytes | 0 |
| ID | envelope:CharacterSet |
| Label | – |
| Name | CharacterSet |
| Tag ID | 90 |
| Definiton | This tag consisting of one or more control functions used for the announcement, invocation or designation of coded character sets. The control functions follow the ISO 2022 standard and may consist of the escape control character and one or more graphic characters. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `envelope:UNO` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.envelope.UNO |
| Maximum bytes | 80 |
| Minimum bytes | 14 |
| ID | envelope:UNO |
| Label | – |
| Name | UNO |
| Tag ID | 100 |
| Definiton | This tag provide a globally unique identification for objects as specified in the IIM, independent of provider and for any media form. The provider must ensure the UNO is unique. Objects with the same UNO are identical. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `envelope:ARMID` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.envelope.ARMID |
| Maximum bytes | 2 |
| Minimum bytes | 2 |
| ID | envelope:ARMID |
| Label | – |
| Name | ARMID |
| Tag ID | 120 |
| Definiton | The DataSet identifies the Abstract Relationship Method identifier (ARM) which is described in a document registered by the originator of the ARM with the IPTC and NAA organizations. |
| Repeatable? | No |
| Required? | No |
| Type | Short |

### The `envelope:ARMVersion` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.envelope.ARMVersion |
| Maximum bytes | 2 |
| Minimum bytes | 2 |
| ID | envelope:ARMVersion |
| Label | – |
| Name | ARMVersion |
| Tag ID | 122 |
| Definiton | This tag consisting of a binary number representing the particular version of the ARM specified by tag 'ARMID'. |
| Repeatable? | No |
| Required? | No |
| Type | Short |

The IPTC metadata model's 'Application' namespace offers 70 fields which are detailed below:

### The `application:RecordVersion` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.RecordVersion |
| Maximum bytes | 2 |
| Minimum bytes | 2 |
| ID | application:RecordVersion |
| Label | – |
| Name | RecordVersion |
| Tag ID | 0 |
| Definiton | A binary number identifying the version of the Information Interchange Model, Part II, utilised by the provider. Version numbers are assigned by IPTC and NAA organizations. |
| Repeatable? | No |
| Required? | Yes |
| Type | Short |

### The `application:ObjectType` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.ObjectType |
| Maximum bytes | 67 |
| Minimum bytes | 3 |
| ID | application:ObjectType |
| Label | – |
| Name | ObjectType |
| Tag ID | 3 |
| Definiton | The Object Type is used to distinguish between different types of objects within the IIM. The first part is a number representing a language independent international reference to an Object Type followed by a colon separator. The second part, if used, is a text representation of the Object Type Number consisting of graphic characters plus spaces either in English or in the language of the service as indicated in tag <LanguageIdentifier>. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:ObjectAttribute` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.ObjectAttribute |
| Maximum bytes | 68 |
| Minimum bytes | 4 |
| ID | application:ObjectAttribute |
| Label | – |
| Name | ObjectAttribute |
| Tag ID | 4 |
| Definiton | The Object Attribute defines the nature of the object independent of the Subject. The first part is a number representing a language independent international reference to an Object Attribute followed by a colon separator. The second part, if used, is a text representation of the Object Attribute Number consisting of graphic characters plus spaces either in English, or in the language of the service as indicated in tag <LanguageIdentifier>. |
| Repeatable? | Yes |
| Required? | No |
| Type | String |

### The `application:ObjectName` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.ObjectName |
| Maximum bytes | 64 |
| Minimum bytes | 0 |
| ID | application:ObjectName |
| Label | – |
| Name | ObjectName |
| Tag ID | 5 |
| Definiton | Used as a shorthand reference for the object. Changes to exist-ing data, such as updated stories or new crops on photos, should be identified in tag <EditStatus>. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:EditStatus` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.EditStatus |
| Maximum bytes | 64 |
| Minimum bytes | 0 |
| ID | application:EditStatus |
| Label | – |
| Name | EditStatus |
| Tag ID | 7 |
| Definiton | Status of the object data, according to the practice of the provider. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:EditorialUpdate` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.EditorialUpdate |
| Maximum bytes | 2 |
| Minimum bytes | 2 |
| ID | application:EditorialUpdate |
| Label | – |
| Name | EditorialUpdate |
| Tag ID | 8 |
| Definiton | Indicates the type of update that this object provides to a previous object. The link to the previous object is made using the tags <ARMIdentifier> and <ARMVersion>, according to the practices of the provider. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:Urgency` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.Urgency |
| Maximum bytes | 1 |
| Minimum bytes | 1 |
| ID | application:Urgency |
| Label | – |
| Name | Urgency |
| Tag ID | 10 |
| Definiton | Specifies the editorial urgency of content and not necessarily the envelope handling priority (see tag <EnvelopePriority>). The "1" is most urgent, "5" normal and "8" denotes the least-urgent copy. |
| Options | 0: 0 (reserved), 1: 1 (most urgent), 2: 2, 3: 3, 4: 4, 5: 5 (normal urgency), 6: 6, 7: 7, 8: 8 (least urgent), 9: 9 (user-defined priority) |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:Subject` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.Subject |
| Maximum bytes | 236 |
| Minimum bytes | 13 |
| ID | application:Subject |
| Label | – |
| Name | Subject |
| Tag ID | 12 |
| Definiton | The Subject Reference is a structured definition of the subject matter. |
| Repeatable? | Yes |
| Required? | No |
| Type | String |

### The `application:Category` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.Category |
| Maximum bytes | 3 |
| Minimum bytes | 0 |
| ID | application:Category |
| Label | – |
| Name | Category |
| Tag ID | 15 |
| Definiton | Identifies the subject of the object data in the opinion of the provider. A list of categories will be maintained by a regional registry, where available, otherwise by the provider. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:SupplementalCategories` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.SupplementalCategories |
| Maximum bytes | 32 |
| Minimum bytes | 0 |
| ID | application:SupplementalCategories |
| Label | – |
| Name | SupplementalCategories |
| Tag ID | 20 |
| Definiton | Supplemental categories further refine the subject of an object data. A supplemental category may include any of the recognised categories as used in tag 'Category'. Otherwise, selection of supplemental categories are left to the provider. |
| Repeatable? | Yes |
| Required? | No |
| Type | String |

### The `application:FixtureID` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.FixtureID |
| Maximum bytes | 32 |
| Minimum bytes | 0 |
| ID | application:FixtureID |
| Label | – |
| Name | FixtureID |
| Tag ID | 22 |
| Definiton | Identifies object data that recurs often and predictably. Enables users to immediately find or recall such an object. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:Keywords` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.Keywords |
| Maximum bytes | 64 |
| Minimum bytes | 0 |
| ID | application:Keywords |
| Label | – |
| Name | Keywords |
| Tag ID | 25 |
| Definiton | Used to indicate specific information retrieval words. It is expected that a provider of various types of data that are related in subject matter uses the same keyword, enabling the receiving system or subsystems to search across all types of data for related material. |
| Repeatable? | Yes |
| Required? | No |
| Type | String |

### The `application:LocationCode` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.LocationCode |
| Maximum bytes | 3 |
| Minimum bytes | 3 |
| ID | application:LocationCode |
| Label | – |
| Name | LocationCode |
| Tag ID | 26 |
| Definiton | Indicates the code of a country/geographical location referenced by the content of the object. Where ISO has established an appropriate country code under ISO 3166, that code will be used. When ISO 3166 does not adequately provide for identification of a location or a country, e.g. ships at sea, space, IPTC will assign an appropriate three-character code under the provisions of ISO 3166 to avoid conflicts. |
| Repeatable? | Yes |
| Required? | No |
| Type | String |

### The `application:LocationName` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.LocationName |
| Maximum bytes | 64 |
| Minimum bytes | 0 |
| ID | application:LocationName |
| Label | – |
| Name | LocationName |
| Tag ID | 27 |
| Definiton | Provides a full, publishable name of a country/geographical location referenced by the content of the object, according to guidelines of the provider. |
| Repeatable? | Yes |
| Required? | No |
| Type | String |

### The `application:ReleaseDate` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.ReleaseDate |
| Maximum bytes | 8 |
| Minimum bytes | 8 |
| ID | application:ReleaseDate |
| Label | – |
| Name | ReleaseDate |
| Tag ID | 30 |
| Definiton | Designates in the form CCYYMMDD the earliest date the provider intends the object to be used. Follows ISO 8601 standard. |
| Repeatable? | No |
| Required? | No |
| Type | Date |

### The `application:ReleaseTime` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.ReleaseTime |
| Maximum bytes | 11 |
| Minimum bytes | 11 |
| ID | application:ReleaseTime |
| Label | – |
| Name | ReleaseTime |
| Tag ID | 35 |
| Definiton | Designates in the form HHMMSS:HHMM the earliest time the provider intends the object to be used. Follows ISO 8601 standard. |
| Repeatable? | No |
| Required? | No |
| Type | Time |

### The `application:ExpirationDate` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.ExpirationDate |
| Maximum bytes | 8 |
| Minimum bytes | 8 |
| ID | application:ExpirationDate |
| Label | – |
| Name | ExpirationDate |
| Tag ID | 37 |
| Definiton | Designates in the form CCYYMMDD the latest date the provider or owner intends the object data to be used. Follows ISO 8601 standard. |
| Repeatable? | No |
| Required? | No |
| Type | Date |

### The `application:ExpirationTime` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.ExpirationTime |
| Maximum bytes | 11 |
| Minimum bytes | 11 |
| ID | application:ExpirationTime |
| Label | – |
| Name | ExpirationTime |
| Tag ID | 38 |
| Definiton | Designates in the form HHMMSS:HHMM the latest time the provider or owner intends the object data to be used. Follows ISO 8601 standard. |
| Repeatable? | No |
| Required? | No |
| Type | Time |

### The `application:SpecialInstructions` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.SpecialInstructions |
| Maximum bytes | 256 |
| Minimum bytes | 0 |
| ID | application:SpecialInstructions |
| Label | – |
| Name | SpecialInstructions |
| Tag ID | 40 |
| Definiton | Other editorial instructions concerning the use of the object data, such as embargoes and warnings. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:ActionAdvised` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.ActionAdvised |
| Maximum bytes | 2 |
| Minimum bytes | 2 |
| ID | application:ActionAdvised |
| Label | – |
| Name | ActionAdvised |
| Tag ID | 42 |
| Definiton | Indicates the type of action that this object provides to a previous object. The link to the previous object is made using tags <ARMIdentifier> and <ARMVersion>, according to the practices of the provider. |
| Options | 01: Object Kill, 02: Object Replace, 03: Object Append, 04: Object Reference |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:ReferenceService` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.ReferenceService |
| Maximum bytes | 10 |
| Minimum bytes | 0 |
| ID | application:ReferenceService |
| Label | – |
| Name | ReferenceService |
| Tag ID | 45 |
| Definiton | Identifies the Service Identifier of a prior envelope to which the current object refers. |
| Repeatable? | Yes |
| Required? | No |
| Type | String |

### The `application:ReferenceDate` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.ReferenceDate |
| Maximum bytes | 8 |
| Minimum bytes | 8 |
| ID | application:ReferenceDate |
| Label | – |
| Name | ReferenceDate |
| Tag ID | 47 |
| Definiton | Identifies the date of a prior envelope to which the current object refers. |
| Repeatable? | Yes |
| Required? | No |
| Type | Date |

### The `application:ReferenceNumber` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.ReferenceNumber |
| Maximum bytes | 8 |
| Minimum bytes | 8 |
| ID | application:ReferenceNumber |
| Label | – |
| Name | ReferenceNumber |
| Tag ID | 50 |
| Definiton | Identifies the Envelope Number of a prior envelope to which the current object refers. |
| Repeatable? | Yes |
| Required? | No |
| Type | String |

### The `application:DateCreated` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.DateCreated |
| Maximum bytes | 8 |
| Minimum bytes | 8 |
| ID | application:DateCreated |
| Label | – |
| Name | DateCreated |
| Tag ID | 55 |
| Definiton | Represented in the form CCYYMMDD to designate the date the intellectual content of the object data was created rather than the date of the creation of the physical representation. Follows ISO 8601 standard. |
| Repeatable? | No |
| Required? | No |
| Type | Date |

### The `application:TimeCreated` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.TimeCreated |
| Maximum bytes | 11 |
| Minimum bytes | 11 |
| ID | application:TimeCreated |
| Label | – |
| Name | TimeCreated |
| Tag ID | 60 |
| Definiton | Represented in the form HHMMSS:HHMM to designate the time the intellectual content of the object data current source material was created rather than the creation of the physical representation. Follows ISO 8601 standard. |
| Repeatable? | No |
| Required? | No |
| Type | Time |

### The `application:DigitizationDate` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.DigitizationDate |
| Maximum bytes | 8 |
| Minimum bytes | 8 |
| ID | application:DigitizationDate |
| Label | – |
| Name | DigitizationDate |
| Tag ID | 62 |
| Definiton | Represented in the form CCYYMMDD to designate the date the digital representation of the object data was created. Follows ISO 8601 standard. |
| Repeatable? | No |
| Required? | No |
| Type | Date |

### The `application:DigitizationTime` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.DigitizationTime |
| Maximum bytes | 11 |
| Minimum bytes | 11 |
| ID | application:DigitizationTime |
| Label | – |
| Name | DigitizationTime |
| Tag ID | 63 |
| Definiton | Represented in the form HHMMSS:HHMM to designate the time the digital representation of the object data was created. Follows ISO 8601 standard. |
| Repeatable? | No |
| Required? | No |
| Type | Time |

### The `application:Program` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.Program |
| Maximum bytes | 32 |
| Minimum bytes | 0 |
| ID | application:Program |
| Label | – |
| Name | Program |
| Tag ID | 65 |
| Definiton | Identifies the type of program used to originate the object data. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:ProgramVersion` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.ProgramVersion |
| Maximum bytes | 10 |
| Minimum bytes | 0 |
| ID | application:ProgramVersion |
| Label | – |
| Name | ProgramVersion |
| Tag ID | 70 |
| Definiton | Used to identify the version of the program mentioned in tag <Program>. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:ObjectCycle` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.ObjectCycle |
| Maximum bytes | 1 |
| Minimum bytes | 1 |
| ID | application:ObjectCycle |
| Label | – |
| Name | ObjectCycle |
| Tag ID | 75 |
| Definiton | Used to identify the editorial cycle of object data. |
| Options | a: Morning, b: Both Morning and Evening, p: Evening |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:Byline` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.Byline |
| Maximum bytes | 32 |
| Minimum bytes | 0 |
| ID | application:Byline |
| Label | – |
| Name | Byline |
| Tag ID | 80 |
| Definiton | Contains name of the creator of the object data, e.g. writer, photographer or graphic artist. |
| Repeatable? | Yes |
| Required? | No |
| Type | String |

### The `application:BylineTitle` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.BylineTitle |
| Maximum bytes | 32 |
| Minimum bytes | 0 |
| ID | application:BylineTitle |
| Label | – |
| Name | BylineTitle |
| Tag ID | 85 |
| Definiton | A by-line title is the title of the creator or creators of an object data. Where used, a by-line title should follow the by-line it modifies. |
| Repeatable? | Yes |
| Required? | No |
| Type | String |

### The `application:City` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.City |
| Maximum bytes | 32 |
| Minimum bytes | 0 |
| ID | application:City |
| Label | – |
| Name | City |
| Tag ID | 90 |
| Definiton | Identifies city of object data origin according to guidelines established by the provider. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:SubLocation` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.SubLocation |
| Maximum bytes | 32 |
| Minimum bytes | 0 |
| ID | application:SubLocation |
| Label | – |
| Name | SubLocation |
| Tag ID | 92 |
| Definiton | Identifies the location within a city from which the object data originates, according to guidelines established by the provider. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:ProvinceState` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.ProvinceState |
| Maximum bytes | 32 |
| Minimum bytes | 0 |
| ID | application:ProvinceState |
| Label | – |
| Name | ProvinceState |
| Tag ID | 95 |
| Definiton | Identifies Province/State of origin according to guidelines established by the provider. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:CountryCode` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.CountryCode |
| Maximum bytes | 3 |
| Minimum bytes | 3 |
| ID | application:CountryCode |
| Label | – |
| Name | CountryCode |
| Tag ID | 100 |
| Definiton | Indicates the code of the country/primary location where the intellectual property of the object data was created, e.g. a photo was taken, an event occurred. Where ISO has established an appropriate country code under ISO 3166, that code will be used. When ISO 3166 does not adequately provide for identification of a location or a new country, e.g. ships at sea, space, IPTC will assign an appropriate three-character code under the provisions of ISO 3166 to avoid conflicts. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:CountryName` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.CountryName |
| Maximum bytes | 64 |
| Minimum bytes | 0 |
| ID | application:CountryName |
| Label | – |
| Name | CountryName |
| Tag ID | 101 |
| Definiton | Provides full, publishable, name of the country/primary location where the intellectual property of the object data was created, according to guidelines of the provider. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:TransmissionReference` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.TransmissionReference |
| Maximum bytes | 32 |
| Minimum bytes | 0 |
| ID | application:TransmissionReference |
| Label | – |
| Name | TransmissionReference |
| Tag ID | 103 |
| Definiton | A code representing the location of original transmission according to practices of the provider. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:Headline` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.Headline |
| Maximum bytes | 256 |
| Minimum bytes | 0 |
| ID | application:Headline |
| Label | – |
| Name | Headline |
| Tag ID | 105 |
| Definiton | A publishable entry providing a synopsis of the contents of the object data. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:Credit` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.Credit |
| Maximum bytes | 32 |
| Minimum bytes | 0 |
| ID | application:Credit |
| Label | – |
| Name | Credit |
| Tag ID | 110 |
| Definiton | Identifies the provider of the object data, not necessarily the owner/creator. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:Source` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.Source |
| Maximum bytes | 32 |
| Minimum bytes | 0 |
| ID | application:Source |
| Label | – |
| Name | Source |
| Tag ID | 115 |
| Definiton | Identifies the original owner of the intellectual content of the object data. This could be an agency, a member of an agency or an individual. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:Copyright` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.Copyright |
| Maximum bytes | 128 |
| Minimum bytes | 0 |
| ID | application:Copyright |
| Label | – |
| Name | Copyright |
| Tag ID | 116 |
| Definiton | Contains any necessary copyright notice. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:Contact` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.Contact |
| Maximum bytes | 128 |
| Minimum bytes | 0 |
| ID | application:Contact |
| Label | – |
| Name | Contact |
| Tag ID | 118 |
| Definiton | Identifies the person or organisation which can provide further background information on the object data. |
| Repeatable? | Yes |
| Required? | No |
| Type | String |

### The `application:Caption` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.Caption |
| Maximum bytes | 2000 |
| Minimum bytes | 0 |
| ID | application:Caption |
| Label | – |
| Name | Caption |
| Tag ID | 120 |
| Definiton | A textual description of the object data. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:LocalCaption` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.LocalCaption |
| Maximum bytes | 256 |
| Minimum bytes | 0 |
| ID | application:LocalCaption |
| Label | – |
| Name | LocalCaption |
| Tag ID | 121 |
| Definiton | A localized textual description of the object data. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:Writer` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.Writer |
| Maximum bytes | 32 |
| Minimum bytes | 0 |
| ID | application:Writer |
| Label | – |
| Name | Writer |
| Tag ID | 122 |
| Definiton | Identification of the name of the person involved in the writing, editing or correcting the object data or caption/abstract. |
| Repeatable? | Yes |
| Required? | No |
| Type | String |

### The `application:RasterizedCaption` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.RasterizedCaption |
| Maximum bytes | 7360 |
| Minimum bytes | 7360 |
| ID | application:RasterizedCaption |
| Label | – |
| Name | RasterizedCaption |
| Tag ID | 125 |
| Definiton | Contains the rasterized object data description and is used where characters that have not been coded are required for the caption. |
| Repeatable? | No |
| Required? | No |
| Type | Undefined |

### The `application:ImageType` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.ImageType |
| Maximum bytes | 2 |
| Minimum bytes | 2 |
| ID | application:ImageType |
| Label | – |
| Name | ImageType |
| Tag ID | 130 |
| Definiton | Indicates the color components of an image. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:ImageOrientation` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.ImageOrientation |
| Maximum bytes | 1 |
| Minimum bytes | 1 |
| ID | application:ImageOrientation |
| Label | – |
| Name | ImageOrientation |
| Tag ID | 131 |
| Definiton | Indicates the layout of an image. |
| Options | L: Landscape, P: Portrait, S: Square |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:Language` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.Language |
| Maximum bytes | 3 |
| Minimum bytes | 2 |
| ID | application:Language |
| Label | – |
| Name | Language |
| Tag ID | 135 |
| Definiton | Describes the major national language of the object, according to the 2-letter codes of ISO 639:1988. Does not define or imply any coded character set, but is used for internal routing, e.g. to various editorial desks. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:AudioType` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.AudioType |
| Maximum bytes | 2 |
| Minimum bytes | 2 |
| ID | application:AudioType |
| Label | – |
| Name | AudioType |
| Tag ID | 150 |
| Definiton | Indicates the type of an audio content. |
| Options | 0T: Text Only, 1A: Mono Actuality, 1C: Mono Question and Answer Session, 1M: Mono Music, 1Q: Mono Response to a Question, 1R: Mono Raw Sound, 1S: Mono Scener, 1V: Mono Voicer, 1W: Mono Wrap, 2A: Stereo Actuality, 2C: Stereo Question and Answer Session, 2M: Stereo Music, 2Q: Stereo Response to a Question, 2R: Stereo Raw Sound, 2S: Stereo Scener, 2V: Stereo Voicer, 2W: Stereo Wrap |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:AudioSamplingRate` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.AudioSamplingRate |
| Maximum bytes | 6 |
| Minimum bytes | 6 |
| ID | application:AudioSamplingRate |
| Label | – |
| Name | AudioSamplingRate |
| Tag ID | 151 |
| Definiton | Indicates the sampling rate in Hertz of an audio content. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:AudioSamplingResolution` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.AudioSamplingResolution |
| Maximum bytes | 2 |
| Minimum bytes | 2 |
| ID | application:AudioSamplingResolution |
| Label | – |
| Name | AudioSamplingResolution |
| Tag ID | 152 |
| Definiton | Indicates the sampling resolution of an audio content. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:AudioDuration` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.AudioDuration |
| Maximum bytes | 6 |
| Minimum bytes | 6 |
| ID | application:AudioDuration |
| Label | – |
| Name | AudioDuration |
| Tag ID | 153 |
| Definiton | Indicates the duration of an audio content. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:AudioOutcue` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.AudioOutcue |
| Maximum bytes | 64 |
| Minimum bytes | 0 |
| ID | application:AudioOutcue |
| Label | – |
| Name | AudioOutcue |
| Tag ID | 154 |
| Definiton | Identifies the content of the end of an audio object data, according to guidelines established by the provider. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:JobID` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.JobID |
| Maximum bytes | 64 |
| Minimum bytes | 0 |
| ID | application:JobID |
| Label | – |
| Name | JobID |
| Tag ID | 184 |
| Definiton | Job ID. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:MasterDocumentID` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.MasterDocumentID |
| Maximum bytes | 256 |
| Minimum bytes | 0 |
| ID | application:MasterDocumentID |
| Label | – |
| Name | MasterDocumentID |
| Tag ID | 185 |
| Definiton | Master Document ID. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:ShortDocumentID` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.ShortDocumentID |
| Maximum bytes | 64 |
| Minimum bytes | 0 |
| ID | application:ShortDocumentID |
| Label | – |
| Name | ShortDocumentID |
| Tag ID | 186 |
| Definiton | Short Document ID. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:UniqueDocumentID` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.UniqueDocumentID |
| Maximum bytes | 64 |
| Minimum bytes | 0 |
| ID | application:UniqueDocumentID |
| Label | – |
| Name | UniqueDocumentID |
| Tag ID | 187 |
| Definiton | Unique Document ID. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:OwnerID` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.OwnerID |
| Maximum bytes | 64 |
| Minimum bytes | 0 |
| ID | application:OwnerID |
| Label | – |
| Name | OwnerID |
| Tag ID | 188 |
| Definiton | Owner ID. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:PreviewFormat` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.PreviewFormat |
| Maximum bytes | 2 |
| Minimum bytes | 2 |
| ID | application:PreviewFormat |
| Label | – |
| Name | PreviewFormat |
| Tag ID | 200 |
| Definiton | A binary number representing the file format of the object data preview. The file format must be registered with IPTC or NAA organizations with a unique number assigned to it. |
| Options | 0: No ObjectData, 1: IPTC-NAA Digital Newsphoto Parameter Record, 2: IPTC7901 Recommended Message Format, 3: Tagged Image File Format [.TIFF] (Adobe/Aldus Image Data), 4: Illustrator (Adobe Graphics Data), 5: AppleSingle (Apple Computer Inc), 6: NAA 89-3 (ANPA 1312), 7: MacBinary II, 8: IPTC Unstructured Character Oriented File Format (UCOFF), 9: United Press International ANPA 1312 variant, 10: United Press International Down-Load Message, 11: JPEG File Interchange (JFIF), 12: Photo-CD Image-Pac (Eastman Kodak), 13: Bit Mapped Graphics File [.BMP] (Microsoft), 14: Digital Audio File [.WAV] (Microsoft & Creative Labs), 15: Audio plus Moving Video [.AVI] (Microsoft), 16: PC DOS/Windows Executable Files [.COM][.EXE], 17: Compressed Binary File [.ZIP] (PKWare Inc), 18: Audio Interchange File Format [.AIFF] (Apple Computer Inc), 19: RIFF Wave (Microsoft Corporation), 20: Freehand (Macromedia/Aldus), 21: Hypertext Markup Language [.HTML] (The Internet Society), 22: MPEG 2 Audio Layer 2 (Musicom), ISO/IEC, 23: MPEG 2 Audio Layer 3, ISO/IEC, 24: Portable Document File [.PDF] Adobe, 25: News Industry Text Format (NITF), 26: Tape Archive [.TAR], 27: Tidningarnas Telegrambyra NITF version (TTNITF DTD), 28: Ritzaus Bureau NITF version (RBNITF DTD), 29: Corel Draw [.CDR] |
| Repeatable? | No |
| Required? | No |
| Type | Short |

### The `application:PreviewVersion` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.PreviewVersion |
| Maximum bytes | 2 |
| Minimum bytes | 2 |
| ID | application:PreviewVersion |
| Label | – |
| Name | PreviewVersion |
| Tag ID | 201 |
| Definiton | A binary number representing the particular version of the object data preview file format specified in tag <PreviewFormat>. |
| Repeatable? | No |
| Required? | No |
| Type | Short |

### The `application:PreviewData` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.PreviewData |
| Maximum bytes | 256000 |
| Minimum bytes | 0 |
| ID | application:PreviewData |
| Label | – |
| Name | PreviewData |
| Tag ID | 202 |
| Definiton | Binary image preview data. |
| Repeatable? | No |
| Required? | No |
| Type | Bytes |

### The `application:Prefs` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.Prefs |
| Maximum bytes | 64 |
| Minimum bytes | 0 |
| ID | application:Prefs |
| Label | – |
| Name | Prefs |
| Tag ID | 221 |
| Definiton | PhotoMechanic Preferences. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:ClassifyState` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.ClassifyState |
| Maximum bytes | 64 |
| Minimum bytes | 0 |
| ID | application:ClassifyState |
| Label | – |
| Name | ClassifyState |
| Tag ID | 225 |
| Definiton | Classify State. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:SimilarityIndex` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.SimilarityIndex |
| Maximum bytes | 32 |
| Minimum bytes | 0 |
| ID | application:SimilarityIndex |
| Label | – |
| Name | SimilarityIndex |
| Tag ID | 228 |
| Definiton | Similarity Index. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:DocumentNotes` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.DocumentNotes |
| Maximum bytes | 1024 |
| Minimum bytes | 0 |
| ID | application:DocumentNotes |
| Label | – |
| Name | DocumentNotes |
| Tag ID | 230 |
| Definiton | Document Notes. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:DocumentHistory` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.DocumentHistory |
| Maximum bytes | 256 |
| Minimum bytes | 0 |
| ID | application:DocumentHistory |
| Label | – |
| Name | DocumentHistory |
| Tag ID | 231 |
| Definiton | Document History. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:EXIFCameraInfo` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.EXIFCameraInfo |
| Maximum bytes | 4096 |
| Minimum bytes | 0 |
| ID | application:EXIFCameraInfo |
| Label | – |
| Name | EXIFCameraInfo |
| Tag ID | 232 |
| Definiton | EXIF Camera Info. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `application:CatalogSets` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.app.CatalogSets |
| Maximum bytes | 256 |
| Minimum bytes | 0 |
| ID | application:CatalogSets |
| Label | – |
| Name | CatalogSets |
| Tag ID | 255 |
| Definiton | Catalog Sets. |
| Repeatable? | No |
| Required? | No |
| Type | String |

The IPTC metadata model's 'News Photo Tags' namespace offers 26 fields which are detailed below:

### The `newsPhoto:Version` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.news.Version |
| Maximum bytes | 2 |
| Minimum bytes | 2 |
| ID | newsPhoto:Version |
| Label | Version |
| Name | Version |
| Tag ID | 0 |
| Definiton | Version. |
| Repeatable? | No |
| Required? | No |
| Type | Short |

### The `newsPhoto:IPTCPictureNumber` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.news.IPTCPictureNumber |
| Maximum bytes | 16 |
| Minimum bytes | 16 |
| ID | newsPhoto:IPTCPictureNumber |
| Label | IPTC Picture Number |
| Name | IPTCPictureNumber |
| Tag ID | 10 |
| Definiton | IPTC Picture Number. |
| Repeatable? | No |
| Required? | No |
| Type | String |

### The `newsPhoto:IPTCImageWidth` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.news.IPTCImageWidth |
| Maximum bytes | 2 |
| Minimum bytes | 2 |
| ID | newsPhoto:IPTCImageWidth |
| Label | IPTC Image Width |
| Name | IPTCImageWidth |
| Tag ID | 20 |
| Definiton | IPTC Image Width. |
| Repeatable? | No |
| Required? | No |
| Type | Short |

### The `newsPhoto:IPTCImageHeight` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.news.IPTCImageHeight |
| Maximum bytes | 2 |
| Minimum bytes | 2 |
| ID | newsPhoto:IPTCImageHeight |
| Label | IPTC Image Height |
| Name | IPTCImageHeight |
| Tag ID | 30 |
| Definiton | IPTC Image Height. |
| Repeatable? | No |
| Required? | No |
| Type | Short |

### The `newsPhoto:IPTCPixelWidth` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.news.IPTCPixelWidth |
| Maximum bytes | 2 |
| Minimum bytes | 2 |
| ID | newsPhoto:IPTCPixelWidth |
| Label | IPTC Pixel Width |
| Name | IPTCPixelWidth |
| Tag ID | 40 |
| Definiton | IPTC Pixel Width. |
| Repeatable? | No |
| Required? | No |
| Type | Short |

### The `newsPhoto:IPTCPixelHeight` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.news.IPTCPixelHeight |
| Maximum bytes | 2 |
| Minimum bytes | 2 |
| ID | newsPhoto:IPTCPixelHeight |
| Label | IPTC Pixel Height |
| Name | IPTCPixelHeight |
| Tag ID | 50 |
| Definiton | IPTC Pixel Height. |
| Repeatable? | No |
| Required? | No |
| Type | Short |

### The `newsPhoto:SupplementalType` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.news.SupplementalType |
| Maximum bytes | 1 |
| Minimum bytes | 1 |
| ID | newsPhoto:SupplementalType |
| Label | Supplemental Type |
| Name | SupplementalType |
| Tag ID | 55 |
| Definiton | Supplemental Type. |
| Options | 0: Main Image, 1: Reduced Resolution Image, 2: Logo, 3: Rasterized Caption |
| Repeatable? | No |
| Required? | No |
| Type | UInt8 |

### The `newsPhoto:ColorRepresentation` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.news.ColorRepresentation |
| Maximum bytes | 2 |
| Minimum bytes | 2 |
| ID | newsPhoto:ColorRepresentation |
| Label | Color Representation |
| Name | ColorRepresentation |
| Tag ID | 60 |
| Definiton | Color Representation. |
| Options | 0x000: No Image, Single Frame, 0x100: Monochrome, Single Frame, 0x300: 3 Components, Single Frame, 0x301: 3 Components, Frame Sequential in Multiple Objects, 0x302: 3 Components, Frame Sequential in One Object, 0x303: 3 Components, Line Sequential, 0x304: 3 Components, Pixel Sequential, 0x305: 3 Components, Special Interleaving, 0x400: 4 Components, Single Frame, 0x401: 4 Components, Frame Sequential in Multiple Objects, 0x402: 4 Components, Frame Sequential in One Object, 0x403: 4 Components, Line Sequential, 0x404: 4 Components, Pixel Sequential, 0x405: 4 Components, Special Interleaving |
| Repeatable? | No |
| Required? | No |
| Type | Short |

### The `newsPhoto:InterchangeColorSpace` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.news.InterchangeColorSpace |
| Maximum bytes | 1 |
| Minimum bytes | 1 |
| ID | newsPhoto:InterchangeColorSpace |
| Label | Interchange Color Space |
| Name | InterchangeColorSpace |
| Tag ID | 64 |
| Definiton | Interchange Color Space. |
| Options | 1: X,Y,Z CIE, 2: RGB SMPTE, 3: Y,U,V (K) (D65), 4: RGB Device Dependent, 5: CMY (K) Device Dependent, 6: Lab (K) CIE, 7: YCbCr, 8: sRGB |
| Repeatable? | No |
| Required? | No |
| Type | UInt8 |

### The `newsPhoto:ColorSequence` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.news.ColorSequence |
| Maximum bytes | 1 |
| Minimum bytes | 1 |
| ID | newsPhoto:ColorSequence |
| Label | Color Sequence |
| Name | ColorSequence |
| Tag ID | 65 |
| Definiton | Color Sequence. |
| Repeatable? | No |
| Required? | No |
| Type | UInt8 |

### The `newsPhoto:ICCProfile` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.news.ICCProfile |
| Maximum bytes | – |
| Minimum bytes | – |
| ID | newsPhoto:ICCProfile |
| Label | ICC Profile |
| Name | ICCProfile |
| Tag ID | 66 |
| Definiton | ICC Profile. |
| Read Only? | Yes |
| Repeatable? | No |
| Required? | No |
| Type | Undefined |

### The `newsPhoto:ColorCalibrationMatrix` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.news.ColorCalibrationMatrix |
| Maximum bytes | – |
| Minimum bytes | – |
| ID | newsPhoto:ColorCalibrationMatrix |
| Label | Color Calibration Matrix |
| Name | ColorCalibrationMatrix |
| Tag ID | 70 |
| Definiton | Color Calibration Matrix. |
| Read Only? | Yes |
| Repeatable? | No |
| Required? | No |
| Type | Undefined |

### The `newsPhoto:LookupTable` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.news.LookupTable |
| Maximum bytes | – |
| Minimum bytes | – |
| ID | newsPhoto:LookupTable |
| Label | Lookup Table |
| Name | LookupTable |
| Tag ID | 80 |
| Definiton | Lookup Table. |
| Read Only? | Yes |
| Repeatable? | No |
| Required? | No |
| Type | Undefined |

### The `newsPhoto:NumIndexEntries` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.news.NumIndexEntries |
| Maximum bytes | 2 |
| Minimum bytes | 2 |
| ID | newsPhoto:NumIndexEntries |
| Label | Number of Index Entries |
| Name | NumIndexEntries |
| Tag ID | 84 |
| Definiton | Number of Index Entries. |
| Repeatable? | No |
| Required? | No |
| Type | Short |

### The `newsPhoto:ColorPalette` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.news.ColorPalette |
| Maximum bytes | – |
| Minimum bytes | – |
| ID | newsPhoto:ColorPalette |
| Label | Color Palette |
| Name | ColorPalette |
| Tag ID | 85 |
| Definiton | Color Palette. |
| Repeatable? | No |
| Required? | No |
| Type | Undefined |

### The `newsPhoto:IPTCBitsPerSample` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.news.IPTCBitsPerSample |
| Maximum bytes | 1 |
| Minimum bytes | 1 |
| ID | newsPhoto:IPTCBitsPerSample |
| Label | IPTC Bits Per Sample |
| Name | IPTCBitsPerSample |
| Tag ID | 86 |
| Definiton | IPTC Bits Per Sample. |
| Repeatable? | No |
| Required? | No |
| Type | UInt8 |

### The `newsPhoto:SampleStructure` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.news.SampleStructure |
| Maximum bytes | 1 |
| Minimum bytes | 1 |
| ID | newsPhoto:SampleStructure |
| Label | Sample Structure |
| Name | SampleStructure |
| Tag ID | 90 |
| Definiton | Sample Structure. |
| Options | 0: OrthogonalConstangSampling, 1: Orthogonal4-2-2Sampling, 2: CompressionDependent |
| Repeatable? | No |
| Required? | No |
| Type | UInt8 |

### The `newsPhoto:ScanningDirection` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.news.ScanningDirection |
| Maximum bytes | 1 |
| Minimum bytes | 1 |
| ID | newsPhoto:ScanningDirection |
| Label | Scanning Direction |
| Name | ScanningDirection |
| Tag ID | 100 |
| Definiton | Scanning Direction. |
| Options | 0: Left-Right, Top-Bottom, 1: Right-Left, Top-Bottom, 2: Left-Right, Bottom-Top, 3: Right-Left, Bottom-Top, 4: Top-Bottom, Left-Right, 5: Bottom-Top, Left-Right, 6: Top-Bottom, Right-Left, 7: Bottom-Top, Right-Left |
| Repeatable? | No |
| Required? | No |
| Type | UInt8 |

### The `newsPhoto:IPTCImageRotation` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.news.IPTCImageRotation |
| Maximum bytes | 1 |
| Minimum bytes | 1 |
| ID | newsPhoto:IPTCImageRotation |
| Label | IPTC Image Rotation |
| Name | IPTCImageRotation |
| Tag ID | 102 |
| Definiton | IPTC Image Rotation. |
| Options | 0: 0, 1: 90, 2: 180, 3: 270 |
| Repeatable? | No |
| Required? | No |
| Type | UInt8 |

### The `newsPhoto:DataCompressionMethod` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.news.DataCompressionMethod |
| Maximum bytes | 4 |
| Minimum bytes | 4 |
| ID | newsPhoto:DataCompressionMethod |
| Label | Data Compression Method |
| Name | DataCompressionMethod |
| Tag ID | 110 |
| Definiton | Data Compression Method. |
| Repeatable? | No |
| Required? | No |
| Type | Long |

### The `newsPhoto:QuantizationMethod` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.news.QuantizationMethod |
| Maximum bytes | 1 |
| Minimum bytes | 1 |
| ID | newsPhoto:QuantizationMethod |
| Label | Quantization Method |
| Name | QuantizationMethod |
| Tag ID | 120 |
| Definiton | Quantization Method. |
| Options | 0: Linear Reflectance/Transmittance, 1: Linear Density, 2: IPTC Ref B, 3: Linear Dot Percent, 4: AP Domestic Analogue, 5: Compression Method Specific, 6: Color Space Specific, 7: Gamma Compensated |
| Repeatable? | No |
| Required? | No |
| Type | UInt8 |

### The `newsPhoto:EndPoints` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.news.EndPoints |
| Maximum bytes | – |
| Minimum bytes | – |
| ID | newsPhoto:EndPoints |
| Label | End Points |
| Name | EndPoints |
| Tag ID | 125 |
| Definiton | End Points. |
| Read Only? | Yes |
| Repeatable? | No |
| Required? | No |
| Type | Undefined |

### The `newsPhoto:ExcursionTolerance` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.news.ExcursionTolerance |
| Maximum bytes | 1 |
| Minimum bytes | 1 |
| ID | newsPhoto:ExcursionTolerance |
| Label | Excursion Tolerance |
| Name | ExcursionTolerance |
| Tag ID | 125 |
| Definiton | Excursion Tolerance. |
| Options | 0: Not Allowed, 1: Allowed |
| Repeatable? | No |
| Required? | No |
| Type | UInt8 |

### The `newsPhoto:BitsPerComponent` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.news.BitsPerComponent |
| Maximum bytes | 1 |
| Minimum bytes | 1 |
| ID | newsPhoto:BitsPerComponent |
| Label | Bits Per Component |
| Name | BitsPerComponent |
| Tag ID | 135 |
| Definiton | Bits Per Component. |
| Repeatable? | No |
| Required? | No |
| Type | UInt8 |

### The `newsPhoto:MaximumDensityRange` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.news.MaximumDensityRange |
| Maximum bytes | 2 |
| Minimum bytes | 2 |
| ID | newsPhoto:MaximumDensityRange |
| Label | Maximum Density Range |
| Name | MaximumDensityRange |
| Tag ID | 140 |
| Definiton | Maximum Density Range. |
| Repeatable? | No |
| Required? | No |
| Type | UInt16 |

### The `newsPhoto:GammaCompensatedValue` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.news.GammaCompensatedValue |
| Maximum bytes | 2 |
| Minimum bytes | 2 |
| ID | newsPhoto:GammaCompensatedValue |
| Label | Gamma Compensated Value |
| Name | GammaCompensatedValue |
| Tag ID | 145 |
| Definiton | Gamma Compensated Value. |
| Repeatable? | No |
| Required? | No |
| Type | UInt16 |

The IPTC metadata model's 'Pre Object Data Tags' namespace offers four fields which are detailed below:

### The `preObjectData:SizeMode` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.pre.SizeMode |
| Maximum bytes | – |
| Minimum bytes | – |
| ID | preObjectData:SizeMode |
| Label | Size Mode |
| Name | SizeMode |
| Tag ID | 10 |
| Definiton | Size Mode. |
| Read Only? | Yes |
| Repeatable? | No |
| Required? | No |
| Type | Undefined |

### The `preObjectData:MaxSubfileSize` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.pre.MaxSubfileSize |
| Maximum bytes | – |
| Minimum bytes | – |
| ID | preObjectData:MaxSubfileSize |
| Label | Max Subfile Size |
| Name | MaxSubfileSize |
| Tag ID | 20 |
| Definiton | Max Subfile Size. |
| Read Only? | Yes |
| Repeatable? | No |
| Required? | No |
| Type | Undefined |

### The `preObjectData:ObjectSizeAnnounced` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.pre.ObjectSizeAnnounced |
| Maximum bytes | – |
| Minimum bytes | – |
| ID | preObjectData:ObjectSizeAnnounced |
| Label | Object Size Announced |
| Name | ObjectSizeAnnounced |
| Tag ID | 90 |
| Definiton | Object Size Announced. |
| Read Only? | Yes |
| Repeatable? | No |
| Required? | No |
| Type | Undefined |

### The `preObjectData:MaximumObjectSize` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.pre.MaximumObjectSize |
| Maximum bytes | – |
| Minimum bytes | – |
| ID | preObjectData:MaximumObjectSize |
| Label | Maximum Object Size |
| Name | MaximumObjectSize |
| Tag ID | 95 |
| Definiton | Maximum Object Size. |
| Read Only? | Yes |
| Repeatable? | No |
| Required? | No |
| Type | Undefined |

The IPTC metadata model's 'Object Data Tags' namespace offers one field which are detailed below:

### The `objectData:SubFile` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.object.SubFile |
| Maximum bytes | – |
| Minimum bytes | – |
| ID | objectData:SubFile |
| Label | Sub File |
| Name | SubFile |
| Tag ID | 10 |
| Definiton | Sub File. |
| Read Only? | Yes |
| Repeatable? | No |
| Required? | No |
| Type | Undefined |

The IPTC metadata model's 'Post Object Data Tags' namespace offers one field which are detailed below:

### The `postObjectData:ConfirmedObjectSize` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | iptc.post.ConfirmedObjectSize |
| Maximum bytes | – |
| Minimum bytes | – |
| ID | postObjectData:ConfirmedObjectSize |
| Label | Confirmed Object Size |
| Name | ConfirmedObjectSize |
| Tag ID | 10 |
| Definiton | Confirmed Object Size. |
| Read Only? | Yes |
| Repeatable? | No |
| Required? | No |
| Type | Undefined |

The IPTC metadata model's 'FotoStation Tags' namespace offers zero fields which are detailed below:

