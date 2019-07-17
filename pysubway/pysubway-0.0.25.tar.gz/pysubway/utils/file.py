import io
import os
import tempfile
from typing import TextIO, Union, Tuple

import chardet
from chardet.gb2312prober import GB2312Prober
from chardet.latin1prober import Latin1Prober

try:
    from utils.ustring import replace_chinese_comma
except (ImportError, ModuleNotFoundError) as e:
    from pysubway.utils.ustring import replace_chinese_comma


def file_dirname(file: str) -> str:
    return os.path.split(file)[0]


def join_path(dirname: str, *path: str) -> str:
    return os.path.join(dirname, *path)


class File:
    file_dirname = staticmethod(file_dirname)
    join_path = staticmethod(join_path)

    gdk_compatibility = [
        # ascii
        Latin1Prober().charset_name,
        # gbk
        GB2312Prober().charset_name,
        'ISO-8859-9',
    ]

    def __init__(self, file: Union[str, TextIO]):
        self.file: Union[str, TextIO] = file
        self.dirname, self.filename = os.path.split(self.file) if isinstance(self.file, str) else ('', '')
        self.pure_name, self.suffix = self.get_pure_name_and_suffix(self.filename)
        self._encoding: str = ''

    @staticmethod
    def get_pure_name_and_suffix(filename: str) -> Tuple[str, str]:
        split = filename.split('.')
        if len(split) == 1:
            split.append('')
        return split[0], split[-1]

    @property
    def encoding(self) -> str:
        """
        {'encoding': 'ascii', 'confidence': 1.0, 'language': ''}
        :param self:
        :return:
        """
        if not self._encoding:
            if isinstance(self.file, str):
                with open(self.file, mode='rb') as f:
                    # must read all, or the detect result is imprecision
                    encoding = chardet.detect(f.read())
                    self._encoding = 'gbk' if encoding in self.gdk_compatibility else 'utf-8'
        return self._encoding

    def remove_chinese_comma(self, output: str = 'io') -> Union[str, TextIO, io.StringIO]:
        f: TextIO = io.StringIO()
        try:
            # if not str, treat self.file as TextIO
            f = open(self.file) if isinstance(self.file, str) else self.file
            s = replace_chinese_comma(f.read())
            if output != 'io':
                temp = tempfile.NamedTemporaryFile(mode='w', delete=False, encoding=self.encoding)
                temp.write(s)
                temp.close()
                return temp.name
            else:
                temp = io.StringIO()
                temp.write(s)
                temp.seek(0)
                return temp
        finally:
            f.close()

    @staticmethod
    def this_dir(path: str) -> str:
        """
        return current file dirname
        you can call this method like this_dir(__file__)
        :return: str
        """
        return os.path.dirname(os.path.abspath(path))


class Open(File):
    """
    example:
    >>>with File(__file__) as f:
    >>> for i in range(10):
    >>>     print(f.readline())
    """

    def __init__(self, file: Union[str, TextIO]):
        super().__init__(file)
        self.f = self.file if isinstance(self.file, (io.StringIO, TextIO)) else open(self.file, encoding=self.encoding)

    def __enter__(self) -> TextIO:
        return self.f

    def __exit__(self, exc_type: str, exc_val: str, exc_tb: str) -> None:
        self.f.close()
