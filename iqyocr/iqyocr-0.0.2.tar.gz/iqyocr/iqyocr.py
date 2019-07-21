import requests
import six
import uiautomator2.ext.ocr as ocr
import base64
import time
class QYOCRObjectNotFound(Exception):
    pass

class iqyocr(ocr.OCR):
    def __init__(self, d,text=None,index=0,contains=None):
        self._d = d
        self._text=text
        self._index=index
        self._contains=contains

    def all(self,_text):
        rawdata = self._d.screenshot(format='raw')
        b64=base64.b64encode(rawdata)
        r = requests.post("http://10.39.30.115/pic/wordPosition", {"image":b64,"target":_text})
        r.raise_for_status()
        resp = r.json()
        print(resp)
        # assert resp['success']
        result = []
        if resp['data']:
            for item in resp['data']:
                for child in item['data']:
                    result.append((child['word'], int(child['x']), int(child['y'])))
        result.sort(key=lambda v: (v[2], v[1]))
        return result

    def __call__(self):
        return QYOCRSelector(self, self._text,self._index,self._contains)
        
class QYOCRSelector(ocr.OCRSelector):
    def __init__(self, server, text=None,index=0, textContains=None):
        self._server = server
        self._d = server._d
        self._text = text
        self._text_contains = textContains
        self._index=index

    def all(self):
        result = []
        for (ocr_text, x, y) in self._server.all(self._text):
            matched = False
            if self._text == ocr_text:  # exactly match
                matched = True
            elif self._text_contains and self._text_contains in ocr_text:
                matched = True
            if matched:
                result.append((ocr_text, x, y))
        return result

    def wait(self, timeout=10):
        deadline = time.time() + timeout
        first = True
        while first or time.time() < deadline:
            first = False
            all = self.all()
            if all:
                return all
        raise QYOCRObjectNotFound(self._text)

    def click(self, timeout=10):
        result = self.wait(timeout=timeout)
        _, x, y = result[self._index]
        self._d.click(x, y)