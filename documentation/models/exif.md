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

The EXIF metadata model has one namespace which is documented below.

The EXIF metadata model's 'exif' namespace offers 135 fields which are detailed below:

### The `exif:EXIFIFDPointer` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.EXIFIFDPointer |
| ID | exif:EXIFIFDPointer |
| Label | – |
| Name | EXIFIFDPointer |
| Tag ID | 34665 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | EXIF IDF pointer. |
| Citaton | 8769.H |
| Type | Long |

### The `exif:GPSInfoIFDPointer` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GPSInfoIFDPointer |
| ID | exif:GPSInfoIFDPointer |
| Label | – |
| Name | GPSInfoIFDPointer |
| Tag ID | 34853 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | GPS Info IDF pointer. |
| Citaton | 8825.H |
| Type | Long |

### The `exif:InteroperabilityIFDPointer` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.InteroperabilityIFDPointer |
| ID | exif:InteroperabilityIFDPointer |
| Label | – |
| Name | InteroperabilityIFDPointer |
| Tag ID | 40965 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Interoperability IDF pointer. |
| Citaton | A005.H |
| Type | Long |

### The `exif:ImageWidth` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.ImageWidth |
| ID | exif:ImageWidth |
| Label | – |
| Name | ImageWidth |
| Tag ID | 256 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Image width. |
| Citaton | – |
| Type | Short, Long |

### The `exif:ImageHeight` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.ImageHeight |
| ID | exif:ImageHeight |
| Label | – |
| Name | ImageHeight |
| Tag ID | 257 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Image height. |
| Citaton | – |
| Type | Short, Long |

### The `exif:BitsPerSample` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.BitsPerSample |
| ID | exif:BitsPerSample |
| Label | – |
| Name | BitsPerSample |
| Tag ID | 258 |
| Count/Length | 3 |
| Default Value | – |
| Definiton | Number of bits per component. |
| Citaton | – |
| Type | Short |

### The `exif:Compression` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.Compression |
| ID | exif:Compression |
| Label | – |
| Name | Compression |
| Tag ID | 259 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Compression scheme. |
| Citaton | – |
| Type | Short |

### The `exif:PhotometricInterpretation` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.PhotometricInterpretation |
| ID | exif:PhotometricInterpretation |
| Label | – |
| Name | PhotometricInterpretation |
| Tag ID | 262 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Pixel composition. |
| Citaton | – |
| Type | Short |

### The `exif:Orientation` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.Orientation |
| ID | exif:Orientation |
| Label | – |
| Name | Orientation |
| Tag ID | 274 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Orientation of image. |
| Citaton | – |
| Type | Short |

### The `exif:SamplesPerPixel` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.SamplesPerPixel |
| ID | exif:SamplesPerPixel |
| Label | – |
| Name | SamplesPerPixel |
| Tag ID | 277 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Number of components. |
| Citaton | – |
| Type | Short |

### The `exif:PlanarConfiguration` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.PlanarConfiguration |
| ID | exif:PlanarConfiguration |
| Label | – |
| Name | PlanarConfiguration |
| Tag ID | 284 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Image data arrangement. |
| Citaton | – |
| Type | Short |

### The `exif:YCbCrSubSampling` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.YCbCrSubSampling |
| ID | exif:YCbCrSubSampling |
| Label | – |
| Name | YCbCrSubSampling |
| Tag ID | 530 |
| Count/Length | 2 |
| Default Value | – |
| Definiton | Subsampling ratio of Y to C. |
| Citaton | – |
| Type | Short |

### The `exif:YCbCrPositioning` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.YCbCrPositioning |
| ID | exif:YCbCrPositioning |
| Label | – |
| Name | YCbCrPositioning |
| Tag ID | 531 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Y and C positioning. |
| Citaton | – |
| Type | Short |

### The `exif:XResolution` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.XResolution |
| ID | exif:XResolution |
| Label | – |
| Name | XResolution |
| Tag ID | 282 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Image resolution in width direction. |
| Citaton | – |
| Type | Rational |

### The `exif:YResolution` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.YResolution |
| ID | exif:YResolution |
| Label | – |
| Name | YResolution |
| Tag ID | 283 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Image resolution in height direction. |
| Citaton | – |
| Type | Rational |

### The `exif:ResolutionUnit` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.ResolutionUnit |
| ID | exif:ResolutionUnit |
| Label | – |
| Name | ResolutionUnit |
| Tag ID | 296 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Unit of X and Y resolution. |
| Citaton | – |
| Type | Short |

### The `exif:PageNumber` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.PageNumber |
| ID | exif:PageNumber |
| Label | – |
| Name | PageNumber |
| Tag ID | 297 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | The page number of the page from which this image was scanned. |
| Citaton | – |
| Type | Short |

