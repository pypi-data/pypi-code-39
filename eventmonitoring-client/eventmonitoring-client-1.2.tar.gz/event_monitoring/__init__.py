import requests
import datetime
import traceback
import time
from pytz import timezone
from django.conf import settings
from .utils import notify_telegram


execute_token = settings.SYSTEM_EVENT_TOKEN
system_name = settings.SYSTEM_EVENT_NAME 
system_url = settings.SYSTEM_EVENT_URL

try:
	em_notifier = False
	if not settings.DEBUG:
		em_notifier = settings.SYSTEM_EM_NOTIFIER
except AttributeError:
	em_notifier = False


if not system_url.endswith("/api/event/"):
	if system_url.endswith("/"):
		system_url = f"{system_url}api/event/"
	else:
		system_url = f"{system_url}/api/event/"


def push_to_event(name, description=None, status=False):
	timestamp = datetime.datetime.fromtimestamp(int(time.time())) + datetime.timedelta(hours=3)
	headers = {"executetoken": execute_token}
	data = {
		"system_name": system_name,
		"event_name": name,
		"event_description": description,
		"finish": status
	}
	if status:
		data["event_end_time"] = timestamp.strftime('%Y-%m-%d %H:%M:%S')
	else:
		time.sleep(0.6)
		data["event_start_time"] = timestamp.strftime('%Y-%m-%d %H:%M:%S')
		data["event_end_time"] = "pending..."
	try:
		r = requests.post(system_url, json=data, headers=headers)
		if r.status_code != 200:
			return False
		return True
	except requests.ConnectionError:
		return False


def push_exception(name, description, trb):
	print(trb)
	exception_url = system_url.split("/api/event/")[0] + "/api/exception/"
	headers = {"executetoken": execute_token}
	data = {
		"system_name": system_name,
		"exc_name": name,
		"exc_description": description,
		"traceback": trb if trb else description
	}
	try:
		r = requests.post(exception_url, json=data, headers=headers)
		if r.status_code != 200:
			return False
		return description
	except requests.ConnectionError:
		return False


def log_exception(name, description, trb=None):
	push_to_event(name=name, description=description, status=True)
	if em_notifier:
		notify_telegram(system_name, name, description, trb)

	return push_exception(name, description, trb)


def get_list_values(keys,description_key, list_value, iter_key, var_names, *args, **kwargs):
	description = ""
	name= ""
	if list_value in kwargs and iter_key in kwargs:
		list_ = kwargs[list_value]
		index = kwargs[iter_key]
		data = list_[index]
		for i in data:
			if isinstance(keys, str):
				if i == keys:
					name = f"{i}:{data[i]}"
			elif keys is not None:
				for k in keys:
					if i == k and i != description_key:
						if name:
							name = f"{name}, {i}:{data[i]}"
						else:
							name = f"{i}:{data[i]}"
		if description_key in kwargs:
			description = kwargs[description_key]
	elif list_value in var_names \
		and iter_key in var_names:
		list_ = args[var_names.index(list_value)]
		index = args[var_names.index(iter_key)] 
		data = list_[index]
		for i in data:
			if isinstance(keys, str):
				if i == keys:
					name = f"{i}:{data[i]}"
			elif keys is not None:
				for k in keys:
					if i == k:
						if name:
							name = f"{name}, {i}:{data[i]}"
						else:
							name = f"{i}:{data[i]}"
			if description_key in var_names:
				description = args[var_names.index(description_key)]
	return {"name": name, "description": description}


def get_values(keys, var_names, *args, **kwargs):
	name = ""
	if isinstance(keys, str):
		if keys in kwargs:
			name = f"{keys}:{kwargs[keys]}"
		elif keys in var_names:
			name = args[var_names.index(keys)]
		else:
			name = keys
	else:
		for key in keys:
			if key in kwargs:
				if name:
					name = f"{name}, {key}:{kwargs[key]}"
				else:
					name = f"{key}:{kwargs[key]}"
			elif key in var_names:
				if name:
					name = f"{name}, {key}:{args[var_names.index(key)]}"
				else:
					name = f"{key}:{args[var_names.index(key)]}"
	return {"name": name}


def _check_lambda_args(args):
	for arg in args:
		if arg.__class__.__name__ == 'LambdaContext':
			return tuple()
	return args

def event(keys=None, description_key=None, custom_description=None, list_value=None, iter_key=None):
	def decorator(function, *args, **kwargs):
		def push_function_results(*args, **kwargs):
			pushed = False
			name = ''
			description = ''
			var_names = function.__code__.co_varnames
			try:
				if list_value:
					list_values = get_list_values(keys, description_key, list_value, iter_key, var_names, *args, **kwargs)
					name = list_values['name']
					description = list_values['description']
				elif keys is not None:
					values = get_values(keys,var_names, *args, **kwargs)
					name = values["name"]
				else:
					name = function.__name__
				
				if not description and custom_description:
					description = custom_description

				pushed = True
				push_to_event(name=name, description=description, status=False)
			except IndexError:
				pass
			# print(pushed)
			try:
				args = _check_lambda_args(args)
				if args or kwargs:
					func_result = function(*args, **kwargs)
				else:
					func_result = function()
			except Exception as exc_description:
				t = traceback.format_exc()
				t = t.replace('func_result = function', f"{function.__name__} - args: {args}, kwargs: {kwargs}")
				return log_exception(name, description=f"{exc_description}", trb=t) 
			if pushed:
				push_to_event(name=name, description=description, status=True)
			return func_result
		return push_function_results
	return decorator