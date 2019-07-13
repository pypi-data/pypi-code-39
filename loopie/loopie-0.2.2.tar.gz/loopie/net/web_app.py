'''
Created on Friday 12/07/2019

@author: yaztown
'''

from flask import Flask, request
from flask_cors import CORS
from flask_jsonrpc import JSONRPC

import os

from loopie.core.metaclasses import Singleton
from loopie.logging import get_logger
logger = get_logger()


class WebApp(metaclass=Singleton):
    _web_app = None
    _json_rpc = None

    @classmethod
    def getWebApp(cls, *, static_url_path='', www_folder='www', enable_cors=False):
        '''
        the main flask app
        '''
        if cls._web_app:
            return cls._web_app
        
        app_dir_path = os.getcwd()
        www_path = os.path.join(app_dir_path, www_folder)
        cls._web_app = Flask(__name__, static_url_path=static_url_path, static_folder=www_path)
        if enable_cors:
            CORS(cls._web_app)
            # cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
        
        logger.debug('Created web_app (Flask)')
        
        return cls._web_app

    @classmethod
    def getJsonRpc(cls, *, web_app=_web_app, service_url='/api', enable_web_browsable_api=True):
        '''
        the main flask json_rpc
        '''
        if cls._json_rpc:
            return cls._json_rpc
        
        if web_app is None:
            return None
        
        cls._json_rpc = JSONRPC(app=web_app, service_url=service_url, enable_web_browsable_api=enable_web_browsable_api)

        logger.debug('Created web_app (Flask)')
        
        return cls._json_rpc
    
    @classmethod
    def getRequest(cls):
        return request
    
    @classmethod
    def makeResponse(cls, *, success=True, success_msg='', err_msg='', err_code=0, rpc_ret_value=None):
        '''
        Standard Response objects
        '''
        return dict(
            status='Success' if success else 'Error',
            success_msg=success_msg,
            err_msg=err_msg, err_code=err_code,
            rpc_ret_value=rpc_ret_value)
    
    @classmethod
    def makeResponseSuccess(cls, success_msg='', rpc_ret_value=None):
        return cls.makeResponse(success_msg=success_msg, rpc_ret_value=rpc_ret_value)
    
    @classmethod
    def makeResponseError(cls, err_msg='', err_code=-1, rpc_ret_value=None):
        return cls.makeResponse(success=False, err_msg=err_msg, err_code=err_code, rpc_ret_value=rpc_ret_value)
