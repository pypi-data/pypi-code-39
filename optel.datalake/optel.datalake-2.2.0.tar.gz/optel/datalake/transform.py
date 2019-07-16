from functools import reduce
from pyspark.sql import functions as sf
from pyspark.sql import DataFrame
from pyspark.sql.types import DecimalType
from tzlocal import get_localzone


def convert_ms_timestamp(table, date_columns):
    """
    Convert unix timestamp (ms) to date.

    Args:
        table (pyspark.sql.DataFrame): Spark DataFrame
        date_columns (list): A list of columns to convert
    """
    localtz = get_localzone()
    for date_column in date_columns:
        df_tmp = table.withColumn(
            date_column, (sf.col(date_column)/1000).cast(DecimalType(12, 0)))
        df_tmp = df_tmp.withColumn(
            date_column, df_tmp[date_column].cast('timestamp'))
        df_tmp = df_tmp.withColumn(date_column, sf.to_utc_timestamp(
            df_tmp[date_column], str(localtz)))
        table = df_tmp
    return df_tmp


def rename_some_columns(df, name_mapping):
    """Renames the columns found in the dictionary, leaves the other alone.

    Will ignore any key that is not found in the DataFrame.

    Args:
        df (pyspark.sql.DataFrame): DataFrame to rename.
        name_mapping (dict): old_name: new_name

    Returns:
        pyspark.sql.DataFrame: Renamed.

    """
    columns = {col: df[col] for col in df.columns}

    for old, new in name_mapping.items():
        if old in columns:
            columns[old] = df[old].alias(new)

    return df.select(*columns.values())


def strict_rename_columns(df, name_mapping):
    """Selects the columns found in keys and rename to the associated values.

    Args:
        df (pyspark.sql.DataFrame): DataFrame to rename the columns.
        name_mapping (dict): old_name: new_name.

    Returns:
        pyspark.sql.DataFrame: DataFrame with renamed columns.

    """
    new_columns = [df[old].alias(new) for old, new in name_mapping.items()]
    return df.select(new_columns)


def union_dataframes_by_names(dataframes):
    """Union all the DataFrames using the column names.

    Args:
        dataframes (Iterable): gives at least 2 :class:pyspark.sql.DataFrame:

    Returns:
        pyspark.sql.DataFrame: The union of all DataFrames

    """
    def union_two_dataframe(a: DataFrame, b: DataFrame) -> DataFrame:
        return a.unionByName(b)

    return reduce(union_two_dataframe, dataframes)
