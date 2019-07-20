from wfdload import WFDLoader
import label as lb


class WFD:
    def __init__(self, filepath):
        self._loader = WFDLoader()
        self._load(filepath)

    def _load(self, filepath):
        self._loader.open(filepath)
        self.headers = self._loader.readHeader()
        self.indexes = self._loader.readIndex()
        self.WFD_data = self._loader.readData()

    @property
    def tempo(self):
        """テンポ(BPM)"""
        return self._loader.headerA(lb.TEMPO)

    @property
    def block_per_semitone(self):
        """半音あたりのブロック数"""
        return self._loader.headerA(lb.BLOCK_PER_SEMITONE)

    @property
    def min_note(self):
        """解析する最低音"""
        return self._loader.headerA(lb.MIN_NOTE)

    @property
    def range_of_scale(self):
        """解析する音階の範囲"""
        return self._loader.headerA(lb.RANGE_OF_SCALE)

    @property
    def block_per_second(self):
        """1秒あたりのブロック数"""
        return self._loader.headerA(lb.BLOCK_PER_SECOND)

    @property
    def time_all_block(self):
        """時間方向の全ブロック数"""
        return self._loader.headerA(lb.TIME_ALL_BLOCK)

    @property
    def beat_offset(self):
        """第1小節1拍目の時間 (ミリ秒)"""
        return self._loader.headerA(lb.OFFSET)

    @property
    def beat(self):
        """拍子"""
        return self._loader.headerA(lb.BEAT)

    @property
    def spectrumStereo(self):
        """音声スペクトル(stereo)"""
        return self.getdata(lb.SPECTRUM_STEREO)

    @property
    def spectrumLRM(self):
        """音声スペクトル(L-R)"""
        return self.getdata(lb.SPECTRUM_LR_M)

    @property
    def spectrumLRP(self):
        """音声スペクトル(L+R)"""
        return self.getdata(lb.SPECTRUM_LR_P)

    @property
    def spectrumL(self):
        """音声スペクトル(L)"""
        return self.getdata(lb.SPECTRUM_L)
    
    @property
    def spectrumR(self):
        """	音声スペクトル(R)"""
        return self.getdata(lb.SPECTRUM_R)

    def getdata(self, key):
        return self.WFD_data[key]
