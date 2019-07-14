from wfdload.loader import WFDLoader
import numpy as np


class WFD:
    def __init__(self, filepath):
        self._loader = WFDLoader()
        self._load(filepath)

    def _load(self, filepath):
        self._loader.open(filepath)
        self.headers = self._loader.readHeader()
        self.indexes = self._loader.readIndex()
        # print(self.indexes)
        self._loader.readData()
        self.WFD_data = self._loader.wfd_data

        self._spectrum_stereo = np.array(
            self.WFD_data[self._loader.SPECTRUM_STEREO], dtype="float32").T
        self._spectrum_lrm = np.array(
            self.WFD_data[self._loader.SPECTRUM_LR_M], dtype="float32").T
        self._spectrum_lrp = np.array(
            self.WFD_data[self._loader.SPECTRUM_LR_P], dtype="float32").T
        self._spectrum_l = np.array(
            self.WFD_data[self._loader.SPECTRUM_L], dtype="float32").T
        self._spectrum_r = np.array(
            self.WFD_data[self._loader.SPECTRUM_R], dtype="float32").T

    @property
    def tempo(self):
        """テンポ(BPM)"""
        return self._loader.headerA("tempo")

    @property
    def block_per_semitone(self):
        """半音あたりのブロック数"""
        return self._loader.headerA("block_per_semitone")

    @property
    def min_note(self):
        """解析する最低音"""
        return self._loader.headerA("min_note")

    @property
    def range_of_scale(self):
        """解析する音階の範囲"""
        return self._loader.headerA("range_of_scale")

    @property
    def block_per_second(self):
        """1秒あたりのブロック数"""
        return self._loader.headerA("block_per_second")

    @property
    def time_all_block(self):
        """時間方向の全ブロック数"""
        return self._loader.headerA("time_all_block")

    @property
    def beat_offset(self):
        """第1小節1拍目の時間 (ミリ秒)"""
        return self._loader.headerA("offset")

    @property
    def beat(self):
        """拍子"""
        return self._loader.headerA("beat")

    @property
    def spectrumStereo(self):
        """音声スペクトル(stereo)"""
        return self._spectrum_stereo

    @property
    def spectrumLRM(self):
        """音声スペクトル(L-R)"""
        return self._spectrum_lrm

    @property
    def spectrumLRP(self):
        """音声スペクトル(L+R)"""
        return self._spectrum_lrp

    @property
    def spectrumL(self):
        """音声スペクトル(L)"""
        return self._spectrum_l
    
    @property
    def spectrumR(self):
        """	音声スペクトル(R)"""
        return self._spectrum_r
