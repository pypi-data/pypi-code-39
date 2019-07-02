import os
import numpy as np
from math import ceil
class FileUtil():
    """
        FileUtil class is where the dataset manipulation occur.
        
        The class should be instantiated with a ``with`` statement.

        Args:
            f: a IFileInfo specialization must be supplied!
    """
    def __init__(self, f):
        
        from .ifileinfo import IFileInfo
        assert issubclass(type(f),IFileInfo),"Not a specialization of IFileInfo"
        self.file = f
    
    def __enter__(self):
        return self

    def __exit__(self,type,value,traceback):
        pass

    def fix_duration(self, expected_duration, grid_rate = 50):
        """
            Fixes the file to the expected duration.
            
            Args:
                expected_duration: Duration the file should have in minutes.
                grid_rate: frequency of the grid in hertz, this is used to discover the wave signal in order to upsample.
        """
        data = self.file.getSamples()
        sample_rate = self.file.getSamplerate()

        actual_frame_number = len(data)
        expected_frame_number = ceil(sample_rate * expected_duration * 60)
        #rate * minutes * seconds
        if(actual_frame_number == expected_frame_number):
            #no cleaning needed
            return
        else:
            if(actual_frame_number > expected_frame_number):
                self.file.truncate(expected_frame_number)
            else:
                #needs adding
                wave_length = int((sample_rate / grid_rate) )
                last_wave = list(data[-wave_length:]) # gets the last wave_length elements
                samples_missing = int(expected_frame_number - actual_frame_number)
                last_wave *= ceil(samples_missing/wave_length) #replicates the last wave several times
                last_wave = np.asarray(last_wave[:samples_missing]) #removes any more than its actually missing
                self.file.addSamples(last_wave)
    
    def standardize(self,*dividers):
        """
            This method transforms the values to fit between -1 and 1, in order to be used in soundfiles.

            If the source file isn't a soundfile the target file will not be well formated,
            hence you should run this method to make the file well formated.
            
            Args:
                *dividers: The number which each channel will be divided by in order to standardize that channel.

            NOTE:
                In order to maintain consistency throughout the dataset it is advised that the
                divider chosen for each channel to be a bit higher than the max value.
                It is also advised to keep record of the divider for each channel for future unstardartization.
                    
                Example:
                    Max amplitude is 75
                    divider chosen: 90.

            Returns:
                A tuple with the dividers used to standardize.
                    Example:
                        (40,30,30) in a three channel file.
                        
                You should keep these values for future reference.
             
        """
        iter = 0
        print(type(dividers))
        dividers = list(dividers) #convert tuple to list
        if(len(dividers)>self.file.getNumberOfChannels()):
            raise TypeError("There are more dividers than channels in the file!")
        elif(len(dividers) == 0): #if there are no dividers we find the max value in each channel and divide by it
            for i in range(0,self.file.getNumberOfChannels()):
                try:
                    dividers.append(ceil(max(self.file.getSamples()[:,i]))) #iterates over each channel
                except IndexError as e:
                    dividers.append(ceil(max(self.file.getSamples())))
        try:
            tmp = np.ndarray(shape = self.file.getSamples().shape)
        except IndexError as e:
            tmp = np.array()
        for divider in dividers:
            if(divider in (int,float,0)):
                TypeError("Not a number")
            try:
                tmp[:,iter] = self.file.getSamples()[:,iter]/divider
            except IndexError as e:
                tmp = self.file.getSamples()/divider   
            iter += 1
        self.file.setSamples(tmp)
        return (dividers)

    def resample(self, new_framerate, method = 'kaiser_fast'):
        """
            Resamples the data to the new framerate using librosa resample.
            
            Args:
                data: numpy.array shaped like (num_frames,num_channels) is expected to receive the soundfile.getSamples()
                    not the transposed array.
                original_framerate: the original framerate the data array uses.
                new_framerate: the new framerate that data will be resampled to.
                method: Methods that librosa accepts are also accepted here, uses `kaiser_fast` by default.
        """
        data = self.file.getSamples()
        new_framerate = ceil(new_framerate)
        import librosa
        new_data = librosa.resample(data.T, self.file.getSamplerate(), new_framerate, res_type=method, fix=True)
        self.file.setSamples(new_data.T,new_framerate)