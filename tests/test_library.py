from exifdata import (
    Models,
    Metadata,
    EXIF,
    IPTC,
    XMP,
)

from exifdata.adapters import (
    TIFFData,
)


def test_exifdata_models_initialisation(path: callable):
    filepath: str = path("test.tiff")

    models = Models.adapt(TIFFData).open(filepath, decode=False)

    assert isinstance(models, Models)

    assert isinstance(models.exif, EXIF)
    assert isinstance(models.exif, Metadata)

    assert isinstance(models.iptc, IPTC)
    assert isinstance(models.iptc, Metadata)

    assert isinstance(models.xmp, XMP)
    assert isinstance(models.xmp, Metadata)
