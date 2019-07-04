import logging
from django.db import models

from .storage import S3PrivateStorage

logger = logging.getLogger(__name__)


class S3PrivateFileField(models.FileField):
    """
    A FileField with a default 'private' ACL to the files it uploads to S3, instead of the default ACL.
    You can pass also pass 'public-read' for testing but it may be confusing.
    """

    def __init__(self, verbose_name=None, name=None, upload_to='', storage=None, default_acl='private', **kwargs):
        self.storage = storage or S3PrivateStorage(default_acl)
        super().__init__(verbose_name=verbose_name, name=name, upload_to=upload_to, storage=self.storage, **kwargs)
