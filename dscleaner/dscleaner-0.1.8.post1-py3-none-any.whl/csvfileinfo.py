from . import ifileinfo
import pandas as pd

class CsvFileInfo(ifileinfo.IFileInfo):
    """
        CsvFileInfo is used when there is no actual file, but an array.
        
        The array must be shaped in (n,c) where c is the number of channels.
    """
    def __init__(self, samples, samplerate):
        self._samples = samples
        self._samplerate = samplerate
        pass

    def __enter__(self):
        """
            See the base class ``ifileinfo``.
        """
        return self

    def __exit__(self,type,value,traceback):
        """
            See the base class ``ifileinfo``.
        """
        self.close()

    def getSamples(self):
        """
            See the base class ``ifileinfo``.
        """

        return self._samples

    def getSamplerate(self):
        """
            See the base class ``ifileinfo``.
        """

        return self._samplerate
    
    def getNumberOfFrames(self):
        """
            See the base class ``ifileinfo``.
        """

        return len(self._samples)
    
    def getNumberOfChannels(self):
        """
            See the base class ``ifileinfo``.
        """

        try:
            numchannels = self._samples.shape[1]
        except IndexError as e:
            numchannels = 1
        return numchannels

    def getFilepath(self):
        """
            Don't rely on this method because it's not implemented.
        """
        raise NotImplementedError("Not avaliable in csvFileInfo")

    #WRITE
    def setSamples(self, samples, framerate = None):
        """
            See the base class ``ifileinfo``.
        """

        if (framerate == None):
            framerate = self.getSamplerate()
        self._samples = samples
        self._samplerate = framerate
        return
    
    def truncate(self, num_frames):
        """
            See the base class ``ifileinfo``.
        """

        self._samples = self._samples[:num_frames]
        return

    def addSamples(self, samples):
        """
            See the base class ``ifileinfo``.
        """

        self._samples.append(samples)
        return 

    def close(self):
        """
            Does nothing since the sample container is an array.
        """
        
        return