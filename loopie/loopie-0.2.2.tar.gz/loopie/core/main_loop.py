'''
Created on Monday 02/07/2018

file: base_threads.py

@author: yaztown
'''

from loopie.logging import get_logger
logger = get_logger()

from loopie.net.web_app import WebApp
from loopie.net.wsgiserver import WSThread

from loopie.core.base_threads.base_threads import LoopingThread


class MainLoop(LoopingThread):
    def __init__(self,
                 enable_http_server=True,
                 wsgi_app=None,
                 server_host='0.0.0.0',
                 server_port=8000,
                 server_name=None,
                 server_root_dir='www',
                 json_rpc_service_url='/api',
                 enable_web_browsable_api=False,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.name = 'main_loop'
        
        self.httpd = None
        
        self.enable_http_server = enable_http_server
        self.wsgi_app = wsgi_app
        self.server_host = server_host
        self.server_port = server_port
        self.server_name = '{}_server'.format(self.name) if not server_name else server_name
        self.server_root_dir = server_root_dir
        self.json_rpc_service_url = json_rpc_service_url
        self.enable_web_browsable_api = enable_web_browsable_api
        
        self.web_app = self._create_web_app()
        self.json_rpc = self._create_json_rpc()
        
        logger.debug('Initialized {}'.format(self.name))
    
    def importDefaultRoutes(self):
        from loopie.net import routes
    
    def importRoutes(self):
        self.importDefaultRoutes()
    
#     def _setup_mainloop(self):
#         pass
#     
#     def start_sub_threads(self):
#         for sensor in self.sensors:
#             sensor.start()
#         sleep(3)
#         for controller in self.controllers:
#             controller.start()
#     
    def _create_web_app(self):
        return WebApp.getWebApp(www_folder=self.server_root_dir, enable_cors=True)
    
    def _create_json_rpc(self):
        return WebApp.getJsonRpc(web_app=self.web_app, service_url=self.json_rpc_service_url, enable_web_browsable_api=self.enable_web_browsable_api)

    def _start_wsgiserver(self):
        self.httpd = WSThread(self.web_app, host=self.server_host, port=self.server_port, server_name=self.server_name, name='server_thread')
        self.httpd.start()
    
    def start_server(self):
        self._start_wsgiserver()
#     
    def loop_setup(self):
#         self._setup_mainloop()
#         self.start_sub_threads()
        if self.enable_http_server:
            self.start_server()
#         raise NotImplementedError('must implement in subclasses')

    def loop_logic(self):
        pass
#         raise NotImplementedError('must implement in subclasses')
        
    def _stop_wsgiserver(self):
        self.httpd.stop()
    
    def stop_server(self):
        self._stop_wsgiserver()
     
    def stop_sub_threads(self):
        self.stop_server()
#         for controller in self.controllers:
#             controller.stop()
#             controller.join()
#         for sensor in self.sensors:
#             sensor.stop()
#             sensor.join()
#         raise NotImplementedError('must implement in subclasses')
    
    def clean_up(self):
        self.stop_sub_threads()
        
#     def get_status(self):
#         pass
