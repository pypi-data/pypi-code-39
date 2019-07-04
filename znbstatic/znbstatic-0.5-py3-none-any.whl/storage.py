from django.contrib.staticfiles.storage import StaticFilesStorage
from django.utils.deconstruct import deconstructible
from django.conf import settings

from storages.backends.s3boto3 import S3Boto3Storage
from znbstatic.utils import add_version_to_url


@deconstructible
class VersionedStaticFilesStorage(StaticFilesStorage):
    """
    A static file system storage backend that appends
    the value from the ZNBSTATIC_VERSION setting.

    The storage class must be deconstructible.
    See `<https://docs.djangoproject.com/en/2.1/howto/custom-file-storage/>`_.
    """
    def url(self, name):
        url = super(VersionedStaticFilesStorage, self).url(name)
        version = getattr(settings, 'ZNBSTATIC_VERSION', '0.0')
        return add_version_to_url(url, version)


@deconstructible
class VersionedS3StaticFilesStorage(S3Boto3Storage):
    """
    A static file system storage backend that stores files on Amazon S3 and
    appends the value from the ZNBSTATIC_VERSION setting.

    The storage class must be deconstructible.
    See `<https://docs.djangoproject.com/en/2.1/howto/custom-file-storage/>`_.

    Using bucket_name attribute to override default AWS_STORAGE_BUCKET_NAME setting.
    See S3Boto3Storage for other available attributes.
    """

    bucket_name = getattr(settings, 'AWS_STORAGE_STATIC_BUCKET_NAME', '')

    def url(self, name):
        url = super(VersionedS3StaticFilesStorage, self).url(name)
        version = getattr(settings, 'ZNBSTATIC_VERSION', '0.0')
        return add_version_to_url(url, version)
