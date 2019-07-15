import os
import logging
from contextlib import contextmanager

import boto3

from emporium.base import AbstractStore, Encoding, ChimearicIO
from emporium.utils import select_keys

log = logging.getLogger(__name__)


class RemoteStoreS3(AbstractStore):
    """Store that puts data on S3."""

    # Reuse the client over multiple puts and gets
    _client = None

    def __init__(self, bucket, prefix=None, **extra):
        """Instantiate a store.

        :param bucket: The bucket to store data in.
        :param prefix: The prefix within that bucket, under which to store data.
        :param config: Additional configuration passed to the boto3 client
            constructor.  This might include, `aws_key_id` and
            `aws_secret_access_key`.

        :returns: Instance of a subclass of :class:`~emporium.base.AbstractStore`.
        """

        self._bucket = bucket
        self._prefix = prefix or ""
        self._extra = self._extract_config(extra)

    @classmethod
    def from_config(cls, config):
        return cls(**config)

    @classmethod
    def _extract_config(cls, extra):
        if not extra:
            return {}
        restriction = ["aws_access_key_id", "aws_secret_access_key"]
        return select_keys(extra, *restriction)

    @property
    def s3(self):
        if self._client is None:
            log.info(
                "Creating S3 client with access key ID: %s",
                self._extra.get("aws_access_key_id"),
            )
            self._client = boto3.client("s3", **self._extra)
        return self._client

    @contextmanager
    def read(self, path, encoding=Encoding.STRING):
        key = self._expand_path(path)
        response = self.s3.get_object(Bucket=self._bucket, Key=key)
        yield response["Body"]

    @contextmanager
    def write(self, path, encoding=Encoding.STRING):
        resource = ChimearicIO()
        yield resource
        resource.seek(0)
        key = self._expand_path(path)
        self.s3.put_object(Body=resource, Bucket=self._bucket, Key=key)

    def _expand_path(self, path):
        return os.path.join(self._prefix, path)

    def __repr__(self):
        return "<{}({}:{})>".format(self.__class__.__name__, self._bucket, self._prefix)
