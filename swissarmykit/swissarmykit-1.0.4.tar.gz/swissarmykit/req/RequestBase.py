import abc

try: from definitions_prod import *
except Exception as e: pass # Surpass error. Note: Create definitions_prod.py
from swissarmykit.utils.loggerutils import LoggerUtils


class RequestBase(abc.ABC):
    """
    Ref: https://github.com/uhub/awesome-python
    All method here for bridge between Base Component.
    """
    MAX_THREAD = 20

    def __init__(self):
        self.is_log = False
        self.is_debug = False
        self.is_notify = True
        self.log = LoggerUtils(appConfig.LOG_PATH + '/' + self.__class__.__name__) # type: LoggerUtils
        self.retry_request = True
        self.req_session = None
        self.fail_stop = 0

        self.pool = None
        self.custom_callback = None

    @abc.abstractmethod
    def get_user_agent(self):
        pass

    @abc.abstractmethod
    def get(self, url, params:dict=None):
        pass

    @abc.abstractmethod
    def _get_kw(self, url, override_headers:dict=None, **kw):
        ''' RequestCommon. '''
        pass

    @abc.abstractmethod
    def get_output_path(self):
        pass

    @abc.abstractmethod
    def get_download_images_path(self, sub_path='', num_folder=True, is_favicon=False):
        pass

    @abc.abstractmethod
    def get_html_path(self, file_name=None):
        pass

    @abc.abstractmethod
    def notify(self, msg):
        pass

    @abc.abstractmethod
    def notify_error(self, msg):
        pass

    @abc.abstractmethod
    def enable_notify(self, enable=True):
        pass

    @abc.abstractmethod
    def html_to_desktop(self, html):
        pass

    def enable_debug(self):
        self.is_debug = True

    def enable_log(self):
        self.is_log = True

    def disable_notify(self):
        self.is_notify = False

    def disable_retry(self, value=False, fail_stop=0):
        self.retry_request = value
        self.fail_stop = fail_stop

    def thread_pool(self, task_lst=None, callback=None, number_threads=None, multiple_process=False):
        from proxy.utils.TheadPool import ThreadPoolUtils

        def set_pool(pool, callback):
            self.pool = pool
            self.custom_callback = callback


        if task_lst:
            if not number_threads:
                number_threads = RequestBase.MAX_THREAD  # Default 20 threads

            pool = ThreadPoolUtils()
            pool.set_request_utils(self)
            pool.process(task_lst=task_lst, callback=callback, number_threads=number_threads, callback_getpool=set_pool, multiple_process=multiple_process)
        else:
            self.log.info('Empty task list')

    def add_task(self, task):
        self.pool.add_task(self.custom_callback, task)
        msg = task if isinstance(task, str) else ''
        print('INFO: add new task ' + msg)