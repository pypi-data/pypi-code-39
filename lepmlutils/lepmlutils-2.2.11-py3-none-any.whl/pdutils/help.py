import pandas as pd
import numpy as np
from typing import List, Dict
from .globals import *
from .estmode import EstMode
from pandas.api.types import is_string_dtype, is_numeric_dtype
from scipy import stats
from scipy.special import boxcox1p

def most_related_columns(df: pd.DataFrame, target: str, number: int) -> List[str]:
    return list(df.corr()[target].abs().sort_values(ascending=False)[:number].index.values)

def all_cols_except(df: pd.DataFrame, targets: List[str]) -> List[str]:
    return list(set(df.columns.values) - set(targets))

def dummify(df, cols: List[str]):
        onehot = pd.get_dummies(df[cols])
        confirm_all_dropped(onehot, cols)
        df.drop(cols, axis=1, inplace=True)
        for col in onehot:
                df[col] = onehot[col]

def confirm_all_dropped(df: pd.DataFrame, cols: List[str]):
        dropped = set(cols) - set(df.columns.values)
        if len(dropped) < len(cols):
            raise ValueError("the following columns were not one-hot encoded: ", *set(cols) - dropped)

def downsize(df :pd.DataFrame, verbose=True) -> None:
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    start_mem = df.memory_usage().sum() / 1024**2    
    for col in df.columns:
        col_type = df[col].dtypes
        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)  
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)    
    end_mem = df.memory_usage().sum() / 1024**2
    if verbose: print('Mem. usage decreased to {:5.2f} Mb ({:.1f}% reduction)'.format(end_mem, 100 * (start_mem - end_mem) / start_mem))
    return df

# set_true_na replaces all the na values in the given columns with 
# an anomolous integer value if the column is ordinal, or "unknown" 
# if the column is an object.
# The idea is that NA values for these values means that any value
# would be nonsensical. Passing in the names of categorical columns
# will cause errors to be thrown.
def set_true_na(df: pd.DataFrame, cols: List[str]):
        for col in cols:
                assert df[col].dtype.name != "category", f"column {col} was categorical, cannot set true NA values on it"
                if is_string_dtype(df[col]):
                        assert UNKNOWN_STR_VAL not in df[col].unique(), f"column {col} already contains value {UNKNOWN_STR_VAL}."
                        df[col].fillna(UNKNOWN_STR_VAL, inplace=True)
                else:
                        df[col].fillna(UNKNOWN_NUM_VAL, inplace=True)

def convert_to_cat_codes(df: pd.DataFrame, cols: List[str]):
        for col in cols:
                df[col] = df[col].astype('category').cat.codes

def fill_ordinal_na(df: pd.DataFrame, cols: List[str]):
        for col in cols:
                assert ORDINAL_BAD_VALUE not in df[col].unique(), f"column {col} already contains {ORDINAL_BAD_VALUE}" 
                df[col].fillna(ORDINAL_BAD_VALUE, inplace=True)

def encode_to_int(df: pd.DataFrame, encoding: Dict[str, Dict[str, int]]):
        df.replace(encoding, inplace=True)
        for col in encoding.keys():
                df[col].fillna(-1, inplace=True)
                df[col] = df[col].astype("int8")

def cls_impute(est, df: pd.DataFrame, cols: List[str], ignore: List[str]=[]):
        est_impute(est, df, cols, EstMode.classify, ignore=ignore)

def reg_impute(est, df: pd.DataFrame, cols: List[str], ignore: List[str]=[]):
        est_impute(est, df, cols, EstMode.regress, ignore=ignore)

# est_impute replaces all bad values with the given 
# classifier's predictions. It is assmed that the bad values
# have already been replaced with certain integers.
def est_impute(est, df: pd.DataFrame, cols: List[str], mode: EstMode, ignore: List[str]=[]):
        if mode == EstMode.classify:
                bad_val = CATEGORICAL_BAD_VALUE
        else:
                bad_val = ORDINAL_BAD_VALUE

        for col in cols:
                features = all_cols_except(df, [col] + ignore)

                # when training the model we remove rows where the
                # target column has a bad value (since these are 
                # the row's we're trying to predict for). 
                clean_frame =  df.loc[df[col] != bad_val, :]
                est.fit(
                        clean_frame[features], 
                        clean_frame[col]
                )
                preds = est.predict(df[features])
                df.loc[df[col] == bad_val, col] = np.extract((df[col] == bad_val).values, preds)

def str_cols(df: pd.DataFrame) -> List[str]:
        return df.select_dtypes(["category", "object"]).columns.values

def int_cols(df: pd.DataFrame) -> List[str]:
        return all_cols_except(df, str_cols(df))

# used for viewing the results of a Sklearn CV searcher
# more easily.
def best_n_params(results, number):
    params = []
    scores = []
    all_ranks = list(results["rank_test_score"])
    all_params = results["params"]
    all_scores = results["mean_test_score"]
    
    for i in range(number):
        if i+1 in all_ranks:
                indices = [index for index, rank in enumerate(all_ranks) if rank == i+1]
                for index in indices:
                        params.append(all_params[index])
                        scores.append(all_scores[index])
    return (params, scores)

def skew(df: pd.DataFrame, cols: List[str]):
        for col in cols:
                if np.abs(stats.skew(df[col])) > 0.75:
                        df[col] = boxcox1p(
                                df[col], 
                                stats.boxcox_normmax(df[col] + 1)
                        )

def split_at_proportion(df: pd.DataFrame, prop: float):
    a = int(len(df) * prop)
    
    return df.head(a), df.tail(len(df) - a)