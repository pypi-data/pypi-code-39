import json
import shutil
import os

from notebook.base.handlers import IPythonHandler
import tornado
import boto3
from botocore.client import Config
from tornado.web import HTTPError

class TestHandler(IPythonHandler):
    def get(self):
        self.write('hello')
        self.flush()

class PublishS3Handler(IPythonHandler):
    def initialize(self, nbapp, access_key, secret_key, endpoint_url, region_name, bucket):
        self.nbapp = nbapp
        self.access_key = access_key
        self.secret_key = secret_key
        self.endpoint_url = endpoint_url
        self.region_name = region_name
        self.bucket = bucket

    def post(self):
        post_data = tornado.escape.json_decode(self.request.body)

        nb_path = post_data['nb_path']
        version = post_data['version']

        self.nbapp.log.info('nb_path: ' + nb_path + ' version: ' + version)
        new_filename = '/published/{}__{}.{}'.format(nb_path.split('.')[0], version, nb_path.split('.')[1])
        self.nbapp.log.info('new path :' + new_filename)

        # s3 put
        # save checkpoint, duplicate file to published folder, rename file, upload
        try: 
            shutil.copy(nb_path, new_filename)
        except IOError as io_err:
            os.makedirs(os.path.dirname(new_filename))
            shutil.copy(nb_path, new_filename)

        s3 = boto3.resource('s3',
                endpoint_url=self.endpoint_url,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                config=Config(signature_version='s3v4'),
                region_name=self.region_name)

        key = new_filename
        if key[0] == '/':
            key = key[1:]

        is_key_exists = True
        try:
            # check if exists
            s3.Bucket(self.bucket).Object(key).last_modified
        except:
            is_key_exists = False

        if is_key_exists:
            raise HTTPError(409, 'version is exists')

        s3.Bucket(self.bucket).upload_file(new_filename, key)
        ret = {
                'uploaded' : new_filename
                }
        self.write(json.dumps(ret))
        self.flush()
        




