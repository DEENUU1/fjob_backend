from django.conf import settings
from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize = value.size

    if filesize > settings.MAX_IMAGE_SIZE:
        raise ValidationError("Max file size is 5 MB")
