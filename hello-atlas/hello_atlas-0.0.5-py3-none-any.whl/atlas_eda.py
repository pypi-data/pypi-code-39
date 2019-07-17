
"""
EDA Functions
Author: Mei Yong
Updated Date: 2019-07-16
    
"""

def say_hello(name):
	print(f"Hello {name}!")

###################################################################################################
    
    
    
"""
Identify if column should be 1 and 0.
Yes/no y/n yes/nan

If high cardinality, check if can bucket smaller categories into other

Identify if data skewed and should be logarithmic. Must be positive values. Can add 1 to data to transform it to br positive

Is there a way to auto identify if a column needs to be split or pivoted?

Identify if there are only a few different numbers which represent categories

For transactional data, should aggregate into max transaction value or similar

Treat dates
Split into year month day
Days between current date and column date
Convert to weekday, weekend, holidays

Can we look at more than 1 table to form a cohesive view of the data?


Outlier functions 
Tukey
If value has a distance to the average higher than x*std. X usually 2-4



"""

## Testing
#import pandas as pd
#df = pd.read_csv(r"C:\Users\shaom\Desktop\Machine_Learning\House_Prices\train.csv")
#nulls_threshold=50.0
#zeroes_threshold=50.0
#cardinality_threshold=50.0



def df_eda(df, nulls_threshold=50.0, zeroes_threshold=50.0, cardinality_threshold=50.0):
    '''
    Input(s):
        1) df - dataframe to analyse
        2) nulls_threshold - int - default 50. Adds warning if >50% nulls
        3) zeroes_threshold - int - default 50. Adds warning if >50% zeroes for numerical dtype columns
        4) cardinality_threshold - int - default 50. Adds warning if >50% nulls for categorical dtype columns
    Output(s):
        1) Dataframe with statistics and data quality warnings about the input df
    '''
    ### Import libraries
    import pandas as pd
    import numpy as np
    
    ### Note row and column count
    rowcount = (df.shape)[0]
    colcount = (df.shape)[1]

            
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
    
    warning_null_list = []
    warning_zeroes_list = []
    warning_cardinality_list = []
    warning_one_unique_list = []
    
    warning_yesno_list = []
    warning_categorical_list = []
    
    ### Start looping through the columns to get their stats
    for column in df:
        
        ##### Stats for any data type #####
        dtype_list.append(df[column].dtype.name) # Dtype
        count_list.append(df[column].count()) # Count
        null_list_n.append(df[column].isnull().sum()) # Null (n)
        null_list_p.append(round(df[column].isnull().sum() / rowcount * 100 , 2)) # Null (%)
        
        # Null warning
        warning_null = 1 if round(df[column].isnull().sum() / rowcount * 100 , 2) >= nulls_threshold else 0
        warning_null_list.append(warning_null)
        
        # Convert to string for checks based on unique values
        stringify = df[column].astype(str)
        dist_string_vals = stringify.value_counts().count()
        
        # y/n
        warning_yesno = 1 if dist_string_vals==2 else 0
        warning_yesno_list.append(warning_yesno)
        
        # Numbers representing categories and should be categorical dtype instead
        warning_categorical = 1 if (df[column].dtypes in ['int64','float64']) and (dist_string_vals / rowcount * 100 < 5) else 0
        warning_categorical_list.append(warning_categorical)
        
        
        
        
        
        ##### Stats for if the data type is object (categorical) #####
        if df[column].dtype in ['object']:
            
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
            
            # Zeroes warning
            warning_zeroes_list.append(np.NaN)
            
            # Cardinality warning
            warning_cardinality = 1 if round(df[column].value_counts().count() / rowcount * 100 , 2) >= cardinality_threshold else 0
            warning_cardinality_list.append(warning_cardinality)
            
            # Only 1 unique value warning
            warning_one_unique = 1 if df[column].value_counts().count() == 1 else 0
            warning_one_unique_list.append(warning_one_unique)
            
            
        ##### Stats for if the data type is not object (numerical) #####
        elif df[column].dtype in ['int64','float64']:
                        
            unique_list.append(np.NaN) # Unique values (n)
            cardinality_list.append(np.NaN) # Cardinality (%)
            zeroes_n = (df[column]==0).sum() # Zeroes (n)
            zeroes_list_n.append(zeroes_n) # Zeroes (n)
            zeroes_list_p.append(round(zeroes_n / rowcount * 100 , 2)) # Zeroes (%)
            mean_list.append(df[column].mean()) # Mean
            min_list.append(df[column].min()) # Min
            q1_list.append(np.percentile(df[column], 25)) # 25%
            q2_list.append(np.percentile(df[column], 50)) # 50%
            q3_list.append(np.percentile(df[column], 75)) # 75%
            max_list.append(df[column].max()) # Max
            
            # Zeroes warning
            warning_zeroes = 1 if (zeroes_n / rowcount * 100) >= zeroes_threshold else 0
            warning_zeroes_list.append(warning_zeroes)
            
            # Cardinality warning
            warning_cardinality_list.append(np.NaN)
            
            # Only 1 unique value warning
            warning_one_unique_list.append(np.NaN)
        
        
        
        ##### Other datatypes WIP #####
        else:
            unique_list.append(42.42) # Unique values (n)
            cardinality_list.append(42.42) # Cardinality (%)
            zeroes_list_n.append(42.42) # Zeroes (n)
            zeroes_list_p.append(42.42) # Zeroes (%)
            mean_list.append(42.42) # Mean
            min_list.append(42.42) # Min
            q1_list.append(42.42) # 25%
            q2_list.append(42.42) # 50%
            q3_list.append(42.42) # 75%
            max_list.append(42.42) # Max
            warning_zeroes_list.append(42.42) # Zeroes warning
            warning_cardinality_list.append(42.42) # Cardinality warning
            warning_one_unique_list.append(42.42)# Only 1 unique value warning
    
    
    ##### Stitch all the stats together #####
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
                            
                            ,warning_null_list
                            ,warning_zeroes_list
                            ,warning_cardinality_list
                            ,warning_one_unique_list
                            
                            ,warning_categorical_list
                            ,warning_yesno_list
                            
                         ))
                         )
    df_EDA = df_EDA.T # Transpose
    
    ### Note column & index names and assign them to the EDA df
    column_names = list(df.columns)
    index_names = ['Dtype', 'Count', 'Null(n)', 'Null(%)', 'Unique_categories(n)', 'Cardinality(%)', 'Zeroes(n)', 'Zeroes(%)', 'Mean', 'Min', '25%', '50%', '75%', 'Max', 'Warning_nulls', 'Warning_zeroes', 'Warning_cardinality', 'Warning_1unique_value', 'Warning_should_be_categorical', 'Warning_yesno']
    
    df_EDA.columns = column_names
    df_EDA.index = index_names
    
    
    final_warnings_list = []
    for column in df_EDA:
        
        column_warnings = []
        
        if df_EDA.loc['Warning_nulls' , column] == 1:
            column_warnings.append('High_null_percentage')
        if df_EDA.loc['Warning_zeroes' , column] == 1:
            column_warnings.append('High_zeroes_percentage')
        if df_EDA.loc['Warning_cardinality' , column] == 1:
            column_warnings.append('High_cardinality')
        if df_EDA.loc['Warning_1unique_value' , column] == 1:
            column_warnings.append('Only_1_unique_value')
        if df_EDA.loc['Warning_should_be_categorical' , column] == 1:
            column_warnings.append('Numeric_might_be_categorical')
        if df_EDA.loc['Warning_yesno' , column] == 1:
            column_warnings.append('Only_2_unique_values_inc_nulls')
            
        final_warnings_list.append(column_warnings)
    
    ### Attach the warnings lists to the EDA df and drop the rows that are no longer needed
    df_EDA = df_EDA.append(pd.Series(final_warnings_list, index=df_EDA.columns ), ignore_index=True)  
    df_EDA.index = index_names + ['Warnings']
    
    warnings_to_drop = ['Warning_nulls', 'Warning_zeroes', 'Warning_cardinality', 'Warning_1unique_value', 'Warning_should_be_categorical', 'Warning_yesno']
    df_EDA = df_EDA.drop(warnings_to_drop, axis=0)
        
    
    return df_EDA
    

## Testing
#df_EDA = df_eda(df)





###################################################################################################

def df_overview(df):
    '''
    Input(s):
        1) df - dataframe to analyse
    Output(s):
        1) Dataframe with overview statistics based on the input df
    '''
    
    ### Import libraries
    import pandas as pd
    import numpy as np
    
    ### Note row and column count
    rowcount = (df.shape)[0]
    colcount = (df.shape)[1]
    
    ### Total nulls (%) of whole df
    total_null_p = round(df.isnull().sum().sum() / (rowcount*colcount) * 100 , 2)
    
    ### Counts of data types
    dtype_list = []
    for column in df:
        dtype_list.append(df[column].dtype.name)
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
    
    return df_overview



###################################################################################################

### To enable this module to be called from another Python file
    
if __name__ == '__main__':
    say_hello()
    df_eda()
    df_overview()
    
    
    
    
    
    
    
    