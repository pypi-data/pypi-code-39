import pathlib
from pyspark.sql import SQLContext, DataFrame

class TDSparkContextBuilder:
    """
    Util method to set TD-specific configuration and validation
    """
    ENDPOINTS = ["us", "jp", "eu01"]

    @classmethod
    def default_jar_path(self):
        return str(pathlib.Path(__file__).parent / 'jars/td-spark-assembly.jar')

    def __init__(self, builder):
        self.builder = builder

    def apikey(self, apikey):
        self.builder.config("spark.td.apikey", apikey)
        return self

    def api_endpoint(self, endpoint):
        self.builder.config("spark.td.api.host", endpoint)
        return self

    def presto_endpoint(self, endpoint):
        self.builder.config("spark.td.presto_api.host", endpoint)
        return self

    def plazma_endpoint(self, endpoint):
        self.builder.config("spark.td.plazma_api.host", endpoint)
        return self

    def site(self, siteName):
        """Set td-spark site to use

        :param siteName: "us", "jp", or "eu01"
        :return: self
        """
        if not siteName in TDSparkContextBuilder.ENDPOINTS:
            raise Exception("Unknown site name: {}. Use one of [{}]".format(siteName, ', '.join(TDSparkContextBuilder.ENDPOINTS)))
        self.builder.config("spark.td.site", siteName)
        return self

    def jars(self, jar_path):
        """Set spark.jars

        :param jar_path: Comma-separated list of jar file paths. Globs are allowed
        :return: self
        """
        self.builder.config("spark.jars", jar_path)
        return self

    def build(self):
        """Build TDSparkContext"""
        spark = self.builder.getOrCreate()
        return TDSparkContext(spark)

class TDSparkContext:
    """
    Treasure Data Spark Context
    """
    def __init__(self, spark):
        self.spark = spark
        self.sqlContext = SQLContext(spark.sparkContext)
        self.sc = spark.sparkContext
        self.td = self.sc._jvm.com.treasuredata.spark.TDSparkContext.apply(self.sqlContext._ssql_ctx)
        self.context_db = "information_schema"

    def df(self, table):
        return self.spark.read.format("com.treasuredata.spark").load(table)

    def __to_df(self, sdf):
        return DataFrame(sdf, self.sqlContext)

    def presto(self, sql, database=None):
        if database is None:
            database = self.context_db
        sdf = self.td.presto(sql, database)
        return self.__to_df(sdf)

    def execute_presto(self, sql, database=None):
        if database is None:
            database = self.context_db
        self.td.executePresto(sql, database)

    def table(self, table):
        return TDTable(self.td.table(table), self.sc, self.sqlContext)

    def db(self, name):
        return TDDatabase(self.td.db(name), self.sc, self.sqlContext)

    def set_log_level(self, log_level):
        self.td.setLogLevel(log_level)

    def use(self, name):
        self.context_db = name

    def insert_into(self, df, table_name):
        df.write.mode("append").format("com.treasuredata.spark").option("table", table_name).save()

    def create_or_replace(self, df, table_name):
        df.write.mode("overwrite").format("com.treasuredata.spark").option("table", table_name).save()

    def create_table_if_not_exists(self, table_name):
        self.td.createTableIfNotExists(table_name)

    def drop_table_if_exists(self, table_name):
        self.td.dropTableIfExists(table_name)

    def create_database_if_not_exists(self, db_name):
        self.td.createDatabaseIfNotExists(db_name)

    def drop_database_if_exists(self, db_name):
        self.td.dropDatabaseIfExists(db_name)

    def create_udp_l(self, table_name, long_column_name):
        self.td.createLongPartitionedTable(table_name, long_column_name)

    def create_udp_s(self, table_name, string_column_name):
        self.td.createStringPartitionedTable(table_name, string_column_name)


class TDDatabase:
    def __init__(self, db, sc, sqlContext):
        self.db = db
        self.sc = sc
        self.sqlContext = sqlContext

    def exists(self):
        return self.db.exists()

    def create_if_not_exists(self):
        self.db.createIfNotExists()

    def drop_if_exists(self):
        self.db.dropIfExists()

    def table(self, table):
        return TDTable(self.db.table(table), self.sc, self.sqlContext)


class TDTable:
    def __init__(self, table, sc, sqlContext):
        self.table = table
        self.sc = sc
        self.sqlContext = sqlContext

    def __new_table(self, table):
        return TDTable(table, self.sc, self.sqlContext)

    def within(self, duration):
        return self.__new_table(self.table.within(duration))

    def drop_if_exists(self):
        self.table.dropIfExists()

    def create_if_not_exists(self):
        self.table.createIfNotExists()

    def exists(self):
        return self.table.exists()

    def within_unixtime_range(self, from_unixtime, to_unixtime):
        return self.__new_table(self.table.withinUnixTimeRange(from_unixtime, to_unixtime))

    def within_utc_time_range(self, from_string, to_string):
        return self.__new_table(self.table.withinTimeRange(from_string, to_string, self.sc._jvm.java.time.ZoneOffset.UTC))

#    def within_time_range(self, from_string, to_string, timezone):
#        return self.__new_table(self.table.withinTimeRange(from_string, to_string, self.sc._jvm.java.time.ZoneOffset.UTC))

    def __to_pydf(self, sdf):
        return DataFrame(sdf, self.sqlContext)

    def df(self):
        return self.__to_pydf(self.table.df())
