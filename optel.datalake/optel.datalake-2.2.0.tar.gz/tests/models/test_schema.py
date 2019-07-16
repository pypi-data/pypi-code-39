from optel.datalake.models import schemas

import pytest


@pytest.fixture(scope="module")
def schema_test_dataframe(spark_session):
    cols = ["col1", "col2", "col3", "col5", "col8"]
    vals = [(1, 2, 3, 5, 8)]

    return spark_session.createDataFrame(vals, cols).persist()


def test_select_no_rename_apply(schema_test_dataframe):
    wanted_schema = ["col1", "col2", "col3"]
    schema = schemas.SelectNoRename(wanted_schema)

    df = schema.apply(schema_test_dataframe)
    assert df.columns == wanted_schema


def test_rename_no_select(schema_test_dataframe):
    wanted_schema = {
        "col1": "c1",
        "col8": "c8",
    }
    expected_schema = {"c1", "col2", "col3", "col5", "c8"}

    schema = schemas.RenameNoSelect(wanted_schema)
    df = schema.apply(schema_test_dataframe)

    assert set(df.columns) == expected_schema


def test_rename_and_select_from_nested_dict():
    nested_schema = {
        "col1": {
            "col2": {
                "col3": "c3",
                "col5": "c5"
            },
            "col10": "c10",
        },
        "col4": "c4",
    }
    expected_name_map = {
        "col1.col2.col3": "c3",
        "col1.col2.col5": "c5",
        "col1.col10": "c10",
        "col4": "c4"
    }

    schema = schemas.RenameAndSelect.from_nested(nested_schema)
    assert schema.name_map == expected_name_map


def test_rename_and_select(schema_test_dataframe):
    wanted_schema = {
        "col1": "c1",
        "col5": "c5",
    }

    schema = schemas.RenameAndSelect(wanted_schema)

    df = schema.apply(schema_test_dataframe)
    assert set(df.columns) == set(wanted_schema.values())