### The `exif:StripOffsets` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.StripOffsets |
| ID | exif:StripOffsets |
| Label | – |
| Name | StripOffsets |
| Tag ID | 273 |
| Count/Length | -1 |
| Default Value | – |
| Definiton | Image data location. |
| Citaton | – |
| Type | Short, Long |

### The `exif:RowsPerStrip` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.RowsPerStrip |
| ID | exif:RowsPerStrip |
| Label | – |
| Name | RowsPerStrip |
| Tag ID | 278 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Number of rows per strip. |
| Citaton | – |
| Type | Short, Long |

### The `exif:StripByteCounts` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.StripByteCounts |
| ID | exif:StripByteCounts |
| Label | – |
| Name | StripByteCounts |
| Tag ID | 279 |
| Count/Length | -1 |
| Default Value | – |
| Definiton | Bytes per compressed strip. |
| Citaton | – |
| Type | Short, Long |

### The `exif:JPEGInterchangeFormat` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.JPEGInterchangeFormat |
| ID | exif:JPEGInterchangeFormat |
| Label | – |
| Name | JPEGInterchangeFormat |
| Tag ID | 513 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Offset to JPEG SOI. |
| Citaton | – |
| Type | Long |

### The `exif:JPEGInterchangeFormatLength` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.JPEGInterchangeFormatLength |
| ID | exif:JPEGInterchangeFormatLength |
| Label | – |
| Name | JPEGInterchangeFormatLength |
| Tag ID | 514 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Bytes of JPEG data. |
| Citaton | – |
| Type | Long |

### The `exif:TransferFunction` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.TransferFunction |
| ID | exif:TransferFunction |
| Label | – |
| Name | TransferFunction |
| Tag ID | 301 |
| Count/Length | -2 |
| Default Value | – |
| Definiton | Transfer function. |
| Citaton | – |
| Type | Short |

### The `exif:WhitePoint` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.WhitePoint |
| ID | exif:WhitePoint |
| Label | – |
| Name | WhitePoint |
| Tag ID | 318 |
| Count/Length | 2 |
| Default Value | – |
| Definiton | White point chromaticity. |
| Citaton | – |
| Type | Rational |

### The `exif:PrimaryChromaticities` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.PrimaryChromaticities |
| ID | exif:PrimaryChromaticities |
| Label | – |
| Name | PrimaryChromaticities |
| Tag ID | 319 |
| Count/Length | 6 |
| Default Value | – |
| Definiton | Chromaticities of primaries. |
| Citaton | – |
| Type | Rational |

### The `exif:YCbCrCoefficients` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.YCbCrCoefficients |
| ID | exif:YCbCrCoefficients |
| Label | – |
| Name | YCbCrCoefficients |
| Tag ID | 529 |
| Count/Length | 3 |
| Default Value | – |
| Definiton | Color space transformation matrix coefficients. |
| Citaton | – |
| Type | Rational |

### The `exif:ReferenceBlackWhite` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.ReferenceBlackWhite |
| ID | exif:ReferenceBlackWhite |
| Label | – |
| Name | ReferenceBlackWhite |
| Tag ID | 532 |
| Count/Length | 6 |
| Default Value | – |
| Definiton | Pair of black and white reference values. |
| Citaton | – |
| Type | Rational |

### The `exif:DateTime` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.DateTime |
| ID | exif:DateTime |
| Label | – |
| Name | DateTime |
| Tag ID | 306 |
| Count/Length | 20 |
| Default Value | – |
| Definiton | File change date and time. |
| Citaton | – |
| Type | ASCII |

### The `exif:ImageDescription` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.ImageDescription |
| ID | exif:ImageDescription |
| Label | – |
| Name | ImageDescription |
| Tag ID | 270 |
| Alias | Description |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Image title. |
| Pseudonym | exifdata: dc:Title |
| Citaton | – |
| Type | ASCII |

### The `exif:Make` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.Make |
| ID | exif:Make |
| Label | – |
| Name | Make |
| Tag ID | 271 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Image input equipment manufacturer. |
| Citaton | – |
| Type | ASCII |

### The `exif:Model` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.Model |
| ID | exif:Model |
| Label | – |
| Name | Model |
| Tag ID | 272 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Image input equipment model. |
| Citaton | – |
| Type | ASCII |

### The `exif:Software` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.Software |
| ID | exif:Software |
| Label | – |
| Name | Software |
| Tag ID | 305 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Software used. |
| Citaton | – |
| Type | ASCII |

### The `exif:Artist` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.Artist |
| ID | exif:Artist |
| Label | – |
| Name | Artist |
| Tag ID | 315 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Person who created the image. |
| Citaton | – |
| Type | ASCII |

### The `exif:Copyright` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.Copyright |
| ID | exif:Copyright |
| Label | – |
| Name | Copyright |
| Tag ID | 33432 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Copyright holder. |
| Citaton | – |
| Type | ASCII |

