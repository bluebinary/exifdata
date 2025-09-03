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

The EXIFData library provides support for writing EXIF metadata model fields. The model provides one namespace.

The EXIF metadata model's `exif` namespace offers 145 fields which are listed below along with a link to each field's technical information:

| Namespace  | Field Path | Field Name | Required? | Info |
|------------|------------|------------|:---------:|------|
| `exif` | `exif.EXIFIFDPointer` | EXIFIFDPointer | No | [🔗](#exif-exif-exififdpointer) |
| `exif` | `exif.GPSInfoIFDPointer` | GPSInfoIFDPointer | No | [🔗](#exif-exif-gpsinfoifdpointer) |
| `exif` | `exif.InteroperabilityIFDPointer` | InteroperabilityIFDPointer | No | [🔗](#exif-exif-interoperabilityifdpointer) |
| `exif` | `exif.ImageWidth` | ImageWidth | No | [🔗](#exif-exif-imagewidth) |
| `exif` | `exif.ImageHeight` | ImageHeight | No | [🔗](#exif-exif-imageheight) |
| `exif` | `exif.BitsPerSample` | BitsPerSample | No | [🔗](#exif-exif-bitspersample) |
| `exif` | `exif.Compression` | Compression | No | [🔗](#exif-exif-compression) |
| `exif` | `exif.PhotometricInterpretation` | PhotometricInterpretation | No | [🔗](#exif-exif-photometricinterpretation) |
| `exif` | `exif.Orientation` | Orientation | No | [🔗](#exif-exif-orientation) |
| `exif` | `exif.SamplesPerPixel` | SamplesPerPixel | No | [🔗](#exif-exif-samplesperpixel) |
| `exif` | `exif.PlanarConfiguration` | PlanarConfiguration | No | [🔗](#exif-exif-planarconfiguration) |
| `exif` | `exif.YCbCrSubSampling` | YCbCrSubSampling | No | [🔗](#exif-exif-ycbcrsubsampling) |
| `exif` | `exif.YCbCrPositioning` | YCbCrPositioning | No | [🔗](#exif-exif-ycbcrpositioning) |
| `exif` | `exif.XResolution` | XResolution | No | [🔗](#exif-exif-xresolution) |
| `exif` | `exif.YResolution` | YResolution | No | [🔗](#exif-exif-yresolution) |
| `exif` | `exif.ResolutionUnit` | ResolutionUnit | No | [🔗](#exif-exif-resolutionunit) |
| `exif` | `exif.PageNumber` | PageNumber | No | [🔗](#exif-exif-pagenumber) |
| `exif` | `exif.StripOffsets` | StripOffsets | No | [🔗](#exif-exif-stripoffsets) |
| `exif` | `exif.RowsPerStrip` | RowsPerStrip | No | [🔗](#exif-exif-rowsperstrip) |
| `exif` | `exif.StripByteCounts` | StripByteCounts | No | [🔗](#exif-exif-stripbytecounts) |
| `exif` | `exif.JPEGInterchangeFormat` | JPEGInterchangeFormat | No | [🔗](#exif-exif-jpeginterchangeformat) |
| `exif` | `exif.JPEGInterchangeFormatLength` | JPEGInterchangeFormatLength | No | [🔗](#exif-exif-jpeginterchangeformatlength) |
| `exif` | `exif.TransferFunction` | TransferFunction | No | [🔗](#exif-exif-transferfunction) |
| `exif` | `exif.WhitePoint` | WhitePoint | No | [🔗](#exif-exif-whitepoint) |
| `exif` | `exif.PrimaryChromaticities` | PrimaryChromaticities | No | [🔗](#exif-exif-primarychromaticities) |
| `exif` | `exif.YCbCrCoefficients` | YCbCrCoefficients | No | [🔗](#exif-exif-ycbcrcoefficients) |
| `exif` | `exif.ReferenceBlackWhite` | ReferenceBlackWhite | No | [🔗](#exif-exif-referenceblackwhite) |
| `exif` | `exif.DateTime` | DateTime | No | [🔗](#exif-exif-datetime) |
| `exif` | `exif.ImageDescription` | ImageDescription | No | [🔗](#exif-exif-imagedescription) |
| `exif` | `exif.Make` | Make | No | [🔗](#exif-exif-make) |
| `exif` | `exif.Model` | Model | No | [🔗](#exif-exif-model) |
| `exif` | `exif.Software` | Software | No | [🔗](#exif-exif-software) |
| `exif` | `exif.Artist` | Artist | No | [🔗](#exif-exif-artist) |
| `exif` | `exif.Copyright` | Copyright | No | [🔗](#exif-exif-copyright) |
| `exif` | `exif.EXIFVersion` | EXIFVersion | No | [🔗](#exif-exif-exifversion) |
| `exif` | `exif.FlashpixVersion` | FlashpixVersion | No | [🔗](#exif-exif-flashpixversion) |
| `exif` | `exif.ColorSpace` | ColorSpace | No | [🔗](#exif-exif-colorspace) |
| `exif` | `exif.Gamma` | Gamma | No | [🔗](#exif-exif-gamma) |
| `exif` | `exif.ComponentsConfiguration` | ComponentsConfiguration | No | [🔗](#exif-exif-componentsconfiguration) |
| `exif` | `exif.CompressedBitsPerPixel` | CompressedBitsPerPixel | No | [🔗](#exif-exif-compressedbitsperpixel) |
| `exif` | `exif.PixelXDimension` | PixelXDimension | No | [🔗](#exif-exif-pixelxdimension) |
| `exif` | `exif.PixelYDimension` | PixelYDimension | No | [🔗](#exif-exif-pixelydimension) |
| `exif` | `exif.MakerNote` | MakerNote | No | [🔗](#exif-exif-makernote) |
| `exif` | `exif.UserComment` | UserComment | No | [🔗](#exif-exif-usercomment) |
| `exif` | `exif.RelatedSoundFile` | RelatedSoundFile | No | [🔗](#exif-exif-relatedsoundfile) |
| `exif` | `exif.DateTimeOriginal` | DateTimeOriginal | No | [🔗](#exif-exif-datetimeoriginal) |
| `exif` | `exif.DateTimeDigitized` | DateTimeDigitized | No | [🔗](#exif-exif-datetimedigitized) |
| `exif` | `exif.SubSecTime` | SubSecTime | No | [🔗](#exif-exif-subsectime) |
| `exif` | `exif.SubSecTimeOriginal` | SubSecTimeOriginal | No | [🔗](#exif-exif-subsectimeoriginal) |
| `exif` | `exif.SubSecTimeDigitized` | SubSecTimeDigitized | No | [🔗](#exif-exif-subsectimedigitized) |
| `exif` | `exif.ExposureTime` | ExposureTime | No | [🔗](#exif-exif-exposuretime) |
| `exif` | `exif.FNumber` | FNumber | No | [🔗](#exif-exif-fnumber) |
| `exif` | `exif.ExposureProgram` | ExposureProgram | No | [🔗](#exif-exif-exposureprogram) |
| `exif` | `exif.SpectralSensitivity` | SpectralSensitivity | No | [🔗](#exif-exif-spectralsensitivity) |
| `exif` | `exif.PhotographicSensitivity` | PhotographicSensitivity | No | [🔗](#exif-exif-photographicsensitivity) |
| `exif` | `exif.OptoElectricConversionFactor` | OptoElectricConversionFactor | No | [🔗](#exif-exif-optoelectricconversionfactor) |
| `exif` | `exif.SensitivityType` | SensitivityType | No | [🔗](#exif-exif-sensitivitytype) |
| `exif` | `exif.StandardOutputSensitivity` | StandardOutputSensitivity | No | [🔗](#exif-exif-standardoutputsensitivity) |
| `exif` | `exif.RecommendedExposureIndex` | RecommendedExposureIndex | No | [🔗](#exif-exif-recommendedexposureindex) |
| `exif` | `exif.ISOSpeed` | ISOSpeed | No | [🔗](#exif-exif-isospeed) |
| `exif` | `exif.ISOSpeedLatitudeYYY` | ISOSpeedLatitudeYYY | No | [🔗](#exif-exif-isospeedlatitudeyyy) |
| `exif` | `exif.ISOSpeedLatitudeZZZ` | ISOSpeedLatitudeZZZ | No | [🔗](#exif-exif-isospeedlatitudezzz) |
| `exif` | `exif.ShutterSpeedValue` | ShutterSpeedValue | No | [🔗](#exif-exif-shutterspeedvalue) |
| `exif` | `exif.ApertureValue` | ApertureValue | No | [🔗](#exif-exif-aperturevalue) |
| `exif` | `exif.BrightnessValue` | BrightnessValue | No | [🔗](#exif-exif-brightnessvalue) |
| `exif` | `exif.ExposureBiasValue` | ExposureBiasValue | No | [🔗](#exif-exif-exposurebiasvalue) |
| `exif` | `exif.MaxApertureValue` | MaxApertureValue | No | [🔗](#exif-exif-maxaperturevalue) |
| `exif` | `exif.SubjectDistance` | SubjectDistance | No | [🔗](#exif-exif-subjectdistance) |
| `exif` | `exif.MeteringMode` | MeteringMode | No | [🔗](#exif-exif-meteringmode) |
| `exif` | `exif.LightSource` | LightSource | No | [🔗](#exif-exif-lightsource) |
| `exif` | `exif.Flash` | Flash | No | [🔗](#exif-exif-flash) |
| `exif` | `exif.FocalLength` | FocalLength | No | [🔗](#exif-exif-focallength) |
| `exif` | `exif.SubjectArea` | SubjectArea | No | [🔗](#exif-exif-subjectarea) |
| `exif` | `exif.FlashEnergy` | FlashEnergy | No | [🔗](#exif-exif-flashenergy) |
| `exif` | `exif.SpatialFrequencyResponse` | SpatialFrequencyResponse | No | [🔗](#exif-exif-spatialfrequencyresponse) |
| `exif` | `exif.FocalPlaneXResolution` | FocalPlaneXResolution | No | [🔗](#exif-exif-focalplanexresolution) |
| `exif` | `exif.FocalPlaneYResolution` | FocalPlaneYResolution | No | [🔗](#exif-exif-focalplaneyresolution) |
| `exif` | `exif.FocalPlaneResolutionUnit` | FocalPlaneResolutionUnit | No | [🔗](#exif-exif-focalplaneresolutionunit) |
| `exif` | `exif.SubjectLocation` | SubjectLocation | No | [🔗](#exif-exif-subjectlocation) |
| `exif` | `exif.ExposureIndex` | ExposureIndex | No | [🔗](#exif-exif-exposureindex) |
| `exif` | `exif.SensingMethod` | SensingMethod | No | [🔗](#exif-exif-sensingmethod) |
| `exif` | `exif.FileSource` | FileSource | No | [🔗](#exif-exif-filesource) |
| `exif` | `exif.SceneType` | SceneType | No | [🔗](#exif-exif-scenetype) |
| `exif` | `exif.CFAPattern` | CFAPattern | No | [🔗](#exif-exif-cfapattern) |
| `exif` | `exif.CustomRendered` | CustomRendered | No | [🔗](#exif-exif-customrendered) |
| `exif` | `exif.ExposureMode` | ExposureMode | No | [🔗](#exif-exif-exposuremode) |
| `exif` | `exif.WhiteBalance` | WhiteBalance | No | [🔗](#exif-exif-whitebalance) |
| `exif` | `exif.DigitalZoomRatio` | DigitalZoomRatio | No | [🔗](#exif-exif-digitalzoomratio) |
| `exif` | `exif.FocalLength35mmFilm` | FocalLength35mmFilm | No | [🔗](#exif-exif-focallength35mmfilm) |
| `exif` | `exif.SceneCaptureType` | SceneCaptureType | No | [🔗](#exif-exif-scenecapturetype) |
| `exif` | `exif.GainControl` | GainControl | No | [🔗](#exif-exif-gaincontrol) |
| `exif` | `exif.Contrast` | Contrast | No | [🔗](#exif-exif-contrast) |
| `exif` | `exif.Saturation` | Saturation | No | [🔗](#exif-exif-saturation) |
| `exif` | `exif.Sharpness` | Sharpness | No | [🔗](#exif-exif-sharpness) |
| `exif` | `exif.DeviceSettingDescription` | DeviceSettingDescription | No | [🔗](#exif-exif-devicesettingdescription) |
| `exif` | `exif.SubjectDistanceRange` | SubjectDistanceRange | No | [🔗](#exif-exif-subjectdistancerange) |
| `exif` | `exif.ImageUniqueID` | ImageUniqueID | No | [🔗](#exif-exif-imageuniqueid) |
| `exif` | `exif.CameraOwnerName` | CameraOwnerName | No | [🔗](#exif-exif-cameraownername) |
| `exif` | `exif.BodySerialNumber` | BodySerialNumber | No | [🔗](#exif-exif-bodyserialnumber) |
| `exif` | `exif.LensSpecification` | LensSpecification | No | [🔗](#exif-exif-lensspecification) |
| `exif` | `exif.LensMake` | LensMake | No | [🔗](#exif-exif-lensmake) |
| `exif` | `exif.LensModel` | LensModel | No | [🔗](#exif-exif-lensmodel) |
| `exif` | `exif.LensSerialNumber` | LensSerialNumber | No | [🔗](#exif-exif-lensserialnumber) |
| `exif` | `exif.ImageTitle` | ImageTitle | No | [🔗](#exif-exif-imagetitle) |
| `exif` | `exif.Photographer` | Photographer | No | [🔗](#exif-exif-photographer) |
| `exif` | `exif.ImageEditor` | ImageEditor | No | [🔗](#exif-exif-imageeditor) |
| `exif` | `exif.CameraFirmware` | CameraFirmware | No | [🔗](#exif-exif-camerafirmware) |
| `exif` | `exif.RAWDevelopingSoftware` | RAWDevelopingSoftware | No | [🔗](#exif-exif-rawdevelopingsoftware) |
| `exif` | `exif.ImageEditingSoftware` | ImageEditingSoftware | No | [🔗](#exif-exif-imageeditingsoftware) |
| `exif` | `exif.MetadataEditingSoftware` | MetadataEditingSoftware | No | [🔗](#exif-exif-metadataeditingsoftware) |
| `exif` | `exif.CompositeImage` | CompositeImage | No | [🔗](#exif-exif-compositeimage) |
| `exif` | `exif.SourceImageNumberOfCompositeImage` | SourceImageNumberOfCompositeImage | No | [🔗](#exif-exif-sourceimagenumberofcompositeimage) |
| `exif` | `exif.SourceExposureTimesOfCompositeImage` | SourceExposureTimesOfCompositeImage | No | [🔗](#exif-exif-sourceexposuretimesofcompositeimage) |
| `exif` | `exif.GPSVersionID` | GPSVersionID | No | [🔗](#exif-exif-gpsversionid) |
| `exif` | `exif.GPSLatitudeRef` | GPSLatitudeRef | No | [🔗](#exif-exif-gpslatituderef) |
| `exif` | `exif.GPSLatitude` | GPSLatitude | No | [🔗](#exif-exif-gpslatitude) |
| `exif` | `exif.GPSLongitudeRef` | GPSLongitudeRef | No | [🔗](#exif-exif-gpslongituderef) |
| `exif` | `exif.GPSLongitude` | GPSLongitude | No | [🔗](#exif-exif-gpslongitude) |
| `exif` | `exif.GPSAltitudeRef` | GPSAltitudeRef | No | [🔗](#exif-exif-gpsaltituderef) |
| `exif` | `exif.GPSAltitude` | GPSAltitude | No | [🔗](#exif-exif-gpsaltitude) |
| `exif` | `exif.GPSTimeStamp` | GPSTimeStamp | No | [🔗](#exif-exif-gpstimestamp) |
| `exif` | `exif.GPSSatellites` | GPSSatellites | No | [🔗](#exif-exif-gpssatellites) |
| `exif` | `exif.GPSStatus` | GPSStatus | No | [🔗](#exif-exif-gpsstatus) |
| `exif` | `exif.GPSMeasureMode` | GPSMeasureMode | No | [🔗](#exif-exif-gpsmeasuremode) |
| `exif` | `exif.GPSDOP` | GPSDOP | No | [🔗](#exif-exif-gpsdop) |
| `exif` | `exif.GPSSpeedRef` | GPSSpeedRef | No | [🔗](#exif-exif-gpsspeedref) |
| `exif` | `exif.GPSSpeed` | GPSSpeed | No | [🔗](#exif-exif-gpsspeed) |
| `exif` | `exif.GPSTrackRef` | GPSTrackRef | No | [🔗](#exif-exif-gpstrackref) |
| `exif` | `exif.GPSTrack` | GPSTrack | No | [🔗](#exif-exif-gpstrack) |
| `exif` | `exif.GPSImgDirectionRef` | GPSImgDirectionRef | No | [🔗](#exif-exif-gpsimgdirectionref) |
| `exif` | `exif.GPSImgDirection` | GPSImgDirection | No | [🔗](#exif-exif-gpsimgdirection) |
| `exif` | `exif.GPSMapDatum` | GPSMapDatum | No | [🔗](#exif-exif-gpsmapdatum) |
| `exif` | `exif.GPSDestLatitudeRef` | GPSDestLatitudeRef | No | [🔗](#exif-exif-gpsdestlatituderef) |
| `exif` | `exif.GPSDestLatitude` | GPSDestLatitude | No | [🔗](#exif-exif-gpsdestlatitude) |
| `exif` | `exif.GPSDestLongitudeRef` | GPSDestLongitudeRef | No | [🔗](#exif-exif-gpsdestlongituderef) |
| `exif` | `exif.GPSDestLongitude` | GPSDestLongitude | No | [🔗](#exif-exif-gpsdestlongitude) |
| `exif` | `exif.GPSDestBearingRef` | GPSDestBearingRef | No | [🔗](#exif-exif-gpsdestbearingref) |
| `exif` | `exif.GPSDestBearing` | GPSDestBearing | No | [🔗](#exif-exif-gpsdestbearing) |
| `exif` | `exif.GPSDestDistanceRef` | GPSDestDistanceRef | No | [🔗](#exif-exif-gpsdestdistanceref) |
| `exif` | `exif.GPSDestDistance` | GPSDestDistance | No | [🔗](#exif-exif-gpsdestdistance) |
| `exif` | `exif.GPSProcessingMethod` | GPSProcessingMethod | No | [🔗](#exif-exif-gpsprocessingmethod) |
| `exif` | `exif.GPSAreaInformation` | GPSAreaInformation | No | [🔗](#exif-exif-gpsareainformation) |
| `exif` | `exif.GPSDateStamp` | GPSDateStamp | No | [🔗](#exif-exif-gpsdatestamp) |
| `exif` | `exif.GPSDifferential` | GPSDifferential | No | [🔗](#exif-exif-gpsdifferential) |
| `exif` | `exif.GPSHPositioningError` | GPSHPositioningError | No | [🔗](#exif-exif-gpshpositioningerror) |

The technical details of each field may be found below:

<a id="exif-exif-exififdpointer"></a>
### The `exif:EXIFIFDPointer` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.EXIFIFDPointer` |
| ID | `exif:EXIFIFDPointer` |
| Name | EXIFIFDPointer |
| Label | – |
| Tag ID | 34665 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | EXIF IDF pointer. |
| Required? | No |
| Citaton | 8769.H |
| Type | Long |

<a id="exif-exif-gpsinfoifdpointer"></a>
### The `exif:GPSInfoIFDPointer` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GPSInfoIFDPointer` |
| ID | `exif:GPSInfoIFDPointer` |
| Name | GPSInfoIFDPointer |
| Label | – |
| Tag ID | 34853 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | GPS Info IDF pointer. |
| Required? | No |
| Citaton | 8825.H |
| Type | Long |

<a id="exif-exif-interoperabilityifdpointer"></a>
### The `exif:InteroperabilityIFDPointer` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.InteroperabilityIFDPointer` |
| ID | `exif:InteroperabilityIFDPointer` |
| Name | InteroperabilityIFDPointer |
| Label | – |
| Tag ID | 40965 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Interoperability IDF pointer. |
| Required? | No |
| Citaton | A005.H |
| Type | Long |

<a id="exif-exif-imagewidth"></a>
### The `exif:ImageWidth` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.ImageWidth` |
| ID | `exif:ImageWidth` |
| Name | ImageWidth |
| Label | – |
| Tag ID | 256 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Image width. |
| Required? | No |
| Citaton | – |
| Type | Short; Long |

<a id="exif-exif-imageheight"></a>
### The `exif:ImageHeight` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.ImageHeight` |
| ID | `exif:ImageHeight` |
| Name | ImageHeight |
| Label | – |
| Tag ID | 257 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Image height. |
| Required? | No |
| Citaton | – |
| Type | Short; Long |

<a id="exif-exif-bitspersample"></a>
### The `exif:BitsPerSample` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.BitsPerSample` |
| ID | `exif:BitsPerSample` |
| Name | BitsPerSample |
| Label | – |
| Tag ID | 258 |
| Count/Length | 3 |
| Default Value | – |
| Definiton | Number of bits per component. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-compression"></a>
### The `exif:Compression` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.Compression` |
| ID | `exif:Compression` |
| Name | Compression |
| Label | – |
| Tag ID | 259 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Compression scheme. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-photometricinterpretation"></a>
### The `exif:PhotometricInterpretation` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.PhotometricInterpretation` |
| ID | `exif:PhotometricInterpretation` |
| Name | PhotometricInterpretation |
| Label | – |
| Tag ID | 262 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Pixel composition. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-orientation"></a>
### The `exif:Orientation` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.Orientation` |
| ID | `exif:Orientation` |
| Name | Orientation |
| Label | – |
| Tag ID | 274 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Orientation of image. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-samplesperpixel"></a>
### The `exif:SamplesPerPixel` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.SamplesPerPixel` |
| ID | `exif:SamplesPerPixel` |
| Name | SamplesPerPixel |
| Label | – |
| Tag ID | 277 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Number of components. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-planarconfiguration"></a>
### The `exif:PlanarConfiguration` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.PlanarConfiguration` |
| ID | `exif:PlanarConfiguration` |
| Name | PlanarConfiguration |
| Label | – |
| Tag ID | 284 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Image data arrangement. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-ycbcrsubsampling"></a>
### The `exif:YCbCrSubSampling` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.YCbCrSubSampling` |
| ID | `exif:YCbCrSubSampling` |
| Name | YCbCrSubSampling |
| Label | – |
| Tag ID | 530 |
| Count/Length | 2 |
| Default Value | – |
| Definiton | Subsampling ratio of Y to C. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-ycbcrpositioning"></a>
### The `exif:YCbCrPositioning` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.YCbCrPositioning` |
| ID | `exif:YCbCrPositioning` |
| Name | YCbCrPositioning |
| Label | – |
| Tag ID | 531 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Y and C positioning. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-xresolution"></a>
### The `exif:XResolution` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.XResolution` |
| ID | `exif:XResolution` |
| Name | XResolution |
| Label | – |
| Tag ID | 282 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Image resolution in width direction. |
| Required? | No |
| Citaton | – |
| Type | Rational |

<a id="exif-exif-yresolution"></a>
### The `exif:YResolution` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.YResolution` |
| ID | `exif:YResolution` |
| Name | YResolution |
| Label | – |
| Tag ID | 283 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Image resolution in height direction. |
| Required? | No |
| Citaton | – |
| Type | Rational |

<a id="exif-exif-resolutionunit"></a>
### The `exif:ResolutionUnit` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.ResolutionUnit` |
| ID | `exif:ResolutionUnit` |
| Name | ResolutionUnit |
| Label | – |
| Tag ID | 296 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Unit of X and Y resolution. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-pagenumber"></a>
### The `exif:PageNumber` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.PageNumber` |
| ID | `exif:PageNumber` |
| Name | PageNumber |
| Label | – |
| Tag ID | 297 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | The page number of the page from which this image was scanned. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-stripoffsets"></a>
### The `exif:StripOffsets` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.StripOffsets` |
| ID | `exif:StripOffsets` |
| Name | StripOffsets |
| Label | – |
| Tag ID | 273 |
| Count/Length | -1 |
| Default Value | – |
| Definiton | Image data location. |
| Required? | No |
| Citaton | – |
| Type | Short; Long |

<a id="exif-exif-rowsperstrip"></a>
### The `exif:RowsPerStrip` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.RowsPerStrip` |
| ID | `exif:RowsPerStrip` |
| Name | RowsPerStrip |
| Label | – |
| Tag ID | 278 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Number of rows per strip. |
| Required? | No |
| Citaton | – |
| Type | Short; Long |

<a id="exif-exif-stripbytecounts"></a>
### The `exif:StripByteCounts` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.StripByteCounts` |
| ID | `exif:StripByteCounts` |
| Name | StripByteCounts |
| Label | – |
| Tag ID | 279 |
| Count/Length | -1 |
| Default Value | – |
| Definiton | Bytes per compressed strip. |
| Required? | No |
| Citaton | – |
| Type | Short; Long |

<a id="exif-exif-jpeginterchangeformat"></a>
### The `exif:JPEGInterchangeFormat` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.JPEGInterchangeFormat` |
| ID | `exif:JPEGInterchangeFormat` |
| Name | JPEGInterchangeFormat |
| Label | – |
| Tag ID | 513 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Offset to JPEG SOI. |
| Required? | No |
| Citaton | – |
| Type | Long |

<a id="exif-exif-jpeginterchangeformatlength"></a>
### The `exif:JPEGInterchangeFormatLength` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.JPEGInterchangeFormatLength` |
| ID | `exif:JPEGInterchangeFormatLength` |
| Name | JPEGInterchangeFormatLength |
| Label | – |
| Tag ID | 514 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Bytes of JPEG data. |
| Required? | No |
| Citaton | – |
| Type | Long |

<a id="exif-exif-transferfunction"></a>
### The `exif:TransferFunction` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.TransferFunction` |
| ID | `exif:TransferFunction` |
| Name | TransferFunction |
| Label | – |
| Tag ID | 301 |
| Count/Length | -2 |
| Default Value | – |
| Definiton | Transfer function. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-whitepoint"></a>
### The `exif:WhitePoint` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.WhitePoint` |
| ID | `exif:WhitePoint` |
| Name | WhitePoint |
| Label | – |
| Tag ID | 318 |
| Count/Length | 2 |
| Default Value | – |
| Definiton | White point chromaticity. |
| Required? | No |
| Citaton | – |
| Type | Rational |

<a id="exif-exif-primarychromaticities"></a>
### The `exif:PrimaryChromaticities` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.PrimaryChromaticities` |
| ID | `exif:PrimaryChromaticities` |
| Name | PrimaryChromaticities |
| Label | – |
| Tag ID | 319 |
| Count/Length | 6 |
| Default Value | – |
| Definiton | Chromaticities of primaries. |
| Required? | No |
| Citaton | – |
| Type | Rational |

<a id="exif-exif-ycbcrcoefficients"></a>
### The `exif:YCbCrCoefficients` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.YCbCrCoefficients` |
| ID | `exif:YCbCrCoefficients` |
| Name | YCbCrCoefficients |
| Label | – |
| Tag ID | 529 |
| Count/Length | 3 |
| Default Value | – |
| Definiton | Color space transformation matrix coefficients. |
| Required? | No |
| Citaton | – |
| Type | Rational |

<a id="exif-exif-referenceblackwhite"></a>
### The `exif:ReferenceBlackWhite` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.ReferenceBlackWhite` |
| ID | `exif:ReferenceBlackWhite` |
| Name | ReferenceBlackWhite |
| Label | – |
| Tag ID | 532 |
| Count/Length | 6 |
| Default Value | – |
| Definiton | Pair of black and white reference values. |
| Required? | No |
| Citaton | – |
| Type | Rational |

<a id="exif-exif-datetime"></a>
### The `exif:DateTime` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.DateTime` |
| ID | `exif:DateTime` |
| Name | DateTime |
| Label | – |
| Tag ID | 306 |
| Count/Length | 20 |
| Default Value | – |
| Definiton | File change date and time. |
| Required? | No |
| Citaton | – |
| Type | ASCII |

<a id="exif-exif-imagedescription"></a>
### The `exif:ImageDescription` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.ImageDescription` |
| ID | `exif:ImageDescription` |
| Name | ImageDescription |
| Label | – |
| Tag ID | 270 |
| Alias | Description |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Image description. |
| Pseudonym | exiftool: dc:Description |
| Required? | No |
| Citaton | – |
| Type | String |

<a id="exif-exif-make"></a>
### The `exif:Make` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.Make` |
| ID | `exif:Make` |
| Name | Make |
| Label | – |
| Tag ID | 271 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Image input equipment manufacturer. |
| Required? | No |
| Citaton | – |
| Type | String |

<a id="exif-exif-model"></a>
### The `exif:Model` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.Model` |
| ID | `exif:Model` |
| Name | Model |
| Label | – |
| Tag ID | 272 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Image input equipment model. |
| Required? | No |
| Citaton | – |
| Type | String |

<a id="exif-exif-software"></a>
### The `exif:Software` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.Software` |
| ID | `exif:Software` |
| Name | Software |
| Label | – |
| Tag ID | 305 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Software used. |
| Required? | No |
| Citaton | – |
| Type | String |

<a id="exif-exif-artist"></a>
### The `exif:Artist` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.Artist` |
| ID | `exif:Artist` |
| Name | Artist |
| Label | – |
| Tag ID | 315 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | The name of the person who created the image. |
| Required? | No |
| Citaton | – |
| Type | String |

<a id="exif-exif-copyright"></a>
### The `exif:Copyright` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.Copyright` |
| ID | `exif:Copyright` |
| Name | Copyright |
| Label | – |
| Tag ID | 33432 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Copyright holder. |
| Required? | No |
| Citaton | – |
| Type | String |

<a id="exif-exif-exifversion"></a>
### The `exif:EXIFVersion` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.EXIFVersion` |
| ID | `exif:EXIFVersion` |
| Name | EXIFVersion |
| Label | – |
| Tag ID | 36864 |
| Count/Length | 4 |
| Default Value | – |
| Definiton | EXIF version. |
| Required? | No |
| Citaton | – |
| Type | Undefined |

<a id="exif-exif-flashpixversion"></a>
### The `exif:FlashpixVersion` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.FlashpixVersion` |
| ID | `exif:FlashpixVersion` |
| Name | FlashpixVersion |
| Label | – |
| Tag ID | 40960 |
| Count/Length | 4 |
| Default Value | – |
| Definiton | Supported Flashpix version. |
| Required? | No |
| Citaton | – |
| Type | Undefined |

<a id="exif-exif-colorspace"></a>
### The `exif:ColorSpace` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.ColorSpace` |
| ID | `exif:ColorSpace` |
| Name | ColorSpace |
| Label | – |
| Tag ID | 40961 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Color space information. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-gamma"></a>
### The `exif:Gamma` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.Gamma` |
| ID | `exif:Gamma` |
| Name | Gamma |
| Label | – |
| Tag ID | 42240 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Gamma. |
| Required? | No |
| Citaton | – |
| Type | Rational |

<a id="exif-exif-componentsconfiguration"></a>
### The `exif:ComponentsConfiguration` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.ComponentsConfiguration` |
| ID | `exif:ComponentsConfiguration` |
| Name | ComponentsConfiguration |
| Label | – |
| Tag ID | 37121 |
| Count/Length | 4 |
| Default Value | – |
| Definiton | Meaning of each component. |
| Required? | No |
| Citaton | – |
| Type | Undefined |

<a id="exif-exif-compressedbitsperpixel"></a>
### The `exif:CompressedBitsPerPixel` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.CompressedBitsPerPixel` |
| ID | `exif:CompressedBitsPerPixel` |
| Name | CompressedBitsPerPixel |
| Label | – |
| Tag ID | 37122 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Image compression mode. |
| Required? | No |
| Citaton | – |
| Type | Rational |

<a id="exif-exif-pixelxdimension"></a>
### The `exif:PixelXDimension` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.PixelXDimension` |
| ID | `exif:PixelXDimension` |
| Name | PixelXDimension |
| Label | – |
| Tag ID | 40962 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Valid image width. |
| Required? | No |
| Citaton | – |
| Type | Short; Long |

<a id="exif-exif-pixelydimension"></a>
### The `exif:PixelYDimension` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.PixelYDimension` |
| ID | `exif:PixelYDimension` |
| Name | PixelYDimension |
| Label | – |
| Tag ID | 40963 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Valid image height. |
| Required? | No |
| Citaton | – |
| Type | Short; Long |

<a id="exif-exif-makernote"></a>
### The `exif:MakerNote` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.MakerNote` |
| ID | `exif:MakerNote` |
| Name | MakerNote |
| Label | – |
| Tag ID | 37500 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Manufacturer notes. |
| Required? | No |
| Citaton | – |
| Type | Undefined |

<a id="exif-exif-usercomment"></a>
### The `exif:UserComment` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.UserComment` |
| ID | `exif:UserComment` |
| Name | UserComment |
| Label | – |
| Tag ID | 37510 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | User comments. |
| Required? | No |
| Citaton | – |
| Type | Undefined |

<a id="exif-exif-relatedsoundfile"></a>
### The `exif:RelatedSoundFile` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.RelatedSoundFile` |
| ID | `exif:RelatedSoundFile` |
| Name | RelatedSoundFile |
| Label | – |
| Tag ID | 40964 |
| Count/Length | 13 |
| Default Value | – |
| Definiton | Related audio file. |
| Required? | No |
| Citaton | – |
| Type | String |

<a id="exif-exif-datetimeoriginal"></a>
### The `exif:DateTimeOriginal` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.DateTimeOriginal` |
| ID | `exif:DateTimeOriginal` |
| Name | DateTimeOriginal |
| Label | – |
| Tag ID | 36867 |
| Count/Length | 20 |
| Default Value | – |
| Definiton | Date and time of original data generation. |
| Required? | No |
| Citaton | – |
| Type | ASCII |

<a id="exif-exif-datetimedigitized"></a>
### The `exif:DateTimeDigitized` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.DateTimeDigitized` |
| ID | `exif:DateTimeDigitized` |
| Name | DateTimeDigitized |
| Label | – |
| Tag ID | 36868 |
| Count/Length | 20 |
| Default Value | – |
| Definiton | Date and time of digital data generation. |
| Required? | No |
| Citaton | – |
| Type | ASCII |

<a id="exif-exif-subsectime"></a>
### The `exif:SubSecTime` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.SubSecTime` |
| ID | `exif:SubSecTime` |
| Name | SubSecTime |
| Label | – |
| Tag ID | 37520 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | File change date and time sub-seconds. |
| Required? | No |
| Citaton | – |
| Type | ASCII |

<a id="exif-exif-subsectimeoriginal"></a>
### The `exif:SubSecTimeOriginal` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.SubSecTimeOriginal` |
| ID | `exif:SubSecTimeOriginal` |
| Name | SubSecTimeOriginal |
| Label | – |
| Tag ID | 37521 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Date and time of original data generation sub-seconds. |
| Required? | No |
| Citaton | – |
| Type | ASCII |

<a id="exif-exif-subsectimedigitized"></a>
### The `exif:SubSecTimeDigitized` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.SubSecTimeDigitized` |
| ID | `exif:SubSecTimeDigitized` |
| Name | SubSecTimeDigitized |
| Label | – |
| Tag ID | 37522 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Date and time of digital data generation sub-seconds. |
| Required? | No |
| Citaton | – |
| Type | ASCII |

<a id="exif-exif-exposuretime"></a>
### The `exif:ExposureTime` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.ExposureTime` |
| ID | `exif:ExposureTime` |
| Name | ExposureTime |
| Label | – |
| Tag ID | 33434 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Exposure time. |
| Required? | No |
| Citaton | – |
| Type | Rational |

<a id="exif-exif-fnumber"></a>
### The `exif:FNumber` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.FNumber` |
| ID | `exif:FNumber` |
| Name | FNumber |
| Label | – |
| Tag ID | 33437 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | F number. |
| Required? | No |
| Citaton | – |
| Type | Rational |

<a id="exif-exif-exposureprogram"></a>
### The `exif:ExposureProgram` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.ExposureProgram` |
| ID | `exif:ExposureProgram` |
| Name | ExposureProgram |
| Label | – |
| Tag ID | 34850 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Exposure program. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-spectralsensitivity"></a>
### The `exif:SpectralSensitivity` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.SpectralSensitivity` |
| ID | `exif:SpectralSensitivity` |
| Name | SpectralSensitivity |
| Label | – |
| Tag ID | 34852 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Spectral sensitivity. |
| Required? | No |
| Citaton | – |
| Type | ASCII |

<a id="exif-exif-photographicsensitivity"></a>
### The `exif:PhotographicSensitivity` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.PhotographicSensitivity` |
| ID | `exif:PhotographicSensitivity` |
| Name | PhotographicSensitivity |
| Label | – |
| Tag ID | 34855 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Photographic sensitivity. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-optoelectricconversionfactor"></a>
### The `exif:OptoElectricConversionFactor` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.OptoElectricConversionFactor` |
| ID | `exif:OptoElectricConversionFactor` |
| Name | OptoElectricConversionFactor |
| Label | – |
| Tag ID | 34856 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Opto-electric conversion factor. |
| Required? | No |
| Citaton | – |
| Type | Undefined |

<a id="exif-exif-sensitivitytype"></a>
### The `exif:SensitivityType` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.SensitivityType` |
| ID | `exif:SensitivityType` |
| Name | SensitivityType |
| Label | – |
| Tag ID | 34864 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Sensitivity type. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-standardoutputsensitivity"></a>
### The `exif:StandardOutputSensitivity` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.StandardOutputSensitivity` |
| ID | `exif:StandardOutputSensitivity` |
| Name | StandardOutputSensitivity |
| Label | – |
| Tag ID | 34865 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Standard output sensitivity. |
| Required? | No |
| Citaton | – |
| Type | Long |

<a id="exif-exif-recommendedexposureindex"></a>
### The `exif:RecommendedExposureIndex` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.RecommendedExposureIndex` |
| ID | `exif:RecommendedExposureIndex` |
| Name | RecommendedExposureIndex |
| Label | – |
| Tag ID | 34866 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Recommended exposure index. |
| Required? | No |
| Citaton | – |
| Type | Long |

<a id="exif-exif-isospeed"></a>
### The `exif:ISOSpeed` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.ISOSpeed` |
| ID | `exif:ISOSpeed` |
| Name | ISOSpeed |
| Label | – |
| Tag ID | 34867 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | ISO speed. |
| Required? | No |
| Citaton | – |
| Type | Long |

<a id="exif-exif-isospeedlatitudeyyy"></a>
### The `exif:ISOSpeedLatitudeYYY` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.ISOSpeedLatitudeYYY` |
| ID | `exif:ISOSpeedLatitudeYYY` |
| Name | ISOSpeedLatitudeYYY |
| Label | – |
| Tag ID | 34868 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | ISO speed latitude YYY. |
| Required? | No |
| Citaton | – |
| Type | Long |

<a id="exif-exif-isospeedlatitudezzz"></a>
### The `exif:ISOSpeedLatitudeZZZ` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.ISOSpeedLatitudeZZZ` |
| ID | `exif:ISOSpeedLatitudeZZZ` |
| Name | ISOSpeedLatitudeZZZ |
| Label | – |
| Tag ID | 34869 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | ISO speed latitude ZZZ. |
| Required? | No |
| Citaton | – |
| Type | Long |

<a id="exif-exif-shutterspeedvalue"></a>
### The `exif:ShutterSpeedValue` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.ShutterSpeedValue` |
| ID | `exif:ShutterSpeedValue` |
| Name | ShutterSpeedValue |
| Label | – |
| Tag ID | 37377 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Shutter speed. |
| Required? | No |
| Citaton | – |
| Type | RationalSigned |

<a id="exif-exif-aperturevalue"></a>
### The `exif:ApertureValue` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.ApertureValue` |
| ID | `exif:ApertureValue` |
| Name | ApertureValue |
| Label | – |
| Tag ID | 37378 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Aperture. |
| Required? | No |
| Citaton | – |
| Type | Rational |

<a id="exif-exif-brightnessvalue"></a>
### The `exif:BrightnessValue` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.BrightnessValue` |
| ID | `exif:BrightnessValue` |
| Name | BrightnessValue |
| Label | – |
| Tag ID | 37379 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Brightness. |
| Required? | No |
| Citaton | – |
| Type | RationalSigned |

<a id="exif-exif-exposurebiasvalue"></a>
### The `exif:ExposureBiasValue` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.ExposureBiasValue` |
| ID | `exif:ExposureBiasValue` |
| Name | ExposureBiasValue |
| Label | – |
| Tag ID | 37380 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Exposure bias. |
| Required? | No |
| Citaton | – |
| Type | RationalSigned |

<a id="exif-exif-maxaperturevalue"></a>
### The `exif:MaxApertureValue` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.MaxApertureValue` |
| ID | `exif:MaxApertureValue` |
| Name | MaxApertureValue |
| Label | – |
| Tag ID | 37381 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Maximum lens aperture. |
| Required? | No |
| Citaton | – |
| Type | Rational |

<a id="exif-exif-subjectdistance"></a>
### The `exif:SubjectDistance` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.SubjectDistance` |
| ID | `exif:SubjectDistance` |
| Name | SubjectDistance |
| Label | – |
| Tag ID | 37382 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Subject distance. |
| Required? | No |
| Citaton | – |
| Type | Rational |

<a id="exif-exif-meteringmode"></a>
### The `exif:MeteringMode` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.MeteringMode` |
| ID | `exif:MeteringMode` |
| Name | MeteringMode |
| Label | – |
| Tag ID | 37383 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Metering mode. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-lightsource"></a>
### The `exif:LightSource` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.LightSource` |
| ID | `exif:LightSource` |
| Name | LightSource |
| Label | – |
| Tag ID | 37384 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Light source. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-flash"></a>
### The `exif:Flash` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.Flash` |
| ID | `exif:Flash` |
| Name | Flash |
| Label | – |
| Tag ID | 37385 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Flash. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-focallength"></a>
### The `exif:FocalLength` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.FocalLength` |
| ID | `exif:FocalLength` |
| Name | FocalLength |
| Label | – |
| Tag ID | 37386 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Lens focal length. |
| Required? | No |
| Citaton | – |
| Type | Rational |

<a id="exif-exif-subjectarea"></a>
### The `exif:SubjectArea` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.SubjectArea` |
| ID | `exif:SubjectArea` |
| Name | SubjectArea |
| Label | – |
| Tag ID | 37396 |
| Count/Length | 2; 3; 4 |
| Default Value | – |
| Definiton | Subject area. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-flashenergy"></a>
### The `exif:FlashEnergy` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.FlashEnergy` |
| ID | `exif:FlashEnergy` |
| Name | FlashEnergy |
| Label | – |
| Tag ID | 41483 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Flash energy. |
| Required? | No |
| Citaton | – |
| Type | Rational |

<a id="exif-exif-spatialfrequencyresponse"></a>
### The `exif:SpatialFrequencyResponse` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.SpatialFrequencyResponse` |
| ID | `exif:SpatialFrequencyResponse` |
| Name | SpatialFrequencyResponse |
| Label | – |
| Tag ID | 41484 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Spatial frequency response. |
| Required? | No |
| Citaton | – |
| Type | Undefined |

<a id="exif-exif-focalplanexresolution"></a>
### The `exif:FocalPlaneXResolution` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.FocalPlaneXResolution` |
| ID | `exif:FocalPlaneXResolution` |
| Name | FocalPlaneXResolution |
| Label | – |
| Tag ID | 41486 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Focal plane X resolution. |
| Required? | No |
| Citaton | – |
| Type | Rational |

<a id="exif-exif-focalplaneyresolution"></a>
### The `exif:FocalPlaneYResolution` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.FocalPlaneYResolution` |
| ID | `exif:FocalPlaneYResolution` |
| Name | FocalPlaneYResolution |
| Label | – |
| Tag ID | 41487 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Focal plane Y resolution. |
| Required? | No |
| Citaton | – |
| Type | Rational |

<a id="exif-exif-focalplaneresolutionunit"></a>
### The `exif:FocalPlaneResolutionUnit` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.FocalPlaneResolutionUnit` |
| ID | `exif:FocalPlaneResolutionUnit` |
| Name | FocalPlaneResolutionUnit |
| Label | – |
| Tag ID | 41488 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Focal plane resolution unit. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-subjectlocation"></a>
### The `exif:SubjectLocation` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.SubjectLocation` |
| ID | `exif:SubjectLocation` |
| Name | SubjectLocation |
| Label | – |
| Tag ID | 41492 |
| Count/Length | 2 |
| Default Value | – |
| Definiton | Subject location. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-exposureindex"></a>
### The `exif:ExposureIndex` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.ExposureIndex` |
| ID | `exif:ExposureIndex` |
| Name | ExposureIndex |
| Label | – |
| Tag ID | 41493 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Exposure index. |
| Required? | No |
| Citaton | – |
| Type | Rational |

<a id="exif-exif-sensingmethod"></a>
### The `exif:SensingMethod` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.SensingMethod` |
| ID | `exif:SensingMethod` |
| Name | SensingMethod |
| Label | – |
| Tag ID | 41495 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Sensing method. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-filesource"></a>
### The `exif:FileSource` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.FileSource` |
| ID | `exif:FileSource` |
| Name | FileSource |
| Label | – |
| Tag ID | 41728 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | File source. |
| Required? | No |
| Citaton | – |
| Type | Undefined |

<a id="exif-exif-scenetype"></a>
### The `exif:SceneType` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.SceneType` |
| ID | `exif:SceneType` |
| Name | SceneType |
| Label | – |
| Tag ID | 41729 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Scene type. |
| Required? | No |
| Citaton | – |
| Type | Undefined |

<a id="exif-exif-cfapattern"></a>
### The `exif:CFAPattern` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.CFAPattern` |
| ID | `exif:CFAPattern` |
| Name | CFAPattern |
| Label | – |
| Tag ID | 41730 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | CFA pattern. |
| Required? | No |
| Citaton | – |
| Type | Undefined |

<a id="exif-exif-customrendered"></a>
### The `exif:CustomRendered` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.CustomRendered` |
| ID | `exif:CustomRendered` |
| Name | CustomRendered |
| Label | – |
| Tag ID | 41985 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Custom image processing. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-exposuremode"></a>
### The `exif:ExposureMode` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.ExposureMode` |
| ID | `exif:ExposureMode` |
| Name | ExposureMode |
| Label | – |
| Tag ID | 41986 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Exposure mode. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-whitebalance"></a>
### The `exif:WhiteBalance` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.WhiteBalance` |
| ID | `exif:WhiteBalance` |
| Name | WhiteBalance |
| Label | – |
| Tag ID | 41987 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | White balance. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-digitalzoomratio"></a>
### The `exif:DigitalZoomRatio` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.DigitalZoomRatio` |
| ID | `exif:DigitalZoomRatio` |
| Name | DigitalZoomRatio |
| Label | – |
| Tag ID | 41988 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Digital zoom ratio. |
| Required? | No |
| Citaton | – |
| Type | Rational |

<a id="exif-exif-focallength35mmfilm"></a>
### The `exif:FocalLength35mmFilm` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.FocalLength35mmFilm` |
| ID | `exif:FocalLength35mmFilm` |
| Name | FocalLength35mmFilm |
| Label | – |
| Tag ID | 41989 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Focal length in 35mm film. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-scenecapturetype"></a>
### The `exif:SceneCaptureType` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.SceneCaptureType` |
| ID | `exif:SceneCaptureType` |
| Name | SceneCaptureType |
| Label | – |
| Tag ID | 41990 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Scene capture type. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-gaincontrol"></a>
### The `exif:GainControl` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GainControl` |
| ID | `exif:GainControl` |
| Name | GainControl |
| Label | – |
| Tag ID | 41991 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Gain control. |
| Required? | No |
| Citaton | – |
| Type | Rational |

<a id="exif-exif-contrast"></a>
### The `exif:Contrast` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.Contrast` |
| ID | `exif:Contrast` |
| Name | Contrast |
| Label | – |
| Tag ID | 41992 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Contrast. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-saturation"></a>
### The `exif:Saturation` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.Saturation` |
| ID | `exif:Saturation` |
| Name | Saturation |
| Label | – |
| Tag ID | 41993 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Saturation. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-sharpness"></a>
### The `exif:Sharpness` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.Sharpness` |
| ID | `exif:Sharpness` |
| Name | Sharpness |
| Label | – |
| Tag ID | 41964 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Sharpness. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-devicesettingdescription"></a>
### The `exif:DeviceSettingDescription` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.DeviceSettingDescription` |
| ID | `exif:DeviceSettingDescription` |
| Name | DeviceSettingDescription |
| Label | – |
| Tag ID | 41995 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Device setting description. |
| Required? | No |
| Citaton | – |
| Type | Undefined |

<a id="exif-exif-subjectdistancerange"></a>
### The `exif:SubjectDistanceRange` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.SubjectDistanceRange` |
| ID | `exif:SubjectDistanceRange` |
| Name | SubjectDistanceRange |
| Label | – |
| Tag ID | 41996 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Subject distance range. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-imageuniqueid"></a>
### The `exif:ImageUniqueID` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.ImageUniqueID` |
| ID | `exif:ImageUniqueID` |
| Name | ImageUniqueID |
| Label | – |
| Tag ID | 42016 |
| Count/Length | 33 |
| Default Value | – |
| Definiton | Unique image ID. |
| Required? | No |
| Citaton | – |
| Type | String |

<a id="exif-exif-cameraownername"></a>
### The `exif:CameraOwnerName` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.CameraOwnerName` |
| ID | `exif:CameraOwnerName` |
| Name | CameraOwnerName |
| Label | – |
| Tag ID | 42032 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Camera owner name. |
| Required? | No |
| Citaton | – |
| Type | String |

<a id="exif-exif-bodyserialnumber"></a>
### The `exif:BodySerialNumber` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.BodySerialNumber` |
| ID | `exif:BodySerialNumber` |
| Name | BodySerialNumber |
| Label | – |
| Tag ID | 42033 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Camera body serial number. |
| Required? | No |
| Citaton | – |
| Type | String |

<a id="exif-exif-lensspecification"></a>
### The `exif:LensSpecification` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.LensSpecification` |
| ID | `exif:LensSpecification` |
| Name | LensSpecification |
| Label | – |
| Tag ID | 42034 |
| Count/Length | 4 |
| Default Value | – |
| Definiton | Lens specification. |
| Required? | No |
| Citaton | – |
| Type | Rational |

<a id="exif-exif-lensmake"></a>
### The `exif:LensMake` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.LensMake` |
| ID | `exif:LensMake` |
| Name | LensMake |
| Label | – |
| Tag ID | 42035 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Lens make. |
| Required? | No |
| Citaton | – |
| Type | String |

<a id="exif-exif-lensmodel"></a>
### The `exif:LensModel` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.LensModel` |
| ID | `exif:LensModel` |
| Name | LensModel |
| Label | – |
| Tag ID | 42036 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Lens model. |
| Required? | No |
| Citaton | – |
| Type | String |

<a id="exif-exif-lensserialnumber"></a>
### The `exif:LensSerialNumber` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.LensSerialNumber` |
| ID | `exif:LensSerialNumber` |
| Name | LensSerialNumber |
| Label | – |
| Tag ID | 42037 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Lens serial number. |
| Required? | No |
| Citaton | – |
| Type | String |

<a id="exif-exif-imagetitle"></a>
### The `exif:ImageTitle` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.ImageTitle` |
| ID | `exif:ImageTitle` |
| Name | ImageTitle |
| Label | – |
| Tag ID | 42038 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Title of the image. |
| Pseudonym | exiftool: dc:Title |
| Required? | No |
| Citaton | – |
| Type | String |

<a id="exif-exif-photographer"></a>
### The `exif:Photographer` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.Photographer` |
| ID | `exif:Photographer` |
| Name | Photographer |
| Label | – |
| Tag ID | 42039 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Name of the photographer. |
| Required? | No |
| Citaton | – |
| Type | String |

<a id="exif-exif-imageeditor"></a>
### The `exif:ImageEditor` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.ImageEditor` |
| ID | `exif:ImageEditor` |
| Name | ImageEditor |
| Label | – |
| Tag ID | 42040 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Name of the main person who edited the image. |
| Required? | No |
| Citaton | – |
| Type | String |

<a id="exif-exif-camerafirmware"></a>
### The `exif:CameraFirmware` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.CameraFirmware` |
| ID | `exif:CameraFirmware` |
| Name | CameraFirmware |
| Label | – |
| Tag ID | 42041 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Name and version of software or firmware of the camera. |
| Required? | No |
| Citaton | – |
| Type | String |

<a id="exif-exif-rawdevelopingsoftware"></a>
### The `exif:RAWDevelopingSoftware` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.RAWDevelopingSoftware` |
| ID | `exif:RAWDevelopingSoftware` |
| Name | RAWDevelopingSoftware |
| Label | – |
| Tag ID | 42042 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Name and version of software used to develop the RAW image. |
| Required? | No |
| Citaton | – |
| Type | String |

<a id="exif-exif-imageeditingsoftware"></a>
### The `exif:ImageEditingSoftware` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.ImageEditingSoftware` |
| ID | `exif:ImageEditingSoftware` |
| Name | ImageEditingSoftware |
| Label | – |
| Tag ID | 42043 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Name and version of software used to edit the image. |
| Required? | No |
| Citaton | – |
| Type | String |

<a id="exif-exif-metadataeditingsoftware"></a>
### The `exif:MetadataEditingSoftware` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.MetadataEditingSoftware` |
| ID | `exif:MetadataEditingSoftware` |
| Name | MetadataEditingSoftware |
| Label | – |
| Tag ID | 42044 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Name and version of software used to edit the image metadata. |
| Required? | No |
| Citaton | – |
| Type | String |

<a id="exif-exif-compositeimage"></a>
### The `exif:CompositeImage` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.CompositeImage` |
| ID | `exif:CompositeImage` |
| Name | CompositeImage |
| Label | – |
| Tag ID | 42080 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Notes whether the image is a composite image or not. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-sourceimagenumberofcompositeimage"></a>
### The `exif:SourceImageNumberOfCompositeImage` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.SourceImageNumberOfCompositeImage` |
| ID | `exif:SourceImageNumberOfCompositeImage` |
| Name | SourceImageNumberOfCompositeImage |
| Label | – |
| Tag ID | 42081 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Number of source images captured for the composite image. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-sourceexposuretimesofcompositeimage"></a>
### The `exif:SourceExposureTimesOfCompositeImage` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.SourceExposureTimesOfCompositeImage` |
| ID | `exif:SourceExposureTimesOfCompositeImage` |
| Name | SourceExposureTimesOfCompositeImage |
| Label | – |
| Tag ID | 42082 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | For composite images, records parameters relating to exposure. |
| Required? | No |
| Citaton | – |
| Type | Undefined |

<a id="exif-exif-gpsversionid"></a>
### The `exif:GPSVersionID` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GPSVersionID` |
| ID | `exif:GPSVersionID` |
| Name | GPSVersionID |
| Label | – |
| Tag ID | 0 |
| Count/Length | 4 |
| Default Value | – |
| Definiton | GPS tag version. |
| Required? | No |
| Citaton | – |
| Type | Byte |

<a id="exif-exif-gpslatituderef"></a>
### The `exif:GPSLatitudeRef` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GPSLatitudeRef` |
| ID | `exif:GPSLatitudeRef` |
| Name | GPSLatitudeRef |
| Label | – |
| Tag ID | 1 |
| Count/Length | 2 |
| Default Value | – |
| Definiton | GPS north or south latitude. |
| Required? | No |
| Citaton | – |
| Type | ASCII |

<a id="exif-exif-gpslatitude"></a>
### The `exif:GPSLatitude` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GPSLatitude` |
| ID | `exif:GPSLatitude` |
| Name | GPSLatitude |
| Label | – |
| Tag ID | 2 |
| Count/Length | 3 |
| Default Value | – |
| Definiton | GPS latitude. |
| Required? | No |
| Citaton | – |
| Type | Rational |

<a id="exif-exif-gpslongituderef"></a>
### The `exif:GPSLongitudeRef` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GPSLongitudeRef` |
| ID | `exif:GPSLongitudeRef` |
| Name | GPSLongitudeRef |
| Label | – |
| Tag ID | 3 |
| Count/Length | 2 |
| Default Value | – |
| Definiton | GPS east or west longitude. |
| Required? | No |
| Citaton | – |
| Type | ASCII |

<a id="exif-exif-gpslongitude"></a>
### The `exif:GPSLongitude` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GPSLongitude` |
| ID | `exif:GPSLongitude` |
| Name | GPSLongitude |
| Label | – |
| Tag ID | 4 |
| Count/Length | 3 |
| Default Value | – |
| Definiton | GPS longitude. |
| Required? | No |
| Citaton | – |
| Type | Rational |

<a id="exif-exif-gpsaltituderef"></a>
### The `exif:GPSAltitudeRef` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GPSAltitudeRef` |
| ID | `exif:GPSAltitudeRef` |
| Name | GPSAltitudeRef |
| Label | – |
| Tag ID | 5 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | GPS altitude reference. |
| Required? | No |
| Citaton | – |
| Type | Byte |

<a id="exif-exif-gpsaltitude"></a>
### The `exif:GPSAltitude` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GPSAltitude` |
| ID | `exif:GPSAltitude` |
| Name | GPSAltitude |
| Label | – |
| Tag ID | 6 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | GPS altitude. |
| Required? | No |
| Citaton | – |
| Type | Rational |

<a id="exif-exif-gpstimestamp"></a>
### The `exif:GPSTimeStamp` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GPSTimeStamp` |
| ID | `exif:GPSTimeStamp` |
| Name | GPSTimeStamp |
| Label | – |
| Tag ID | 7 |
| Count/Length | 3 |
| Default Value | – |
| Definiton | GPS time (atomic clock). |
| Required? | No |
| Citaton | – |
| Type | Rational |

<a id="exif-exif-gpssatellites"></a>
### The `exif:GPSSatellites` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GPSSatellites` |
| ID | `exif:GPSSatellites` |
| Name | GPSSatellites |
| Label | – |
| Tag ID | 8 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | GPS satellites used for measurement. |
| Required? | No |
| Citaton | – |
| Type | ASCII |

<a id="exif-exif-gpsstatus"></a>
### The `exif:GPSStatus` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GPSStatus` |
| ID | `exif:GPSStatus` |
| Name | GPSStatus |
| Label | – |
| Tag ID | 9 |
| Count/Length | 2 |
| Default Value | – |
| Definiton | GPS receiver status. |
| Required? | No |
| Citaton | – |
| Type | ASCII |

<a id="exif-exif-gpsmeasuremode"></a>
### The `exif:GPSMeasureMode` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GPSMeasureMode` |
| ID | `exif:GPSMeasureMode` |
| Name | GPSMeasureMode |
| Label | – |
| Tag ID | 10 |
| Count/Length | 2 |
| Default Value | – |
| Definiton | GPS measurement mode. |
| Required? | No |
| Citaton | – |
| Type | ASCII |

<a id="exif-exif-gpsdop"></a>
### The `exif:GPSDOP` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GPSDOP` |
| ID | `exif:GPSDOP` |
| Name | GPSDOP |
| Label | – |
| Tag ID | 11 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | GPS measurement precision. |
| Required? | No |
| Citaton | – |
| Type | Rational |

<a id="exif-exif-gpsspeedref"></a>
### The `exif:GPSSpeedRef` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GPSSpeedRef` |
| ID | `exif:GPSSpeedRef` |
| Name | GPSSpeedRef |
| Label | – |
| Tag ID | 12 |
| Count/Length | 2 |
| Default Value | – |
| Definiton | GPS speed unit. |
| Required? | No |
| Citaton | – |
| Type | ASCII |

<a id="exif-exif-gpsspeed"></a>
### The `exif:GPSSpeed` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GPSSpeed` |
| ID | `exif:GPSSpeed` |
| Name | GPSSpeed |
| Label | – |
| Tag ID | 13 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | Speed of GPS receiver. |
| Required? | No |
| Citaton | – |
| Type | Rational |

<a id="exif-exif-gpstrackref"></a>
### The `exif:GPSTrackRef` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GPSTrackRef` |
| ID | `exif:GPSTrackRef` |
| Name | GPSTrackRef |
| Label | – |
| Tag ID | 14 |
| Count/Length | 2 |
| Default Value | – |
| Definiton | GPS reference for direction of movement. |
| Required? | No |
| Citaton | – |
| Type | ASCII |

<a id="exif-exif-gpstrack"></a>
### The `exif:GPSTrack` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GPSTrack` |
| ID | `exif:GPSTrack` |
| Name | GPSTrack |
| Label | – |
| Tag ID | 15 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | GPS direction of movement. |
| Required? | No |
| Citaton | – |
| Type | Rational |

<a id="exif-exif-gpsimgdirectionref"></a>
### The `exif:GPSImgDirectionRef` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GPSImgDirectionRef` |
| ID | `exif:GPSImgDirectionRef` |
| Name | GPSImgDirectionRef |
| Label | – |
| Tag ID | 16 |
| Count/Length | 2 |
| Default Value | – |
| Definiton | GPS reference for direction of image. |
| Required? | No |
| Citaton | – |
| Type | ASCII |

<a id="exif-exif-gpsimgdirection"></a>
### The `exif:GPSImgDirection` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GPSImgDirection` |
| ID | `exif:GPSImgDirection` |
| Name | GPSImgDirection |
| Label | – |
| Tag ID | 17 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | GPS direction of image. |
| Required? | No |
| Citaton | – |
| Type | Rational |

<a id="exif-exif-gpsmapdatum"></a>
### The `exif:GPSMapDatum` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GPSMapDatum` |
| ID | `exif:GPSMapDatum` |
| Name | GPSMapDatum |
| Label | – |
| Tag ID | 18 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | GPS geodetic survey data used. |
| Required? | No |
| Citaton | – |
| Type | ASCII |

<a id="exif-exif-gpsdestlatituderef"></a>
### The `exif:GPSDestLatitudeRef` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GPSDestLatitudeRef` |
| ID | `exif:GPSDestLatitudeRef` |
| Name | GPSDestLatitudeRef |
| Label | – |
| Tag ID | 19 |
| Count/Length | 2 |
| Default Value | – |
| Definiton | GPS reference for latitude of destination. |
| Required? | No |
| Citaton | – |
| Type | ASCII |

<a id="exif-exif-gpsdestlatitude"></a>
### The `exif:GPSDestLatitude` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GPSDestLatitude` |
| ID | `exif:GPSDestLatitude` |
| Name | GPSDestLatitude |
| Label | – |
| Tag ID | 20 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | GPS latitude of destination. |
| Required? | No |
| Citaton | – |
| Type | Rational |

<a id="exif-exif-gpsdestlongituderef"></a>
### The `exif:GPSDestLongitudeRef` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GPSDestLongitudeRef` |
| ID | `exif:GPSDestLongitudeRef` |
| Name | GPSDestLongitudeRef |
| Label | – |
| Tag ID | 21 |
| Count/Length | 2 |
| Default Value | – |
| Definiton | GPS reference for longitude of destination. |
| Required? | No |
| Citaton | – |
| Type | ASCII |

<a id="exif-exif-gpsdestlongitude"></a>
### The `exif:GPSDestLongitude` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GPSDestLongitude` |
| ID | `exif:GPSDestLongitude` |
| Name | GPSDestLongitude |
| Label | – |
| Tag ID | 22 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | GPS longitude of destination. |
| Required? | No |
| Citaton | – |
| Type | Rational |

<a id="exif-exif-gpsdestbearingref"></a>
### The `exif:GPSDestBearingRef` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GPSDestBearingRef` |
| ID | `exif:GPSDestBearingRef` |
| Name | GPSDestBearingRef |
| Label | – |
| Tag ID | 23 |
| Count/Length | 2 |
| Default Value | – |
| Definiton | GPS reference for bearing of destination. |
| Required? | No |
| Citaton | – |
| Type | ASCII |

<a id="exif-exif-gpsdestbearing"></a>
### The `exif:GPSDestBearing` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GPSDestBearing` |
| ID | `exif:GPSDestBearing` |
| Name | GPSDestBearing |
| Label | – |
| Tag ID | 24 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | GPS bearing of destination. |
| Required? | No |
| Citaton | – |
| Type | Rational |

<a id="exif-exif-gpsdestdistanceref"></a>
### The `exif:GPSDestDistanceRef` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GPSDestDistanceRef` |
| ID | `exif:GPSDestDistanceRef` |
| Name | GPSDestDistanceRef |
| Label | – |
| Tag ID | 25 |
| Count/Length | 2 |
| Default Value | – |
| Definiton | GPS reference for distance of destination. |
| Required? | No |
| Citaton | – |
| Type | ASCII |

<a id="exif-exif-gpsdestdistance"></a>
### The `exif:GPSDestDistance` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GPSDestDistance` |
| ID | `exif:GPSDestDistance` |
| Name | GPSDestDistance |
| Label | – |
| Tag ID | 26 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | GPS distance of destination. |
| Required? | No |
| Citaton | – |
| Type | Rational |

<a id="exif-exif-gpsprocessingmethod"></a>
### The `exif:GPSProcessingMethod` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GPSProcessingMethod` |
| ID | `exif:GPSProcessingMethod` |
| Name | GPSProcessingMethod |
| Label | – |
| Tag ID | 27 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Name of GPS processing method. |
| Required? | No |
| Citaton | – |
| Type | Undefined |

<a id="exif-exif-gpsareainformation"></a>
### The `exif:GPSAreaInformation` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GPSAreaInformation` |
| ID | `exif:GPSAreaInformation` |
| Name | GPSAreaInformation |
| Label | – |
| Tag ID | 28 |
| Count/Length | -3 |
| Default Value | – |
| Definiton | Name of GPS area. |
| Required? | No |
| Citaton | – |
| Type | Undefined |

<a id="exif-exif-gpsdatestamp"></a>
### The `exif:GPSDateStamp` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GPSDateStamp` |
| ID | `exif:GPSDateStamp` |
| Name | GPSDateStamp |
| Label | – |
| Tag ID | 29 |
| Count/Length | 11 |
| Default Value | – |
| Definiton | GPS date. |
| Required? | No |
| Citaton | – |
| Type | ASCII |

<a id="exif-exif-gpsdifferential"></a>
### The `exif:GPSDifferential` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GPSDifferential` |
| ID | `exif:GPSDifferential` |
| Name | GPSDifferential |
| Label | – |
| Tag ID | 30 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | GPS differential correction. |
| Required? | No |
| Citaton | – |
| Type | Short |

<a id="exif-exif-gpshpositioningerror"></a>
### The `exif:GPSHPositioningError` field has the following configuration:

| Attribute | Value    |
|-----------|----------|
| Path      | `exif.GPSHPositioningError` |
| ID | `exif:GPSHPositioningError` |
| Name | GPSHPositioningError |
| Label | – |
| Tag ID | 31 |
| Count/Length | 1 |
| Default Value | – |
| Definiton | GPS horizontal positioning error. |
| Required? | No |
| Citaton | – |
| Type | Rational |



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
