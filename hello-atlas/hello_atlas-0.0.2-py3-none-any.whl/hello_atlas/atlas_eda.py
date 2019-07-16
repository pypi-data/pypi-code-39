
"""
DATA EDA Function
Author: Mei Yong
Updated Date: 2019-07-15
    
"""

def say_hello(name):
	print(f"Hello {name}!")

    
def df_eda(df, overview=False, detailed=True):

    ### Import libraries
    import pandas as pd
    import numpy as np
    
    ### Note row and column count
    rowcount = (df.shape)[0]
    colcount = (df.shape)[1]
    
    ##### DETAILS #####
    if detailed == True:
        
        ### Initiate all the lists
        dtype_list = []
        count_list = []
        null_list_n = []
        null_list_p = []
        
        unique_list = []
        cardinality_list = []
        zeroes_list_n = []
        zeroes_list_p = []
        mean_list = []
        min_list = []
        q1_list = []
        q2_list = []
        q3_list = []
        max_list = []
        
        ### Start looping through the columns to get their stats
        for column in df:
            
            # Stats for any data type
            dtype_list.append(df[column].dtype.name) # Dtype
            count_list.append(df[column].count()) # Count
            null_list_n.append(df[column].isnull().sum()) # Null (n)
            null_list_p.append(round(df[column].isnull().sum() / rowcount * 100 , 2)) # Null (%)
            
            # Stats for if the data type is object (categorical)
            if df[column].dtype==np.object:
                
                unique_list.append(df[column].value_counts().count()) # Unique values (n)
                cardinality_list.append(round(df[column].value_counts().count() / rowcount * 100 , 2)) # Cardinality (%)
                zeroes_list_n.append(np.NaN) # Zeroes (n)
                zeroes_list_p.append(np.NaN) # Zeroes (%)
                mean_list.append(np.NaN) # Mean
                min_list.append(np.NaN) # Min
                q1_list.append(np.NaN) # 25%
                q2_list.append(np.NaN) # 50%
                q3_list.append(np.NaN) # 75%
                max_list.append(np.NaN) # Max
                
            # Stats for if the data type is not object (numerical)
            else:
                
                unique_list.append(np.NaN) # Unique values (n)
                cardinality_list.append(np.NaN) # Cardinality (%)
                zeroes_list_n.append((df[column]==0).sum()) # Zeroes (n)
                zeroes_list_p.append((round(df[column]==0).sum() / rowcount * 100 , 2)) # Zeroes (%)
                mean_list.append(df[column].mean()) # Mean
                min_list.append(df[column].min()) # Min
                q1_list.append(np.percentile(df[column], 25)) # 25%
                q2_list.append(np.percentile(df[column], 50)) # 50%
                q3_list.append(np.percentile(df[column], 75)) # 75%
                max_list.append(df[column].max()) # Max
                
        
        ### Stitch all the stats together
        df_EDA = pd.DataFrame(list(zip(
                                dtype_list
                                ,count_list
                                ,null_list_n
                                ,null_list_p
                                ,unique_list
                                ,cardinality_list
                                ,zeroes_list_n
                                ,zeroes_list_p
                                ,mean_list
                                ,min_list
                                ,q1_list
                                ,q2_list
                                ,q3_list
                                ,max_list
                                
                             ))
                             )
        df_EDA = df_EDA.T # Transpose
        
        ### Note column & index names and assign them to the EDA df
        column_names = list(df.columns)
        index_names = ['Dtype', 'Count', 'Null(n)', 'Null(%)','Unique','Cardinality','Zeroes(n)','Zeroes(%)','Mean','Min','25%','50%','75%','Max']
        
        df_EDA.columns = column_names
        df_EDA.index = index_names
        
        
        
        ### Build the warnings
        warnings_list = []
        for column in df_EDA:
            
            column_warnings = []
            if df_EDA.loc['Null(%)',column] >= 50:
                column_warnings.append('High null percentage')
            try:
                if df_EDA.loc['Zeroes(%)',column] >= 50:
                    column_warnings.append('High zeroes percentage')
            except:
                pass
            if df_EDA.loc['Cardinality',column] >= 50:
                column_warnings.append('High cardinality')
            if df_EDA.loc['Unique',column] == 1:
                column_warnings.append('Only one unique value')
                
            warnings_list.append(column_warnings)
            
        ### Attach the warnings to the EDA df
        df_EDA = df_EDA.append(pd.Series(warnings_list, index=df_EDA.columns ), ignore_index=True)  
        df_EDA.index = index_names + ['Warnings']
        
    
    
    
    
    ##### OVERVIEW #####
    if overview == True:
        
        ### Total nulls (%) of whole df
        total_null_p = round(df.isnull().sum().sum() / (rowcount*colcount) * 100 , 2)
        
        ### Counts of data types
        dtype_object = dtype_list.count('object')
        dtype_int64 = dtype_list.count('int64')
        dtype_float64 = dtype_list.count('float64')
        
        ### Building the dictionary to be later converted to a df
        overview_dict = { 'Row Count' : rowcount # Num of columns
                         , 'Column Count' : colcount # Num of rows
                         , 'Total Null(%)' : total_null_p # Nulls (%)
                         , 'Dtype-object' : dtype_object
                         , 'Dtype-int64' : dtype_int64
                         , 'Dtype-float64' : dtype_float64
                        }
        
        df_overview = pd.DataFrame(overview_dict, index=[0])
        df_overview = df_overview.T
        df_overview.columns = ['Overview']
    
    
    
    if overview == True and detailed == True:
        return df_overview, df_EDA
    elif overview == True and detailed == False:
        return df_overview
    elif overview == False and detailed == True:
        return df_EDA
    else:
        print("Enable either overview or detailed report outputs.")


if __name__ == '__main__':
    say_hello()
    df_eda()