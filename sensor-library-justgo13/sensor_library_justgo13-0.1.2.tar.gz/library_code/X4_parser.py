import csv

import numpy as np


def iq_data(filename,csvname):
    """
    Reads in a binary file and data from range bins is taken and complex iq data is stored in a csv file specified by csvname.

    Parameter:

        filename: str
            The .dat binary file name.
        csvname: str
            User defined .csv file name

    Example:

        >>> iq_data('X4data.dat','X4iq_data')
        >>> 'converted'

    Returns:

        Readable csv file containing complex values.
    """
    with open(filename, "rb") as f:
        data = np.fromfile(f, dtype=np.float32)
    for i in range(0, len(data) // 363 - 1):
        temp = data[3 * (i + 1) + 360 * i:3 * (i + 1) + 360 * (i + 1)]
        iqdata = []
        for j in range(0, 180):
            if temp[j + 180] > 0:
                iqdata.append(str(round(temp[j], 4)) + "+" + str(round(temp[j + 180], 4)) + "j")
            else:
                iqdata.append(str(round(temp[j], 4)) + str(round(temp[j + 180], 4)) + "j")
        with open(csvname+'.csv', 'a', newline="") as csvFile:
             writer = csv.writer(csvFile)
             writer.writerow(iqdata)
    f.close()
    csvFile.close()
    return 'converted'


def raw_data(filename,csvname):
    """
    Reads in a binary file and data from range bins is taken and raw data is stored in a csv file specified by csvname.

    Parameters:

        filename: str
            The .dat binary file name.
        csvname: str
            User defined .csv file name

    Example:

        >>> raw_data('X4data.dat','X4raw_data')
        >>> 'converted'

    Returns:

        Readable csv files containing raw data.
    """
    with open(filename, "rb") as f:
        data = np.fromfile(f, dtype=np.float32)
    for i in range(0, len(data) // 1473 - 1):
        temp = data[3 + 1470 * i:3 + 1470 * (i + 1)]

        with open(csvname+'.csv', 'a', newline="") as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(temp)
    f.close()
    csvFile.close()
    return 'converted'