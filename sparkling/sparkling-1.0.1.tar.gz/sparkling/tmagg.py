from constants import *
from model import KYP
import pandas as pd


def get_feature_mat(kyp):
    inv = kyp.get_summary(by='amount').toPandas()
    tkt = kyp.get_summary(by='ticket').toPandas()



if __name__ == '__main__':
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.max_rows', 5000)
    pd.set_option('display.width', 1000)

    kyp = KYP()
    kyp.load_tickets(PATH, range_start=20180503, range_end=20180503)
    get_feature_mat(kyp)
