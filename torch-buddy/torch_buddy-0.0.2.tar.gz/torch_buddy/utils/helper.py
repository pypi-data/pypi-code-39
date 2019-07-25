import os
import sys
import json
import time
import glob
import argparse
from itertools import chain
from datetime import datetime
from time import strftime, localtime

import numpy as np
import pandas as pd
from IPython.display import display
from sklearn.externals import joblib


# ==============================================================================
# 时间相关
# ==============================================================================
class tick_tock:
    def __init__(self, process_name, verbose=1):
        self.process_name = process_name
        self.verbose = verbose

    def __enter__(self):
        if self.verbose:
            print(self.process_name + " begin ......")
            self.begin_time = time.time()

    def __exit__(self, type, value, traceback):
        if self.verbose:
            end_time = time.time()
            print(self.process_name + " end ......")
            print("time lapsing {0} s \n".format(end_time - self.begin_time))


# ==============================================================================
# 文件相关
# ==============================================================================


def mkdir(path: str):
    """Create directory.

     Create directory if it is not exist, else do nothing.

     Parameters
     ----------
     path: str
        Path of your directory.

     Examples
     --------
     mkdir("data/raw/train")
     """
    try:
        os.stat(path)
    except:
        os.makedirs(path)


def remove_temporary_files(folder_path: str):
    """Remove files begin with ".~".

     Parameters
     ----------
     folder_path: str
        Folder path which you want to clean.

     Examples
     --------
     remove_temporary_files("data/raw/")

    """
    num_of_removed_file = 0
    for fname in os.listdir(folder_path):
        if fname.startswith("~") or fname.startswith("."):
            num_of_removed_file += 1
            os.remove(folder_path + "/" + fname)
    print("{0} file have been removed".format(num_of_removed_file))


def remove_all_files(folder_path: str):
    """Remove all files under folder_path.

     Parameters
     ----------
     folder_path: str
        Folder path which you want to clean.

     Examples
     --------
     remove_all_files("data/raw/")

    """
    folder = folder_path + "*"
    files = glob.glob(folder)
    for file in files:
        os.remove(file)


def save_last_n_files(directory, max_to_keep=10, suffix="*.p"):
    """Save max_to_keep files with suffix in directory

     Parameters
     ----------
     directory: str
        Folder path which you save files.
     max_to_keep: int
        Maximum files to keep.
     suffix: str
        File format.

     Examples
     --------
     save_last_n_files("data/raw/")
    """
    saved_model_files = glob.glob(directory + suffix)
    saved_model_files_lasted_n = sorted(saved_model_files, key=os.path.getctime)[-max_to_keep:]
    files_tobe_deleted = set(saved_model_files).difference(saved_model_files_lasted_n)

    for file in files_tobe_deleted:
        os.remove(file)


def restore(directory, suffix="*.p", filename=None):
    """Restore model from file directory.

     Parameters
     ----------
     directory: str
        Folder path which you save files.
     filename: str
        Filename you want to restore.
     suffix: str
        File format.

     Examples
     --------
     save_last_n_files("data/raw/")
    """
    # If model_file is None, restore the newest one, else restore the specified one.
    if filename is None:
        filename = sorted(glob.glob(directory + suffix), key=os.path.getctime)[-1]
    model = joblib.load(filename)
    print("Restore from file : {}".format(filename))
    return model, filename


# ==============================================================================
# 展示相关
# ==============================================================================
def display_pro(data: pd.DataFrame, n=5):
    """Pro version of display function.

     Display [memory usage], [data shape] and [first n rows] of a pandas dataframe.

     Parameters
     ----------
     data: pandas dataframe
        Pandas dataframe to be displayed.
     n: int
        First n rows to be displayed.

     Example
     -------
     import pandas as pd
     from sklearn.datasets import load_boston
     data = load_boston()
     data = pd.DataFrame(data.data)
     display_pro(data)

        Parameters
        ----------
        data: pandas dataframe


        Returns
        -------
            None
    """
    memory = memory_usage(data, 0)
    print("Data shape   : {}".format(data.shape))
    display(data[:n])


def memory_usage(data: pd.DataFrame, detail=1):
    """Show memory usage.

     Parameters
     ----------
     data: pandas dataframe
     detail: int, optinal (default = 1)
        0: show memory of each column
        1: show total memory

     Examples
     --------
     import pandas as pd
     from sklearn.datasets import load_boston
     data = load_boston()
     data = pd.DataFrame(data.data)
     memory = memory_usage(data)
     """

    memory_info = data.memory_usage()
    if detail:
        display(memory_info)

    if type(memory_info) == int:
        memory = memory_info / (1024 * 1024)
    else:
        memory = data.memory_usage().sum() / (1024 * 1024)
    print("Memory usage : {0:.2f}MB".format(memory))
    return memory


class ProgressBar:
    def __init__(self, n_batch, bar_len=80):
        """Brief description.

        Detailed description.

        Parameters
        ----------
        bar_len: int
            The length you want to display your bar.
        n_batch: int
            Total rounds to iterate.
        Returns
        -------
        None

        Examples
        --------
        import time
        progressBar = ProgressBar(100)

        for i in range(100):
            progressBar.step(i)
            time.sleep(0.1)
        """
        self.bar_len = bar_len
        self.progress_used = 0
        self.progress_remanent = bar_len
        self.n_batch = n_batch

    def step(self, i):
        self.progress_used = int(np.round(i * self.bar_len / self.n_batch))
        self.progress_remanent = self.bar_len - self.progress_used
        sys.stdout.write(
            "\r"
            + ">" * self.progress_used
            + "Epoch Progress: "
            + "{:.2%}".format((i) / self.n_batch)
            + "=" * self.progress_remanent
        )
        sys.stdout.flush()

