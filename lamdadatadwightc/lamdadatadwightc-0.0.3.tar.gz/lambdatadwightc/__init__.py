import pandas as pd

def checkNull(df): 
	"""
	checkNull is a simple function that returns the sum of the number of nulls 
	you have in each column of your dataframe.
	"""
	assert isinstance(df, pd.DataFrame), "Please submit a dataframe when using this function."
	return df.isnull().sum()

def splitDates(df, col): 
	"""
    splitDates function takes two arguments: the dataframe that will 
    be used and the column (string) that will be parsed into individidual columns for month, day, and year. 
	
	month will be given a column name, month
	day will be given a column name, day 
	year will be given a column name, year
	
    Examples of use:

    >>> splitDates(df, 'date')
    """
	assert isinstance(df, pd.DataFrame), "Please submit a dataframe when using this function."
	assert col in df, "Please submit a column name (case sensitive) that is in your DataFrame."
	assert type(col) == str, "Please submit your column name as a string"
	# assert df[col].dtype == datetime,

	df['month'] = df[col].dt.month 
	df['day'] = df[col].dt.day
	df['year'] = df[col].dt.year

	return df.head()
