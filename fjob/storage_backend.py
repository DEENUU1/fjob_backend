from storages.backends.s3boto3 import S3Boto3Storage


class PublicMediaStorage(S3Boto3Storage):
    """
    Custom storage class for handling media files stored in an S3 bucket.

    Attributes:
    - location: The S3 bucket directory where media files will be stored.
    - file_overwrite: Flag indicating whether to overwrite existing files with the same name.
    """

    location = "media"
    file_overwrite = False
