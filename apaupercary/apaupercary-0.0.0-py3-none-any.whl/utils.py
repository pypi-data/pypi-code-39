import urllib.parse, requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


PAYLOAD_ABOUT = {
    'project': 'apaupercary',
    'purpose': 'mtg-community',
    'contact': 'sumner.magruder@zmnh.uni-hamburg.de',
    'good-citizen': '50ms-between-calls'
}

def param_str(url, params={}):
    q = ('?' if '?' not in url else '')
    p = {**PAYLOAD_ABOUT, **params}
    s = ','.join([ '{}={}'.format(k,v) for (k, v) in p.items()])
    return '{}{}'.format(q, s)

def request_soup_js(url, delay=30, params={}):
    '''
    Notes:
        1. Assumes Firefox is install in default location on your system

    Arguments:
        url (str): the page to request
        delay (float): how long to wait to allow JS to activate
        params (dict): optional parameters

    Returns:
        soup (bs4.BeautifulSoup): the soup of the requested url
    '''


    p_st = param_str(url, params)

    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(delay)
    driver.get(url+p_st)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    driver.quit()
    return soup


def request_soup(url, params={}):
    '''
    Requests the url and returns the BeautifulSoup of the response's text.
    In addition, provides the parameters PAYLOAD_ABOUT to the get request.
    This allows the host to know who is crawling their website, why, and how
    to contact should there be an issue.

    Arguments:
        url (str): the URL to request via the python requests library get method
        params (dict): optional params to pass to the url. These will be in
            addition to PAYLOAD_ABOUT.

    Returns:
        soup (bs4.BeautifulSoup)
    '''
    request = requests.get(url, params={**PAYLOAD_ABOUT, **params})
    soup = BeautifulSoup(request.text, features="lxml")
    return soup
