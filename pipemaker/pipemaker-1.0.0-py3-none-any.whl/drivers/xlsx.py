import fs
import pandas as pd

def save(self, obj):
    """ save pandas dataframe locally """
    if not isinstance(self.fs, fs.osfs.OSFS):
        raise Exception(f"No excel driver for {self.fs}. You can add one in the drivers folder.")
    obj.to_excel(self.path)

def load(self):
    """ load pandas dataframe locally """
    if not isinstance(self.fs, fs.osfs.OSFS):
        raise Exception(f"No excel driver for {self.fs}. You can add one in the drivers folder.")
    return pd.read_excel(self.path)