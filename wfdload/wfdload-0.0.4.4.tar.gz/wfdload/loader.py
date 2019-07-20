import numpy as np
from pandas import DataFrame
import struct
import os.path
import wfdload.label as lb


class Loader:
    def __init__(self):
        self._buffer = None
        self.offset = 0

    @property
    def buffer(self):
        return self._buffer

    def open(self, filepath):
        self._buffer = open(filepath, 'rb').read()

    def unpack(self, buffer, format, count, offset):
        data = np.frombuffer(buffer, dtype=format, count=count, offset=offset)
        self.offset += int(struct.calcsize(format) * count)
        return data


class WFDLoader(Loader):
    def __init__(self):
        super().__init__()
        self.headers = DataFrame([
            [lb.FILETYPE, 0, 0],
            [lb.RESERVE_SPACE1, 1, 0],
            [lb.RESERVE_SPACE2, 2, 0],
            [lb.BLOCK_PER_SEMITONE, 3, 0],
            [lb.MIN_NOTE, 4, 0],
            [lb.RANGE_OF_SCALE, 5, 0],
            [lb.BLOCK_PER_SECOND, 6, 0],
            [lb.RESERVE_SPACE3, 7, 0],
            [lb.TIME_ALL_BLOCK, 8, 0],
            [lb.BITS_OF_GRAPH, 9, 0],
            [lb.BEAT_DISPLAY_FLAG, 10, 0],
            [lb.TEMPO, 11, 0],
            [lb.OFFSET, 12, 0],
            [lb.BEAT, 13, 0]],
            columns=["DATATYPE", "OFFSET", "VALUE"])
        self.indexes = DataFrame([
            [lb.DATASIZE, -1, 0, "I", -1],
            [lb._, 0, 0, "H", 0],
            [lb.TEMPO_RESULT, 2, 0, "I", 0],
            [lb.EXTEND_INFO, 4, 0, "I", 0],
            [lb.LABEL_LIST, 6, 0, "I", 0],
            [lb.SPECTRUM_STEREO, 7, 0, "H", 0],
            [lb.SPECTRUM_LR_M, 8, 0, "H", 0],
            [lb.SPECTRUM_LR_P, 9, 0, "H", 0],
            [lb.SPECTRUM_L, 10, 0, "H", 0],
            [lb.SPECTRUM_R, 11, 0, "H", 0],
            [lb.TEMPO_MAP, 12, 0, "I", 0],
            [lb.CHORD_RESULT, 14, 0, "I", 0],
            [lb.RHYTHM_KEYMAP, 15, 0, "I", 0],
            [lb.NOTE_LIST, 16, 0, "I", 0],
            [lb.TEMPO_VOLUME, 17, 0, "I", 0],
            [lb.FREQUENCY, 18, 0, "I", 0],
            [lb.TRACK_SETTING, 19, 0, "I", 0]],
            columns=["DATATYPE", "DATANUM", "DATASIZE", "DATAFORMAT", "INDEX"])

        self.header_format = "I"
        self.index_format = "I"

    @property
    def __indexes__(self):
        return self.indexes

    @property
    def headerlen(self):
        return len(self.headers.index)

    @property
    def indexeslen(self):
        return len(self.indexes.index)

    def open(self, filepath):
        _, ext = os.path.splitext(filepath)
        if ext.lower() != ".wfd":
            raise ValueError("wfdファイルではありません")

        self._buffer = open(filepath, 'rb').read()
        
    def readHeader(self):
        """Headerを読み込みます"""
        data = self.unpack(
            self.buffer, self.header_format, self.headerlen, self.offset)
        for i in range(len(data)):
            self.headers.loc[(self.headers["OFFSET"] == i), "VALUE"] = data[i]
        return self.headers

    def readIndex(self):
        """Indexを読み込みます"""
        if self.offset >= (struct.calcsize(self.header_format) * self.headerlen):
            counter = 1
            for i in self.indexes["DATANUM"]:
                if i == -1:
                    self.indexes.loc[(self.indexes["DATANUM"] == -1), "DATASIZE"] = self.unpack(self.buffer, self.index_format, 1, self.offset)[0]
                else:
                    data = self.unpack(self.buffer, self.index_format, 2, self.offset)
                    self.indexes.loc[(self.indexes["DATANUM"] == data[0]), "DATASIZE"] = data[1]
                    self.indexes.loc[(self.indexes["DATANUM"] == data[0]), "INDEX"] = counter
                    counter += 1
                    
            self.indexes.sort_values("INDEX", inplace=True)
        return self.indexes

    def readData(self):
        """データを読み込みます"""
        bps = self.headerA(lb.BLOCK_PER_SECOND)
        range_scale = self.headerA(lb.RANGE_OF_SCALE)
        time_all_block = self.headerA(lb.TIME_ALL_BLOCK) - 1
        freq_all_block = bps * range_scale

        data = {}

        for dtype in self.indexes["DATATYPE"]:
            if self.indexA("DATATYPE", dtype, "INDEX") <= 0:
                data[dtype] = []
                continue
            
            datasize = self.indexA("DATATYPE", dtype, "DATASIZE")
            dataformat = self.indexA("DATATYPE", dtype, "DATAFORMAT")
            if dtype.find("spectrum") != -1:
                datasize -= freq_all_block * struct.calcsize(dataformat)
                
            data[dtype] = self.unpack(self.buffer, dataformat, int(datasize / struct.calcsize(dataformat)), self.offset)

        result_data = {}
        for k, v in data.items():
            if len(v) == (time_all_block * freq_all_block):
                result_data[k] = np.array(self.__spectrumData(v, time_all_block, freq_all_block), dtype="float32").T
            else:
                result_data[k] = v
        return result_data

    def __spectrumData(self, x, time_all_block, freq_all_block):
        """正規化とリシェイプを行います"""
        data = np.array(x / 65535.0, dtype="float32")
        return np.reshape(data, (time_all_block, freq_all_block))

    def headerA(self, x):
        return self.headers.loc[(self.headers["DATATYPE"] == x), "VALUE"].values[0]
    
    def indexA(self, x, x_key, y):
        return self.indexes.loc[(self.indexes[x] == x_key), y].values[0]
