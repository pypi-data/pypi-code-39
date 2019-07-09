import os
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import pickle
Path.ls = property(lambda self: sorted(list(self.iterdir())))
from .nb_utils import tqdm_nice


def read_pickle(path):
    """pickle.load(path)"""
    with open(path, 'rb') as f:
        return pickle.load(f)


def write_pickle(obj, path):
    """pickle.dump(obj, path)"""
    with open(path, 'wb') as f:
        return pickle.dump(obj, f)

def pickle_load_gzip(path):
    import gzip
    with gzip.open(path, 'rb') as f:
        return pickle.load(f, encoding='latin-1')

# add some aliases to alleviate confusion
pickle_read = read_pickle
pickle_load = read_pickle
save_pickle = write_pickle
pickle_save = write_pickle


def make_directory_if_not_there(path) -> None:
    Path(path).mkdir(exist_ok=True)

def make_dir_structure_under(path) -> None:
    """Uses p.parent.mkdir(parents=True, exist_ok=True)."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)


def tar_compress(folder_path, save_path=None):
    import tarfile
    folder_path = Path(folder_path)
    if save_path is None: save_path = f'{folder_path}.tgz'
    with tarfile.open(save_path, "w:gz") as tar:
        if folder_path.is_dir():
            for name in tqdm_nice(folder_path.ls):
                tar.add(str(name))
        else:
            tar.add(str(folder_path))


def get_git_rev(root='.'):
    '''try to return the current git rev, or None if not a git branch'''

    git_dir = os.path.join(root, '.git')
    if not os.path.exists(git_dir):
        print('found no .git at {}'.format(git_dir))
        return None

    # copy os.environ to avoid setting GIT_DIR for future subprocesses
    env = dict(os.environ)
    env['GIT_DIR'] = git_dir
    return subprocess.check_output(['git', 'rev-parse', 'HEAD'], env=env).strip()
