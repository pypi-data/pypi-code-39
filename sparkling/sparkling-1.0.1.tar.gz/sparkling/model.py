from pyspark.sql import SparkSession
from pyspark.sql.types import StringType
import os
from constants import *
from utils import get_filelist, get_flat_pair


os.environ['PYSPARK_SUBMIT_ARGS'] = '--master local[*] --jars spark-udf-tkf-0.41-SNAPSHOT.jar pyspark-shell'


class KYP:
    """
    A KYP-oriented class that utilize pyspark to perform numerical analysis on EOD files specifically.

    Methods
    -------
    load_tickets(file_dir, range_start=None, range_end=None)
        Load ticket files in advance given file location and date range.
    get_summary(how='amount', groupby=None, flat=False, **kwargs)
        Perform summary on 'amount' and 'ticket', filtered by '**kwargs' and groupby-ed by 'groupby'.
    """
    def __init__(self):
        self.spark = None
        self.spark_df = None

    def load_tickets(self, file_dir, range_start=None, range_end=None):
        """
        Load specified ticket files for further analysis. File location and date range are needed.

        Parameters
        ----------
        file_dir: str
            The location of EOD files.
        range_start: str or int
            The number or string format of the start of the time range, '20180501' for example. None by default.
        range_end: str or int
            The number or string format of the end of the time range, '20180503' for example. None by default.

        Raises
        ------
        ValueError
            range_start or range_end cannot be empty.
        ValueError
            range_start must be less or equal than range_end.
        """

        if not range_start or not range_end:
            raise ValueError("'range_start' or 'range_end' cannot be empty.")
        elif int(range_start) <= int(range_end):
            path = get_filelist(file_dir, range_start, range_end)
            self.spark = SparkSession.builder.getOrCreate()
            self.spark_df = self.spark.read.csv(path, header=False, schema=TICKET_SCHEMA)
        else:
            raise ValueError("'range_start' must be less than or equal to 'range_end'.")

    def get_summary(self, how=None, groupby=None, flat=False, **kwargs):
        """
        Perform summary, filter to ticket files on given keywords.

        Parameters
        ----------
        how: str
        Can only be 'amount' or 'ticket' and perform sum() or count() in either dimension, in descending order.
        None by default and return the original filtered dataframe.
        groupby: str
        Perform the above summary on groupby if any. None by default and return the original filtered dataframe.
        flat: boolean
        If true, explode each row into several using imported udf scala function 'tkf' according to detail and paris
        kwargs: str or int
        Any keyword that can be used to be filtered on. None by default.

        Raises
        ------
        ValueError
            Can only filter by 'flat_pair' if 'flat' is set to True.

        """

        agg_df = self.spark_df
        if flat:
            os.environ[
                'PYSPARK_SUBMIT_ARGS'] = '--master local[*] --jars spark-udf-tkf-0.41-SNAPSHOT.jar pyspark-shell'
            self.spark.udf.registerJavaFunction('tkf', 'io.github.cdarling.tkf')
            self.spark.udf.register('get_flat_pair', get_flat_pair, StringType())
            agg_df.createTempView('df')
            agg_df = self.spark.sql('select *, explode(tkf(detail, pair)) as combination, get_flat_pair(combination) as flat_pair from df')

        for k, v in kwargs.items():
            if not flat and k == 'flat_pair':
                raise ValueError("Can only filter by 'flat_pair' if 'flat' is set to True.")
            else:
                agg_df = agg_df[agg_df[k] == v]

        if groupby:
            if how == 'amount':
                if flat:
                    return agg_df.groupBy(groupby).sum('amount_single').sort('sum(amount_single)', ascending=False)
                else:
                    return agg_df.groupBy(groupby).sum('amount_full').sort('sum(amount_full)', ascending=False)
            elif how == 'ticket':
                return agg_df.groupBy(groupby).count().sort('count', ascending=False)
            else:
                return agg_df
        else:
            return agg_df


if __name__ == '__main__':
    filedir = 'c:/cslo/data/ticket'
    kyp = KYP()
    kyp.load_tickets(filedir, range_start='20180503', range_end='20180503')
    # df = kyp.get_summary(how='ticket', groupby='terminal', flat=True, province=46, flat_pair='2X1')
    df = kyp.get_summary(how='ticket', groupby='terminal', flat=False, province=46, pair='2X1')
    df.show(50, False)
