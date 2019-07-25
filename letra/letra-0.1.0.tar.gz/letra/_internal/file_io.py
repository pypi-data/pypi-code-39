from .yaml import read as read_yaml, write as write_yaml
from os import getcwd
from os.path import abspath, join, exists as path_exists
from string import Template


def get_path(filepath):
    if path_exists(filepath):
        return filepath
    else:
        path = abspath(join(getcwd(), filepath))
        if path_exists(path):
            return path
        else:
            raise ValueError(
                "Specified template file not found.\n"
                f"Checked relative path: '{filepath}' "
                f"and absolute path: '{path}'"
            )


def read_templates_from_file(filepath):
    return read_yaml(get_path(filepath))


def write_templates_to_file(labels, filepath):
    return write_yaml({"labels": labels}, filepath)
