import os
import io
import json
from copy import deepcopy

APP_ROOT_LABEL = 'APP_ROOT'
APP_ROOT = os.path.dirname(os.path.abspath(__package__))

def read_json(file_path):
	with io.open(file_path, 'r', encoding='utf-8') as data_file:
		return json.load(data_file)

def read_total_config():  # type: (void) -> str
	temp = read_json(os.path.join(APP_ROOT,'config.json'))
	#for key in temp:
	#	temp[key][APP_ROOT_LABEL] = APP_ROOT

	return temp

CONFIG = read_total_config()

def get_env():  # type: (void) -> str
	if os.environ.get('PYTHON_ENV') is None:
		raise Exception('PYTHON_ENV not setted')
	return os.environ.get('PYTHON_ENV')

def get_config(env = get_env()):
	if env == 'development':
		return deepcopy(CONFIG['development'])
	elif env == 'staging':
		return deepcopy(CONFIG['staging'])
	elif env == 'production':
		return deepcopy(CONFIG['production'])
	raise Exception('PYTHON_ENV invalid (' + env + ')')