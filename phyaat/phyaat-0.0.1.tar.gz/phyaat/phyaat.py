import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy

'''
Author @ Nikesh Bajaj
Date: 18 Apr 2019
Version : 0.0.1
Project Homepage :  https://phyaat.github.io
Contact: n.bajaj@qmul.ac.uk
'''

class phyaat():
	'''
	Predictive Analysis of Auditory Attention from Physiological Signals
	https://phyaat.github.io
	'''

	def __init__(self, name='PA', verbose=False):
		self.name =name
		self.verbose = verbose
		self.version='0.0.1'

	def info(self):
		print('This is starter for the project - version 0.0.1. \n All the contents will be updated soon')

	def version(self):
		print('Current version :',self.version)

	def get_dataset(self, subject = 1, type=['eeg','ppg','gsr']):
		assest ((type(subject)== int) and subject>=1 and subject <=25)
		print('Downloading subject data')
		Xe = np.random.rand([1024,14])
		Xp = np.random.rand([1024,3])
		Xg = np.random.rand([1024,2])
		y  = np.random.rand([1024,1])
		data ={}
		data['Subject']=subject
		data['data'] ={}
		data['data']['Xe'] =Xe
		data['data']['Xp'] =Xp
		data['data']['Xg'] =Xg
		data['data']['y'] =y
		self.data = data

	def filter(self):
		pass

	def removeArtifact(self, Algo='WPA'):
		print('Algo')

	def CreateXY(self):
		X=0
		y=0
		return X,y
