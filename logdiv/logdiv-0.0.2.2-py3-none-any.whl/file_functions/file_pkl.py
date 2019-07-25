import pandas as pd
import time as timelib

def retrieve_pkl_file(filename, verbose = False):
    """
    Retrieve and return contents of pkl file
    """
    if verbose == True:
        start_time = timelib.time()
        print("\n   * Retrieving %s file ..."%filename)

    data = pd.read_pickle(filename)
    
    if verbose == True:
        print("\n %s retrieved in %.1f seconds."%(filename, timelib.time() - start_time))

    return data;

def save_pkl_file(data, filename, verbose = False):
    """
    Save in pkl form the contents of data
    """
    if verbose == True:
        start_time = timelib.time()
        print("\n   * Saving %s file ..."%filename)

    data.to_pickle(filename)

    if verbose == True:
        print("\n %s saved in %.1f seconds."%(filename, timelib.time() - start_time))

    return;
    
