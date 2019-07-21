#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `neat_panda` package."""

import pytest
import pandas as pd
import numpy as np

from neat_panda import spread, gather, clean_column_names, _clean_column_names

df = pd.DataFrame(
    data={
        "Country": ["Sweden", "Sweden", "Denmark"],
        "Continent": ["Europe", "Europe", "Not known"],
        "Year": [2018, 2019, 2018],
        "Actual": [1, 2, 3],
    }
)


class TestsSpread:
    def test_input_types_1(self):
        with pytest.raises(TypeError):
            spread(df=[1, 2, 3], key="hello", value="Goodbye")

    def test_input_types_key(self):
        with pytest.raises(TypeError):
            spread(df=df, key=1, value="Actual")

    def test_input_types_value(self):
        with pytest.raises(TypeError):
            spread(df=df, key="Country", value=1)

    def test_input_types_fill_bool(self):
        with pytest.raises(TypeError):
            spread(df=df, key="Year", value="Actual", fill=True)

    def test_input_types_fill(self):
        with pytest.raises(TypeError):
            spread(df=df, key="Year", value="Actual", fill=pd.DataFrame)

    def test_input_types_convert(self):
        with pytest.raises(TypeError):
            spread(df=df, key="Year", value="Actual", fill=1, convert="True")

    def test_input_types_sep(self):
        with pytest.raises(TypeError):
            spread(df=df, key="Year", value="Actual", fill=1, convert=True, sep=1)

    def test_user_warning(self):
        with pytest.warns(UserWarning):
            _df = spread(df=df, key="Year", value="Actual", drop=False, convert=True)
            del _df

    def test_no_nan(self):
        _df = spread(df=df, key="Year", value="Actual", drop=True, convert=True)
        assert _df.isna().any().sum() == 0

    def test_fill_other_than_nan(self):
        df1 = spread(df=df, key="Year", value="Actual", fill="Hej", sep="_")
        df2 = spread(df=df, key="Year", value="Actual", sep="_")
        print(df1)
        _idx1 = sorted(df1.query("Year_2019=='Hej'").index.tolist())
        _idx2 = sorted(df2.query("Year_2019.isna()").index.tolist())
        assert _idx1 == _idx2

    def test_spread(self):
        _df = spread(
            df=df,
            key="Year",
            value="Actual",
            fill="NaN",
            drop=False,
            convert=True,
            sep="_",
        )
        print()
        print(_df)
        print()
        print(_df.dtypes)


class TestsGather:
    df_wide = spread(df=df, key="Year", value="Actual")
    # print(df.dtypes)

    def test_equal_df(self, df=df_wide):
        df1 = gather(
            df=df,
            key="Year",
            value="Actual",
            columns=["Country", "Continent"],
            invert_columns=True,
            # convert=True,
        )
        df2 = gather(df=df, key="Year", value="Actual", columns=["2018", "2019"])

        assert df1.equals(df2)

    def test_equal_df_method(self, df=df_wide):
        df1 = gather(
            df=df,
            key="Year",
            value="Actual",
            columns=["Country", "Continent"],
            invert_columns=True,
            # convert=True,
        )
        df2 = df.gather(key="Year", value="Actual", columns=["2018", "2019"])

        assert df1.equals(df2)

    def test_correct_length_range(self):
        with pytest.raises(IndexError):
            gather(df=df, key="Year", value="Actual", columns=range(2, 100))

    # def test_correct_conversion(self, df=df_wide):
    #    print()
    #    print(df.dtypes)
    #    print()
    #    df = gather(
    #        df=df, key="Year", value="Actual", columns=["2018", "2019"], convert=True
    #    )
    #    print(df.dtypes)
    #

    def test_correct_column_type(self):
        with pytest.raises(TypeError):
            gather(df=df, key="Year", value="Actual", columns="string")

    def test_correct_dropna_type(self):
        with pytest.raises(TypeError):
            gather(
                df=df,
                key="Year",
                value="Actual",
                columns=["2018", "2019"],
                drop_na="Yes",
            )

    def test_correct_invertcolumns_type(self):
        with pytest.raises(TypeError):
            gather(
                df=df,
                key="Year",
                value="Actual",
                columns=["2018", "2019"],
                invert_columns="Yes",
            )

    def test_gather(self, df=df_wide):
        __df = gather(
            df=df,
            key="Year",
            value="Actual",
            columns=range(2, 4),
            invert_columns=False,
            drop_na=True,
            # convert=True,
        )
        print()
        print(__df)


