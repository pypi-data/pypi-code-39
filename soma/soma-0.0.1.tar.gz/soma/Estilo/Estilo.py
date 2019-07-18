import mysql.connector
from mysql.connector import Error
import os
import pandas as pd
import re
import warnings


def connect_and_query(query: str) -> pd.DataFrame:
    """
    Opens a connection to a SQL database and returns the output the Query as a pandas DataFrame
    It is important to note that the environment variables need to be set prior to execution. 

    Args:
        query (string): The query to be fetched at the database.

    Returns:
        output (DataFrame): The output of the query in DataFrame format.
    """

    # for the next part, it is important to set the environment variables
    try:
        print("Opening MySQL Connection")
        mySQLconnection = mysql.connector.connect(
            host=os.environ.get("HOST_PLM_DATABASE"),
            database=os.environ.get("PLM_DATABASE"),
            user=os.environ.get("USER_PLM_DATABASE"),
            password=os.environ.get("PASSWORD_PLM_DATABASE"),
        )
        print("Connection Opened, starting Fetch")

        output = pd.read_sql(query, con=mySQLconnection)

    except Error as e:
        print("Error while connecting to MySQL", e)
        return e

    finally:
        # closing database connection.
        if mySQLconnection.is_connected():
            mySQLconnection.close()
            print("MySQL connection is closed")
            return output


def format_produto_animale(produto: str) -> str:
    """
    Formats the 'produto' column to follow a xx.xx.x+ standard, thus removing forbidden characters (letters, specials, etc).

    Args:
        produto (string): A single entry from the produto column.

    Returns:
        string: The formatted string if it fits the pattern. If no match is found returns nothing (empty string)

    """
    m = re.match("(^[0-9]{2}\.[0-9]{2}\.[0-9]+)", produto)
    if m:
        return m.groups()[0]
    else:
        return produto


def calculate_giro(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Calculates giro and disc from a dataframe

    Args:
        df (DataFrame): A correctly structured DataFrame
        columns (list of strings): The column names that represent ____
    
    Returns:
        df (DataFrame): The original DataFrame with two additional columns,
        giro and discount.
    
    Todo:
        Complete the Args documentation.
    """
    # columns[0] = value, columns[1] = qtde, columns[2] = preco_varejo_original, columns[3] = qtty
    nan_indexes = []

    # checking if any important row has a zero (dividend row)
    for c in columns:
        if c == columns[0]:
            pass
        else:
            if df[c].eq(0).any().sum() > 0:
                column_indexes = np.where(df[columns[1]].eq(0).tolist())[0].tolist()
                nan_indexes = nan_indexes + column_indexes
                warnings.warn(
                    "{} column has at least one 0, resulting in NaN.".format(c)
                )

    warnings.warn("The NaN indexes are: {}".format(np.unique(nan_indexes)))

    # calculating giro
    df["giro"] = df[columns[0]] / (df[columns[1]] * df[columns[2]])
    # calculating discount
    df["disc"] = 1 - df[columns[0]] / (df[columns[3]] * df[columns[2]])

    return df
