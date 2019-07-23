# Standard library
from pandas import read_pickle

# Local libraries
from lib.globals import dataDir

# TODO: cache these results? - there must be a more efficient way than loading them every single time they are used in a function


def getVocab50k():
    return read_pickle(dataDir + '/vocabulary.pkl')


def getKernelYearFrequency():
    return read_pickle(dataDir + '/year_count.pkl')


def getSumYear():
    return read_pickle(dataDir + '/sum_year.pkl')