### The `exif:EXIFVersion` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.EXIFVersion |
| ID | exif:EXIFVersion |
| Label | – |
| Name | EXIFVersion |
| Tag ID | 36864 |
| Count/Length | 4 |
| Default Value | – |
| Definiton | EXIF version. |
| Citaton | – |
| Type | Undefined |

### The `exif:FlashpixVersion` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.FlashpixVersion |
| ID | exif:FlashpixVersion |
| Label | – |
| Name | FlashpixVersion |
| Tag ID | 40960 |
| Count/Length | 4 |
| Default Value | – |
| Definiton | Supported Flashpix version. |
| Citaton | – |
| Type | Undefined |

### The `exif:ColorSpace` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.ColorSpace |
| ID | exif:ColorSpace |
| Label | – |
| Name | ColorSpace |
| Tag ID | 40961 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Color space information. |
| Citaton | – |
| Type | Short |

### The `exif:Gamma` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.Gamma |
| ID | exif:Gamma |
| Label | – |
| Name | Gamma |
| Tag ID | 42240 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Gamma. |
| Citaton | – |
| Type | Rational |

### The `exif:ComponentsConfiguration` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.ComponentsConfiguration |
| ID | exif:ComponentsConfiguration |
| Label | – |
| Name | ComponentsConfiguration |
| Tag ID | 37121 |
| Count/Length | 4 |
| Default Value | – |
| Definiton | Meaning of each component. |
| Citaton | – |
| Type | Undefined |

### The `exif:CompressedBitsPerPixel` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.CompressedBitsPerPixel |
| ID | exif:CompressedBitsPerPixel |
| Label | – |
| Name | CompressedBitsPerPixel |
| Tag ID | 37122 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Image compression mode. |
| Citaton | – |
| Type | Rational |

### The `exif:PixelXDimension` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.PixelXDimension |
| ID | exif:PixelXDimension |
| Label | – |
| Name | PixelXDimension |
| Tag ID | 40962 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Valid image width. |
| Citaton | – |
| Type | Short, Long |

### The `exif:PixelYDimension` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.PixelYDimension |
| ID | exif:PixelYDimension |
| Label | – |
| Name | PixelYDimension |
| Tag ID | 40963 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Valid image height. |
| Citaton | – |
| Type | Short, Long |

### The `exif:MakerNote` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.MakerNote |
| ID | exif:MakerNote |
| Label | – |
| Name | MakerNote |
| Tag ID | 37500 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Manufacturer notes. |
| Citaton | – |
| Type | Undefined |

### The `exif:UserComment` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.UserComment |
| ID | exif:UserComment |
| Label | – |
| Name | UserComment |
| Tag ID | 37510 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | User comments. |
| Citaton | – |
| Type | Undefined |

### The `exif:RelatedSoundFile` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.RelatedSoundFile |
| ID | exif:RelatedSoundFile |
| Label | – |
| Name | RelatedSoundFile |
| Tag ID | 40964 |
| Count/Length | 13 |
| Default Value | – |
| Definiton | Related audio file. |
| Citaton | – |
| Type | ASCII |

### The `exif:DateTimeOriginal` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.DateTimeOriginal |
| ID | exif:DateTimeOriginal |
| Label | – |
| Name | DateTimeOriginal |
| Tag ID | 36867 |
| Count/Length | 20 |
| Default Value | – |
| Definiton | Date and time of original data generation. |
| Citaton | – |
| Type | ASCII |

### The `exif:DateTimeDigitized` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.DateTimeDigitized |
| ID | exif:DateTimeDigitized |
| Label | – |
| Name | DateTimeDigitized |
| Tag ID | 36868 |
| Count/Length | 20 |
| Default Value | – |
| Definiton | Date and time of digital data generation. |
| Citaton | – |
| Type | ASCII |

### The `exif:SubSecTime` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.SubSecTime |
| ID | exif:SubSecTime |
| Label | – |
| Name | SubSecTime |
| Tag ID | 37520 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | File change date and time sub-seconds. |
| Citaton | – |
| Type | ASCII |

### The `exif:SubSecTimeOriginal` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.SubSecTimeOriginal |
| ID | exif:SubSecTimeOriginal |
| Label | – |
| Name | SubSecTimeOriginal |
| Tag ID | 37521 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Date and time of original data generation sub-seconds. |
| Citaton | – |
| Type | ASCII |

### The `exif:SubSecTimeDigitized` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.SubSecTimeDigitized |
| ID | exif:SubSecTimeDigitized |
| Label | – |
| Name | SubSecTimeDigitized |
| Tag ID | 37522 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Date and time of digital data generation sub-seconds. |
| Citaton | – |
| Type | ASCII |

