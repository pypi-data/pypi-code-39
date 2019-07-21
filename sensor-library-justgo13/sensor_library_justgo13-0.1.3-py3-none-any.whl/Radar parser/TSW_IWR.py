# The function in the following MATLAB code example can be used to read files saved with the xWR16xx.
# This script is used to read the binary file produced by the TSW1400 and Radar Studio.
import numpy as np
import pandas as pd


def readTSWdata(filename, csvname):
    """
    Reads in a binary file and outputs the iq complex data to a csv file specified by csvname.

    Parameter:

        filename: str
            file name of binary file.
        csvname: str
            csv file name that stores the iq data from binary file.

    Example:

        >>> readTSWdata('TIdata.bin','TIdata')
        >>> 'converted'

    Return:

        Readable csv file containing complex data.
    """
    # Global Variables - change based on sensor config
    numADCSamples = 256; # number of ADC samples per chirp
    numADCBits = 16; # number of ADC bits per sample
    numRX = 4; # number of receivers
    numLanes = 2; # do not change. number of lanes is always 2
    isReal = 0; # set to 1 if real only data, 0 if complex data

    # Read file
    with open(filename, 'rb') as f:
        adcData = np.fromfile(f, dtype="int16")
        for i in range(0, len(adcData)):
            if adcData[i] > 0:
                adcData[i] = adcData[i] - 2**15
            else:
                adcData[i] = adcData[i] + 2**15
        #adcData = adcData - 2**15
        # if 12 or 14 bits ADC per sample compensate for sign extension
        if numADCBits != 16:
            l_max = 2**(numADCBits-1)-1
            for index, val in enumerate(adcData):
                if adcData[index] > l_max:
                    adcData[index] -= 2**(numADCBits)
    f.close()
    fileSize = len(adcData)
    # Organize data by LVDS lane
    # Reshape data based on two samples per LVDS lane
    adcData = np.reshape(adcData, (numLanes*2, -1))
    
    # For real data
    if isReal == 1:
        # seperate each LVDS lane into rows
        LVDS = np.zeros((2, len(adcData[0,:])*2), dtype="uint16")
        # interleave the two sample sets from each lane
        for i in range(2, len(LVDS)-1, 2):
            LVDS[0,0:i] = adcData[0,:]
        for i in range(3,len(LVDS), 2):
            LVDS[0,1:i] = adcData[1,:]

        if numRX > 1:
            for i in range(2, len(LVDS)-1, 2):
                LVDS[1,0:i] = adcData[2,:]
            for i in range(3,len(LVDS), 2):
                LVDS[1,1:i] = adcData[3,:]
            LVDS = np.reshape(LVDS[0:1,:], (1, -1))
            
    # For complex data
    else:
        fileSize = fileSize/2
        # seperate each LVDS lane into rows
        LVDS = np.zeros((2,len(adcData[1,:])), dtype="complex")
        # combine real and imaginary parts
        LVDS[0,:] = [complex(a,b) for a,b in zip(adcData[0,:], adcData[1,:])]
        if numRX > 1:
            LVDS[1,:] = [complex(a,b) for a,b in zip(adcData[2,:], adcData[3,:])]
            LVDS = np.reshape(LVDS, (1, -1))
            
    # organize data by receiver
    # seperate each receiver into a single row
    adcData = np.zeros((numRX, int(fileSize/numRX)), dtype="complex")
    if numRX > 1:
        for j in range(0,numRX):
            iterator = 0
            for i in range(j*numADCSamples, int(fileSize), numADCSamples*numRX):
                adcData[j,iterator:iterator+numADCSamples] = LVDS[0, i:i+numADCSamples]
                iterator = iterator + numADCSamples
    else:
        adcData = LVDS[1,:]
        
    data = pd.DataFrame(adcData)
    data.to_csv(csvname+'.csv', index=False, header=False, mode='w')

    return 'converted'
