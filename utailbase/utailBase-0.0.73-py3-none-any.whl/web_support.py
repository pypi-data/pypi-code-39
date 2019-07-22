# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup, NavigableString
import inspect
import ujson
import logging
import lxml
import re
import requests
import shutil
import urllib.request


"""
 http, https url 파일 다운로드
"""
def download_file(url, downloadPath, fileOpenMode = 'wb',
auth_verify=False, auth_id='usrname', auth_pw='password'
):
    try:
        r = requests.get(url, auth=(auth_id, auth_pw), verify=auth_verify,stream=True)
        r.raw.decode_content = True        
        with open(downloadPath, fileOpenMode) as f:
            shutil.copyfileobj(r.raw, f)
    except Exception as inst:
        logging.error('failed downloadfile. url:{}, downloadPath:{}, msg:{}'.format(url, downloadPath, inst.args))
        return False

    return True

"""
 http send
"""
def http_send(url, body='', content_type='json', method='POST'):
    req = urllib.request.Request(url, method=method)

    if content_type == 'json':
        req.add_header('Content-Type', 'application/json; charset=utf-8')

    try:
        if len(body) > 0:
            jsonbody = ujson.dumps(body)
            jsonbodyAsBytes = jsonbody.encode('utf-8')
            req.add_header('Content-Length', len(jsonbodyAsBytes))
            return urllib.request.urlopen(req, jsonbodyAsBytes, timeout=30)
        else:
            return urllib.request.urlopen(req, timeout=30)
    except urllib.error.HTTPError as err:
        logging.getLogger(__name__).error('faild httpSend. url:{}, errCode:{}'.format(url, err.code))
        return None
    except urllib.error.URLError as err:
        logging.getLogger(__name__).error('faild httpSend. url:{}, reason:{}'.format(url, err.reason))
        return None
    except Exception as inst:
        logging.getLogger(__name__).error('faild httpSend. url:{}, msg:{}'.format(url, inst.args))
        return None



class HttpError(Exception):
    def __init__(self, message, filename, line, function, code):
        super().__init__(message)

        # Now for your custom code...
        self.message = message
        self.filename = filename
        self.line = line
        self.function = function
        self.code = code

    def getErrorString(self):
        return 'http error. code:{}. file:{} line:{} function:{} msg:{}'.format(self.code, 
         self.filename, self.line, self.function, self.message,
        )


def raiseHttpError(log, status_code, msg=''):
    previous_frame = inspect.currentframe().f_back
    (filename, line_number, function_name, lines, index) = inspect.getframeinfo(previous_frame)

    errmsg = 'request failed. file:{}({}). func:{}. code:{} / msg:{}'.format(filename, line_number, function_name, status_code, msg)
    log.error(errmsg)
    raise HttpError('failed request. msg:{}'.format(msg), filename, line_number,
        function_name, status_code)



def addHeaderFiledsForScrap(header:dict):
    header['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    header['Accept'] = 'text/html,application/xhtml+xml,application/xml,application/json;q=0.9,*/*;q=0.8'
    header['Accept-Charset'] = 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'
    header['Accept-Encoding'] = 'none'
    header['Accept-Language'] = 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
    header['Connection'] = 'keep-alive'
    header['cache-control'] = 'no-cache'
    header['Content-Type'] = "application/x-www-form-urlencoded"
    
    return header


def strip_tags(html, invalid_tags = ['span',]):
    soup = BeautifulSoup(html, 'html.parser')

    for tag in soup.findAll(True):
        if tag.name in invalid_tags:
            s = ""

            for c in tag.contents:
                if not isinstance(c, NavigableString):
                    c = strip_tags(str(c), invalid_tags)
                s += str(c)

            sNode = BeautifulSoup(s, 'html.parser')
            tag.replaceWith(sNode)

    return soup


def getTextForReport(soup):
    # eliminate script tag
    [s.extract() for s in soup('script')]
    # eliminate script tag
    [s.extract() for s in soup('img')]

    [s.unwrap() for s in soup('span')]
    [s.unwrap() for s in soup('font')]
    [s.unwrap() for s in soup('strong')]

    newSoup = BeautifulSoup(str(soup), 'lxml')

    text = newSoup.get_text(separator='\n').replace(u'\xa0',u'') 
    text = re.sub('[\n]{3,}', '\n\n', text)
    return text