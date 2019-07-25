from cnvrg.modules.data_connector.base_connector import BaseConnector
import cnvrg.modules.errors as errors
import os
is_loaded = False
try:
    import boto3
    is_loaded = True

except ImportError:
    is_loaded = False



class S3BucketConnector(BaseConnector):

    @staticmethod
    def key_type():
        return "s3_bucket"
    def __init__(self, data_connector, prefix=None, working_dir=None):
        super(S3BucketConnector, self).__init__(data_connector)
        self.client = None
        self.__files = []
        self.__prefix = prefix
        self.__working_dir = os.path.join(working_dir or "/data", self._data_connector)
        os.makedirs(self.__working_dir, exist_ok=True)
        self.__connect(**self.data)

    def __connect(self, access_key_id=None, secret_access_key=None, session_token=None, region=None, bucket=None, **kwargs):
        if not is_loaded: raise errors.CnvrgError("Cant load boto3 library.")
        self.data = {"aws_access_key_id": access_key_id, "aws_secret_access_key": secret_access_key, "aws_session_token": session_token, "region_name": region, "bucket": bucket}


    def get_bucket(self):
        return S3BucketConnector.bucket(**self.data)

    def get_client(self):
        return S3BucketConnector.client(**self.data)

    @staticmethod
    def client(**data):
        return boto3.client('s3', aws_access_key_id=data.get("key"), aws_secret_access_key=data.get("secret"), aws_session_token=data.get("session_token"), region_name=data.get("region"))

    @staticmethod
    def session(**data):
        return boto3.Session(aws_access_key_id=data.get("key"), aws_secret_access_key=data.get("secret"), aws_session_token=data.get("session_token"), region_name=data.get("region"))

    @staticmethod
    def bucket(bucket=None, **data):
        return S3BucketConnector.session(**data).resource('s3').Bucket(bucket)


    def list_files(self, prefix=None):
        self.__files = []
        prefix = prefix or self.__prefix
        for o in self.get_bucket().objects.filter(Prefix=prefix or ''):
            self.__files.append(o.key)
        return self.__files

    def __len__(self):
        if len(self.__files) == 0: self.list_files()
        return len(self.__files)

    def __getitem__(self, item):
        storage_path = self.__files[item]
        local_path = os.path.join(self.__working_dir, storage_path)
        return self.download_file(storage_path, local_path)

    def download_file(self, storage_path, local_path):
        client = S3BucketConnector.client(**self.data)
        if os.path.exists(local_path):
            return local_path
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        client.download_file(self.data.get("bucket"), storage_path, local_path)
        return local_path
