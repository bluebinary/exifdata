import os

secrets = dict(
    language=os.getenv("LANGUAGE", default="en"),
    country=os.getenv("COUNTRY", default="US"),
    exiftool=os.getenv("EXIFTOOL", default=None),
)
