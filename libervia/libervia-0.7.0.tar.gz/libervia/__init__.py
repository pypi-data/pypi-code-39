import os.path

version_file = os.path.join(os.path.dirname(__file__), "VERSION")
try:
    with open(version_file) as f:
        __version__ = f.read().strip()
except NotImplementedError:
    # pyjamas workaround
    __version__ = "0.7.0D"
