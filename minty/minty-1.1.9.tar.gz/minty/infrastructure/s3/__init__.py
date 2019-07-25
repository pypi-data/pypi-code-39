__version__ = "0.0.1"

from minty import Base
from minty.exceptions import ConfigurationConflict

from .s3wrapper import S3Wrapper


class S3Infrastructure(Base):
    """Infrastructure Class for S3 Connection."""

    def __call__(self, config):
        """Create a new S3 connection using the specified configuration

        :param config: The configuration params necessary to connect to a S3 bucket.
        :return: A S3 handle for a bucket on a connection to an S3 server.
        :rtype: S3Wrapper
        """

        try:
            filestore_config = config["filestore"]
            if type(filestore_config) is not list:
                filestore_config = [filestore_config]
        except KeyError as error:
            raise ConfigurationConflict(
                "Invalid configuration for S3 found"
            ) from error

        return S3Wrapper(filestore_config=filestore_config)
