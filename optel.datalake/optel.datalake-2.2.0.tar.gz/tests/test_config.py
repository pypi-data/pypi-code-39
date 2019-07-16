import optel.datalake.config.elastic as config_elastic
import optel.datalake.config.db as config_sql

options = {"test1": "1", "test2": "2", "test4": "not4"}
user_options = {"test3": "3", "test4":"4", "test5":"5"}

def test_elastic_make_write_sql_options(mocker):
    mocker.patch.dict("optel.datalake.config.elastic.elastic_spark_sql_write_options", options, clear=True)
    elastic_options = config_elastic.make_sql_write_elastic_options(user_options)
    assert elastic_options["test1"] == options["test1"]
    assert elastic_options["test4"] == user_options["test4"]


def test_jdbc_make_load_sql_table_options(mocker):
    options = {"test1": "1", "test2": "2"}
    mocker.patch.dict("optel.datalake.config.db.load_jdbc_options", options, clear=True)
    sql_options = config_sql.make_load_sql_table_options(user_options)
    assert sql_options["test1"] == options["test1"]
    assert sql_options["test4"] == user_options["test4"]
