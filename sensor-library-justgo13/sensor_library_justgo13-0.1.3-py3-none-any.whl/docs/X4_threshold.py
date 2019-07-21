import numpy as np
import matplotlib.pyplot as plt
import csv


def csv_into_list(filename): 
    """
    Converts data from a CSV file into a numpy array.
    
    Data is collected from "XEP_X4M200_X4M300_plot_record_playback.py". Then 
    .dat file is converted into a CSV file using the library.
    
    Parameters:
    
        filename: str
            Csv file name.
            
    Example:
    
        >>> csv_into_list("Heli150040.csv")
        >>> array([[2.12019056e-04, 2.66481591e-04, 3.51781533e-04, ...,
            2.51499279e-04, 2.63311858e-04, 2.49837321e-04],
           [1.36839763e-03, 1.13654408e-03, 7.92290507e-04, ...,
            3.49299137e-04, 1.30311682e-04, 1.87399805e-04],
           [7.57068081e-04, 6.54611670e-04, 6.83445863e-04, ...,
            6.95117789e-05, 2.17249015e-04, 3.85946482e-04],
           ...,
           [9.57032957e-04, 5.99047943e-04, 5.37280418e-04, ...,
            2.95999810e-04, 2.42217122e-04, 3.25605109e-04],
           [2.37110777e-03, 1.98986895e-03, 1.28061167e-03, ...,
            2.95363991e-04, 1.50057104e-04, 2.33757752e-04],
           [6.45687293e-04, 5.61334516e-04, 1.63285784e-04, ...,
            6.64671904e-05, 2.17249015e-04, 1.93614790e-04]])
            
    Returns:
    
        A numpy array of the data.
    """    
   
    with open(filename,"rt") as csvfile:
        
        data = list(csv.reader(csvfile))  #Declarations 
        mean=[0]*len(data[0])
        
        for i in range (len(data)):  #Goes through the 180 by n CSV file 
            
            for j in range (len(data[i])):
                
                data[i][j]=complex(data[i][j]) #Converts string to complex number
                mean[j]+=complex(data[i][j]) #Adds up numbers for each 180 column to get to get a mean for each column 
        
        for i in range (len(data)):
            
            for j in range (len(data[i])):
                
                            data[i][j]=abs(data[i][j]-mean[j]/len(data)) #Each complex number is subtracted by it's respective column mean to even it out and the magnitude is taken since it is complex 
                                
    data=np.array(data[0:])    
    csvfile.close()
    
    return data
        

def range_finder(filename,estimated_threshold):
    """
    Finds the range bin/bins from the radar data.
    
    Given the filename, the file is converted to an array. The points above the given threshold are returned.
    
    Parameters:
    
        filename: str
            Csv file name
            
        estimated_threshold: float
            Threshold to block out background noise.
            
    Example:
    
        >>> range_finder("Heli150040.csv",0.02)
        >>> [9]
        
    Returns:
    
        A list of range bins that has signal strength values above the threshold.    
    """    
    
    data=csv_into_list(filename)
    positive_finds=[]
    
    for i in range (len(data[5])):     #Finds points for the 5th sample
        
        if (estimated_threshold<data[5][i]):
            positive_finds.append(i+1)
    
    return positive_finds


def noise_power_estimate(filename,estimated_threshold):
    """
    Finds the noise power estimate.
    
    Given the filename, the file is converted to an array. The average for the the array is taken excluding the points above the threshold and their respective guard cells.
    The noise power estimate is then found by subtracting the positive and guard cells from the overall sum. When the noise power estimate is multiplied by the threshold factor, the threshold can be found.
    
    Parameters:
    
        filename: str
            Csv file name.
            
        estimated_threshold: float
            Threshold to block out background noise.
    
    Example:
    
        >>> noise_power_estimate("Heli150040.csv",0.02)
        >>> 0.00045988029076158947
        
    Returns:
    
        A number representing the noise power estimate.
    """     
    
    data=csv_into_list(filename)
    positive_finds=range_finder(filename,estimated_threshold)
     
    sum_data=sum(data[5])
    
    for i in range (len(positive_finds)):          #Subtracts the positive/guard cells from the overall sum 
        sum_data-=data[5][positive_finds[i]]
        sum_data-=data[5][positive_finds[i]-1]
        sum_data-=data[5][positive_finds[i]+1]
    
    noise_power=sum_data/(len(data[5])-len(positive_finds)*3)  #Takes average excluding guard and positive numbers
    
    return noise_power


def distance_finder(filename,estimate_threshold):
    """
    Converts the positive range bin/bins to a given distance in centimetres for a target.
    Formula used for this is (bin)*5.25-18. Each range bin is 5.25 cm and starting offset is 18 cm.
    
    Parameters:
    
        filename: str
            Csv file name.
            
        estimated_threshold: float
            Threshold to block out background noise.

    Example:
    
        >>> distance_finder("Heli150040.csv",0.02)
        >>> [29.25]
    
    Returns:
    
        List of ranges in centimetres where all the possible targets above the threshold are located. 
    """     
    
    positive_finds=range_finder(filename,estimate_threshold)
    distance=[]
    
    for i in range (len(positive_finds)):
        
        distance.append(positive_finds[i]*5.25-18)
    
    return distance


def plot_data(filename):
    """
    Plots the data array for the 5th sample set.
    
    Parameters:

         filename: str
            Csv file name.

    Example:
    
        >>> plot_data("Heli150040.csv")

    Returns:
    
        Graph showing the range bin with respect to their corresponding strength of signal.
    """     
    
    data=csv_into_list(filename)
    plt.plot(data[5])
    plt.xlabel('Range bin')
    plt.ylabel('Signal strength')
    plt.title('Detection of target in range bins with equivalent signal strength')
    plt.show()