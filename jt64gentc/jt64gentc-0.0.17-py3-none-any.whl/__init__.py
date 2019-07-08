version_info = (0, 0, 17)
__title__ = "jt64gentc"
__version__ = '.'.join(str(c) for c in version_info)
__name__ = "jt64gentc"
__author__ = "Greg Beam, KI7MT"
__license__ = "GPLv3"
__email__ = "ki7mt@yahoo.com"
__summary__ = "Generates Tool Chain files for each QT version supported"

# Supported QT version List
__qt_version_list__ = ['5.12.2', '5.12.3', '5.12.4', '5.13.0']
__qt_version_dict__ = {'5.12.2': 'GCC 7.3.0 x86_64',
                       '5.12.3': 'GCC 7.3.0 x86_64',
                       '5.12.4': 'GCC 7.3.0 x86_64',
                       '5.13.0': 'GCC 7.3.0 x86_64'}
# TODO:
# * Add Method to return __qt_version_dict__ from self-contained applications.