### The `exif:ExposureTime` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.ExposureTime |
| ID | exif:ExposureTime |
| Label | – |
| Name | ExposureTime |
| Tag ID | 33434 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Exposure time. |
| Citaton | – |
| Type | Rational |

### The `exif:FNumber` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.FNumber |
| ID | exif:FNumber |
| Label | – |
| Name | FNumber |
| Tag ID | 33437 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | F number. |
| Citaton | – |
| Type | Rational |

### The `exif:ExposureProgram` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.ExposureProgram |
| ID | exif:ExposureProgram |
| Label | – |
| Name | ExposureProgram |
| Tag ID | 34850 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Exposure program. |
| Citaton | – |
| Type | Short |

### The `exif:SpectralSensitivity` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.SpectralSensitivity |
| ID | exif:SpectralSensitivity |
| Label | – |
| Name | SpectralSensitivity |
| Tag ID | 34852 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Spectral sensitivity. |
| Citaton | – |
| Type | ASCII |

### The `exif:PhotographicSensitivity` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.PhotographicSensitivity |
| ID | exif:PhotographicSensitivity |
| Label | – |
| Name | PhotographicSensitivity |
| Tag ID | 34855 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Photographic sensitivity. |
| Citaton | – |
| Type | Short |

### The `exif:OptoElectricConversionFactor` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.OptoElectricConversionFactor |
| ID | exif:OptoElectricConversionFactor |
| Label | – |
| Name | OptoElectricConversionFactor |
| Tag ID | 34856 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Opto-electric conversion factor. |
| Citaton | – |
| Type | Undefined |

### The `exif:SensitivityType` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.SensitivityType |
| ID | exif:SensitivityType |
| Label | – |
| Name | SensitivityType |
| Tag ID | 34864 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Sensitivity type. |
| Citaton | – |
| Type | Short |

### The `exif:StandardOutputSensitivity` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.StandardOutputSensitivity |
| ID | exif:StandardOutputSensitivity |
| Label | – |
| Name | StandardOutputSensitivity |
| Tag ID | 34865 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Standard output sensitivity. |
| Citaton | – |
| Type | Long |

### The `exif:RecommendedExposureIndex` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.RecommendedExposureIndex |
| ID | exif:RecommendedExposureIndex |
| Label | – |
| Name | RecommendedExposureIndex |
| Tag ID | 34866 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Recommended exposure index. |
| Citaton | – |
| Type | Long |

### The `exif:ISOSpeed` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.ISOSpeed |
| ID | exif:ISOSpeed |
| Label | – |
| Name | ISOSpeed |
| Tag ID | 34867 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | ISO speed. |
| Citaton | – |
| Type | Long |

### The `exif:ISOSpeedLatitudeYYY` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.ISOSpeedLatitudeYYY |
| ID | exif:ISOSpeedLatitudeYYY |
| Label | – |
| Name | ISOSpeedLatitudeYYY |
| Tag ID | 34868 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | ISO speed latitude YYY. |
| Citaton | – |
| Type | Long |

### The `exif:ISOSpeedLatitudeZZZ` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.ISOSpeedLatitudeZZZ |
| ID | exif:ISOSpeedLatitudeZZZ |
| Label | – |
| Name | ISOSpeedLatitudeZZZ |
| Tag ID | 34869 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | ISO speed latitude ZZZ. |
| Citaton | – |
| Type | Long |

### The `exif:ShutterSpeedValue` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.ShutterSpeedValue |
| ID | exif:ShutterSpeedValue |
| Label | – |
| Name | ShutterSpeedValue |
| Tag ID | 37377 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Shutter speed. |
| Citaton | – |
| Type | RationalSigned |

### The `exif:ApertureValue` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.ApertureValue |
| ID | exif:ApertureValue |
| Label | – |
| Name | ApertureValue |
| Tag ID | 37378 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Aperture. |
| Citaton | – |
| Type | Rational |

### The `exif:BrightnessValue` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.BrightnessValue |
| ID | exif:BrightnessValue |
| Label | – |
| Name | BrightnessValue |
| Tag ID | 37379 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Brightness. |
| Citaton | – |
| Type | RationalSigned |

### The `exif:ExposureBiasValue` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.ExposureBiasValue |
| ID | exif:ExposureBiasValue |
| Label | – |
| Name | ExposureBiasValue |
| Tag ID | 37380 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Exposure bias. |
| Citaton | – |
| Type | RationalSigned |

### The `exif:MaxApertureValue` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.MaxApertureValue |
| ID | exif:MaxApertureValue |
| Label | – |
| Name | MaxApertureValue |
| Tag ID | 37381 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Maximum lens aperture. |
| Citaton | – |
| Type | Rational |

