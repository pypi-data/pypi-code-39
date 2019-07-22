import json
import os
import boto3
import botocore
from boto3.session import Session
from .collections import OrderedSet

class S3Values():
    def __init__(self, namespace, chart, app, region=False, extra_files=[], extra_values=[]):
        self.namespace = namespace
        self.chart = chart.split('/').pop()
        self.app = app
        self.extra_files = extra_files
        self.extra_values = extra_values
        self.namespace_size = len(self.namespace.split('-'))
        self.region = region

    def download_values(self, src, dest):
        session = Session(region_name="eu-west-2")
        s3 = session.resource('s3')
        source_bucket = s3.Bucket(src)
        #s3 = boto3.client('s3', aws_region="eu-west-2")
        downloaded = []
        if self.region:
            required_files = list(OrderedSet(self.get_all_paths() + self.get_all_paths(self.region)))
        else:
            required_files = self.get_all_paths()

        for extra_values_file in self.extra_values:
            required_files.append(extra_values_file.strip('/'))

        s3list = self.get_s3_objects_as_list(source_bucket.objects.all())

        for required_file in required_files:
            if required_file in s3list:
                destination = dest + '/' + required_file
                destination_folder = os.path.dirname(destination)
                if os.path.exists(destination_folder) == False:
                    os.makedirs(destination_folder)
                source_bucket.download_file(required_file, destination)
                downloaded.append(destination)

        return downloaded

    def get_s3_objects_as_list(self, s3_objects):
        s3list = []
        for s3_object in s3_objects:
            s3list.append(s3_object.key)
        return s3list

    def get_all_paths(self, root=''):
        paths = []
        path_parts = self.get_path_parts()
        level = 0
        for index, path_part in enumerate(path_parts):
            level += 1
            path = root + '/' + path_part
            path = path.strip('/')
            if level > 0:
                paths.append(path + '/common.yaml')
            if level > 1 and level < self.namespace_size:
                paths.append(path + '/_' + self.chart + '/common.yaml')

            if level > self.namespace_size:
                for extra_file in self.extra_files:
                    extra_file = os.path.splitext(extra_file)[0]
                    paths.append(path + '/' + extra_file + '.yaml')
                paths.append(path + '/' + self.app + '.yaml')

            root = path

        return paths

    def get_path_parts(self):
        parts = self.namespace.split('-')
        parts.append(self.chart)
        parts.append(self.app)
        return parts

