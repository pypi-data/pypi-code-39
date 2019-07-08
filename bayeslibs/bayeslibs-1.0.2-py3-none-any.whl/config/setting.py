# conding=utf-8
"""
@project:bayeslibs
@language:Python3
@create:2019/5/30
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
import yaml
from bayeslibs.config import const
from bayeslibs.utils.pattern.code_design import singleton
import os

HEAR = os.path.abspath(os.path.dirname(__file__))
APOLLO_INI_PATH = os.path.join(HEAR, const.APOLLO_INI)


class YamlParser:
    def __init__(self, file_path, encoding='utf-8'):
        self.file_path = file_path
        self.encoding = encoding
        self.config = self.read(file_path, encoding)

    @staticmethod
    def read(file_path, encoding):
        try:
            with open(file_path, 'r', encoding=encoding) as fp:
                config = yaml.load(fp, Loader=yaml.SafeLoader)
            return config
        except FileNotFoundError as err:
            print('file open error:{}'.format(err))
            return None

    def get(self, section, option=None):
        try:
            if not self.config:
                print('Please open a yaml file first')
                return False
            if section not in self.config.keys():
                print('section {} not in yaml file, please add first'.format(section))
                return False
            elif not option:
                return self.config[section]
            elif option not in self.config[section].keys():
                print('sub_section {} not in yaml file, please add first')
                return False
            else:
                return self.config[section][option]
        except Exception as err:
            print('Some unexpected error happen:{}'.format(err))
            return None

    def set_option(self, section, option, value):
        if not self.config:
            print('Please open a yaml file first')
            return False
        if section not in self.config.keys():
            self.config[section] = dict()
        self.config[section][option] = value
        return True

    def set(self, section, option=None, **kwargs):
        try:
            if not self.config:
                print('Please open a yaml file first')
                return False
            if section not in self.config.keys():
                self.config[section] = dict()
            if not option and kwargs:
                for item, value in kwargs.items():
                    self.config[section][item] = value
                return True
            if option and option not in self.config[section].keys():
                self.config[section][option] = dict()
            for item, value in kwargs.items():
                self.config[section][option][item] = value
            return True
        except Exception as err:
            print('Some unexpected error happen:{}'.format(err))
            return None

    def write(self):
        with open(self.file_path, 'w', encoding=self.encoding) as fw:
            yaml.dump(self.config, fw)


@singleton
class ApolloConfig:

    def __init__(self, yaml_path=None):
        self.__yaml_parser = YamlParser(APOLLO_INI_PATH) if not yaml_path else YamlParser(yaml_path)
        self.__ip = self.__yaml_parser.get(const.APOLLO_T200, const.IP)
        self.__port = self.__yaml_parser.get(const.APOLLO_T200, const.PORT)
        self.__apollo_url = 'http://{}:{}'.format(self.__ip, self.__port)
        self.__appid = self.__yaml_parser.get(const.ACCESS_AUTH, const.APPID)
        self.__appkey = self.__yaml_parser.get(const.ACCESS_AUTH, const.APPKEY)
        self.__max_dist = self.__yaml_parser.get(const.MOTION, const.MAX_DIST)
        self.__max_angle = self.__yaml_parser.get(const.MOTION, const.MAX_ANGLE)

    def set_apollo_url(self, ip, port):
        self.__ip = ip
        self.__port = port
        self.__apollo_url = 'http://{}:{}'.format(ip, port)
        self.__yaml_parser.set(const.APOLLO_T200, ip=ip, port=port)
        self.save()

    def set_apollo_access(self, appid, appkey=None):
        self.__appid = appid
        self.__yaml_parser.set(const.ACCESS_AUTH, appid=appid, appkey=appkey)
        self.save()

    def set_nav_pos(self, dest, x, y):
        self.__yaml_parser.set(const.NAV_POS, option=dest, x=x, y=y)
        self.save()

    def set_common_option(self, section, option, value):
        self.__yaml_parser.set_option(section, option, value)
        self.save()

    def get_apollo_url(self):
        return self.__apollo_url

    def get_appid(self):
        return self.__appid

    def get_appkey(self):
        return self.__appkey

    def get_nav_pos_map(self):
        return self.__yaml_parser.get(const.NAV_POS)

    def get_nav_pos(self, dest):
        return self.__yaml_parser.get(const.NAV_POS)[dest]

    def get_robot_route_url(self, route):
        return '{}/bayes/{}'.format(self.__apollo_url, route)

    def get_max_dist(self):
        return self.__max_dist

    def get_max_angle(self):
        return self.__max_angle

    def save(self):
        self.__yaml_parser.write()