### The `exif:SubjectDistance` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.SubjectDistance |
| ID | exif:SubjectDistance |
| Label | – |
| Name | SubjectDistance |
| Tag ID | 37382 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Subject distance. |
| Citaton | – |
| Type | Rational |

### The `exif:MeteringMode` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.MeteringMode |
| ID | exif:MeteringMode |
| Label | – |
| Name | MeteringMode |
| Tag ID | 37383 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Metering mode. |
| Citaton | – |
| Type | Short |

### The `exif:LightSource` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.LightSource |
| ID | exif:LightSource |
| Label | – |
| Name | LightSource |
| Tag ID | 37384 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Light source. |
| Citaton | – |
| Type | Short |

### The `exif:Flash` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.Flash |
| ID | exif:Flash |
| Label | – |
| Name | Flash |
| Tag ID | 37385 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Flash. |
| Citaton | – |
| Type | Short |

### The `exif:FocalLength` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.FocalLength |
| ID | exif:FocalLength |
| Label | – |
| Name | FocalLength |
| Tag ID | 37386 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Lens focal length. |
| Citaton | – |
| Type | Rational |

### The `exif:SubjectArea` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.SubjectArea |
| ID | exif:SubjectArea |
| Label | – |
| Name | SubjectArea |
| Tag ID | 37396 |
| Count/Length | 2, 3, 4 |
| Default Value | – |
| Definiton | Subject area. |
| Citaton | – |
| Type | Short |

### The `exif:FlashEnergy` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.FlashEnergy |
| ID | exif:FlashEnergy |
| Label | – |
| Name | FlashEnergy |
| Tag ID | 41483 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Flash energy. |
| Citaton | – |
| Type | Rational |

### The `exif:SpatialFrequencyResponse` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.SpatialFrequencyResponse |
| ID | exif:SpatialFrequencyResponse |
| Label | – |
| Name | SpatialFrequencyResponse |
| Tag ID | 41484 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Spatial frequency response. |
| Citaton | – |
| Type | Undefined |

### The `exif:FocalPlaneXResolution` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.FocalPlaneXResolution |
| ID | exif:FocalPlaneXResolution |
| Label | – |
| Name | FocalPlaneXResolution |
| Tag ID | 41486 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Focal plane X resolution. |
| Citaton | – |
| Type | Rational |

### The `exif:FocalPlaneYResolution` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.FocalPlaneYResolution |
| ID | exif:FocalPlaneYResolution |
| Label | – |
| Name | FocalPlaneYResolution |
| Tag ID | 41487 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Focal plane Y resolution. |
| Citaton | – |
| Type | Rational |

### The `exif:FocalPlaneResolutionUnit` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.FocalPlaneResolutionUnit |
| ID | exif:FocalPlaneResolutionUnit |
| Label | – |
| Name | FocalPlaneResolutionUnit |
| Tag ID | 41488 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Focal plane resolution unit. |
| Citaton | – |
| Type | Short |

### The `exif:SubjectLocation` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.SubjectLocation |
| ID | exif:SubjectLocation |
| Label | – |
| Name | SubjectLocation |
| Tag ID | 41492 |
| Count/Length | 2 |
| Default Value | – |
| Definiton | Subject location. |
| Citaton | – |
| Type | Short |

### The `exif:ExposureIndex` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.ExposureIndex |
| ID | exif:ExposureIndex |
| Label | – |
| Name | ExposureIndex |
| Tag ID | 41493 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Exposure index. |
| Citaton | – |
| Type | Rational |

### The `exif:SensingMethod` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.SensingMethod |
| ID | exif:SensingMethod |
| Label | – |
| Name | SensingMethod |
| Tag ID | 41495 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Sensing method. |
| Citaton | – |
| Type | Short |

### The `exif:FileSource` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.FileSource |
| ID | exif:FileSource |
| Label | – |
| Name | FileSource |
| Tag ID | 41728 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | File source. |
| Citaton | – |
| Type | Undefined |

### The `exif:SceneType` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.SceneType |
| ID | exif:SceneType |
| Label | – |
| Name | SceneType |
| Tag ID | 41729 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Scene type. |
| Citaton | – |
| Type | Undefined |

### The `exif:CFAPattern` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.CFAPattern |
| ID | exif:CFAPattern |
| Label | – |
| Name | CFAPattern |
| Tag ID | 41730 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | CFA pattern. |
| Citaton | – |
| Type | Undefined |

### The `exif:CustomRendered` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.CustomRendered |
| ID | exif:CustomRendered |
| Label | – |
| Name | CustomRendered |
| Tag ID | 41985 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Custom image processing. |
| Citaton | – |
| Type | Short |

### The `exif:ExposureMode` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.ExposureMode |
| ID | exif:ExposureMode |
| Label | – |
| Name | ExposureMode |
| Tag ID | 41986 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Exposure mode. |
| Citaton | – |
| Type | Short |

