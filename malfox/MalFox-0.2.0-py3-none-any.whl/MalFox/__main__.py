#Imports

import os
import sys
import requests
import json
from time import sleep
from time import strftime



#Global Variables

delay = 10

presets = {
	'dataimagelink': '.data.image a[href^="/{type}/{id}/"]{{background-image:url({image})}}\n',
	
	'dataimagelinkbefore': '.data.image a[href^="/{type}/{id}/"]:before{{background-image:url({image})}}\n',
	
	'dataimagelinkafter': '.data.image a[href^="/{type}/{id}/"]:after{{background-image:url({image})}}\n',
	
	'datatitlelink': '.data.title>a[href^="/{type}/{id}/"]{{background-image:url({image})}}\n',
	
	'datatitlelinkbefore': '.data.title>a[href^="/{type}/{id}/"]:before{{background-image:url({image})}}\n',
	
	'datatitlelinkafter': '.data.title>a[href^="/{type}/{id}/"]:after{{background-image:url({image})}}\n',
	
	'animetitle': '.animetitle[href^="/{type}/{id}/"]{{background-image:url({image})}}\n',
	
	'animetitlebefore': '.animetitle[href^="/{type}/{id}/"]:before{{background-image:url({image})}}\n',
	
	'animetitleafter': '.animetitle[href^="/{type}/{id}/"]:after{{background-image:url({image})}}\n',
	
	'more': '#more{id}{{background-image:url({image})}}\n'
}



#CSS Generation Methods

def createCSS(user, type, preset):
	if type != 'both':
		createLocal(user, type, preset)
	
	else:
		createLocal(user, 'anime', preset)
		print('[Log] Waiting %ss artificial delay to avoid MAL spam prevention.' % delay)
		sleep(delay)
		createLocal(user, 'manga', preset)



def createLocal(user, type, preset):
	#Set Variables
	
	errorImage = 'https://cdn.myanimelist.net/r/96x136/images/qm_50.gif?s=3f32c5b34005de86599954f2656b9482';
	fileName = 'MalFox Results/%s\'s %slist.css' % (user, type)
	
	
	#Check Directory OK
	
	if not os.path.exists('MalFox Results'):
		os.makedirs('MalFox Results')
	
	
	# Fetch List Items
	
	offset = 0
	
	while True:
		#Set URL
		
		fetchUrl = 'https://myanimelist.net/%slist/%s/load.json?status=7&offset=%s' % (type, user, offset)
		
		#Add to List
		
		try:
			if offset == 0:
				items = requests.get(fetchUrl).json()
			else:
				items += requests.get(fetchUrl).json()
		except Exception as e:
			print('[Error] Undefined error while writing CSS: %s' % e)
			halt('[Error] Error while writing CSS: %s' % str(e))
		
		#Loop if Needed
		
		if len(items) == 300:
			if offset == 0:
				print('[Log] Waiting %ss artificial delay to avoid MAL spam prevention. Depending on how many entries your list has, there may be a lot of these.' % delay)
			else:
				print('[Log] Waiting %ss artificial delay to avoid MAL spam prevention.' % delay)
			offset += 300
			sleep(delay)
			continue
		else:
			break
	
	# Write to file
	
	file = open(fileName,'w+')
	
	for item in items:
		#Set ID
		
		id = item[type + '_id']
		
		#Set Image
		
		image = item[type + '_image_path']
		image = image.split('?', 1)[0]
		image = image.replace('r/96x136/', '')
		
		#Begin writing
		
		cssLine = presets[preset].format(type = type, id = id, image = image)
		file.write(cssLine)
	
	print('[Log] CSS file for %s successfully created.' % type)
	file.close()



#Generic Methods

def logtofile(string):
	log = open('MalFox errorlog %s.txt' % strftime('%y-%m-%d %H;%M;%S'),'a')
	log.write(str(string))
	log.close()

def halt(*args):
	for ar in args:
		logtofile(ar)
		print(ar)
	print('-- HALTING PROGRAM --')
	sys.exit()



#Main Method

def main():
	#Set User
	
	try:
		user = sys.argv[1]
	except Exception as e:
		if str(e) == 'list index out of range':
			print('[Error] User not specified.')
			halt()
		else:
			print('[Error] Undefined error while setting type: %s' % e)
			halt(e)
	
	
	#Set Type
	
	types = ['anime', 'manga', 'both']
	
	try:
		type = sys.argv[2]
		if type not in types:
			print('[Error] Type is not valid. Please use a valid type i.e: %s' % ', '.join(types))
			halt()
	except Exception as e:
		type = 'both'
		if str(e) == 'list index out of range':
			print('[Log] Type not specified, defaulting to "both".')
		else:
			print('[Error] Undefined error while setting type: %s\nDefaulted to "both".' % e)
			halt('[Error] Error while setting type: %s' % str(e))
	
	
	#Set Preset
	
	try:
		preset = sys.argv[3]
		if preset not in presets:
			print('[Error] Preset is not valid. Please use a valid preset i.e: %s' % ', '.join(presets))
			halt()
	except Exception as e:
		preset = 'dataimagelinkbefore'
		if str(e) == 'list index out of range':
			print('[Log] Preset not specified, defaulting to "dataimagelinkbefore".')
		else:
			print('[Error] Undefined error while setting preset: %s\nDefaulted to "dataimagelinkbefore".' % e)
			'[Error] Error while setting preset: %s' % str(e)
	
	
	#Call CSS
	
	print('[Log] Beginning CSS file creation of %s for user %s with preset %s' % (type, user, preset))
	
	createCSS(user, type, preset)



if __name__ == '__main__':
    main()