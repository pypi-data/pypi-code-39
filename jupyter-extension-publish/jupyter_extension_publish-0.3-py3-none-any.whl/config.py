from traitlets import Integer, Unicode, Bool
from traitlets.config import LoggingConfigurable


class PublishSettings(LoggingConfigurable):
    s3_access_key_id = Unicode(
        help="S3/AWS access key ID", allow_none=True, default_value=None
    ).tag(config=True, env="JPYNB_S3_ACCESS_KEY_ID")
    s3_secret_access_key = Unicode(
        help="S3/AWS secret access key", allow_none=True, default_value=None
    ).tag(config=True, env="JPYNB_S3_SECRET_ACCESS_KEY")

    s3_endpoint_url = Unicode("https://s3.amazonaws.com", help="S3 endpoint URL").tag(
        config=True, env="JPYNB_S3_ENDPOINT_URL"
    )
    s3_region_name = Unicode("us-east-1", help="Region name").tag(
        config=True, env="JPYNB_S3_REGION_NAME"
    )
    s3_bucket = Unicode("", help="Bucket name to store notebooks").tag(
        config=True, env="JPYNB_S3_BUCKET"
    )

    def __init__(self, *args, **kwargs):
        self.config_manager = kwargs.pop('config_manager')
        super(PublishSettings, self).__init__(*args, **kwargs)
