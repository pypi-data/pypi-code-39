import requests
class ConfigBase:
	def __init__(self, accessKey, secretKey):
		self.accessKey = accessKey
		self.secretKey = secretKey

class Authenticate(ConfigBase):
	def __init__(self, *args):
		super().__init__(*args)
		self.apiurl = "https://api.leadsquared.com/"
		self.endpoint = "v2/Authentication.svc/UserByAccessKey.Get"
		self.authurl = self.apiurl + self.endpoint
		self.params = {
		'accessKey' : self.accessKey,
		'secretKey' : self.secretKey,
		}
		self.auth = requests.get(self.authurl , params=self.params)
	def data(self):
		return self.auth.json()