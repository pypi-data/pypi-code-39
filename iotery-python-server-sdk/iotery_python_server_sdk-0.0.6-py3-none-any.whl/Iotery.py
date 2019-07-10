from requests import get, post, patch, delete
import json
from types import MethodType


def hydrate_route(path, obj):
    """Hydrates a given route path with dictionary items found in obj"""
    split_route = path.split("/")
    for s in split_route:
        if len(s) > 0 and s[0] == ":":
            path = path.replace(
                s, obj[s[1:]])
    return path

def build_query_str(parameters):
    payload = {}
    def flatten(root,path,depth):
        nonlocal payload
        if depth > 0:
            format_string = "{0}[{1}]"
        else:
            format_string = "{0}{1}"
        if isinstance(root,dict):
            for k, val in root.items():
                flatten(val,format_string.format(path,k),depth+1)
        elif isinstance(root,list):
            for idx, val in enumerate(root):
                flatten(val,format_string.format(path,idx),depth+1)
        else:
            payload[path] = root

    flatten(parameters,"",0)
    query_str = "&".join("%s=%s" % (k,v) for k,v in payload.items())
    return query_str


class Iotery:
    """iotery.io python library class for interacting with iotery.io platform.  Wraps the iotery.io REST API.
        Usage: 
            iotery = Iotery("my-key-from-iotery.io")
            device_type = iotery.createDeviceType(data={"name": "My Device Type", ...})

        All SDK specifications can be at https://iotery.io/v1/docs
    """

    def __init__(self, api_key, base_url="https://api.iotery.io/v1"):
        self._api_key = api_key
        self._base_url = base_url
        self._headers = {
            "x-api-key": self._api_key, "Content-Type": "application/json"}


# get the spec:
with open("./spec/api.json", "r") as f:
    _spec = json.load(f)

    # set up the api
    for route in _spec["routes"]:

        # handle methods for each route
        if route["method"] == "GET":
            def handler(self, opts={},  __path=route["path"], **kwargs):
                hydrated_route = hydrate_route(__path, kwargs)
                query_str = build_query_str(opts)

                res = get(self._base_url + hydrated_route, params=query_str,
                          headers=self._headers)
                if res.status_code >= 400:
                    raise res.json()

                return res.json()

        if route["method"] == "POST":
            def handler(self, opts={}, data={},  __path=route["path"], **kwargs):
                hydrated_route = hydrate_route(__path, kwargs)
                query_str = build_query_str(opts)

                res = post(self._base_url + hydrated_route, params=query_str,
                           headers=self._headers, json=data)
                if res.status_code >= 400:
                    raise res.json()

                return res.json()

        if route["method"] == "PATCH":
            def handler(self, opts={}, data={},  __path=route["path"], **kwargs):
                hydrated_route = hydrate_route(__path, kwargs)
                query_str = build_query_str(opts)

                res = patch(self._base_url + hydrated_route, params=query_str,
                            headers=self._headers, json=data)
                if res.status_code >= 400:
                    raise res.json()

                return res.json()

        if route["method"] == "DELETE":
            def handler(self, opts={},  __path=route["path"], **kwargs):
                hydrated_route = hydrate_route(__path, kwargs)
                query_str = build_query_str(opts)

                res = delete(self._base_url + hydrated_route, params=query_str,
                             headers=self._headers)
                if res.status_code >= 400:
                    raise res.json()

                return res.json()
        # attach to the class
        a = setattr(Iotery, route["name"], handler)
