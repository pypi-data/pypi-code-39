# External libraries
from numpy import argsort, array, sort, concatenate
from pandas import DataFrame

# Standard library
from typing import Tuple
import os

# Local libraries
from lib.closestSynonyms import closest_synonyms
from lib.getPickleData import getVocab50k, getSumYear
from lib.globals import dataDir
from lib.loadSparseCsr import load_sparse_csr


def change_of_contextW(targetWord: str, years: Tuple[int], k: int, increase: bool):
    if not isinstance(years, Tuple):
        raise Exception("Years variable array must be a Tuple of ints")

    voc_50k = getVocab50k()
    sum_year = getSumYear()

    startYear = min(years)  # year_old
    endYear = max(years)  # year_new

    oldWords = closest_synonyms((targetWord,), startYear, k=100)[1][0]
    newWords = closest_synonyms((targetWord,), endYear, k=100)[1][0]

    oldIndex = [voc_50k.index(w) for w in oldWords]
    newIndex = [voc_50k.index(w) for w in newWords]

    index_o = list(set(oldIndex + newIndex))

    file = dataDir + '/50k-matrix-front/' + targetWord[:2] + '/' + str(voc_50k.index(targetWord)) + '.npz'

    if not os.path.isfile(file):
        raise Exception('Context change is not available for this word.')

    data = load_sparse_csr(file)

    old = data.getrow(startYear - 1700)/sum_year[str(startYear)]
    new = data.getrow(endYear - 1700)/sum_year[str(endYear)]

    old = old.toarray()[:, index_o]
    new = new.toarray()[:, index_o]

    w, dif, dif_i = [], [], []

    if increase:
        dif_i = new - old
    else:
        dif_i = old - new

    order = argsort(-dif_i[0])
    index = array(index_o)[order]
    dif_i = sort(-dif_i)*-1
    w_i = [voc_50k[i] for i in index[:k]]
    dif_i = dif_i[0, :k]
    w = w+w_i
    dif.append(dif_i)

    dif[0] = dif[0]*-1
    dif = concatenate(dif)

    dif = list(dif)

    outputD = DataFrame({'name': w, 'value': dif})

    return outputD.to_csv(index=False)
