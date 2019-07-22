# -*- coding: utf-8 -*-
import logging
import queue
from selenium import webdriver
import subprocess
import threading

log = logging.getLogger(__name__)

class SeleniumPoolBaseClass:
	pass

class SeleniumPoolSingleton(type):
	_instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(SeleniumPoolSingleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]


class SeleniumPool(SeleniumPoolBaseClass, metaclass=SeleniumPoolSingleton):
    def __init__(self, webDriverPath, poolCnt=0):
        log.info('Create SeleniumPool ... ')

        self._lock = threading.Lock()

        self._poolCnt = poolCnt
        self._webDriverPath = webDriverPath


        self._options = webdriver.ChromeOptions()
        self._options.add_argument('headless')
        self._options.add_argument('no-sandbox')
        self._options.add_argument('disable-dev-shm-usage')
        self._options.add_argument('window-size=1920x1080')
        self._options.add_argument("disable-gpu")
        self._options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        self._options.add_argument("lang=ko_KR")
        self._options.add_argument('--remote-debugging-port=45447')

        if 0 < self._poolCnt:
            self._q = queue.Queue()

            with self._lock:
                for i in range(self._poolCnt):
                    i

                    log.debug('chrome driver loading... ')
                    driver = webdriver.Chrome(self._webDriverPath, chrome_options=self._options)
                    driver.set_page_load_timeout(60)
                    driver.implicitly_wait(5)

                    self._q.put(driver)
        else:
            self._map = dict()

    def createPool(self, threadName):
        log.debug('chrome driver loading... ')

        with self._lock:
            driver = webdriver.Chrome(self._webDriverPath, chrome_options=self._options)
            driver.set_page_load_timeout(60)
            self._map[threadName] = driver
            driver.implicitly_wait(5)

            #SeleniumPool._execute_script_imitating_people(driver)

    @staticmethod
    def _execute_script_imitating_people(driver):
        driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5]}})")
        driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")
        driver.execute_script("const getParameter = WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'NVIDIA Corporation'} if (parameter === 37446) {return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine';}return getParameter(parameter);};")

    def getDriver(self, threadName):
        with self._lock:
            return self._map[threadName]

    @staticmethod
    def clearResource(driverPath):
        driver = webdriver.Chrome(driverPath)
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            driver.close()

    @staticmethod
    def clearResourceCmd():
        result = subprocess.Popen("killall -9 'Google Chrome Helper'",
         shell=True,
         stdout=subprocess.PIPE,
         universal_newlines=True).communicate()[0]

        result = subprocess.Popen('killall -9 chromedriver',
         shell=True,
         stdout=subprocess.PIPE,
         universal_newlines=True).communicate()[0]
        

    



