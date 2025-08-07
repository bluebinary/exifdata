import enumerific

from exifdata.logging import logger


logger = logger.getChild(__name__)


class TagType(enumerific.Enumeration):
    Undefined = -1
    Short = 1
    Long = 2
    Rational = 3
    RationalSigned = 4
    Byte = 5
    ASCII = 6


class TagCount(enumerific.Enumeration):
    Any = -3
    Fixed = -2
    Computed = -1
    One = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Eleven = 11
    Twelve = 12
    Thirteen = 13
    Fourteen = 14
    Fifteen = 15
    Sixteen = 16
    Seventeen = 17
    Eighteen = 18
    Nineteen = 19
    Twenty = 20
    ThirtyThree = 33


class TagID(enumerific.Enumeration, aliased=True):
    # 4.6.3 EXIF Specific IFDs
    EXIFIFDPointer = 34665
    GPSInfoIFDPointer = 34853
    InteroperabilityIFDPointer = 40965
    # 4.6.4 TIFF Rev. 6.0 Attribute Information: A. Tags Relating to Image Data Structure
    ImageWidth = 256
    ImageHeight = 257
    BitsPerSample = 258
    Compression = 259
    PhotometricInterpretation = 262
    Orientation = 274
    SamplesPerPixel = 277
    PlanarConfiguration = 284
    YCbCrSubSampling = 530
    YCbCrPositioning = 531
    XResolution = 282
    YResolution = 283
    ResolutionUnit = 296
    PageNumber = 297
    # 4.6.4 TIFF Rev. 6.0 Attribute Information: B. Tags Relating to Recording Offset
    StripOffsets = 273
    RowsPerStrip = 278
    StripByteCounts = 279
    JPEGInterchangeFormat = 513
    JPEGInterchangeFormatLength = 514
    # 4.6.4 TIFF Rev. 6.0 Attribute Information: C. Tags Relating to Image Data Characteristics
    TransferFunction = 301
    WhitePoint = 318
    PrimaryChromaticities = 319
    YCbCrCoefficients = 529
    ReferenceBlackWhite = 532
    # 4.6.4 TIFF Rev. 6.0 Attribute Information: D. Other Tags
    DateTime = 306
    ImageDescription = 270
    Make = 271
    Model = 272
    Software = 305
    Artist = 315
    Copyright = 33432
    Rating = 18246
    RatingPercent = 18249
    # 4.6.5 EXIF IFD Attribute Information: A. Tags Relating to Version
    EXIFVersion = 36864
    FlashpixVersion = 40960
    # 4.6.5 EXIF IFD Attribute Information: B. Tags Relating to Image Data Characteristics
    ColorSpace = 40961
    Gamma = 42240
    # 4.6.5 EXIF IFD Attribute Information: C. Tags Relating to Image Configuration
    ComponentsConfiguration = 37121
    CompressedBitsPerPixel = 37122
    PixelXDimension = 40962
    PixelYDimension = 40963
    # 4.6.5 EXIF IFD Attribute Information: D. Tags Relating to User Information
    MakerNote = 37500
    UserComment = 37510
    # 4.6.5 EXIF IFD Attribute Information: E. Tags Relating to Related File Information
    RelatedSoundFile = 40964
    # 4.6.5 EXIF IFD Attribute Information: F. Tags Relating to Date and Time
    DateTimeOriginal = 36867
    DateTimeDigitized = 36868
    SubSecTime = 37520
    SubSecTimeOriginal = 37521
    SubSecTimeDigitized = 37522
    # 4.6.5 EXIF IFD Attribute Information: G. Tags Relating to Picture-Taking Conditions (Table 8)
    ExposureTime = 33434
    FNumber = 33437
    ExposureProgram = 34850
    SpectralSensitivity = 34852
    PhotographicSensitivity = 34855
    OptoElectricConversionFactor = 34856
    OECF = 34856
    SensitivityType = 34864
    StandardOutputSensitivity = 34865
    RecommendedExposureIndex = 34866
    ISOSpeed = 34867
    ISOSpeedLatitudeYYY = 34868
    ISOSpeedLatitudeZZZ = 34869
    ShutterSpeedValue = 37377
    ApertureValue = 37378
    BrightnessValue = 37379
    ExposureBiasValue = 37380
    MaxApertureValue = 37381
    SubjectDistance = 37382
    MeteringMode = 37383
    LightSource = 37384
    Flash = 37385
    FocalLength = 37386
    SubjectArea = 37396
    FlashEnergy = 41483
    SpatialFrequencyResponse = 41484
    FocalPlaneXResolution = 41486
    FocalPlaneYResolution = 41487
    FocalPlaneResolutionUnit = 41488
    SubjectLocation = 41492
    ExposureIndex = 41493
    SensingMethod = 41495
    FileSource = 41728
    SceneType = 41729
    CFAPattern = 41730
    CustomRendered = 41985
    ExposureMode = 41986
    WhiteBalance = 41987
    DigitalZoomRatio = 41988
    FocalLength35mmFilm = 41989
    SceneCaptureType = 41990
    GainControl = 41991
    Contrast = 41992
    Saturation = 41993
    Sharpness = 41964
    DeviceSettingDescription = 41995
    SubjectDistanceRange = 41996
    # 4.6.5 EXIF IFD Attribute Information: H. Other Tags
    ImageUniqueID = 42016
    CameraOwnerName = 42032
    BodySerialNumber = 42033
    LensSpecification = 42034
    LensMake = 42035
    LensModel = 42036
    LensSerialNumber = 42037
    # 4.6.6 GPS Attribute Information: A. Tags Relating to GPS
    GPSVersionID = 0
    GPSLatitudeRef = 1
    GPSLatitude = 2
    GPSLongitudeRef = 3
    GPSLongitude = 4
    GPSAltitudeRef = 5
    GPSAltitude = 6
    GPSTimeStamp = 7
    GPSSatellites = 8
    GPSStatus = 9
    GPSReceiverStatus = 9
    GPSMeasureMode = 10
    GPSDOP = 11
    GPSSpeedRef = 12
    GPSSpeed = 13
    GPSTrackRef = 14
    GPSTrack = 15
    GPSImgDirectionRef = 16
    GPSImageDirectionRef = 16
    GPSImgDirection = 17
    GPSImageDirection = 17
    GPSMapDatum = 18
    GPSDestLatitudeRef = 19
    GPSDestinationLatitudeRef = 19
    GPSDestLatitude = 20
    GPSDestinationLatitude = 20
    GPSDestLongitudeRef = 21
    GPSDestinationLongitudeRef = 21
    GPSDestLongitude = 22
    GPSDestinationLongitude = 22
    GPSDestBearingRef = 23
    GPSDestinationBearingRef = 23
    GPSDestBearing = 24
    GPSDestinationBearing = 24
    GPSDestDistanceRef = 25
    GPSDestinationDistanceRef = 25
    GPSDestDistance = 26
    GPSDestinationDistance = 26
    GPSProcessingMethod = 27
    GPSAreaInformation = 28
    GPSDateStamp = 29
    GPSDifferential = 30
    GPSHPositioningError = 31
    GPSHorizontalPositioningError = 31


