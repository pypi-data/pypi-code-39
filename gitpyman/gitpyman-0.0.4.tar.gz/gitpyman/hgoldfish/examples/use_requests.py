import logging;

# import requests
import aiohttp

from util.github import get_watching

logging.basicConfig(level=logging.DEBUG)
from hgoldfish.utils import eventlet

try:
    from eventlet.green.urllib import urlopen
except ImportError:  # py3k
    from eventlet.green.urllib.request import urlopen

try:
    from PyQt4.QtCore import Qt
    from PyQt4.QtGui import QApplication, QTextBrowser
except ImportError:
    from PyQt5.QtCore import Qt, QThread, QTimer
    from PyQt5.QtWidgets import QApplication, QTextBrowser

requests = eventlet.import_patched('requests.__init__')
# eventlet.monkey_patch()  # must execute as early as possible
import requests


# import requests_async as requests
# import erequests
class TestWidget(QTextBrowser):
    def __init__(self):
        QTextBrowser.__init__(self)
        self.operations = eventlet.GreenletGroup()

        self.setPlainText("click middle button to navigate www.163.com")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.operations.spawnWithName("print_number", self.printNumbers)
            self.operations.spawn(self.getpage)
        QTextBrowser.mousePressEvent(self, event)

    def printNumbers(self):
        i = 0
        while True:
            eventlet.sleep(0.1)
            i += 1
            self.append(str(i))

    def getpage(self):
        headers = {
            'Connection'               : 'keep-alive',
            'Cache-Control'            : 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent'               : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            'Accept'                   : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding'          : 'gzip, deflate, br',
            'Accept-Language'          : 'zh-CN,zh;q=0.9',
            'If-None-Match'            : 'W/"c59fd8a30c13e5524e4fb6bc0cbd3103"',
        }
        response = get_watching("625781186@qq.com","qq666888")
        # -------------------------- ↓
        # require = erequests.async.get('https://api.github.com/users/625781186/subscriptions',headers=headers)

        # def send(req):
        #     try:
        #         return req.send()
        #     except Exception as e:
        #         return e
        #
        # pool = eventlet.GreenPool(2)
        # job = pool.spawn(send, require)
        #
        #
        # response = job.wait()
        # -------------------------- ↑
        # print(response.content.decode())
        import json

        j = json.loads(response.content.decode())
        page = list(
            map(
                lambda info_dict: {
                    "url"      : info_dict["html_url"],
                    "full_name": info_dict["full_name"],
                }, j)
        )
        self.append(repr(page))
        self.operations.kill("print_number")


if __name__ == "__main__":
    app = QApplication([])
    w = TestWidget()
    w.show()
    eventlet.start_application(quitOnLastWindowClosed=True)
