from .base_connector import BaseConnector
from .files_connector import DatasetConnector, S3BucketConnector
from .sql_connector import MysqlConnector, SnowflakeConnector, HiveConnector



def DataConnector(data_connector):
    connector = BaseConnector(data_connector)
    if connector.connector_type() == HiveConnector.key_type():
        return HiveConnector(data_connector)

    if connector.connector_type() == MysqlConnector.key_type():
        return MysqlConnector(data_connector)

    if connector.connector_type() == SnowflakeConnector.key_type():
        return SnowflakeConnector(data_connector)

    if connector.connector_type() == DatasetConnector(data_connector):
        return DatasetConnector(data_connector)

    if connector.connector_type() == S3BucketConnector.key_type():
        return S3BucketConnector(data_connector)

