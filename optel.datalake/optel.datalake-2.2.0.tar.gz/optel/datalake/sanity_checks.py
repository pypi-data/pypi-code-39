import pyspark.sql.functions as sf
import logging

from pyspark.sql.types import DecimalType


def real_dups(df):
    """
    Check and remove duplicated rows.

    Args:
        df (pyspark.sql.DataFrame): A Spark DataFrame
    """
    nb_rows = df.count()
    nb_distinct = df.distinct().count()
    nb_dups = nb_rows - nb_distinct
    if nb_rows != nb_distinct:
        logging.info("%s real duplicates found, removing them" % nb_dups)
        dedup_df = df.drop_duplicates()
    else:
        logging.info("No real duplicates found")
        dedup_df = df
    return dedup_df


def empty_columns(df):
    """
    Remove columns with 100% missing values.

    Args:
        df (pyspark.sql.DataFrame): A Spark DataFrame

    Returns:
        pyspark.sql.DataFrame: A data frame free of any empty columns.
    """
    missing_obs = df.agg(*[(1 - (sf.count(c) / sf.count('*'))).
                           alias(c) for c in df.columns])
    values = missing_obs.first()
    dict_values = values.asDict()
    logging.info(
        "Percentage of empties in each columns %s", dict_values)
    empty_cols = find_key(dict_values, 1.0)
    logging.info("Empty columns found %s", empty_cols)
    for column in empty_cols:
        df = df.drop(column)
    return df


def convert_decimal_to_float(df):
    """
    Convert columns with decimal types to floating type.

    Args:
        df (pyspark.sql.DataFrame): A Spark DataFrame.

    Returns:
        pyspark.sql.DataFrame: A DataFrame free of any decimal type column.

    """
    names = [c[0] for c in df.dtypes if 'decimal' in c[1]]
    return_df = df
    for name in names:
        return_df = return_df.withColumn(name, return_df[name].cast("float"))
    return return_df


def convert_double_to_float(df):
    """
    Convert columns with decimal types to floating type.

    Args:
        df (pyspark.sql.DataFrame): A Spark DataFrame.

    Returns:
        pyspark.sql.DataFrame: A DataFrame free of any double type column.
    """
    names = [c[0] for c in df.dtypes if 'double' in c[1]]
    return_df = df
    for name in names:
        return_df = return_df.withColumn(name, return_df[name].cast("float"))
    return return_df


def convert_date_to_string(df):
    """
    Convert columns with timestamp and date types to string type with
    the following formatting: yyyy/MM/dd

    Args:
        df (pyspark.sql.DataFrame): A Spark DataFrame.

    Returns:
        pyspark.sql.DataFrame: A DataFrame with dates converted to string

    """
    names = [c[0] for c in df.dtypes if "timestamp" in c[1] or "date" in c[1]]
    return_df = df
    for name in names:
        return_df = (
            return_df.withColumn(
                name, sf.date_format(return_df[name], "yyyy-MM-dd'T'HH:mm:ss")
            )
        )
    return return_df


def find_key(dic, val):
    """
    Return the key of dictionary dic given the value.

    Args:
        dic (dict): A dictionary.
        val (str): A string to search for in the dictionary.

    Returns:
        list: A list of keys (columns) containing a
            specified value (val).
    """
    empty_cols = []
    for key, value in dic.items():
        if value == val:
            empty_cols.append(key)
        else:
            pass
    return empty_cols


def sanitize_datatypes_for_bigquery(df):
    """Change datatypes to make them interoperable between Spark and BigQuery.

    BigQuery support decimal of scale(38,9) while Spark supports (38,18).


    Args:
        df (pyspark.sql.DataFrame):

    Returns:
        pyspark.sql.DataFrame: DataFrame with no decimal type.

    """
    cols = []
    for field in df.schema:
        datatype = field.dataType
        if isinstance(datatype, DecimalType):
            new_precision, new_scale = conform_decimal(
                datatype.precision, datatype.scale
            )
            col = df[field.name].cast(DecimalType(new_precision, new_scale))
        else:
            col = df[field.name]

        cols.append(col)

    return df.select(cols)


def conform_decimal(precision, scale):
    """
    BigQuery supports decimal of type (38, 9) while Spark supports (38, 18).
    Parquet supports decimal with 29 digits max (so precision - scale <= 29).

    Args:
        precision (int):
        scale (int):

    Returns:

        int, int: new_precision and scale for the decimal to be supported.

    """
    if scale > 9:
        scale = 9
    if precision - scale > 29:
        precision = 29 + scale
    return precision, scale
