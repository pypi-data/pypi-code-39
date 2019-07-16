# coding=utf8

import os
import configparser

database_engines = {
    'sqlite3': 'django.db.backends.sqlite3',
    'mysql': 'django.db.backends.mysql',
    'postgres': 'django.db.backends.postgres'
}


def _dict_getter(dic_, item):
    return dic_.get(item, item)


class DjangoSettingsReader:
    def __init__(self, file_path):
        if not os.path.exists(file_path):
            raise Exception('File: {} is not found.'.format(file_path))
        self.cp = configparser.ConfigParser()
        self.cp.read(file_path, encoding='utf8')

    def read_database(self, section):
        engine = self.cp.get(section, 'ENGINE')
        return {
            'ENGINE': _dict_getter(database_engines, engine),
            'HOST': self.cp.get(section, 'HOST'),
            'PORT': self.cp.get(section, 'PORT'),
            'USER': self.cp.get(section, 'USER'),
            'PASSWORD': self.cp.get(section, 'PASSWORD'),
            'NAME': self.cp.get(section, 'NAME')
        }