# https://www.cipa.jp/std/documents/e/DC-008-2012_E.pdf


class Tags(object):
    tags = {
        # 4.6.3 EXIF Specific IFDs
        TagID.EXIFIFDPointer: {
            "description": "EXIF IDF pointer",
            "section": "8769.H",
            "type": TagType.Long,
            "count": TagCount.One,
            "default": None,
        },
        TagID.GPSInfoIFDPointer: {
            "description": "GPS Info IDF pointer",
            "section": "8825.H",
            "type": TagType.Long,
            "count": TagCount.One,
            "default": None,
        },
        TagID.InteroperabilityIFDPointer: {
            "description": "Interoperability IDF pointer",
            "section": "A005.H",
            "type": TagType.Long,
            "count": TagCount.One,
            "default": None,
        },
        # 4.6.4 TIFF Rev. 6.0 Attribute Information: A. Tags Relating to Image Data Structure
        TagID.ImageWidth: {
            "description": "Image width",
            "type": (TagType.Short, TagType.Long),
            "count": TagCount.One,
        },
        TagID.ImageHeight: {
            "description": "Image height",
            "type": (TagType.Short, TagType.Long),
            "count": TagCount.One,
        },
        TagID.BitsPerSample: {
            "description": "Number of bits per component",
            "type": TagType.Short,
            "count": TagCount.Three,
        },
        TagID.Compression: {
            "description": "Compression scheme",
            "type": TagType.Short,
            "count": TagCount.One,
        },
        TagID.PhotometricInterpretation: {
            "description": "Pixel composition",
            "type": TagType.Short,
            "count": TagCount.One,
        },
        TagID.Orientation: {
            "description": "Orientation of image",
            "type": TagType.Short,
            "count": TagCount.One,
        },
        TagID.SamplesPerPixel: {
            "description": "Number of components",
            "type": TagType.Short,
            "count": TagCount.One,
        },
        TagID.PlanarConfiguration: {
            "description": "Image data arrangement",
            "type": TagType.Short,
            "count": TagCount.One,
        },
        TagID.YCbCrSubSampling: {
            "description": "Subsampling ratio of Y to C",
            "type": TagType.Short,
            "count": TagCount.Two,
        },
        TagID.YCbCrPositioning: {
            "description": "Y and C positioning",
            "type": TagType.Short,
            "count": TagCount.One,
        },
        TagID.XResolution: {
            "description": "Image resolution in width direction",
            "type": TagType.Rational,
            "count": TagCount.One,
        },
        TagID.YResolution: {
            "description": "Image resolution in height direction",
            "type": TagType.Rational,
            "count": TagCount.One,
        },
        TagID.ResolutionUnit: {
            "description": "Unit of X and Y resolution",
            "type": TagType.Short,
            "count": TagCount.One,
        },
        TagID.PageNumber: {
            "description": "The page number of the page from which this image was scanned",
            "type": TagType.Short,
            "count": TagCount.One,
        },
        # 4.6.4 TIFF Rev. 6.0 Attribute Information: B. Tags Relating to Recording Offset
        TagID.StripOffsets: {
            "description": "Image data location",
            "type": (TagType.Short, TagType.Long),
            "count": TagCount.Computed,
        },
        TagID.RowsPerStrip: {
            "description": "Number of rows per strip",
            "type": (TagType.Short, TagType.Long),
            "count": TagCount.One,
        },
        TagID.StripByteCounts: {
            "description": "Bytes per compressed strip",
            "type": (TagType.Short, TagType.Long),
            "count": TagCount.Computed,
        },
        TagID.JPEGInterchangeFormat: {
            "description": "Offset to JPEG SOI",
            "type": TagType.Long,
            "count": TagCount.One,
        },
        TagID.JPEGInterchangeFormatLength: {
            "description": "Bytes of JPEG data",
            "type": TagType.Long,
            "count": TagCount.One,
        },
        # 4.6.4 TIFF Rev. 6.0 Attribute Information: C. Tags Relating to Image Data Characteristics
        TagID.TransferFunction: {
            "description": "Transfer function",
            "type": TagType.Short,
            "count": TagCount.Fixed,
            "fixed": 3 * 256,
        },
        TagID.WhitePoint: {
            "description": "White point chromaticity",
            "type": TagType.Rational,
            "count": TagCount.Two,
        },
        TagID.PrimaryChromaticities: {
            "description": "Chromaticities of primaries",
            "type": TagType.Rational,
            "count": TagCount.Six,
        },
        TagID.YCbCrCoefficients: {
            "description": "Color space transformation matrix coefficients",
            "type": TagType.Rational,
            "count": TagCount.Three,
        },
        TagID.ReferenceBlackWhite: {
            "description": "Pair of black and white reference values",
            "type": TagType.Rational,
            "count": TagCount.Six,
        },
        # 4.6.4 TIFF Rev. 6.0 Attribute Information: D. Other Tags
        TagID.DateTime: {
            "description": "File change date and time",
            "type": TagType.ASCII,
            "count": TagCount.Twenty,
        },
        TagID.ImageDescription: {
            "description": "Image title",
            "alias": "Description",
            "type": TagType.ASCII,
            "count": TagCount.Any,
        },
        TagID.Make: {
            "description": "Image input equipment manufacturer",
            "type": TagType.ASCII,
            "count": TagCount.Any,
        },
        TagID.Model: {
            "description": "Image input equipment model",
            "type": TagType.ASCII,
            "count": TagCount.Any,
        },
        TagID.Software: {
            "description": "Software used",
            "type": TagType.ASCII,
            "count": TagCount.Any,
        },
        TagID.Artist: {
            "description": "Person who created the image",
            "type": TagType.ASCII,
            "count": TagCount.Any,
        },
        TagID.Copyright: {
            "description": "Copyright holder",
            "type": TagType.ASCII,
            "count": TagCount.Any,
        },
        # 4.6.5 EXIF IFD Attribute Information: A. Tags Relating to Version
        TagID.EXIFVersion: {
            "description": "EXIF version",
            "type": TagType.Undefined,
            "count": TagCount.Four,
        },
        TagID.FlashpixVersion: {
            "description": "Supported Flashpix version",
            "type": TagType.Undefined,
            "count": TagCount.Four,
        },
        # 4.6.5 EXIF IFD Attribute Information: B. Tags Relating to Image Data Characteristics
        TagID.ColorSpace: {
            "description": "Color space information",
            "type": TagType.Short,
            "count": TagCount.One,
        },
        TagID.Gamma: {
            "description": "Gamma",
            "type": TagType.Rational,
            "count": TagCount.One,
        },
        # 4.6.5 EXIF IFD Attribute Information: C. Tags Relating to Image Configuration
        TagID.ComponentsConfiguration: {
            "description": "Meaning of each component",
            "type": TagType.Undefined,
            "count": TagCount.Four,
        },
        TagID.CompressedBitsPerPixel: {
            "description": "Image compression mode",
            "type": TagType.Rational,
            "count": TagCount.One,
        },
        TagID.PixelXDimension: {
            "description": "Valid image width",
            "type": (TagType.Short, TagType.Long),
            "count": TagCount.One,
        },
        TagID.PixelYDimension: {
            "description": "Valid image height",
            "type": (TagType.Short, TagType.Long),
            "count": TagCount.One,
        },
        # 4.6.5 EXIF IFD Attribute Information: D. Tags Relating to User Information
        TagID.MakerNote: {
            "description": "Manufacturer notes",
            "type": TagType.Undefined,
            "count": TagCount.Any,
        },
        TagID.UserComment: {
            "description": "User comments",
            "type": TagType.Undefined,
            "count": TagCount.Any,
        },
        # 4.6.5 EXIF IFD Attribute Information: E. Tags Relating to Related File Information
        TagID.RelatedSoundFile: {
            "description": "Related audio file",
            "type": TagType.ASCII,
            "count": TagCount.Thirteen,
        },
        # 4.6.5 EXIF IFD Attribute Information: F. Tags Relating to Date and Time
        TagID.DateTimeOriginal: {
            "description": "Date and time of original data generation",
            "type": TagType.ASCII,
            "count": TagCount.Twenty,
        },
        TagID.DateTimeDigitized: {
            "description": "Date and time of digital data generation",
            "type": TagType.ASCII,
            "count": TagCount.Twenty,
        },
        TagID.SubSecTime: {
            "description": "File change date and time sub-seconds",
            "type": TagType.ASCII,
            "count": TagCount.Any,
            "related": TagID.DateTime,
        },
        TagID.SubSecTimeOriginal: {
            "description": "Date and time of original data generation sub-seconds",
            "type": TagType.ASCII,
            "count": TagCount.Any,
            "related": TagID.DateTimeOriginal,
        },
        TagID.SubSecTimeDigitized: {
            "description": "Date and time of digital data generation sub-seconds",
            "type": TagType.ASCII,
            "count": TagCount.Any,
            "related": TagID.DateTimeDigitized,
        },
        # 4.6.5 EXIF IFD Attribute Information: G. Tags Relating to Picture-Taking Conditions
        TagID.ExposureTime: {
            "description": "Exposure time",
            "type": TagType.Rational,
            "count": TagCount.One,
        },
        TagID.FNumber: {
            "description": "F number",
            "type": TagType.Rational,
            "count": TagCount.One,
        },
        TagID.ExposureProgram: {
            "description": "Exposure program",
            "type": TagType.Short,
            "count": TagCount.One,
        },
        TagID.SpectralSensitivity: {
            "description": "Spectral sensitivity",
            "type": TagType.ASCII,
            "count": TagCount.Any,
        },
        TagID.PhotographicSensitivity: {
            "description": "Photographic sensitivity",
            "type": TagType.Short,
            "count": TagCount.Any,
        },
        TagID.OptoElectricConversionFactor: {
            "description": "Opto-electric conversion factor",
            "type": TagType.Undefined,
            "count": TagCount.Any,
            "alias": TagID.OECF,
        },
        TagID.SensitivityType: {
            "description": "Sensitivity type",
            "type": TagType.Short,
            "count": TagCount.One,
        },
        TagID.StandardOutputSensitivity: {
            "description": "Standard output sensitivity",
            "type": TagType.Long,
            "count": TagCount.One,
        },
        TagID.RecommendedExposureIndex: {
            "description": "Recommended exposure index",
            "type": TagType.Long,
            "count": TagCount.One,
        },
        TagID.ISOSpeed: {
            "description": "ISO speed",
            "type": TagType.Long,
            "count": TagCount.One,
        },
        TagID.ISOSpeedLatitudeYYY: {
            "description": "ISO speed latitude YYY",
            "type": TagType.Long,
            "count": TagCount.One,
        },
        TagID.ISOSpeedLatitudeZZZ: {
            "description": "ISO speed latitude ZZZ",
            "type": TagType.Long,
            "count": TagCount.One,
        },
        TagID.ShutterSpeedValue: {
            "description": "Shutter speed",
            "type": TagType.RationalSigned,
            "count": TagCount.One,
        },
        TagID.ApertureValue: {
            "description": "Aperture",
            "type": TagType.Rational,
            "count": TagCount.One,
        },
        TagID.BrightnessValue: {
            "description": "Brightness",
            "type": TagType.RationalSigned,
            "count": TagCount.One,
        },
        TagID.ExposureBiasValue: {
            "description": "Exposure bias",
            "type": TagType.RationalSigned,
            "count": TagCount.One,
        },
        TagID.MaxApertureValue: {
            "description": "Maximum lens aperture",
            "type": TagType.Rational,
            "count": TagCount.One,
        },
        TagID.SubjectDistance: {
            "description": "Subject distance",
            "type": TagType.Rational,
            "count": TagCount.One,
        },
        TagID.MeteringMode: {
            "description": "Metering mode",
            "type": TagType.Short,
            "count": TagCount.One,
        },
        TagID.LightSource: {
            "description": "Light source",
            "type": TagType.Short,
            "count": TagCount.One,
        },
        TagID.Flash: {
            "description": "Flash",
            "type": TagType.Short,
            "count": TagCount.One,
        },
        TagID.FocalLength: {
            "description": "Lens focal length",
            "type": TagType.Rational,
            "count": TagCount.One,
        },
        TagID.SubjectArea: {
            "description": "Subject area",
            "type": TagType.Short,
            "count": (TagCount.Two, TagCount.Three, TagCount.Four),
        },
        TagID.FlashEnergy: {
            "description": "Flash energy",
            "type": TagType.Rational,
            "count": TagCount.One,
        },
        TagID.SpatialFrequencyResponse: {
            "description": "Spatial frequency response",
            "type": TagType.Undefined,
            "count": TagCount.Any,
        },
        TagID.FocalPlaneXResolution: {
            "description": "Focal plane X resolution",
            "type": TagType.Rational,
            "count": TagCount.One,
        },
        TagID.FocalPlaneYResolution: {
            "description": "Focal plane Y resolution",
            "type": TagType.Rational,
            "count": TagCount.One,
        },
        TagID.FocalPlaneResolutionUnit: {
            "description": "Focal plane resolution unit",
            "type": TagType.Short,
            "count": TagCount.One,
        },
        TagID.SubjectLocation: {
            "description": "Subject location",
            "type": TagType.Short,
            "count": TagCount.Two,
        },
        TagID.ExposureIndex: {
            "description": "Exposure index",
            "type": TagType.Rational,
            "count": TagCount.One,
        },
        TagID.SensingMethod: {
            "description": "Sensing method",
            "type": TagType.Short,
            "count": TagCount.One,
        },
        TagID.FileSource: {
            "description": "File source",
            "type": TagType.Undefined,
            "count": TagCount.Any,
        },
        TagID.SceneType: {
            "description": "Scene type",
            "type": TagType.Undefined,
            "count": TagCount.Any,
        },
        TagID.CFAPattern: {
            "description": "CFA pattern",
            "type": TagType.Undefined,
            "count": TagCount.Any,
        },
        TagID.CustomRendered: {
            "description": "Custom image processing",
            "type": TagType.Short,
            "count": TagCount.One,
        },
        TagID.ExposureMode: {
            "description": "Exposure mode",
            "type": TagType.Short,
            "count": TagCount.One,
        },
        TagID.WhiteBalance: {
            "description": "White balance",
            "type": TagType.Short,
            "count": TagCount.One,
        },
        TagID.DigitalZoomRatio: {
            "description": "Digital zoom ratio",
            "type": TagType.Rational,
            "count": TagCount.One,
        },
        TagID.FocalLength35mmFilm: {
            "description": "Focal length in 35mm film",
            "type": TagType.Short,
            "count": TagCount.One,
        },
        TagID.SceneCaptureType: {
            "description": "Scene capture type",
            "type": TagType.Short,
            "count": TagCount.One,
        },
        TagID.GainControl: {
            "description": "Gain control",
            "type": TagType.Rational,
            "count": TagCount.One,
        },
        TagID.Contrast: {
            "description": "Contrast",
            "type": TagType.Short,
            "count": TagCount.One,
        },
        TagID.Saturation: {
            "description": "Saturation",
            "type": TagType.Short,
            "count": TagCount.One,
        },
        TagID.Sharpness: {
            "description": "Sharpness",
            "type": TagType.Short,
            "count": TagCount.One,
        },
        TagID.DeviceSettingDescription: {
            "description": "Device setting description",
            "type": TagType.Undefined,
            "count": TagCount.Any,
        },
        TagID.SubjectDistanceRange: {
            "description": "Subject distance range",
            "type": TagType.Short,
            "count": TagCount.One,
        },
        # 4.6.5 EXIF IFD Attribute Information: H. Other Tags
        TagID.ImageUniqueID: {
            "description": "Unique image ID",
            "type": TagType.ASCII,
            "count": TagCount.ThirtyThree,
        },
        TagID.CameraOwnerName: {
            "description": "Camera owner name",
            "type": TagType.ASCII,
            "count": TagCount.Any,
        },
        TagID.BodySerialNumber: {
            "description": "Camera body serial number",
            "type": TagType.ASCII,
            "count": TagCount.Any,
        },
        TagID.LensSpecification: {
            "description": "Lens specification",
            "type": TagType.Rational,
            "count": TagCount.Four,
        },
        TagID.LensMake: {
            "description": "Lens make",
            "type": TagType.Rational,
            "count": TagCount.Four,
        },
        TagID.LensModel: {
            "description": "Lens model",
            "type": TagType.ASCII,
            "count": TagCount.Any,
        },
        TagID.LensSerialNumber: {
            "description": "Lens serial number",
            "type": TagType.ASCII,
            "count": TagCount.Any,
        },
        # 4.6.6 GPS Attribute Information: A. Tags Relating to GPS
        TagID.GPSVersionID: {
            "description": "GPS tag version",
            "type": TagType.Byte,
            "count": TagCount.Four,
        },
        TagID.GPSLatitudeRef: {
            "description": "GPS north or south latitude",
            "type": TagType.ASCII,
            "count": TagCount.Two,
        },
        TagID.GPSLatitude: {
            "description": "GPS latitude",
            "type": TagType.Rational,
            "count": TagCount.Three,
        },
        TagID.GPSLongitudeRef: {
            "description": "GPS east or west longitude",
            "type": TagType.ASCII,
            "count": TagCount.Two,
        },
        TagID.GPSLongitude: {
            "description": "GPS longitude",
            "type": TagType.Rational,
            "count": TagCount.Three,
        },
        TagID.GPSAltitudeRef: {
            "description": "GPS altitude reference",
            "type": TagType.Byte,
            "count": TagCount.One,
        },
        TagID.GPSAltitude: {
            "description": "GPS altitude",
            "type": TagType.Rational,
            "count": TagCount.One,
        },
        TagID.GPSTimeStamp: {
            "description": "GPS time (atomic clock)",
            "type": TagType.Rational,
            "count": TagCount.Three,
        },
        TagID.GPSSatellites: {
            "description": "GPS satellites used for measurement",
            "type": TagType.ASCII,
            "count": TagCount.Any,
        },
        TagID.GPSReceiverStatus: {
            "description": "GPS receiver status",
            "type": TagType.ASCII,
            "count": TagCount.Two,
            "alias": TagID.GPSStatus,
        },
        TagID.GPSStatus: {
            "description": "GPS receiver status",
            "type": TagType.ASCII,
            "count": TagCount.Two,
        },
        TagID.GPSMeasureMode: {
            "description": "GPS measurement mode",
            "type": TagType.ASCII,
            "count": TagCount.Two,
        },
        TagID.GPSDOP: {
            "description": "GPS measurement precision",
            "type": TagType.Rational,
            "count": TagCount.One,
        },
        TagID.GPSSpeedRef: {
            "description": "GPS speed unit",
            "type": TagType.ASCII,
            "count": TagCount.Two,
        },
        TagID.GPSSpeed: {
            "description": "Speed of GPS receiver",
            "type": TagType.Rational,
            "count": TagCount.One,
        },
        TagID.GPSTrackRef: {
            "description": "GPS reference for direction of movement",
            "type": TagType.ASCII,
            "count": TagCount.Two,
        },
        TagID.GPSTrack: {
            "description": "GPS direction of movement",
            "type": TagType.Rational,
            "count": TagCount.One,
        },
        TagID.GPSImageDirectionRef: {
            "description": "GPS reference for direction of image",
            "type": TagType.ASCII,
            "count": TagCount.Two,
        },
        TagID.GPSImageDirection: {
            "description": "GPS direction of image",
            "type": TagType.Rational,
            "count": TagCount.One,
        },
        TagID.GPSMapDatum: {
            "description": "GPS geodetic survey data used",
            "type": TagType.ASCII,
            "count": TagCount.Any,
        },
        TagID.GPSDestinationLatitudeRef: {
            "description": "GPS reference for latitude of destination",
            "type": TagType.ASCII,
            "count": TagCount.Two,
            "alias": TagID.GPSDestLatitudeRef,
        },
        TagID.GPSDestinationLatitude: {
            "description": "GPS latitude of destination",
            "type": TagType.Rational,
            "count": TagCount.One,
            "alias": TagID.GPSDestLatitude,
        },
        TagID.GPSDestinationLongitudeRef: {
            "description": "GPS reference for longitude of destination",
            "type": TagType.ASCII,
            "count": TagCount.Two,
            "alias": TagID.GPSDestLongitudeRef,
        },
        TagID.GPSDestinationLongitude: {
            "description": "GPS longitude of destination",
            "type": TagType.Rational,
            "count": TagCount.One,
            "alias": TagID.GPSDestLongitude,
        },
        TagID.GPSDestinationBearingRef: {
            "description": "GPS reference for bearing of destination",
            "type": TagType.ASCII,
            "count": TagCount.Two,
            "alias": TagID.GPSDestBearingRef,
        },
        TagID.GPSDestinationBearing: {
            "description": "GPS bearing of destination",
            "type": TagType.Rational,
            "count": TagCount.One,
            "alias": TagID.GPSDestBearing,
        },
        TagID.GPSDestinationDistanceRef: {
            "description": "GPS reference for distance of destination",
            "type": TagType.ASCII,
            "count": TagCount.Two,
            "alias": TagID.GPSDestDistanceRef,
        },
        TagID.GPSDestinationDistance: {
            "description": "GPS distance of destination",
            "type": TagType.Rational,
            "count": TagCount.One,
            "alias": TagID.GPSDestDistance,
        },
        TagID.GPSProcessingMethod: {
            "description": "Name of GPS processing method",
            "type": TagType.Undefined,
            "count": TagCount.Any,
        },
        TagID.GPSAreaInformation: {
            "description": "Name of GPS area",
            "type": TagType.Undefined,
            "count": TagCount.Any,
        },
        TagID.GPSDateStamp: {
            "description": "GPS date",
            "type": TagType.ASCII,
            "count": TagCount.Eleven,
        },
        TagID.GPSDifferential: {
            "description": "GPS differential correction",
            "type": TagType.Short,
            "count": TagCount.One,
        },
        TagID.GPSHorizontalPositioningError: {
            "description": "GPS horizontal positioning error",
            "type": TagType.Rational,
            "count": TagCount.One,
            "alias": TagID.GPSHPositioningError,
        },
    }

    metadata = {
        "exif": {
            "name": "exif",
            "label": "EXIF namespace",
            "fields": {},
            "unwrap": True,
        },
    }

    for tagid, info in tags.items():
        count = info.get("count")
        if isinstance(count, (set, tuple, list)):
            count = [e.value for e in count]
        elif isinstance(count, TagCount):
            count = count.value

        typed = info.get("type")
        if isinstance(typed, (set, tuple, list)):
            typed = [e.name for e in typed]
        elif isinstance(typed, TagType):
            typed = typed.name

        metadata["exif"]["fields"][f"exif:{tagid.name}"] = field = {
            "name": tagid.name,
            "label": None,
            "definition": info.get("description"),
            "section": info.get("section"),
            "type": typed,
            "count": count,
            "tagid": tagid.value,
            "default": info.get("default"),
        }

        if alias := info.get("alias"):
            if isinstance(alias, str):
                field["alias"] = alias
            elif isinstance(alias, TagID):
                # field["alias"] = alias.name
                pass

    # if os.path.exists(
    #     filepath := os.path.join(os.path.dirname(__file__), "data", "schema.json")
    # ):
    #     logger.warning(f"Cannot overwrite '{filepath}' as the file already exists!")
    # else:
    #     with open(filepath, "w+") as handle:
    #         json.dump(metadata, handle, indent=2)

    @classmethod
    def reconcile(cls, tag_id: TagID | int) -> dict[str, object] | None:
        if isinstance(tag_id, TagID):
            tag_id = tag_id.value
        elif not isinstance(tag_id, int):
            raise TypeError(
                "The 'tag_id' argument must have a TagID enumeration or integer value!"
            )

        for tagid, info in cls.tags.items():
            if tagid.value == tag_id:
                return dict(info, name=tagid.name)


