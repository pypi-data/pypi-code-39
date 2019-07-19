import logging
from contextlib import contextmanager
from posixpath import join as url_join
import boto3

import smart_open as smart

from emporium.base import AbstractStore
from emporium.utils import select_keys

log = logging.getLogger(__name__)


class RemoteStoreS3(AbstractStore):
    """Store that puts data on S3."""

    def __init__(self, bucket, prefix=None, **extra):
        """Instantiate a store.

        :param bucket: The bucket to store data in.
        :param prefix: The prefix within that bucket, under which to store data.
        :param extra: Additional configuration passed to the boto3 session
            constructor.  This might include, `aws_key_id` and
            `aws_secret_access_key`.

        :returns: Instance of a subclass of :class:`~emporium.base.AbstractStore`.
        """

        self._bucket = bucket
        self._prefix = None if not prefix else prefix.lstrip("/")
        self._extra = self._extract_config(extra)

    @classmethod
    def from_config(cls, config):
        return cls(**config)

    @contextmanager
    def open(self, path, mode, *args, **kwargs):
        uri = self._uri(path)
        transport_params = self._create_transport_params()
        transport_params.update(kwargs.get("transport_params", {}))
        if transport_params:
            kwargs["transport_params"] = transport_params
        with smart.open(uri, mode, *args, **kwargs) as handle:
            yield handle

    def substore(self, path):
        subpath = url_join(self._prefix, path.lstrip("/"))
        return RemoteStoreS3(self._bucket, subpath, **self._extra)

    @classmethod
    def _extract_config(cls, extra):
        if not extra:
            return {}
        restriction = ["aws_access_key_id", "aws_secret_access_key"]
        return select_keys(extra, *restriction)

    def _create_transport_params(self):
        if self._extra:
            return {"session": boto3.Session()}
        return {}

    def _uri(self, path=None):
        segments = [s.lstrip("/") for s in [self._bucket, self._prefix, path] if s]
        return "s3://{}".format(url_join(*segments))

    def __repr__(self):
        return "<{}({})>".format(self.__class__.__name__, self._uri())
