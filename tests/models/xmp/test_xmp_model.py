from exifdata.logging import logger
from exifdata.framework import Metadata
from exifdata.models.xmp import XMP

logger = logger.getChild(__name__)


def test_xmp_model(data: callable):
    # The model is dynamically created with the namespaces and fields at import time, so
    # we can start assigning data to the available model namespaced fields, and then use
    # that data to generate a serialized representation of the data for use elsewhere.

    # Create the top-level container for the data model, in this case the XMP model:
    xmp = XMP()

    assert isinstance(xmp, XMP)
    assert isinstance(xmp, Metadata)

    # Assign some property values
    xmp.basic.label = "testing"
    xmp.basic.createDate = "2025-03-21"
    xmp.basic.creatorTool = "exifdata"
    xmp.basic.identifier = "123"
    xmp.basic.metadataDate = "2025-03-21"
    xmp.basic.modifyDate = "2025-03-21"
    xmp.basic.rating = 5
    xmp.basic.baseURL = "https://www.example.com"
    xmp.basic.nickname = "nickname"

    # Ensure that the assigned property values are as expected
    assert xmp.basic.label == "testing"
    assert xmp.basic.createDate == "2025-03-21"
    assert xmp.basic.creatorTool == "exifdata"
    assert xmp.basic.identifier == "123"
    assert xmp.basic.metadataDate == "2025-03-21"
    assert xmp.basic.modifyDate == "2025-03-21"
    assert xmp.basic.rating == 5
    assert xmp.basic.baseURL == "https://www.example.com"
    assert xmp.basic.nickname == "nickname"

    # Encode the XMP payload into its binary form
    encoded: bytes = xmp.encode(pretty=True)
    assert isinstance(encoded, bytes)
    assert len(encoded) > 0

    # Load the previously generated XMP payload that should exactly match the above
    payload: bytes = data("examples/xmp/payload01.xml", binary=True)
    assert isinstance(payload, bytes)
    assert len(payload) > 0

    # Ensure that the newly generated payload matches the previously generated payload
    assert encoded == payload
