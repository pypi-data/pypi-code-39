import pandas as pd

class LambData:
    def __init__(self):
        pass
    
    def get_numeric_column_labels(self):
        pass
    
    def get_categorical_column_labels(self, df: pd.DataFrame):
        column_labels = df.select_dtypes(exclude=["number","bool_","object_"]).columns.tolist()
        return column_labels
    
    def check_categoricals_for_blanks(self, df: pd.DataFrame):
        df = df.copy()
        mask = pd.DataFrame()
        column_labels = self.get_categorical_column_labels(df)
        for col in column_labels:
            mask[col] = df[col].apply(lambda x: 1 if x.strip(' ')=='' else 0)
        return mask
    
    def check_categoricals_for_question_marks(self, df:pd.DataFrame):
        df = df.copy()
        mask = pd.DataFrame()
        column_labels = self.get_categorical_column_labels(df)
        for col in column_labels:
            mask[col] = df[col].apply(lambda x: 1 if x.strip(' ')=='?' else 0)
        return mask

    def null_check(self, df):
        df = df.copy()
        nulls = df.isna()
        blanks = self.check_categoricals_for_blanks(df)
        question_marks = self.check_categoricals_for_question_marks(df)
        if nulls.sum().sum() > 0:
            print('This dataframe has null values.')
        elif blanks.sum().sum() > 0:
            print('This dataframe has categorical columns with empty strings as values.')
        elif question_marks.sum().sum() > 0:
            print('This dataframe has categorical columns with lone question marks as values.')
        else:
            print('This dataframe has no obvious null or missing values.')
    def add_column_to_df(self, df: pd.DataFrame, new_col: list, name: str):
        df = df.copy()
        new_col = pd.Series(new_col)
        df[name] = new_col
        return df