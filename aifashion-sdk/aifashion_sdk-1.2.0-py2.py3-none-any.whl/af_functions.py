"""
AI Fashion functions sdk


"""




import os
import re
from enum import Enum
import json
import base64
import warnings
import requests



from .af_oauth2 import OAuth2GrandTypes, AFOAuth2


BASEDIR = os.path.dirname(os.path.realpath(__file__))

URL_REGEX = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE
)

TEST_PICTURE_URL = "https://images.aifashion.com/1c/26/fa/1c26fab52ac34349225dcccea3f86f1d.jpg"


APIS_FILE = 'apis.json'
APIS_FILE = os.path.join(BASEDIR, APIS_FILE)

class AFRunMode(Enum):
    """docstring for OAuth2GrandTypes"""
    normal = 10
    batch = 20


ERROR_CODE = {
    400 : "Bad Request 请求出现语法错误",
    401 : "Unauthorized    请求未授权",
    403 : "Forbidden   禁止访问",
    404 : "Not Found   资源未找到",
    405 : "Method Not Allowed  请求方法不适用",
    406 : "Not Acceptable  资源MIME类型不兼容",
    413 : "Request Entity Too Large    请求实体过大",
    429 : "Too Many Requests   请求次数过多或过频繁",
    500 : "Internal Server Error   服务器内部错误",
    503 : "Service Unavailable 服务不可用",
}


class AIFashionFunctions(AFOAuth2):
    """docstring for AIFashionFunctions"""
    with open(APIS_FILE) as fd:
        APIs_dict = json.load(fd)

    def __init__(self, client_id=None, client_secret=None, client_filename=None,
                 grant_type=OAuth2GrandTypes.client_credentials, run_mode=AFRunMode.normal,
                 warning=True, debug=False):
        self.run_mode = run_mode
        assert self.run_mode == AFRunMode.normal or self.run_mode == AFRunMode.batch, \
            "run mode should be AFRunMode.normal or AFRunMode.batch"
        self.warning = warning
        self.debug = debug
        if self.run_mode == AFRunMode.batch:
            self.__check_function_validity__()
            check=True
        else:
            check=False
        super(AIFashionFunctions, self).__init__(client_id, client_secret, client_filename,
                                                 grant_type, check=check, debug=debug)


    def __check_function_validity__(self):
        """
        check validity of inputs
        """
        assert isinstance(self.warning, bool), 'warning should be True/False'
        assert isinstance(self.debug, bool), 'debug should be True/False'


    def get_aifashion_response_json(self, func_name, image_url=None, image_fname=None,
                      image_base64=None, **kwargs):
        """
        get response and transform to dict

        input:
            func_name: name of function, using API_url_dict to get final url
            * image_url: url of image
            * image_fname: filename of local image
            * image_base64: base64 string of image

        output:
            if the result is correct, return the data section
        """
        url = self.APIs_dict[func_name]['url']
        if image_url:
            assert re.match(URL_REGEX, image_url), '{0} is not a valid url'.format(image_url)
            payload = kwargs.copy()
            payload.update({"image_url" : image_url})
        else:
            if image_fname:
                assert os.path.exists(image_fname), '{0} does not exist'.format(image_fname)
                with open(image_fname, 'rb') as fd:
                    image_base64 = base64.b64encode(fd.read()).decode()
            if image_base64:
                payload = kwargs.copy()
                payload.update({"image_base64" : image_base64})
        assert payload, "you need to give image_url, image_fname or image_base64"
        headers = {
            'authorization' : "Bearer {0}".format(self.token)
        }
        if self.debug:
            print('payload : {0}'.format(payload))
            print('headers : {0}'.format(headers))
        response = requests.request("POST", url, json=payload, headers=headers)
        if self.debug:
            print('reture json : {0}'.format(response.text))
        try:
            rjson = json.loads(response.text)
        except:
            return None
        if not 'code' in rjson:
            raise NotImplementedError(rjson['message'])
        else:
            code =rjson['code']
            if code != 100:
                if code in ERROR_CODE:
                    print(ERROR_CODE[code])
                print(rjson['message'])
                if self.debug:
                    print(rjson)
                if self.run_mode == AFRunMode.normal:
                    raise NotImplementedError()
                return None
        return rjson['data']


    def __getattr__(self, name):
        if name in self.APIs_dict:
            if self.run_mode == AFRunMode.batch:
                return lambda image_url=None, image_fname=None, image_base64=None, **kwargs: \
                    self.__proto_function__(name, image_url, image_fname, image_base64, **kwargs)
            elif self.run_mode == AFRunMode.normal:
                return AF_Function_Instance(self, name, self.APIs_dict)
        return super(AIFashionFunctions, self).__getattribute__(name)


    def __proto_function__(self, func_name, image_url=None, image_fname=None, image_base64=None, **kwargs):
        # warnings.warn("This function is just prototype, not complete yet", FutureWarning)
        # func_name = sys._getframe().f_code.co_name # acquire function name, for getting URL
        # print(func_name, image_url, image_fname, image_base64, **kwargs)
        rsjson = self.get_aifashion_response_json(func_name, image_url, image_fname, image_base64, **kwargs)
        return rsjson


    def listall(self):
        format_string = '{0:30s} {1:{3}<15s} {2:<}'
        CHINESE_FULL_CHAR = chr(12288)
        func_name, name, url = '函数名', '功能名称', 'URL'
        print(format_string.format(func_name, name, url, CHINESE_FULL_CHAR))
        for func_name, func_property in self.APIs_dict.items():
            name = func_property.get('name', '')
            url = func_property.get('url', '')
            print(format_string.format(func_name, name, url, CHINESE_FULL_CHAR))

class AF_Function_Instance():
    """docstring for AF_Function_Instance"""
    def __init__(self, func_obj, func_name, APIs_dict):
        super(AF_Function_Instance, self).__init__()
        self.func_obj = func_obj
        self.func_name = func_name
        self.APIs_dict = APIs_dict
        
    def __call__(self, image_url=None, image_fname=None, image_base64=None, **kwargs):
        rsjson = self.func_obj.get_aifashion_response_json(self.func_name, image_url, image_fname, image_base64, **kwargs)
        return rsjson

    @property
    def help(self):
        manual = self.APIs_dict[self.func_name]['manual']
        if manual:
            print(manual)
    
