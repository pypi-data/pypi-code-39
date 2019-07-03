import yaml


class TableDefnition(object):
  def __init__(self, table_def):
    self.fields = []

  def sql_fields_definition(self):
    pass

  def sql_fileds_name(self):
    pass


def load_table_definition(location):
  return '-- loaded load_table_definition {}'.format(location)


def define_spark_table(table_def, table_location, schema, table):
'''CREATE TABLE {schema}.{table} IF NOT EXISTS
USING PARQUET
OPTIONS (

)
'''
  pass
