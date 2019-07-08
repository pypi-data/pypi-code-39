def Authentication(accessKey, secretKey, api_url):
    try:
        params = {"accessKey": accessKey, "secretKey": secretKey}
        method = "GET"
        url = "https://" + api_url + "/v2/Authentication.svc/UserByAccessKey.Get"
        return make_request(method=method, url=url, params=params)
    except Exception as error:
        raise error


def make_request(method, url, params=None, data=None):
    try:
        import requests,json
        headers = {'content-type': 'application/json'}
        req = requests.request(method=method, url=url, params=params, data=json.dumps(data), headers=headers)
        if req.status_code == 200:
            return req.json()
        else: raise Exception(req.text)
    except Exception as error:
        raise error