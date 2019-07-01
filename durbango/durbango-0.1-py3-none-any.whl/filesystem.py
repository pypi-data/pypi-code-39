from pathlib import Path

import numpy as np
import pandas as pd
import pickle
Path.ls = property(lambda self: sorted(list(self.iterdir())))
from .nb_utils import tqdm_nice
import tarfile

def read_pickle(path):
    """pickle.load(path)"""
    with open(path, 'rb') as f:
        return pickle.load(f)


def write_pickle(X, path):
    """pickle.dump(X, path)"""
    with open(path, 'wb') as f:
        return pickle.dump(X, f)

def read_msgpack(path):
    # Fix bug where saving nans in msgpack get converted
    return pd.read_msgpack(path).fillna(np.nan)


# add some aliases to alleviate confusion
pickle_read = read_pickle
load_pickle = read_pickle
save_pickle = write_pickle
pickle_save = write_pickle


def make_directory_if_not_there(path) -> None:
    Path(path).mkdir(exist_ok=True)



def make_dir_structure_under(path) -> None:
    """Uses p.parent.mkdir(parents=True, exist_ok=True)."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)




def tar_compress(folder_path, save_path=None):

    folder_path = Path(folder_path)
    if save_path is None: save_path = f'{folder_path}.tgz'
    with tarfile.open(save_path, "w:gz") as tar:
        if folder_path.is_dir():
            for name in tqdm_nice(folder_path.ls):
                tar.add(str(name))
        else:
            tar.add(str(folder_path))

