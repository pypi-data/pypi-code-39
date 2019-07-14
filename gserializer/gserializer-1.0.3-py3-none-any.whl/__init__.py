__version__ = "1.0.0"
from gserializer.Tools.Filter import Filter
from gserializer.Tools.Reader import Reader

def init():
    print("Welcome to the GoogleSheetsSerializer v1.0 beta by Paul Shao")

def create_reader():
    return Reader()

def create_filter(r):
    if not isinstance(r, Reader):
        print("input must be of type Reader")
        return
    return Filter(r)

if __name__ == "__init__":
    init()
