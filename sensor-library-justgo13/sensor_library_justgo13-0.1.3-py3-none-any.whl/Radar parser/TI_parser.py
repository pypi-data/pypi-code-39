# This script is used to read the binary file produced by the DCA1000 and Mmwave Studio
import numpy as np
import pandas as pd


def readTIdata(filename,csvname):
    """
    Reads in a binary file and outputs the iq complex data to a csv file specified by csvname.

    Parameter:

        filename: str
            file name of binary file.

        csvname: str
            csv file name that stores the iq data from binary file.

    Example:

        >>> readTIdata('TIdata.bin','TIdata')
        >>> 'converted'

    Return:

        Readable csv file containing complex data.
    """
    # global variables
    # change based on sensor config
    numADCSamples = 256 # number of ADC samples per chirp
    numADCBits = 16 # number of ADC bits per sample
    numRX = 4 # number of receivers
    numLanes = 2 # do not change. number of lanes is always 2
    isReal = False # set to True if real only data, False if complex data
    # read file
    # read .bin file
    with open(filename, 'rb') as f:
        adcData = np.fromfile(f, dtype='int16', count=-1)
        adcData = np.transpose([adcData])
        # if 12 or 14 bits ADC per sample compensate for sign extension
        if numADCBits != 16:
            l_max = 2**(numADCBits-1)-1
            # If value greater than l_max, this loop prevents it
            for index, val in enumerate(adcData):
                if adcData[index] > l_max:
                    adcData[index] -= 2**(numADCBits)
        fileSize = len(adcData)
        # real data reshape, filesize = numADCSamples*numChirps

        if isReal:
            numChirps = int(fileSize/numADCSamples/numRX)
            LVDS = np.zeros((1, fileSize), dtype='int16')
            # each row is data from one chirp
            LVDS = np.reshape(adcData, (numChirps, numADCSamples*numRX))
        else:
            # for complex data
            # filesize = 2 * numADCSamples*numChirps
            numChirps = int(fileSize/2/numADCSamples/numRX)
            LVDS = np.zeros((1, int(fileSize/2)), dtype='complex')
            # combine real and imaginary part into complex data
            # read in file: 2I is followed by 2Q
            counter  = 0
            for i in range(0, fileSize-2, 4):
                # LVDS[0, i] = adcData[i, 0]
                # LVDS[0, i+1] = adcData[i+2, 0]
                LVDS[0, counter] = complex(adcData[i], adcData[i+2])
                LVDS[0, counter+1] = complex(adcData[i+1], adcData[i+3])
                counter += 2
            # each row is data from one chirp
            LVDS = np.reshape(LVDS, (numChirps, numADCSamples*numRX))
            # organize data per RX
            adcData = np.zeros((numRX, numChirps * numADCSamples), dtype='complex')
            for row in range(0, numRX):
                for i in range(0, numChirps):
                    adcData[row, i * numADCSamples:(i + 1) * numADCSamples] = LVDS[i, row * numADCSamples:(row + 1) * numADCSamples]

            data = pd.DataFrame(adcData)
            data.to_csv(csvname+'.csv', index=False, header=False, mode='w')
    f.close()
    return 'converted'