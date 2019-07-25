# External libraries
from numpy import load
from sklearn import preprocessing
from heapq import nlargest

# Standard library
from typing import Tuple

# Local libraries
from lib.globals import configFileName, dataDirPropName
from lib.jsonfs import getJsonFromFile
from lib.enums import ClosestSearchMethod as Method


# class DataReader:
#     def __init__(self, path):
#         self.path = path

#     def getSgnsData(year):
#         m = load(dataDir + '/sgns-hamilton/' + str(year) + '-w.npy')
#         vocabArray = load(dataDir + '/sgns-hamilton/' +
#                           str(year) + '-vocab.pkl', allow_pickle=True)


# closest = closest_synonyms(["blue"], 1800, 1, Method.SGNS)
def closest_synonyms(words: Tuple[str], year: int = 1990, k: int = 10, method: Method = Method.SVD):
    # words     : a tuple of words
    # year      : select year from 1800 to 2000
    # k         : number of k-nearest neighbors to display

    dataDir = getJsonFromFile(configFileName).get(dataDirPropName)

    if not isinstance(words, Tuple):
        raise Exception("Words variable must be a Tuple of strings")

    # TODO: Add more flexible path and suffix naming - maybe a wrapper class
    # add DataPaths class that reading of file - does caching work with click? How can this be done - store things in memory???

    # Get data for method
    m, vocabArray = [], []
    if method == Method.SGNS:
        m = load(dataDir + '/sgns-hamilton/' + str(year) + '-w.npy')
        vocabArray = load(dataDir + '/sgns-hamilton/' +
                          str(year) + '-vocab.pkl', allow_pickle=True)

    elif method == method.SVD:
        m = load(dataDir + '/embeddings/' + str(year) + '_svd_PPMI.npy')
        vocabArray = load(dataDir + '/vocabulary.pkl', allow_pickle=True)
        m = preprocessing.normalize(m)  # possible shouldn't be done here

    # Find closest array [closeIndex, closeWords, closeScore]
    raw_score, score, closeIndex, closeWords, closeScore = [], [], [], [], []
    for word in words:
        raw_score_i = m.dot(m[vocabArray.index(word), :])
        score_i = nlargest(k, zip(raw_score_i, range(0, m.shape[0])))
        closeIndex_i = [x[1] for x in score_i]
        closeWords_i = [vocabArray[x] for x in closeIndex_i]
        closeScore_i = [x[0] for x in score_i]

        raw_score.append(raw_score_i)
        score.append(score_i)
        closeIndex.append(closeIndex_i)
        closeWords.append(closeWords_i)
        closeScore.append(closeScore_i)

    # TODO: Return tuple of synonym objects
    return closeIndex, closeWords, closeScore
