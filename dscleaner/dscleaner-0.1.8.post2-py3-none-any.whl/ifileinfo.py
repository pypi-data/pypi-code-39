from abc import ABC, abstractmethod

class IFileInfo(ABC):
    """
        Interface which must be implemented if you want to support your own filetype;
        Used as an argument to FileWriter, FileUtil and FileMerger.
    """
    def __init__(self,file):
        self.file = file
        pass

    @abstractmethod
    def __enter__(self):
        """
            When entering a context manager the enter method is called.
            This is the most correct way to manipulate files.
            Check the ``FileInfo`` class for examples.
        """

        pass
    @abstractmethod
    def __exit__(self,type,value,traceback):
        """
            When closing a context manager the exit method is called.
            This is the most correct way to manipulate files.
            Check the ``FileInfo`` class for examples.
        """

        pass

    @abstractmethod
    def getFilepath(self):
        """
            Returns:
                The filepath of the current file.
        """
        pass

    @abstractmethod
    def getNumberOfFrames(self):
        """
            Returns:
                The number of frames the file has.
        """
        pass

    @abstractmethod
    def getSamplerate(self):
        """
            Returns:
                The samplerate of the file.
        """
        pass

    @abstractmethod
    def getNumberOfChannels(self):
        """
            Returns:
                The number of channels the file has.
        """
        pass    

    @abstractmethod        
    def getSamples(self):
        """
            Returns:
                All the samples the file has.
        """
        pass

    # writing methods
    @abstractmethod
    def setSamples(self, samples):
        """
            Writes to the file the samples given in ``samples``.

            It will truncate the old samples. 
            If you want to add, use the ``addSamples`` method.

            Args:
                samples: An array containing the new samples.
                    It must be shaped like (n,c) where c is the number of channels
        """
        pass
    
    @abstractmethod
    def truncate(self, num_frames):
        """
            Truncates the file to have only the first ``num_frames`` samples.

            Args:
                num_frames: The number of frames the file will have.
        """

        pass

    @abstractmethod
    def addSamples(self, samples):
        """
            Adds samples given by ``samples``.

            Args: 
                samples: An array containing samples.
                    It must be shaped like (n,c) where c is the number of channels.
        """

        pass
    
    @abstractmethod
    def close(self):
        """
            Defines the behavior the class should have when leaves the context manager.
            
            If a file descriptor is being used you should always define the close method.
        """
        pass
    