# TODO: cache these results? - there must be a more efficient way than loading them every single time they are used in a function

# Standard library
from pandas import read_pickle

# Local libraries
from lib.globals import configFileName, dataDirPropName
from lib.jsonfs import getJsonFromFile


def getVocab50k():
    dataDir = getJsonFromFile(configFileName).get(dataDirPropName)
    return read_pickle(dataDir + '/vocabulary.pkl')


def getKernelYearFrequency():
    dataDir = getJsonFromFile(configFileName).get(dataDirPropName)
    return read_pickle(dataDir + '/year_count.pkl')


def getSumYear():
    dataDir = getJsonFromFile(configFileName).get(dataDirPropName)
    return read_pickle(dataDir + '/sum_year.pkl')
