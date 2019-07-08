import requests

class SomaApi:
    def __init__(self, soma_connect_ip: str):
        self.soma_connect_ip = soma_connect_ip

    def list_devices(self):
        return requests.get(url = "http://"+self.soma_connect_ip+":3000/list_devices").json()['shades']
    
    def open_shade(self, mac: str):
        return requests.get(url = "http://"+self.soma_connect_ip+":3000/open_shade/"+mac).json()['result']
    
    def close_shade(self, mac: str):
        return requests.get(url = "http://"+self.soma_connect_ip+":3000/close_shade/"+mac).json()['result']