### The `exif:WhiteBalance` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.WhiteBalance |
| ID | exif:WhiteBalance |
| Label | – |
| Name | WhiteBalance |
| Tag ID | 41987 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | White balance. |
| Citaton | – |
| Type | Short |

### The `exif:DigitalZoomRatio` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.DigitalZoomRatio |
| ID | exif:DigitalZoomRatio |
| Label | – |
| Name | DigitalZoomRatio |
| Tag ID | 41988 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Digital zoom ratio. |
| Citaton | – |
| Type | Rational |

### The `exif:FocalLength35mmFilm` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.FocalLength35mmFilm |
| ID | exif:FocalLength35mmFilm |
| Label | – |
| Name | FocalLength35mmFilm |
| Tag ID | 41989 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Focal length in 35mm film. |
| Citaton | – |
| Type | Short |

### The `exif:SceneCaptureType` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.SceneCaptureType |
| ID | exif:SceneCaptureType |
| Label | – |
| Name | SceneCaptureType |
| Tag ID | 41990 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Scene capture type. |
| Citaton | – |
| Type | Short |

### The `exif:GainControl` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GainControl |
| ID | exif:GainControl |
| Label | – |
| Name | GainControl |
| Tag ID | 41991 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Gain control. |
| Citaton | – |
| Type | Rational |

### The `exif:Contrast` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.Contrast |
| ID | exif:Contrast |
| Label | – |
| Name | Contrast |
| Tag ID | 41992 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Contrast. |
| Citaton | – |
| Type | Short |

### The `exif:Saturation` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.Saturation |
| ID | exif:Saturation |
| Label | – |
| Name | Saturation |
| Tag ID | 41993 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Saturation. |
| Citaton | – |
| Type | Short |

### The `exif:Sharpness` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.Sharpness |
| ID | exif:Sharpness |
| Label | – |
| Name | Sharpness |
| Tag ID | 41964 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Sharpness. |
| Citaton | – |
| Type | Short |

### The `exif:DeviceSettingDescription` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.DeviceSettingDescription |
| ID | exif:DeviceSettingDescription |
| Label | – |
| Name | DeviceSettingDescription |
| Tag ID | 41995 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Device setting description. |
| Citaton | – |
| Type | Undefined |

### The `exif:SubjectDistanceRange` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.SubjectDistanceRange |
| ID | exif:SubjectDistanceRange |
| Label | – |
| Name | SubjectDistanceRange |
| Tag ID | 41996 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Subject distance range. |
| Citaton | – |
| Type | Short |

### The `exif:ImageUniqueID` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.ImageUniqueID |
| ID | exif:ImageUniqueID |
| Label | – |
| Name | ImageUniqueID |
| Tag ID | 42016 |
| Count/Length | 33 |
| Default Value | – |
| Definiton | Unique image ID. |
| Citaton | – |
| Type | ASCII |

### The `exif:CameraOwnerName` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.CameraOwnerName |
| ID | exif:CameraOwnerName |
| Label | – |
| Name | CameraOwnerName |
| Tag ID | 42032 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Camera owner name. |
| Citaton | – |
| Type | ASCII |

### The `exif:BodySerialNumber` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.BodySerialNumber |
| ID | exif:BodySerialNumber |
| Label | – |
| Name | BodySerialNumber |
| Tag ID | 42033 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Camera body serial number. |
| Citaton | – |
| Type | ASCII |

### The `exif:LensSpecification` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.LensSpecification |
| ID | exif:LensSpecification |
| Label | – |
| Name | LensSpecification |
| Tag ID | 42034 |
| Count/Length | 4 |
| Default Value | – |
| Definiton | Lens specification. |
| Citaton | – |
| Type | Rational |

### The `exif:LensMake` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.LensMake |
| ID | exif:LensMake |
| Label | – |
| Name | LensMake |
| Tag ID | 42035 |
| Count/Length | 4 |
| Default Value | – |
| Definiton | Lens make. |
| Citaton | – |
| Type | Rational |

### The `exif:LensModel` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.LensModel |
| ID | exif:LensModel |
| Label | – |
| Name | LensModel |
| Tag ID | 42036 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Lens model. |
| Citaton | – |
| Type | ASCII |

### The `exif:LensSerialNumber` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.LensSerialNumber |
| ID | exif:LensSerialNumber |
| Label | – |
| Name | LensSerialNumber |
| Tag ID | 42037 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Lens serial number. |
| Citaton | – |
| Type | ASCII |

### The `exif:GPSVersionID` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GPSVersionID |
| ID | exif:GPSVersionID |
| Label | – |
| Name | GPSVersionID |
| Tag ID | 0 |
| Count/Length | 4 |
| Default Value | – |
| Definiton | GPS tag version. |
| Citaton | – |
| Type | Byte |

