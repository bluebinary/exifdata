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
well as via XMP. To work with IPTC metadata using the IPTC-IIM model, use the `IPTC`
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

{{fields}}

### Credits & References

The IPTC field information was researched from various sources including from the IPTC
specification and EXIFTool documentation. Please visit these valuable online resources
to learn more about the IPTC metadata model specification and to support these world
class organizations and their products:

 * https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata
 * https://exiftool.org/TagNames/IPTC.html
