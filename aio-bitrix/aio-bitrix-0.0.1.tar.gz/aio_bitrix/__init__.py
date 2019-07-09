from json import loads
import asyncio
from exceptions import  BitrixExeption

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorError, ContentTypeError

class Bitrix(object):
	""" Class wrapper for Bitrix24 REST API"""
	# Bitrix24 oauth server
	oauth_url = 'https://oauth.bitrix.info/oauth/token/'

	def __init__(self, domain, access_token, refresh_token, client_id='', client_secret=''):
		"""Create Bitrix API object
		:param domain: str Bitrix domain
		:param auth_token: str Auth token
		:param refresh_token: str Refresh token
		:param client_id: str Client ID for refreshing access tokens
		:param client_secret: str Client secret for refreshing access tokens
		"""
		self.crm_url = f'https://{domain}rest/' if domain.endswith("/") else f'https://{domain}/rest/'
		self.access_token = access_token
		self.refresh_token = refresh_token
		self.client_id = client_id
		self.client_secret = client_secret

	
	async def _get_fetch(self, client, url, params, headers=None):
		try:
			async with client.post(url, data=params, params=params, headers=headers) as r:
				return await r.json()
		except AttributeError:
			return {"status": "error", "message": "bad response"}


	async def bitrix_call(self, method, params=None):
		url = f"{self.crm_url}{method}.json"
		query = {'auth': self.access_token}
		if params and isinstance(params, dict):
			query.update(params)
		async with ClientSession() as client:
			json_response = await self._get_fetch(client, url, query)
			if 'error' in json_response and json_response['error'] in ('NO_AUTH_FOUND', 'expired_token'):
				await self.update_tokens(client)

			elif 'error' in json_response and json_response['error'] in 'QUERY_LIMIT_EXCEEDED':
				await asyncio.sleep(3)
				json_response = await self.bitrix_call(method, params)
			else:
				raise BitrixExeption(error=json_response['error'])
			try:
				data = json_response['result']
				while json_response.get('next'):
					# print(params['start'])
					params['start'] = json_response['next']
					query.update(params)
					await asyncio.sleep(1.8)
					json_response = await self._get_fetch(client, url, query)
					data.extend(json_response['result'])
				return {method: data}
			except KeyError:
				return {method: json_response}

	async def update_tokens(self):
		"""Refresh access tokens
		:return:
		"""
		async with ClientSession() as client:
			query = {'grant_type': 'refresh_token', 'client_id': self.client_id, 'client_secret': self.client_secret,
			   'refresh_token': self.refresh_token}
			json_response = await self._get_fetch(client, self.oauth_url, query)
			self.access_token = json_response["access_token"]
			self.refresh_token = json_response["access_token"]
			
			return json_response


	def get_tokens(self):
		return {
			"access_token": self.access_token,
			"refresh_token": self.refresh_token
		}


	async def bitrix_multi_call(self, methods):
		"""
		mutli call method
		methods: dict or list of dicts with "name" => str: method name, "params" => dict: params
		"""
		if isinstance(methods, list) or isinstance(methods, tuple):
			try:
				futures = [
					asyncio.ensure_future(self.bitrix_call(
						method = method["name"],
						params = method["params"])
					) 
					for method in methods
				]
			except KeyError as e:
				raise BitrixExeption(message=f"miss {e}")
		elif isinstance(methods, dict):
			futures = [
					asyncio.ensure_future(self.bitrix_call(
						method = methods["name"],
						params = methods["params"])
					)
				]
		context = dict()
		
		for i, f in enumerate(asyncio.as_completed(futures), start=1):
			context.update(await f)

		return context




