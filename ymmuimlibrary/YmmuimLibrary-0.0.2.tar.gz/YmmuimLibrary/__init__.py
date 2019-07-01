# _*_ coding=utf-8 _*_
__author__  = "8034.com"
__date__    = "2019-07-01"

# from YmmuimLibrary.keywords import *
from YmmuimLibrary.keywords import _YmmiumKeywords
from AppiumLibrary.version import VERSION

__version__ = VERSION

class YmmuimLibrary(_YmmiumKeywords):
    """"""

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self, run_on_failure='Capture Page Screenshot'):
        """YmmuimLibrary can be imported with optional arguments.

        Examples:
        | Library | AppiumLibrary | 10 | # Sets default timeout to 10 seconds                                                                             |
        | Library | AppiumLibrary | timeout=10 | run_on_failure=No Operation | # Sets default timeout to 10 seconds and does nothing on failure           |
        """
        for base in YmmuimLibrary.__bases__:
            base.__init__(self)
        self.click_element("name")
    pass