import os
from typing import Dict, Any

import chardet
from chardet.gb2312prober import GB2312Prober
from chardet.latin1prober import Latin1Prober


class Open:
    """
    example:
    >>>with Open(__file__) as f:
    >>> for i in range(10):
    >>>     print(f.readline())
    """

    def __init__(self, file):
        self.file = file
        self._encoding_type = None
        self.encoding = 'utf-8'
        self.file_encoding_type = self.encoding_type['encoding']
        self.gdk_compatibility = [
            # ascii
            Latin1Prober().charset_name,
            # gbk
            GB2312Prober().charset_name,
            'ISO-8859-9',
        ]
        if self.file_encoding_type in self.gdk_compatibility:
            self.encoding = 'gbk'
        try:
            self.f = open(self.file, encoding=self.encoding)
        except UnicodeEncodeError as e:
            print(e)
            self.f = open(self.file, encoding=self.file_encoding_type)

    @property
    def encoding_type(self) -> Dict[str, Any]:
        """
        {'encoding': 'ascii', 'confidence': 1.0, 'language': ''}
        :param self:
        :return:
        """
        if not self._encoding_type:
            with open(self.file, mode='rb') as f:
                # must read all, or the detect result is imprecision
                self._encoding_type = chardet.detect(f.read())
        return self._encoding_type

    def __enter__(self):
        return self.f

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.f.close()


def file_dirname(file):
    return os.path.split(file)[0]


def join_path(dirname, filename):
    return os.path.join(dirname, filename)
