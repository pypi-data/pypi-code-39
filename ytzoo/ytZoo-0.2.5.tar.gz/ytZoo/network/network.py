import warnings
import datetime
import os
import sys
from ytZoo import humanize_filesize

def GetHTMLSoup(url, encoding=""):
    warnings.warn(
        "GetHTMLSoup is deprecated, use SimpleSoup(url).soup instead.")
    return SimpleSoup(url, False, encoding).soup
# backward capability
getHTMLSoup = GetHTMLSoup

def GetDynamicSoup(url):
    warnings.warn(
        "GetDynamic is deprecated, use SimpleSoup(url,dynamic=True).soup instead.")
    return SimpleSoup(url, True).soup
# backward capability
getDynamicSoup = GetDynamicSoup

class RequestHeaders():
    def __init__(self):
        self.default = {
            'Accept': '*/*; q=0.01',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Language': 'q=0.8,en-US;q=0.6,en;q=0.4',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.102 Safari/537.36'
        }

def get_html_static(url, encoding=''):
    import requests
    r = requests.get(url, headers=RequestHeaders().default)
    if encoding != "":
        r.encoding = encoding
    if 400 <= r.status_code and r.status_code <= 600:
        # Client errors or server errors
        raise Exception(
            'Failed retriving webpage, status :{}'.format(r.status_code))
    content = r.text
    return content


def get_html_phantom(url, phantomjs_path):
    from selenium import webdriver
    import time
    import os
    if not os.path.isfile(phantomjs_path):
        raise ValueError("The PhantomJS executable file cannot "
                         "be found at: %s. Please set the correct path with "
                         "then call the function again." % phantomjs_path)
    driver = webdriver.PhantomJS(executable_path=phantomjs_path)
    driver.get(url)
    content = driver.page_source
    driver.close()
    return content


def get_html_chrome(url, executable_path):
    from sys import platform
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(
        executable_path=executable_path, chrome_options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(3)
    src = driver.page_source
    driver.close()
    return src


def get_html(url, method='static', executable_path=None):
    """Get the URL's HTML content

    Parameters
    url : str
        URL to fetch.
    method : str in ['static', 'phantom', 'chrome']
        Method to use to fetch HTML from the URL. 
        'static' uses plain requests module.
        'phantom' use selenium to drive phantomJS.
        'chrome' use selenium to drive headless chrome.
        For 'phantom' and 'chrome', executable_path need to be specified.
    executable_path : str
        Path to the executable.
    
    Returns
    =======
    src : str
        HTML content.
    """

    if method == 'static':
        src = get_html_static(url, encoding='utf8')
    elif method == 'phantom':
        src = get_html_phantom(url, executable_path)
    elif method == 'chrome':
        src = get_html_chrome(url, executable_path)
    else:
        raise ValueError("Unrecongnized method {}.".format(method))
    return src


def get_soup(url, method='static', executable_path=None):
    from bs4 import BeautifulSoup
    src = get_html(url, method, executable_path)
    soup = BeautifulSoup(src, 'html.parser')
    return soup


class SimpleSoup(object):
    """docstring for SimpleSoup"""
    header = {
        'Accept': '*/*; q=0.01',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'q=0.8,en-US;q=0.6,en;q=0.4',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.102 Safari/537.36'
    }

    def __init__(self, url, dynamic=False, encoding=''):
        print("Warning: SimpleSoup is to be deprecated in the future. Call get_static_soup() and get_dynamic_soup() instead.")
        super(SimpleSoup, self).__init__()
        self.url = url
        self.content = ''
        self.encoding = encoding
        self.soup = self.getDynamicSoup(url) if dynamic else self.getHTMLSoup(url, encoding)

    def getHTMLSoup(self, url, encoding=""):
        from bs4 import BeautifulSoup
        import requests
        r = requests.get(url, headers=self.header)
        if encoding != "":
            r.encoding = encoding
        if 400 <= r.status_code and r.status_code <= 600:
            # Client errors or server errors
            raise Exception
        self.content = r.text
        soup = BeautifulSoup(self.content, "html.parser")
        return soup

    def getDynamicSoup(self, url, phantomjs_path):
        #TODO: check the executable path is availble before continuing
        # Notes: 1. try to make use of the [warnings] module.
        #  2. try to define your own exception by inheriting.
        from selenium import webdriver
        from bs4 import BeautifulSoup
        import time
        import os
        if not os.path.isfile(phantomjs_path):
            raise self.PhantomJSFileNotFound("The PhantomJS executable file cannot "
                                             "be found at: %s. Please set the correct path with "
                                             "SimpleSoup.phantomjs_path=your_executable_path, "
                                             "then call the function again." % phantomjs_path)
        driver = webdriver.PhantomJS(executable_path=phantomjs_path)
        driver.get(url)
        self.content = driver.page_source
        soup = BeautifulSoup(self.content, 'html.parser')
        driver.close()
        return soup

    class PhantomJSFileNotFound(Exception):
        '''Error class'''
        pass


class Queen(SimpleSoup):
    """docstring for Queen"""

    def __init__(self):
        pass

    def parser(self):
        warnings.warn("No parser function specified, returning the soup.")
        return self.soup

    def __call__(self, url, dynamic=False, encoding=""):
        super(Queen, self).__init__(url, dynamic, encoding)
        return self.parser()


class Downloader(object):
    headers = {
        'Accept': '*/*; q=0.01',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Referer': 'https://unsplash.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.102 Safari/537.36'
    }

    def __init__(self, url, filepath):
        self.url = url
        self.filepath = filepath
        self.status = 'Pending'
        self.create_time = datetime.datetime.now()
        self.update_time = None
        self.size = None
        self.time_cost = None
        self.avg_speed = None

    def isFileExists(self, filepath):
        return os.path.isfile(filepath)

    def makeDirs(self, filepath):
        dirpath = os.path.split(filepath)[0]
        try:
            os.makedirs(dirpath)
        except OSError:
            pass

    def readDataFromWeb(self, url):
        import requests
        return requests.get(url, headers=self.headers, timeout=3).content

    def writeFile(self, data, filepath):
        open(filepath, 'wb').write(data)

    def go(self):
        try:
                if self.isFileExists(self.filepath):
                    raise FileExistsError
                time_start = datetime.datetime.now()
                self.makeDirs(self.filepath)
                data = self.readDataFromWeb(self.url)
                self.writeFile(data, self.filepath)
                self.time_cost = datetime.datetime.now()-time_start
                # self.size=len(data)
                self.size = sys.getsizeof(data)
                self.avg_speed = self.size/self.time_cost.total_seconds()
                self.setStatus('Succeed')
        except Exception as e:
            self.setStatus('Failed. {0}:{1}'.format(e.__class__.__name__, e))
        return self.__repr__()

    def setStatus(self, newstatus):
        self.status = newstatus
        self.update_time = datetime.datetime.now()

    def isSuccessful(self):
        if self.status == 'Succeed':
            return True
        else:
            return False

    def _status_to_dict(self):
        return {
            'url': self.url,
            'filepath': self.filepath,
            'status': self.status,
            'create_time': str(self.create_time),
            'update_time': str(self.update_time),
            'size': humanize_filesize(self.size) if self.size else None,
            'time_cost': str(self.time_cost),
            'avg_speed': "%s/s" % humanize_filesize(self.avg_speed) if self.avg_speed else None}

    def __repr__(self):
        d = self._status_to_dict()
        import json
        return(json.dumps(d, indent=2, ensure_ascii=False))


def download(url, fpath):
    dld = Downloader(url, fpath)
    dld.go()
    return dld.isSuccessful()
