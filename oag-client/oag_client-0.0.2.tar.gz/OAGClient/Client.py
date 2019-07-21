import requests
import xmltodict
import json

class Client:
    def __init__(self, username, password):
        self.URL = "http://xml.flightview.com/fvDemoConsOOOI/fvxml.exe?"
        self.username = username
        self.password = password

    def make_request(self, oag_request_object):
        username = "" if self.username == "" else "a={}".format(self.username)
        password = "" if self.password == "" else "b={}".format(self.password)

        request_string = "{}&{}&{}".format(username, password, oag_request_object)
        response = requests.get(self.URL+request_string)
        if response.status_code == 200:
            json_response = json.dumps(xmltodict.parse(response.content))
            return json_response
        else:
            return {"error": response.status_code, "content": response.content}