### The `exif:GPSLatitudeRef` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GPSLatitudeRef |
| ID | exif:GPSLatitudeRef |
| Label | – |
| Name | GPSLatitudeRef |
| Tag ID | 1 |
| Count/Length | 2 |
| Default Value | – |
| Definiton | GPS north or south latitude. |
| Citaton | – |
| Type | ASCII |

### The `exif:GPSLatitude` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GPSLatitude |
| ID | exif:GPSLatitude |
| Label | – |
| Name | GPSLatitude |
| Tag ID | 2 |
| Count/Length | 3 |
| Default Value | – |
| Definiton | GPS latitude. |
| Citaton | – |
| Type | Rational |

### The `exif:GPSLongitudeRef` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GPSLongitudeRef |
| ID | exif:GPSLongitudeRef |
| Label | – |
| Name | GPSLongitudeRef |
| Tag ID | 3 |
| Count/Length | 2 |
| Default Value | – |
| Definiton | GPS east or west longitude. |
| Citaton | – |
| Type | ASCII |

### The `exif:GPSLongitude` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GPSLongitude |
| ID | exif:GPSLongitude |
| Label | – |
| Name | GPSLongitude |
| Tag ID | 4 |
| Count/Length | 3 |
| Default Value | – |
| Definiton | GPS longitude. |
| Citaton | – |
| Type | Rational |

### The `exif:GPSAltitudeRef` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GPSAltitudeRef |
| ID | exif:GPSAltitudeRef |
| Label | – |
| Name | GPSAltitudeRef |
| Tag ID | 5 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | GPS altitude reference. |
| Citaton | – |
| Type | Byte |

### The `exif:GPSAltitude` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GPSAltitude |
| ID | exif:GPSAltitude |
| Label | – |
| Name | GPSAltitude |
| Tag ID | 6 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | GPS altitude. |
| Citaton | – |
| Type | Rational |

### The `exif:GPSTimeStamp` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GPSTimeStamp |
| ID | exif:GPSTimeStamp |
| Label | – |
| Name | GPSTimeStamp |
| Tag ID | 7 |
| Count/Length | 3 |
| Default Value | – |
| Definiton | GPS time (atomic clock). |
| Citaton | – |
| Type | Rational |

### The `exif:GPSSatellites` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GPSSatellites |
| ID | exif:GPSSatellites |
| Label | – |
| Name | GPSSatellites |
| Tag ID | 8 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | GPS satellites used for measurement. |
| Citaton | – |
| Type | ASCII |

### The `exif:GPSStatus` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GPSStatus |
| ID | exif:GPSStatus |
| Label | – |
| Name | GPSStatus |
| Tag ID | 9 |
| Count/Length | 2 |
| Default Value | – |
| Definiton | GPS receiver status. |
| Citaton | – |
| Type | ASCII |

### The `exif:GPSMeasureMode` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GPSMeasureMode |
| ID | exif:GPSMeasureMode |
| Label | – |
| Name | GPSMeasureMode |
| Tag ID | 10 |
| Count/Length | 2 |
| Default Value | – |
| Definiton | GPS measurement mode. |
| Citaton | – |
| Type | ASCII |

### The `exif:GPSDOP` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GPSDOP |
| ID | exif:GPSDOP |
| Label | – |
| Name | GPSDOP |
| Tag ID | 11 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | GPS measurement precision. |
| Citaton | – |
| Type | Rational |

### The `exif:GPSSpeedRef` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GPSSpeedRef |
| ID | exif:GPSSpeedRef |
| Label | – |
| Name | GPSSpeedRef |
| Tag ID | 12 |
| Count/Length | 2 |
| Default Value | – |
| Definiton | GPS speed unit. |
| Citaton | – |
| Type | ASCII |

### The `exif:GPSSpeed` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GPSSpeed |
| ID | exif:GPSSpeed |
| Label | – |
| Name | GPSSpeed |
| Tag ID | 13 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Speed of GPS receiver. |
| Citaton | – |
| Type | Rational |

### The `exif:GPSTrackRef` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GPSTrackRef |
| ID | exif:GPSTrackRef |
| Label | – |
| Name | GPSTrackRef |
| Tag ID | 14 |
| Count/Length | 2 |
| Default Value | – |
| Definiton | GPS reference for direction of movement. |
| Citaton | – |
| Type | ASCII |

### The `exif:GPSTrack` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GPSTrack |
| ID | exif:GPSTrack |
| Label | – |
| Name | GPSTrack |
| Tag ID | 15 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | GPS direction of movement. |
| Citaton | – |
| Type | Rational |

### The `exif:GPSImgDirectionRef` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GPSImgDirectionRef |
| ID | exif:GPSImgDirectionRef |
| Label | – |
| Name | GPSImgDirectionRef |
| Tag ID | 16 |
| Count/Length | 2 |
| Default Value | – |
| Definiton | GPS reference for direction of image. |
| Citaton | – |
| Type | ASCII |

