# encoding: UTF-8
import csv
import os
import sys
import threading
import logging
from .path import Path

_logger = logging.getLogger(__name__)


class FilterNullReader:
    '''过滤null字符防止 csv 读取报错'''

    def __init__(self, iterable):
        if hasattr(iterable, '__next__'):
            self.iterator = iterable
        else:
            self.iterator = iter(iterable)

    def __iter__(self):
        return self

    def __next__(self):
        val = next(self.iterator)
        if isinstance(val, str):
            val = val.replace('\x00', '')
        return val


class Storage(object):
    '''
    提供简单可靠的字符串数据持久化功能。

    数据类似字符串字典，可更新、删除。
    可以像 dict 一样使用，其中涉及数据修改的函数支持 clear pop setdefault 。
    支持多线程，但不要使用同一文件创建多个实例。

    使用 csv 格式读写文件，可设置编码 encoding 。
    平时只追加数据到文件末尾，希望能避免系统异常时覆写数据。
    可以适时手动压缩数据，将以比较可靠谨慎的方式覆写文件。

    为了减少异常文件的影响，解析 csv 前过滤掉了null字符。
    '''

    def __init__(self, filePath, encoding=sys.stdout.encoding, load=True, logger=None):
        '''
        创建仓库实例，绑定一个 csv 数据文件。
        @param load 立即加载数据
        '''
        self.encoding = encoding
        self._filePath = Path(os.path.abspath(filePath))
        self._filename = os.path.basename(filePath)
        self._dirPath = self._filePath.join('..')
        self._lock = threading.RLock()
        self._data = {}
        self._recordCount = 0
        self.logger = logger if logger else _logger
        if load:
            self.reload()
        return

    def reload(self):
        '''重新从文件加载数据'''
        self._lock.acquire()
        try:
            if not os.path.exists(self._dirPath):
                os.makedirs(self._dirPath)
            if os.path.isfile(self._filePath):
                self._readData(self._filePath)
        finally:
            self._lock.release()

    def _readData(self, path):
        '''读取异常情况，目前只能中止，保留已读结果。'''
        data = {}
        recordCount = 0
        try:
            with open(path, 'r', encoding=self.encoding) as file:
                for line in csv.reader(FilterNullReader(file)):
                    if len(line) < 1:
                        continue
                    try:
                        version = line[0]
                        if version == '1':
                            op = line[1]
                            key = line[2]
                            if op == 'u':
                                data[key] = line[3]
                            elif op == 'd':
                                del data[key]
                            else:
                                raise Exception(
                                    'unsupported operation "%s"' % (op))
                        else:
                            raise Exception(
                                'unsupported data version "%s"' % (version))
                        recordCount += 1
                    except Exception:
                        pass
        except Exception as e:
            self.logger.warning(e)
            raise
        finally:
            # 保存已读数据
            self._data = data
            self._recordCount = recordCount

    def compress(self):
        '''压缩数据文件，相当于删除历史记录，每条数据只保留他本身。
        确保可靠：
        1.把数据写出到临时文件
        2.重新读取原文件数据，与内存数据对比，无误则继续
        3.用多次重命名文件的方式慎重地覆盖原文件'''
        self._lock.acquire()
        try:
            # 1.写出到临时文件
            compName = self._filename + '.compress'
            compPath = self._dirPath.join(compName)
            with open(compPath, 'w', newline='', encoding=self.encoding) as compFile:
                compWriter = csv.writer(compFile)
                for key, item in self._data.items():
                    compWriter.writerow(['1', 'u', key, item])

            # 2.重新读原文件进行对比
            data = self._data
            try:
                self._readData(self._filePath)
            except Exception as e:
                self.logger.info(
                    'Exception reading origin file while compressing: ' + e)
            items = data.items()
            originItems = self._data.items()
            if len(items) != len(originItems):
                raise RuntimeError('compress fail: data length not equals')
            for key, item in originItems:
                if key not in data:
                    raise RuntimeError(
                        'compress fail: miss data key "%s"' % key)
                if item != data[key]:
                    raise RuntimeError('compress fail: data mismatch for key "%s" (%s, %s)' % (
                        key, item, data[key]))

            # 3.多次重命名文件覆盖
            # 先把原文件重命名为.bak的备份文件（考虑文件已存在）
            postFix = 0
            bakName = self._filename + '.bak'
            bakPath = self._dirPath.join(bakName)
            while os.path.exists(bakPath):
                bakPath = self._dirPath.join(bakName + '.' + str(postFix))
                postFix += 1
            os.rename(self._filePath, bakPath)
            # 再把新的压缩文件重命名为原文件名，最后再删除备份文件
            os.rename(compPath, self._filePath)
            os.remove(bakPath)

            self.reload()
        finally:
            self._lock.release()

    def clear(self):
        self._lock.acquire()
        try:
            for key in list(self._data.keys()):
                self.pop(key)
        finally:
            self._lock.release()

    def set(self, key, item):
        '''更新一条数据'''
        self._lock.acquire()
        try:
            with open(self._filePath, 'a', newline='', encoding=self.encoding) as file:
                writer = csv.writer(file)
                writer.writerow(['1', 'u', key, item])
                self._recordCount += 1
                self._data[key] = item
        finally:
            self._lock.release()

    def setdefault(self, key, item=''):
        self._lock.acquire()
        try:
            if key in self._data:
                return self._data[key]
            self.set(key, item)
            return item
        finally:
            self._lock.release()

    def pop(self, key):
        '''删除一条数据'''
        self._lock.acquire()
        try:
            if key not in self._data:
                return
            with open(self._filePath, 'a', newline='', encoding=self.encoding) as file:
                writer = csv.writer(file)
                writer.writerow(['1', 'd', key])
                self._recordCount += 1
                del self._data[key]
        finally:
            self._lock.release()

    def getRecordCount(self):
        '''获取数据文件的记录条数'''
        return self._recordCount

    def getUtilization(self):
        '''获取数据文件使用率，即最终的数据量占记录数的百分比'''
        return float(len(self._data.items())) / self._recordCount

    def __getitem__(self, key):
        return self._data.get(key)

    def __setitem__(self, key, value):
        return self.set(key, value)

    def __delitem__(self, key):
        return self.pop(key)

    def __getattr__(self, key):
        return getattr(self._data, key)

    def __contains__(self, key):
        return key in self._data


__all__ = ['Storage']
