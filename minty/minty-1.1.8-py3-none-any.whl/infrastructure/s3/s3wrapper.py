import os

import boto3
from botocore.client import Config

import minty.infrastructure.mime_utils as mu
from minty import Base
from minty.exceptions import ConfigurationConflict


class S3Wrapper(Base):
    def __init__(self, filestore_config: list):
        self.filestore_config = filestore_config
        config_keys = [
            "location_name",
            "bucket_name",
            "endpoint_url",
            "access_id",
            "access_key",
            "addressing_style",
        ]
        try:
            self.location_name, self.bucket_name, self.endpoint_url, self.access_id, self.access_key, self.addressing_style = [
                self.filestore_config[0][k] for k in config_keys
            ]
        except KeyError as error:
            raise ConfigurationConflict(
                "Invalid configuration for S3 found"
            ) from error

    def upload(self, file_handle, uuid):
        timer = self.statsd.get_timer("file_upload")
        with timer.time("s3_upload"):
            # config = Config(addressing_style=self.addressing_style)

            s3_client = boto3.session.Session().client(
                service_name="s3",
                aws_access_key_id=self.access_id,
                aws_secret_access_key=self.access_key,
                # region_name=region,
                endpoint_url=self.endpoint_url,
                config=Config(
                    s3={
                        "addressing_style": self.addressing_style,
                        # "signature_version": signature_version,
                    }
                ),
            )
            response_dict = s3_client.put_object(
                Body=file_handle, Bucket=self.bucket_name, Key=uuid
            )

        file_handle.seek(0, os.SEEK_END)
        total_size = file_handle.tell()

        return {
            "uuid": uuid,
            "md5": response_dict["ETag"][1:-1],
            "size": total_size,
            "mime_type": mu.get_mime_type_from_handle(file_handle),
            "storage_location": self.location_name,
        }