### The `exif:GPSImgDirection` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GPSImgDirection |
| ID | exif:GPSImgDirection |
| Label | – |
| Name | GPSImgDirection |
| Tag ID | 17 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | GPS direction of image. |
| Citaton | – |
| Type | Rational |

### The `exif:GPSMapDatum` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GPSMapDatum |
| ID | exif:GPSMapDatum |
| Label | – |
| Name | GPSMapDatum |
| Tag ID | 18 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | GPS geodetic survey data used. |
| Citaton | – |
| Type | ASCII |

### The `exif:GPSDestLatitudeRef` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GPSDestLatitudeRef |
| ID | exif:GPSDestLatitudeRef |
| Label | – |
| Name | GPSDestLatitudeRef |
| Tag ID | 19 |
| Count/Length | 2 |
| Default Value | – |
| Definiton | GPS reference for latitude of destination. |
| Citaton | – |
| Type | ASCII |

### The `exif:GPSDestLatitude` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GPSDestLatitude |
| ID | exif:GPSDestLatitude |
| Label | – |
| Name | GPSDestLatitude |
| Tag ID | 20 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | GPS latitude of destination. |
| Citaton | – |
| Type | Rational |

### The `exif:GPSDestLongitudeRef` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GPSDestLongitudeRef |
| ID | exif:GPSDestLongitudeRef |
| Label | – |
| Name | GPSDestLongitudeRef |
| Tag ID | 21 |
| Count/Length | 2 |
| Default Value | – |
| Definiton | GPS reference for longitude of destination. |
| Citaton | – |
| Type | ASCII |

### The `exif:GPSDestLongitude` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GPSDestLongitude |
| ID | exif:GPSDestLongitude |
| Label | – |
| Name | GPSDestLongitude |
| Tag ID | 22 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | GPS longitude of destination. |
| Citaton | – |
| Type | Rational |

### The `exif:GPSDestBearingRef` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GPSDestBearingRef |
| ID | exif:GPSDestBearingRef |
| Label | – |
| Name | GPSDestBearingRef |
| Tag ID | 23 |
| Count/Length | 2 |
| Default Value | – |
| Definiton | GPS reference for bearing of destination. |
| Citaton | – |
| Type | ASCII |

### The `exif:GPSDestBearing` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GPSDestBearing |
| ID | exif:GPSDestBearing |
| Label | – |
| Name | GPSDestBearing |
| Tag ID | 24 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | GPS bearing of destination. |
| Citaton | – |
| Type | Rational |

### The `exif:GPSDestDistanceRef` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GPSDestDistanceRef |
| ID | exif:GPSDestDistanceRef |
| Label | – |
| Name | GPSDestDistanceRef |
| Tag ID | 25 |
| Count/Length | 2 |
| Default Value | – |
| Definiton | GPS reference for distance of destination. |
| Citaton | – |
| Type | ASCII |

### The `exif:GPSDestDistance` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GPSDestDistance |
| ID | exif:GPSDestDistance |
| Label | – |
| Name | GPSDestDistance |
| Tag ID | 26 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | GPS distance of destination. |
| Citaton | – |
| Type | Rational |

### The `exif:GPSProcessingMethod` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GPSProcessingMethod |
| ID | exif:GPSProcessingMethod |
| Label | – |
| Name | GPSProcessingMethod |
| Tag ID | 27 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Name of GPS processing method. |
| Citaton | – |
| Type | Undefined |

### The `exif:GPSAreaInformation` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GPSAreaInformation |
| ID | exif:GPSAreaInformation |
| Label | – |
| Name | GPSAreaInformation |
| Tag ID | 28 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Name of GPS area. |
| Citaton | – |
| Type | Undefined |

### The `exif:GPSDateStamp` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GPSDateStamp |
| ID | exif:GPSDateStamp |
| Label | – |
| Name | GPSDateStamp |
| Tag ID | 29 |
| Count/Length | 11 |
| Default Value | – |
| Definiton | GPS date. |
| Citaton | – |
| Type | ASCII |

### The `exif:GPSDifferential` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GPSDifferential |
| ID | exif:GPSDifferential |
| Label | – |
| Name | GPSDifferential |
| Tag ID | 30 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | GPS differential correction. |
| Citaton | – |
| Type | Short |

### The `exif:GPSHPositioningError` field has the following configuration:

| Attribute | Value  |
|-----------|--------|
| Path      | exif.GPSHPositioningError |
| ID | exif:GPSHPositioningError |
| Label | – |
| Name | GPSHPositioningError |
| Tag ID | 31 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | GPS horizontal positioning error. |
| Citaton | – |
| Type | Rational |

