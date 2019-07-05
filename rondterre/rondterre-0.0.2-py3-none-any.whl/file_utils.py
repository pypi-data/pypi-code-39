# -*- coding: utf-8 -*-

import os
import warnings


def check_file_existence(path_):
    if not os.path.isfile(path_):
        raise FileNotFoundError(path_)


def check_dir_existence(path_):
    if not os.path.isdir(path_):
        raise FileNotFoundError(path_)


def mkdir(path_):
    if not os.path.exists(path_):
        os.makedirs(path_)
        return True
    else:
        warnings.warn(path_, ' already exists!')
        return False


if __name__ == "__main__":
    pass
