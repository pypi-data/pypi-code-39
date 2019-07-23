# coding=utf-8


from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from eventlet.hubs import epolls, kqueue, poll, selects
# from eventlet.hubs import *
import eventlet
import hgoldfish
from hgoldfish.utils import eventlet


class MainWindow(QMainWindow):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None, *a, **kw):
        super().__init__(parent)
        self.btn = QPushButton("测试携程", self)
        self.btn.clicked.connect(lambda: self.operations.spawn(self.task_start))
        self.final_result = {}
        self.ckb = QCheckBox("")
        self.operations = eventlet.GreenletGroup()

    def task_start(self):
        data_sets = {
            'xx面膜': [12000, 1500, 3000],
            'xx手机': [28, 55, 98, 108],
            'xx大衣': [280, 560, 778, 70]
        }
        for key, data_sets in data_sets.items():
            print(f"start key :{key}")
            m = self.middle(key)
            m.send(None)
            for value in data_sets:
                m.send(value)
            m.send(None)
        print(f"final_result", self.final_result,id(self.final_result))

    def middle(self, key):
        while True:
            # import time
            # QApplication.processEvents()
            eventlet.sleep(3)
            # QApplication.processEvents()
            self.final_result[key] = yield from self.sales_sun(key)
            print(f"{key}销量统计完成!")

    def sales_sun(self, selfpro_name):
        total = 0
        nums = []
        while True:
            x = yield
            print(f"{selfpro_name} 销量:{x}")
            if not x:
                break
            total += x
            nums.append(x)
        return total, nums


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    ui = MainWindow()
    ui.show()
    # sys.exit(app.exec_())
    eventlet.start_application()