class ColorSpace(enumerific.Enumeration):
    sRGB = 1
    Uncalibrated = 0xFFFF


class EXIFMarkers(enumerific.Enumeration):
    # Generic Segment Prefix
    SegmentPrefix = b"\xff"
    # Start of Image
    SOI = SegmentPrefix + b"\xd8"
    # EXIF Attribute Information (Application Segment 1)
    APP1 = SegmentPrefix + b"\xe1"
    # EXIF Extended Data (Application Segment 2)
    APP2 = SegmentPrefix + b"\xe2"
    # Quantization Table Definition
    DQT = SegmentPrefix + b"\xdb"
    # Huffman Table Definition
    DHT = SegmentPrefix + b"\xc4"
    # Restart Interoperability Definition
    DRI = SegmentPrefix + b"\xdd"
    # Start of Frame
    SOF = SegmentPrefix + b"\xc0"
    # Start of Scan
    SOS = SegmentPrefix + b"\xda"
    # End of Image
    EOI = SegmentPrefix + b"\xd9"


class ExposureMode(enumerific.Enumeration):
    """Exposure mode set when the image was shot."""

    # Auto Exposure
    AutoExposure = 0

    # Manual Exposure
    ManualExposure = 1

    # Auto Bracket
    AutoBracket = 2
