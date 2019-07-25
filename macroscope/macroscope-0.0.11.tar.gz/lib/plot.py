# External libraries
from numpy import transpose, load, seterr
from pandas import DataFrame

# Standard library
from typing import Tuple

# Local libraries
from lib.getDataDirPath import getDataDirPath
from lib.getPickleData import getVocab50k
from lib.enums import PlotType

# TODO: This is not ok! We are ignoring a division by zero
# From here https://stackoverflow.com/questions/14861891/runtimewarning-invalid-value-encountered-in-divide
seterr(divide='ignore', invalid='ignore')


# TODO: only works if start year is 1800 AND end year is 2009
# plot(PlotType.V, ["hello"], 1800, 2009)
def plot(type: PlotType, words: Tuple[str], startYear: int = 1800, endYear: int = 2009):
    if not isinstance(words, Tuple):
        raise Exception("Words variable must be a Tuple of strings")

    dataDirPath = getDataDirPath()

    folderName = dataDirPath + '/norm'
    dataTemp = load(folderName + '/' + 'cache_sum'+'.npy')

    voc_50k = getVocab50k()
    tempIndex = [voc_50k.index(w) for w in words]

    dataArray = []
    if type == PlotType.A:
        dataArray = dataTemp[:, :, 1]/load(folderName + '/' + 'cache_sumCount_denominator_v' + '.npy')
    if type == PlotType.C:
        dataArray = dataTemp[:, :, 2]/load(folderName + '/' + 'cache_sumCount_denominator_c' + '.npy')
    if type == PlotType.V:
        dataArray = dataTemp[:, :, 0]/load(folderName + '/' + 'cache_sumCount'+'.npy')

    if dataArray.__len__() == 0:
        raise Exception('No data in array')

    temp_data = dataArray[tempIndex]
    outputD = DataFrame(transpose(temp_data))
    outputD.columns = words
    insert = list(range(startYear, endYear))
    outputD.insert(loc=0, column='date', value=insert)

    return outputD.to_csv(index=False)
