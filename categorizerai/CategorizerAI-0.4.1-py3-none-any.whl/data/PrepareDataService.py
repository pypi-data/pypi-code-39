import types
from winterboot.Autowired import Autowired
from winterboot.Service import Service

config = Autowired('config')
numericConverterService = Autowired('numericConverterService')

@Service
class PrepareDataService:

    def prepareData(self, trainSet, problemSet):
        result = types.SimpleNamespace()
        result.max_length = self.calculateMaximumStringLength(trainSet, problemSet)
        result.numberOfOutputNeurons = max(trainSet.loc[:, config.TRAINING_SET_OUTPUT_COLUMN])+1
    
        result.trainValues = numericConverterService.createNumericArrayFromTextArray(
            trainSet.loc[:, config.PROBLEM_SET_INPUT_COLUMN].values,
            result.max_length)
        result.trainResults = trainSet.loc[:, config.TRAINING_SET_OUTPUT_COLUMN].values
    
        result.problemValues = numericConverterService.createNumericArrayFromTextArray(
            problemSet.loc[:, config.PROBLEM_SET_INPUT_COLUMN].values,
            result.max_length)
        result.problemOids = problemSet.loc[:, config.PROBLEM_SET_ID_COLUMN].values
        return result
    
    def calculateMaximumStringLength(self, trainSet, problemSet):
        max_length = max([len(s) for s in trainSet.loc[:, config.TRAINING_SET_INPUT_COLUMN]])
        max_length = max([max_length]+[len(s) for s in problemSet.loc[:, config.PROBLEM_SET_INPUT_COLUMN]])
        return max_length