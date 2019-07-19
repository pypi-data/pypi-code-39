#!/usr/bin/python3
#coding=utf-8
import pandas
from winterboot.Autowired import Autowired
from winterboot.Service import Service

config = Autowired('config')
prepareDataService = Autowired('prepareDataService')
neuralNetBuilderService = Autowired('neuralNetBuilderService')
neuralNetTrainerService = Autowired('neuralNetTrainerService')
accuracyCheckService = Autowired('accuracyCheckService')
updateService = Autowired('updateService')

@Service
class CategorizerService:
    def categorize(self):
        trainSet = pandas.read_csv(config.TRAINING_SET_FILE,'\t',encoding='utf-8',names=config.TRAINING_SET_COLUMNS)
        problemSet = pandas.read_csv(config.PROBLEM_SET_FILE,'\t',encoding='utf-8',names=config.PROBLEM_SET_COLUMNS)
        
        data = prepareDataService.prepareData(trainSet, problemSet)
        model = neuralNetBuilderService.buildNeuralNet(data.max_length, data.numberOfOutputNeurons)
        accuracy = neuralNetTrainerService.trainNeuralNet(data.trainValues, data.trainResults, model)
        accuracyCheckService.checkAccuracy(accuracy)
        data.problemResults=model.predict(data.problemValues)
        
        updateService.handleUpdates(data)

