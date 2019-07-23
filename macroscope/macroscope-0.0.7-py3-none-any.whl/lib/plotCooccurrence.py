# External libraries
from matplotlib import pyplot as plt
from pandas import DataFrame

# Standard library
import os
from typing import Tuple
from scipy import sparse

# Local libraries
from lib.getPickleData import getVocab50k, getSumYear, getKernelYearFrequency
from lib.loadSparseCsr import load_sparse_csr
from lib.globals import dataDir


# plot_co_occurence("hello", ["it", "of"], normalize=False)
def plot_co_occurence(targetWord: str, contextWords: Tuple[str], normalize: bool):
    if not isinstance(contextWords, Tuple):
        raise Exception("Context Words variable must be a Tuple of strings")

    voc_50k = getVocab50k()

    file = dataDir + '/50k-matrix-front/' + targetWord[:2] + '/' + str(voc_50k.index(targetWord))+'.npz'

    if not os.path.isfile(file):
        raise Exception('Cooccurrence is not available for this word.')

    data = load_sparse_csr(file)

    cor_occur = []
    for w in contextWords:
        cor_occur.append(data.getcol(voc_50k.index(w)))

    cor_occur = sparse.hstack(cor_occur).todense()
    cor_occur = cor_occur[(1800-1700):, :]

    sum_year = getSumYear()
    kernel_year_freq = getKernelYearFrequency()
    if normalize is False:
        cor_occur = cor_occur/sum_year[:, None]
    else:
        cor_occur = cor_occur/kernel_year_freq[voc_50k.index(targetWord), ][:, None]

    for i in range(cor_occur.shape[1]):
        plt.plot(range(1800, 2009), cor_occur[:, i], label=contextWords[i])
        plt.legend(loc='center left')

    outputD = DataFrame(cor_occur)
    outputD.columns = contextWords
    insert = list(range(1800, 2009))
    outputD.insert(loc=0, column='date', value=insert)

    return outputD.to_csv(index=False)
