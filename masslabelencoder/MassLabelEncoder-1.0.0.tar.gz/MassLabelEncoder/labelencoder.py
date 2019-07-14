import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict
import warnings
warnings.filterwarnings(action='ignore', category=DeprecationWarning)

class MassLabelEncoder:

    def __init__(self):
        pass

    def fit_transform(self, df, dropnan = False, columns = []):
        
        '''
        Main fit_transform function. Takes args df [dataframe], bool to dropNaNs, and allows user
        to specify columns to label_encode.

        Expected usage:
        encodings = MassLabelEncoder().fit_transform(df, dropnan = False, columns = [])
        '''

        leDict = defaultdict(LabelEncoder) # Dict to be populated with LabelEncoder objects

        if dropnan == True: # True by default
            df = df.dropna() # Dropping NaNs. If no NaNs, this will have no effect on DF, hence we keep it True by default.
        else:
            pass

        # Seperating LE and Non-LE
        if len(columns) == 0:
            #User has not defined columns, encoding object columns
            non_LE = df.select_dtypes(exclude=['object']) # no label encoding here
            to_LE = df.select_dtypes(include=['object']) # to be label encoded
            to_LE = to_LE.astype(str) # strips Bools, user must manage datatype of final frame
        else:
            #User has specified columns to encode
            to_LE = df.loc[:,columns] # encode selected columns
            to_LE = to_LE.astype(str) # strips Bools, user must manage datatype of final frame
            non_LE = df.drop[columns] #select the rest of the columns
        if dropnan == False:
            saved_index = to_LE.index #Preserve Index from original set
            to_LE = to_LE.reset_index(drop=True) #Reset index to numbers for manipulation
            to_LE.loc[-1] = np.nan  # adding a row of NaNs so that "NaN" is always encoded to 0
            to_LE.index = to_LE.index + 1  # shifting index
            to_LE = to_LE.sort_index()
            to_LE = to_LE.fillna("NaN") # To be label encoded, learned, replaced later.
        else:
            pass    
        # Encoding the variable
        fit = to_LE.apply(lambda to_LE: leDict[to_LE.name].fit_transform(to_LE))
        # Inverse the encoded
        fit.apply(lambda to_LE: leDict[to_LE.name].inverse_transform(to_LE))

        # Using the dictionary to label future data
        lf = to_LE.apply(lambda to_LE: leDict[to_LE.name].transform(to_LE)) # lf for label encoded dataframe
        if dropnan == True:
         pass # No change if true.
        else:
            lf = lf.drop(lf.index[0])
            lf.index = lf.index - 1
            lf = lf.sort_index()
            lf.index = saved_index
            lf = lf.replace([0],np.nan)
        final_df = non_LE.join(lf)

        #Drop the first column (an extra index column)
        #final_df.drop(columns = final_df.index[0])

        return leDict, final_df # return dictionary of labelEncode models and final dataframe with label encoded data.