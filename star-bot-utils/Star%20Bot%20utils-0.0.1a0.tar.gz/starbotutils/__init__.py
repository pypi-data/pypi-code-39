from os import listdir
raw_default_exts = listdir("default_exts")
default_exts_names = []
p = "starbotutils.default_exts."
for ext in raw_default_exts:
    default_exts_names.append(p+ext)


from .embed import em
from .main import StarBot
from .db import DataBase
from . import default_exts