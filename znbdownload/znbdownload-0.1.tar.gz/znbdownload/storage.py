from storages.backends.s3boto3 import S3Boto3Storage

from django.conf import settings


class S3MediaStorage(S3Boto3Storage):
    """
    Media files stored on Amazon S3.
    See storages.backends.s3boto.S3BotoStorage for other attributes.
    Requires AWS_STORAGE_MEDIA_BUCKET_NAME setting.
    """
    bucket_name = getattr(settings, 'AWS_STORAGE_MEDIA_BUCKET_NAME', '')


class S3PrivateStorage(S3Boto3Storage):
    """
    Private files stored on Amazon S3.
    See storages.backends.s3boto.S3BotoStorage for other attributes.
    Requires AWS_STORAGE_PRIVATE_BUCKET_NAME setting.
    """
    bucket_name = getattr(settings, 'AWS_STORAGE_PRIVATE_BUCKET_NAME', '')
