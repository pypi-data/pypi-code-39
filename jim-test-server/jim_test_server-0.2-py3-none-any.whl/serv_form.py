"""
Модуль описывающий GUI сервера
Изначально сгенерирован в QtBuilder
"""
import os
import sys
# fix для pyinstaller --onefile
#if hasattr(sys, 'frozen'):
#    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

from PyQt5 import QtCore, QtGui, QtWidgets
from jim_test_server.storage import Clients, Sessions, Storage


# модель для виджета отображения клиентов
class AlchQtList(QtCore.QAbstractListModel):
    """
    Класс реализующий ListModel
    для отображения списка клиентов сервера.
    """
    def __init__(self, session, parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.session = session
        self.refresh()

    def refresh(self):
        self.users = self.session.query(Clients).all()

    def rowCount(self, parent):
        return len(self.users)

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            value = self.users[index.row()]
            return value.username

# модель для виджета отображения статистики


class StatQtList(QtCore.QAbstractListModel):
    """
    Класс реализующий ListModel
    для отображения статистики подключения клиентов.
    """

    def __init__(self, session, parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.session = session
        self.refresh()

    def refresh(self):
        self.users = self.session.query(
            Clients.username,
            Sessions.ip,
            Sessions.datetime)\
            .join(Clients)\
            .all()

    def rowCount(self, parent):
        return len(self.users)

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            value = self.users[index.row()]
            return f'{value.username}:{value.ip}:{value.datetime}'


class Ui_MainWindow(object):
    """Класс реализующий GUI интерфейс"""

    db_storage = 0

    def connect_db(self, dbname):
        """
        Метод реализующий подключение к БД
        и связывание элементов интерфейса с данными из БД
        """

        self.db_storage = Storage(dbname)
        self.clientView.setModel(AlchQtList(self.db_storage.session))
        self.statView.setModel(StatQtList(self.db_storage.session))

    def setupUi(self, MainWindow):
        """ Метод создающий обьекты графического интерфейса """

        MainWindow.setObjectName('MainWindow')
        MainWindow.resize(664, 544)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName('centralwidget')
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 0, 631, 81))
        self.groupBox.setMaximumSize(QtCore.QSize(631, 16777215))
        self.groupBox.setObjectName('groupBox')
        self.ipEdit = QtWidgets.QLineEdit(self.groupBox)
        self.ipEdit.setGeometry(QtCore.QRect(10, 40, 113, 20))
        self.ipEdit.setObjectName('ipEdit')
        self.portEdit = QtWidgets.QLineEdit(self.groupBox)
        self.portEdit.setGeometry(QtCore.QRect(140, 40, 113, 20))
        self.portEdit.setObjectName('portEdit')
        self.startBtn = QtWidgets.QPushButton(self.groupBox)
        self.startBtn.setGeometry(QtCore.QRect(460, 40, 75, 23))
        self.startBtn.setObjectName('startBtn')
        self.stopBtn = QtWidgets.QPushButton(self.groupBox)
        self.stopBtn.setGeometry(QtCore.QRect(550, 40, 75, 23))
        self.stopBtn.setObjectName('stopBtn')
        self.stopBtn.setEnabled(False)
        self.iplabel = QtWidgets.QLabel(self.groupBox)
        self.iplabel.setGeometry(QtCore.QRect(10, 20, 47, 13))
        self.iplabel.setObjectName('iplabel')
        self.portlabel = QtWidgets.QLabel(self.groupBox)
        self.portlabel.setGeometry(QtCore.QRect(140, 20, 47, 13))
        self.portlabel.setObjectName('portlabel')
        self.dbnameEdit = QtWidgets.QLineEdit(self.groupBox)
        self.dbnameEdit.setGeometry(QtCore.QRect(270, 40, 171, 20))
        self.dbnameEdit.setObjectName('dbnameEdit')
        self.baselabel = QtWidgets.QLabel(self.groupBox)
        self.baselabel.setGeometry(QtCore.QRect(270, 20, 81, 16))
        self.baselabel.setObjectName('baselabel')
        # Список клиентов
        self.clientView = QtWidgets.QListView(self.centralwidget)
        # self.clientView.setModel(AlchQtList(self.db_storage.session))

        self.clientView.setGeometry(QtCore.QRect(10, 110, 171, 381))
        self.clientView.setObjectName('clientView')
        # Статистика клиентов
        self.statView = QtWidgets.QListView(self.centralwidget)
        # self.statView.setModel(StatQtList(self.db_storage.session))

        self.statView.setGeometry(QtCore.QRect(380, 110, 256, 381))
        self.statView.setObjectName('statView')
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 90, 47, 13))
        self.label.setObjectName('label')
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(380, 90, 101, 20))
        self.label_2.setObjectName('label_2')
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 664, 21))
        self.menubar.setObjectName('menubar')
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setEnabled(True)
        self.statusbar.setStatusTip('')
        self.statusbar.setObjectName('statusbar')
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.datarefresh)
        self.timer.start(1000)

    def retranslateUi(self, MainWindow):
        """ Метод установки текстовых значений графических элементов """

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate('MainWindow', 'Jim server v0.1'))
        self.groupBox.setTitle(_translate('MainWindow', 'Запуск'))
        self.ipEdit.setText(_translate('MainWindow', '127.0.0.1'))
        self.portEdit.setText(_translate('MainWindow', '7777'))
        self.startBtn.setText(_translate('MainWindow', 'Старт'))
        self.stopBtn.setText(_translate('MainWindow', 'Стоп'))
        self.iplabel.setText(_translate('MainWindow', 'IP адрес'))
        self.portlabel.setText(_translate('MainWindow', 'Порт'))
        self.baselabel.setText(_translate('MainWindow', 'База данных'))
        self.dbnameEdit.setText(_translate('MainWindow', r'db\jim.db3'))

        self.label.setText(_translate('MainWindow', 'Клиенты'))
        self.label_2.setText(_translate('MainWindow', 'Статистика'))

    def datarefresh(self):
        """Метод реализующий обновление данных из БД"""

        if self.db_storage:
            self.clientView.setModel(AlchQtList(self.db_storage.session))
            self.statView.setModel(StatQtList(self.db_storage.session))
