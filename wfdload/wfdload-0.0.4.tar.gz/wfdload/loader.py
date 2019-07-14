import numpy as np
from pandas import DataFrame
import struct
import os.path


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
    DATASIZE = "datasize"
    TEMPO_RESULT = "tempo_result"
    EXTEND_INFO = "extend_info"
    LABEL_LIST = "label_list"
    SPECTRUM_STEREO = "spectrum_stereo"
    SPECTRUM_LR_M = "spectrum_LR_M"
    SPECTRUM_LR_P = "spectrum_LR_P"
    SPECTRUM_L = "spectrum_L"
    SPECTRUM_R = "spectrum_R"

    def __init__(self):
        super().__init__()
        self.headers = DataFrame([
            ["filetype", 0, 0],
            ["reserve_space1", 1, 0],
            ["reserve_space2", 2, 0],
            ["block_per_semitone", 3, 0],
            ["min_note", 4, 0],
            ["range_of_scale", 5, 0],
            ["block_per_second", 6, 0],
            ["reserve_space3", 7, 0],
            ["time_all_block", 8, 0],
            ["bits_of_graph", 9, 0],
            ["beat_display_flag", 10, 0],
            ["tempo", 11, 0],
            ["offset", 12, 0],
            ["beat", 13, 0]],
            columns=["DATATYPE", "OFFSET", "VALUE"])
        self.indexes = DataFrame([
            ["datasize", -1, 0, "I", -1],
            ["_", 0, 0, "H", 0],
            ["tempo_result", 2, 0, "I", 0],
            ["extend_info", 4, 0, "I", 0],
            ["label_list", 6, 0, "I", 0],
            [self.SPECTRUM_STEREO, 7, 0, "H", 0],
            [self.SPECTRUM_LR_M, 8, 0, "H", 0],
            [self.SPECTRUM_LR_P, 9, 0, "H", 0],
            [self.SPECTRUM_L, 10, 0, "H", 0],
            [self.SPECTRUM_R, 11, 0, "H", 0],
            ["tempo_map", 12, 0, "I", 0],
            ["chord_result", 14, 0, "I", 0],
            ["rhythm_keymap", 15, 0, "I", 0],
            ["note_list", 16, 0, "I", 0],
            ["tempo_volume", 17, 0, "I", 0],
            ["frequency", 18, 0, "I", 0],
            ["track_setting", 19, 0, "I", 0]],
            columns=["DATATYPE", "DATANUM", "DATASIZE", "DATAFORMAT", "INDEX"])

        self._wfd_data = {}
        self.header_format = "I"
        self.index_format = "I"
        self.data_len = 0

    @property
    def __indexes__(self):
        return self.indexes

    @property
    def headerlen(self):
        return len(self.headers.index)

    @property
    def indexeslen(self):
        return len(self.indexes.index)

    @property
    def wfd_data(self):
        return self._wfd_data

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
        bps = self.headerA("block_per_semitone")
        range_scale = self.headerA("range_of_scale")
        time_all_block = self.headerA("time_all_block")
        freq_all_block = bps * range_scale
        sum_ = 0
        # print(time_all_block, freq_all_block, time_all_block * freq_all_block)
        data = {}

        for dtype in self.indexes["DATATYPE"]:
            if self.indexA("DATATYPE", dtype, "INDEX") <= 0:
                data[dtype] = []
                continue
            
            datasize = self.indexA("DATATYPE", dtype, "DATASIZE")
            dataformat = self.indexA("DATATYPE", dtype, "DATAFORMAT")
            if dtype.find("spectrum") != -1:
                sum_ = struct.calcsize(dataformat)
                datasize -= freq_all_block * sum_
                
            data[dtype] = self.unpack(self.buffer, dataformat, int(datasize / struct.calcsize(dataformat)), self.offset)

        time_all_block -= sum_
        result_data = {}
        for k, v in data.items():
            if len(v) == (time_all_block * freq_all_block):
                result_data[k] = self.spectrumData(v, time_all_block, freq_all_block)
            else:
                result_data[k] = v
        self._wfd_data = result_data

    def spectrumData(self, x, time_all_block, freq_all_block):
        """正規化とリシェイプを行います"""
        data = np.array(x / 65535.0, dtype="float32")
        return np.reshape(data, (time_all_block, freq_all_block))

    def headerA(self, x):
        return self.headers.loc[(self.headers["DATATYPE"] == x), "VALUE"].values[0]
    
    def indexA(self, x, x_key, y):
        return self.indexes.loc[(self.indexes[x] == x_key), y].values[0]
