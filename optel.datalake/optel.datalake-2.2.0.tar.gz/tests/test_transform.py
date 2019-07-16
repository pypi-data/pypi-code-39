from optel.datalake import transform
from optel.datalake import descriptive_stats


def test_convert_ms_timestamp(me_df_timestamp):
    df_transformed = transform.convert_ms_timestamp(
        me_df_timestamp, ["date", "date2"])
    test_date = df_transformed.select("date").collect()[0][0]
    assert(str(test_date) == "2018-02-01 10:16:17")


def test_missing_values(me_df_timestamp):
    df = descriptive_stats.missing_values(me_df_timestamp)
    null_value = df.select("empty").collect()[0][0]
    assert(null_value == 1.0)


def test_rename_some_columns(all_types_df):
    names = {
        "datetime": "DDDD",
        "decimal": "deci",
        "this name is very unlikely": "should not be found",
    }
    expected_columns = {
        "DDDD", "deci", "date", "string", "long", "double",
    }
    df = transform.rename_some_columns(all_types_df, names)
    assert set(df.columns) == set(expected_columns)


def test_strict_renaming(all_types_df):
    names = {
        "datetime": "DatETi_me",
        "decimal": "Hello World",
    }
    df = transform.strict_rename_columns(all_types_df, names)
    assert set(df.columns) == set(names.values())


def test_union_all_dataframes(all_types_df):
    dataframes = [all_types_df for _ in range(3)]
    df = transform.union_dataframes_by_names(dataframes)
    assert df.count() == all_types_df.count() * len(dataframes)


def test_union_dataframes_by_names(all_types_df):
    df2 = all_types_df.select(
        ["string", "datetime", "long", "decimal", "double", "date"]
    )

    transform.union_dataframes_by_names([all_types_df, df2])
