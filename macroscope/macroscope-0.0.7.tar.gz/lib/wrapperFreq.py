# External libraries
from pandas import DataFrame
from numpy import transpose

# Standard library
from typing import Tuple

# Local libraries
from lib.getPickleData import getVocab50k, getKernelYearFrequency, getSumYear


def plotFreq(targetWords: Tuple[str], startYear: int = 1800, endYear: int = 2009):
    voc_50k = getVocab50k()
    kernel_year_freq = getKernelYearFrequency()
    sum_year = getSumYear()

    tempIndex = [voc_50k.index(w) for w in targetWords]
    freq = kernel_year_freq[tempIndex, ]/sum_year[None, :]

    outputD = DataFrame(transpose(freq))
    outputD.columns = targetWords
    insert = list(range(startYear, endYear))
    outputD.insert(loc=0, column='date', value=insert)

    return outputD


# TODO: figure out what middle, end and start are
def wrapper_freq(wordT: Tuple[str], startYear: int = 1800, endYear: int = 2009):
    # if wordT.count('-') == 2:
    #     saveOutPut = plotFreq_middle(wordT)

    # if wordT.count('-') == 1:
    #     if wordT[0] == '-':
    #         saveOutPut = plotFreq_end(wordT)

    #     elif wordT[-1] == '-':
    #         saveOutPut = plotFreq_start(wordT)

    # if wordT.count('-') == 0:
    #   saveOutPut = plotFreq(wordT)

    output = plotFreq(wordT, startYear, endYear)
    return output.to_csv(index=False)

    # saveOutPut.to_csv(dirName + '/../public/tempFiles/' +
    #                   filename, index=False)
    # return output


# def plotFreq_end(wordT, year_s=1800, year_e=2009):
#     label = wordT
#     wordT = wordT[1:]
#     tempIndex = [voc_50k.index(x) for x in voc_50k if x.endswith(wordT)]
#     tempIndex_freq = kernel_year_freq[tempIndex, :]/sum_year[None, :]
#     tempIndex_freq = tempIndex_freq.sum(axis=0)
#     outputD = pd.DataFrame({label: tempIndex_freq})
#     insert = list(range(year_s, year_e))
#     outputD.insert(loc=0, column='date', value=insert)
#     return outputD


# def plotFreq_start(wordT, year_s=1800, year_e=2009):
#     label = wordT
#     wordT = wordT[:-1]
#     tempIndex = [voc_50k.index(x) for x in voc_50k if x.startswith(wordT)]
#     tempIndex_freq = kernel_year_freq[tempIndex, :]/sum_year[None, :]
#     tempIndex_freq = tempIndex_freq.sum(axis=0)
#     outputD = pd.DataFrame({label: tempIndex_freq})
#     insert = list(range(year_s, year_e))
#     outputD.insert(loc=0, column='date', value=insert)
#     return outputD


# def plotFreq_middle(wordT, year_s=1800, year_e=2009):
#     label = wordT
#     wordT = wordT[1:-1]
#     tempIndex = [voc_50k.index(x) for x in voc_50k if wordT in x]
#     tempIndex_freq = kernel_year_freq[tempIndex, :]/sum_year[None, :]
#     tempIndex_freq = tempIndex_freq.sum(axis=0)
#     outputD = pd.DataFrame({label: tempIndex_freq})
#     insert = list(range(year_s, year_e))
#     outputD.insert(loc=0, column='date', value=insert)
#     return outputD
