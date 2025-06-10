# EXIFData: The EXIF Metadata Model

The EXIF (Exchangeable Image File Format) metadata model is a standard that specifies
formats for images, sound, and ancillary tags used by digital cameras and smartphones.
It allows metadata to be embedded directly within image files, including JPEG, TIFF and
HEIF image file formats, providing information about the image and the capturing device.

The key elements of metadata supported by the EXIF metadata model include:

* Technical Image Metadata Fields: These include image dimensions (width and height),
image orientation (landscape, portrait, square), color space and compression settings.

* Camera Information Fields: These include the make and model of the camera; lens
information; and exposure settings, including shutter speed, ISO, and aperture.

* Image Capture Information Fields: These include the date and time of capture; light
metering mode; flash status; white balance; and geolocation data if GPS was available
and enabled during capture, providing latitude, longitude, altitude and the timestamp.

* Thumbnail Field: This field can optionally include a small preview of the image, that
is embedded into the EXIF metadata to support quick previewing of the associated image.

* Interoperability Fields: These include fields used by and often customized to other
standards and applications, and may require the use of the relevant hardware or software
to work with these fields as many are not documented.

### EXIF Metadata Structure

EXIF metadata is stored using the TIFF file structure with Image File Directories (IFDs)
that contain tagged data entries organized in a hierarchical manner:

* IFD0 (the "0th" IFD) is the first IFD in an EXIF file and contains the main image data
including resolution, color space, and other essential image attributes. It also stores
EXIF metadata like camera and lens information and settings, as well as date, and time.

* IFD1 (The "1st" IFD) is often used to store information about a thumbnail image, which
is a smaller version of the main image, and it's included to allow faster previews. All
tags from IFD0 may also be present in IFD1.

* IFD2, while less common, can exist to store additional image data or information
about related images, such as linked images or other image formats.

EXIF metadata is organized into a hierarchy of IFDs, with tags storing the actual data
values. The structure typical of EXIF-compatible image file formats is as follows:

```
Image File (e.g., JPEG, TIFF, HEIF, etc)
    └── APP1 Marker (EXIF Header)
        └── TIFF Header (Byte Alignment Information)
            ├── 0th IFD (Main Image Tags)
            │   ├── EXIF IFD Pointer → EXIF SubIFD (Camera Settings)
            |   ├──── Tag: Camera Make
            |   ├──── Tag: Camera Model
            |   ├──── Tag: Lens Make
            |   ├──── Tag: Lens Model
            |   ├──── ...
            │   ├── GPS IFD Pointer → GPS SubIFD (Location Data; Optional)
            |   ├──── GPS Latitude
            |   ├──── GPS Longitude
            |   ├──── GPS Altitude
            |   ├──── ...
            │   └── Interoperability IFD Pointer (Optional)
            └── 1st IFD (Thumbnail Image)
```

All IFDs comprise the following components:

| Section       | Length   | Description                                               |
|---------------|----------|-----------------------------------------------------------|
| Tag Count     | 2 bytes  | Holds the count of tags that follow                       |
| Tags          | See note | Holds one or more byte-encoded IFD Tags, of 12 bytes each |
| Next Offset   | 4 bytes  | Holds the pointer to the next IFD or 0 if no IFD follows  |

* The tag count is stored as a short integer (`UInt16`) comprised of 2 bytes or 16 bits
* The tags are encoded according to the format specified for IFD Tag as detailed below
* The tags section holds one or more byte-encoded IFD Tag values, the length of which
can be determined by multiplying the tag count by 12
* The next offset is stored as a long integer (`UInt32`) comprised of 4 bytes or 32 bits

Each IFD Tag comprises of the following components, consisting of 12 bytes:

| Tag ID        | Two bytes holding the tag ID                                    |
|---------------|-----------------------------------------------------------------|
| Data Type     | Two bytes holding the data type indicator, from those below:    |
| Data Count    | Four bytes holding the count of data values that follow         |
| Data / Offset | Four bytes holding the data or a pointer to the data            |

The IFD Tag data types are as follows:

| Type Indicator | Data Type       | Description                                      |
|----------------|-----------------|--------------------------------------------------|
| `0`            | Empty           | An empty value                                   |
| `1`            | Byte            | 8-bit unsigned integer                           |
| `2`            | ASCII           | 8-bits holding 7-bit ASCII code, null-terminated |
| `3`            | Short           | 16-bit signed integer                            |
| `4`            | Long            | 32-bit signed integer                            |
| `5`            | Rational        | Two long integers for numerator and denominator  |
| `7`            | Undefined       | 8-bit byte holding any value per field specs     |
| `9`            | Signed Long     | 32-bit signed integer (2's compliment)           |
| `10`           | Signed Rational | A signed rational of two signed long integers    |
| `129`          | UTF-8           | 8-bit byte UTF-8 string, null-terminated         |

### EXIF Metadata Model Namespaces & Fields

The EXIFData library provides support for reading and writing from the following EXIF
fields unless marked otherwise:

{{fields}}

#### Credits & References

The EXIF field information was researched from various sources including from the EXIF
specification and EXIFTool documentation. Please visit these valuable online resources
to learn more about the EXIF metadata model specification and to support these world
class organizations and their products:

 * https://www.cipa.jp/e/index.html
 * https://www.loc.gov/preservation/digital/formats/fdd/fdd000146.shtml
 * https://exiftool.org/TagNames/EXIF.html
 * https://www.media.mit.edu/pia/Research/deepview/exif.html
 * https://exiv2.org/tags.html
