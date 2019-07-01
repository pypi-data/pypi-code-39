import numpy as np
import random

def shuffle(arrays):
    perm_train = np.arange(arrays[0].shape[0])
    np.random.shuffle(perm_train)
    newDataArray = []
    # use tf.random.shuffle (test if it runs out of a session!) 
    for dataArray in arrays:
        newDataArray.append(dataArray[perm_train])
    return newDataArray

def returnable(data):
    def returnIt():
        return data
    return returnIt

def shuffleData(self):
    self.data = shuffle(self.data)

# deprecated ?
def getRandomSample(self, bz = None):
    _bz = bz if bz != None else self.bz
    niters = (self.data[0].shape[0] // _bz) - 10

    try:
        randomStep = random.randint(0, niters)
    except:
        raise Exception('Out of bounds random exeption')
    
    if randomStep == self.step:
        randomStep += 1
    
    return self.getBatch(step = randomStep, bz = bz)


class Manager():
    def __init__(self, data, indexingShape = None, bz = 32, stochasticSampling = True):
        self.bz = bz
        # TODO: the lambda is probably wrong!
        self.data = data if callable(data) else (lambda indexes: data[indexes])
        self.step = 0
        self.indexingShape = indexingShape
        self.stochastic = stochasticSampling
        self.maxIters = np.prod(indexingShape) // self.bz


    def getBatch(self, step = None, bz = None):
        _step = step if step != None else self.step
        _bz = bz if bz != None else self.bz

        totSize = self.indexingShape[0]
        y = 1

        if len(self.indexingShape) == 2:
            totSize = self.indexingShape[0] * self.indexingShape[1]
            y = self.indexingShape[1]

        indexes = []
        offset = (_step * _bz) % totSize
        indexes = range(offset, offset + _bz)

        if len(self.indexingShape) == 2:
            indexes = list(map(lambda val: [val//y, (val - y * (val//y))], indexes ))
            indexes = np.array(list(zip(*indexes)))

        return np.array(indexes)

    def getStochasticBatch(self, shape = None, bz = None):
        _shape = shape if shape != None else self.indexingShape
        _bz = bz if bz != None else self.bz
        indexes = []

        for shapeLen in _shape:
            ramdomIndexes = np.random.choice(shapeLen, _bz, replace=False)
            indexes.append(ramdomIndexes)
        if len(_shape) == 1:
            indexes = indexes[0]

        return np.array(indexes)

    def getIndexes(self, i = 0, stochastic = None):
        _stoc = stochastic if stochastic != None else self.stochastic

        if _stoc:
            batchIndexes = self.getStochasticBatch()
        else:
            batchIndexes = self.getBatch(step = i)
        
        return batchIndexes

    def __call__(self, i = 0, stochastic = None):
        batchIndexes = self.getIndexes(i = i, stochastic = None)
        batch = self.data(batchIndexes)
        return batch
    
    def __iter__(self):
        self.currentIterI = 0
        return self
    
    def __next__(self):
        indexes = self.getIndexes(i = self.currentIterI)
        
        if self.currentIterI == self.maxIters:
            indexes = list(filter(lambda x: x <  (self.maxIters * self.bz), indexes))
        elif self.currentIterI == self.maxIters + 1:
            raise StopIteration
            self.currentIterI = 0
        
        data = self.data(indexes)
        currentIterI = self.currentIterI

        self.currentIterI += 1
        return (currentIterI, data, indexes)
