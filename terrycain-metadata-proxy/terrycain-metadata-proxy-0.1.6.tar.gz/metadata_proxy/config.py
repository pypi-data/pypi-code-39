from collections import abc


class Config(object):
    def load_config(self):
        raise NotImplementedError()

    def save_config(self):
        raise NotImplementedError()

