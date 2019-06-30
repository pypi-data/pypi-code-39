import requests
import json
import os
from cnvrg.modules.errors import CnvrgError
import cnvrg.helpers.auth_helper as auth_helper
import cnvrg.helpers.logger_helper as logger_helper


JSON_HEADERS = {
    "Content-Type": "application/json"
}
def verify_logged_in():
    if not credentials.logged_in:
        raise CnvrgError("Not authenticated")

def __parse_resp(resp, **kwargs):
    try:
        r_j = resp.json()
        return r_j
    except Exception as e:
        logger_helper.log_error(e)
        logger_helper.log_bad_response(**kwargs)



def get(url, data=None):
    verify_logged_in()
    get_url = os.path.join(base_url, url)
    resp = session.get(get_url, params=data)
    return __parse_resp(resp, url=url, data=data)

def post(url, data=None):
    verify_logged_in()
    get_url = os.path.join(base_url, url)
    resp = session.post(get_url, data=json.dumps(data))
    return __parse_resp(resp, url=url, data=data)

def put(url, data=None):
    verify_logged_in()
    get_url = os.path.join(base_url, url)
    resp = session.put(get_url, data=json.dumps(data))
    return __parse_resp(resp, url=url, data=data)

def download_file(url):
    verify_logged_in()
    resp = requests.get(url)
    return resp.text

credentials = auth_helper.CnvrgCredentials()
session = requests.session()
session.headers = {
    "AUTH_TOKEN": credentials.token,
    **JSON_HEADERS
}
base_url = os.path.join(credentials.api_url, "v1")

