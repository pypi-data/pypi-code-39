import json
import os
import socket
from urllib.parse import parse_qs

import requests


class Client:
	def __init__(self, host='http://localhost:5000', token=None):
		if 'ANNA_HOST' in os.environ:
			self.host = os.environ['ANNA_HOST']
		else:
			self.host = host
		if token is None and 'ANNA_TOKEN' in os.environ:
			self.token = os.environ['ANNA_TOKEN']
		else:
			self.token = token

	def get_headers(self):
		return {'Authorization': 'Bearer ' + str(self.token), 'worker': str(socket.gethostname())}

	def authenticate(self, email, retry=True):
		status = requests.get(self.host + '/', headers=self.get_headers()).status_code
		if status != 200 and retry:
			token = requests.get(self.host + '/auth/token', headers={'Authorization': email})
			if token.status_code == 200:
				try:
					self.token = json.loads(token.content.decode('utf-8'))['token']
				except KeyError:
					pass

			self.authenticate(False)

		return status == 200 and len(self.token) > 0

	def is_authorized(self):
		headers = {'Authorization': 'Bearer ' + str(self.token)}
		return 200 == requests.get(self.host + '/', headers=headers).status_code

	def validate(self, params=None):
		# if not self.is_authorized():
		#	raise PermissionError
		if params is None:
			return {}
		elif isinstance(params, list) or isinstance(params, tuple):
			params = {attribute: params for attribute in ('id', 'tag', 'driver', 'site', 'container', 'status', 'log')}
		elif isinstance(params, str):
			_params = parse_qs(params)
			params = {}
			for attribute, value in _params.items():
				params[attribute.replace('[]', '')] = value

		for attribute, value in params.items():
			if not isinstance(value, list):
				params[attribute] = [value]
		return params

	@staticmethod
	def handle_response(response):
		if response.status_code != 200:
			raise TypeError(response.status_code, response)

		try:
			content = json.loads(response.content.decode('utf-8'))
			if isinstance(content, str):
				if len(content) > 0:
					return json.loads(content)
			return content
		except KeyError:
			return []
		except json.decoder.JSONDecodeError as e:
			return []

	def query(self, params=None):
		endpoint = self.host + '/job/get'
		params = self.validate(params)
		return self.handle_response(requests.get(endpoint, json=params, headers=self.get_headers()))

	def push(self, params):
		endpoint = self.host + '/job/push'
		params = self.validate_job_request(self.validate(params))
		return self.handle_response(requests.post(endpoint, json=params, headers=self.get_headers()))

	def remove(self, params=None):
		endpoint = self.host + '/job/rm'
		params = self.validate(params)
		return self.handle_response(requests.post(endpoint, json=params, headers=self.get_headers()))

	@staticmethod
	def validate_job_request(params):
		if 'driver' not in params:
			raise KeyError('You must specify at least one driver')
		elif params['driver'] in (None, [], '', [''], False, [False]):
			raise ValueError('You must specify at least one driver')
		if 'site' not in params:
			raise KeyError('You must specify at least one site')
		elif params['site'] in (None, [], '', [''], False, [False]):
			raise ValueError('You must specify at least one site')
		return params

	def get_tasks(self, namespace: str):
		endpoint = self.host + '/task/' + namespace
		return self.handle_response(requests.get(endpoint, headers=self.get_headers()))

	def update(self, params):
		endpoint = self.host + '/job/update'
		return self.handle_response(requests.post(endpoint, json=params, headers=self.get_headers()))

	def reserve_job(self, limit: int = 1):
		endpoint = self.host + '/job/reserve/' + str(limit)
		return self.handle_response(requests.post(endpoint, headers=self.get_headers()))
