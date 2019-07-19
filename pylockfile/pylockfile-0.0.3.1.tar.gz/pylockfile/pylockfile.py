#! -*-encoding:utf-8-*-

import os
import sys
import re

class pylockfile(object):

	def __init__(self, path):
		self.path = path
	
	def create(self):
		path = self.path
		if re.match(r'/\w+/\w+/\w+',path) is None:
			print('Wrong path!' %path)
			print('Sample usage: /<DIR>/<DIR>/lockfile')
			sys.exit()
		else:
			directory = path[:path.rfind("/") + 1]
			if os.path.exists(directory) == False:
				os.system('mkdir -p %s' %directory)
			if os.path.isfile(path) == False:
				os.system("touch %s" %path)
			else:
				print("%s already exits!" %self.path)
				sys.exit()
	
	def delete(self):
		path = self.path 
		if re.match(r'/\w+/\w+/\w+',path) is None:
			print('Wrong path! %s' %path)
			print('Sample usage: /<DIR>/<DIR>/lockfile')
			sys.exit()
		else:			
			os.system("rm -f %s" %path)

if __name__ == '__main__':
	print('''USAGE:
In your script paste

import sys
from pylockfile import *

lock = pylockfile('<PATH TO LOCKFILE>') #Initialize module

lock.create() # create lockfile
lock.delete # delete lockfile
''')
