import oss2


class OSS(object):
    """
    aliyun oss sdk
    """

    def __init__(self, access_key_id, access_key_secret, bucket_name, endpoint):
        self.bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
        self.get_file_expires = 3600 * 24

    def get(self, file_path):
        """
        从oss获取文件的url
        :param file_path: 文件的oss存储路径
        """
        return self.bucket.sign_url('GET', file_path, self.get_file_expires)

    def upload(self, file_path, file):
        """
        上传文件到oss
        :param file_path: 文件的oss存储路径
        :param file: 上传文件
        :return: 上传状态
        """
        result = self.bucket.put_object(key=file_path, data=file)
        if result.status == 200:
            return True
        else:
            return False