class TestsCleanColumns:
    nasty = [
        "Name    ",
        "hej",
        "  name",
        "country",
        "Region5",
        "country",
        "country-name£---",
        "______country@name",
        "CountryName",
        "countryName",
        "Country_Name",
        1,
    ]

    clean = [
        "name1",
        "hej",
        "name2",
        "country1",
        "region5",
        "country2",
        "country_name1",
        "country_name2",
        "country_name3",
        "country_name4",
        "country_name5",
        "1",
    ]

    actual_camel_case_names = ["CountryName", "SubRegion", "IceHockey"]

    faulty_camel_case_names = ["COuntryNaMe", "SUbRegion", "ICeHOckey"]

    snake_case_names = ["country_name", "sub_region", "ice_hockey"]

    def test_type_error(self, cols=clean):
        with pytest.raises(TypeError):
            clean_column_names(object_=tuple(cols))
            _clean_column_names(columns=tuple(cols))

    def test_assert_type(self, cols=clean, df=df):
        assert isinstance(clean_column_names(cols), list)
        assert isinstance(_clean_column_names(cols), list)
        assert isinstance(clean_column_names(df), pd.DataFrame)
        assert isinstance(clean_column_names(df.columns), list)
        assert isinstance(_clean_column_names(df.columns), list)

    def test_assert_correct_result_basic(self, old=nasty, new=clean):
        assert clean_column_names(old, convert_camel_case=True) == new

    def test_assert_correct_result_camel_case1(
        self, old=actual_camel_case_names, new=snake_case_names
    ):
        assert clean_column_names(old, convert_camel_case=True) == new

    def test_assert_errorenous_result_camel_case(
        self, old=faulty_camel_case_names, new=snake_case_names
    ):
        assert clean_column_names(old, convert_camel_case=True) != new

    def test_assert_correct_result_custom(self, old=nasty, new=clean):
        cols3 = _clean_column_names(
            old,
            expressions=[
                r"column.lower()",
                r're.sub(r"\s+", " ", column).strip()',
                r're.sub(r"\W+", "_", column).strip()',
                r'column.rstrip("_").lstrip("_")',
            ],
            convert_duplicates=True,
            convert_camel_case=True,
        )
        assert cols3 == new

    def test_assert_correct_result_custom2(self):
        a = ["-Hello-", "Goodbye?", "HelloGoodbye", "Hello_Goodbye"]
        b = ["hello", "goodbye!", "hello_goodbye1", "hello_goodbye2"]
        c = _clean_column_names(
            a,
            custom={"-": "", "?": "!"},
            convert_camel_case=True,  # the expression 'column.lower()' is not needed since convert_camel_case invokes it
            convert_duplicates=True,
        )
        assert c == b

    def test_assert_correct_result_custom3(self):
        a = ["-Hello-", "Goodbye?", "HelloGoodbye", "Hello_Goodbye"]
        b = ["hello", "goodbye!", "hellogoodbye", "hello_goodbye"]
        c = _clean_column_names(
            a,
            custom={"-": "", "?": "!"},
            convert_camel_case=False,
            convert_duplicates=True,
            expressions=["column.lower()"],
        )
        assert c == b

    def test_assert_correct_result_dataframe(self, df=df):
        messy_cols = ["COUNTRY    ", "coNtinent£", "@@YEar   ", "actual"]
        clean_cols = df.columns.tolist()
        df.columns = messy_cols
        df = clean_column_names(
            df, convert_camel_case=False
        )  # convert camelcase can lead to unexpected behaviour when large and small letters ar mixed and they are not camelcase. set camelcase dfault as false. eg YEar becomes y_ear
        assert df.columns.tolist() == clean_cols

    def test_assert_correct_result_dataframe_method(self, df=df):
        messy_cols = ["COUNTRY    ", "coNtinent£", "@@YEar   ", "actual"]
        clean_cols = df.columns.tolist()
        df.columns = messy_cols
        df = df.clean_column_names(
            convert_camel_case=False
        )  # convert camelcase can lead to unexpected behaviour when large and small letters ar mixed and they are not camelcase.
        assert df.columns.tolist() == clean_cols


# x = gather(df=df, key="year", value="pop", columns=["country","continent"], invert_columns=True).sort_values(by=["country", "year"]).reset_index(drop=True)
# gapminder2 = gapminder[["country", "continent", "year", "pop"]]
# x = spread(df=gapminder2, key="year", value="pop")
# x.equals(gapminder2) -> False since dtyp of year is not equal
