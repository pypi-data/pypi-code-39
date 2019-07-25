# TODO: cache these results? - there must be a more efficient way than loading them every single time they are used in a function

# Standard library
from pandas import read_pickle

# Local libraries
from lib.getDataDirPath import getDataDirPath


def getVocab50k():
    dataDirPath = getDataDirPath()
    return read_pickle(dataDirPath + '/vocabulary.pkl')


def getKernelYearFrequency():
    dataDirPath = getDataDirPath()
    return read_pickle(dataDirPath + '/year_count.pkl')


def getSumYear():
    dataDirPath = getDataDirPath()
    return read_pickle(dataDirPath + '/sum_year.pkl')
