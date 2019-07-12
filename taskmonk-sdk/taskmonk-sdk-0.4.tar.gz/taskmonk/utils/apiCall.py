import json
import requests
import sys
import logging

def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))


def get(accToken = None,url='', data={}, timeout=10):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + str(accToken)
    }

    try:
        print(url)
        r = requests.get(url, timeout=timeout, headers=headers)
        r.raise_for_status()
        resp = r.json()
        return json.dumps({
            "response": resp,
            "error": None
        })

    except Exception as e:
        return json.dumps({
            "error": str(e),
            "response": None
        })

def post(accToken, url='', data={}, timeout=30):
    #accToken = access_token()

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + accToken
    }

    try:
        print(url, data)
        req = requests.Request('POST',url, data = data, headers = headers)
        # r = requests.post(url,  headers=headers, data=data, timeout=timeout)
        prepared = req.prepare()
        pretty_print_POST(prepared)
        s = requests.Session()
        res = s.send(prepared)

        res.raise_for_status()
        resp = res.json()
        logging.debug('resp = {}', resp)
        return resp

    except Exception as e:
        logging.exception("Fatal error in main loop")
        raise
        



def fileUpload(accToken, url='', files={}, timeout=30):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + str(accToken)
    }
    
    try:
        # print(url, files)
        r = requests.post(url, files=files, timeout=timeout, headers=headers)
        r.raise_for_status()
        resp = r.json()
        return json.dumps({
            "response": resp,
            "error": None
        })

    except Exception as e:
        return json.dumps({
            "error": str(e),
            "response": None
        })
    # except requests.exceptions.ConnectionError as e:
    #     return {
    #         "error": e,
    #         "response": None
    #     }
    #
    # except requests.exceptions.Timeout as e:
    #     return {
    #         "error": e,
    #         "response": None
    #     }
    #
    # except requests.exceptions.TooManyRedirects as e:
    #     return {
    #         "error": e,
    #         "response": None
    #     }
    #
    # except requests.exceptions.HTTPError as e:
    #     return {
    #         "error": e,
    #         "response": None
    #     }
    #
    # except requests.exceptions.RequestException as e:
    #     return {
    #         "error": e,
    #         "response": None
    #     }
