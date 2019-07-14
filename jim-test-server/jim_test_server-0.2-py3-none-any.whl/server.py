
import ipaddress
import os
import sys
from socket import AF_INET, SOCK_STREAM, socket
from jim_test_server.jim_module import *
from jim_test_server.log.server_log_config import log
from jim_test_server.log.log_deco import log_deco
import select
from jim_test_server.metaclass import ServerVerifier
from jim_test_server.storage import Storage
from jim_test_server import serv_form
from PyQt5 import QtWidgets
from threading import Thread, Event
import datetime


@log_deco(log)
def set_server_address(ip_addr):
    """
    Функция проверяет введенный IP адрес и возвращает его если он корректен,
    если нет возращает пустую строку.
    """
    try:
        ipaddress.ip_address(ip_addr)
    except ValueError:
        if ip_addr != 'localhost':
            log.error(
                'Формат IP адреса указан неверно!'
                ' По умолчанию используются все IP адреса.')
            ip_addr = ''
    return ip_addr


@log_deco(log)
def set_server_port(ip_port):
    """
    Функция проверяет введенный порт и возвращает его если он корректен,
    если нет возращает 7777.
    """
    try:
        port = int(ip_port)
        if not (port in range(1, 65535)):
            raise ValueError
    except ValueError:
        log.error('Порт указан неверно! По умолчанию используется 7777 порт.')
        port = 7777
    return port


@log_deco(log)
def presence_response(presence_message):
    """ функция возвращает ответ на presence """

    # Делаем проверки
    if MKeys.ACTION.value in presence_message and \
            presence_message[MKeys.ACTION.value] == MTypes.PRESENCE.value and \
            MKeys.TIME.value in presence_message and \
            isinstance(presence_message[MKeys.TIME.value], float):
        # Если всё хорошо шлем ОК
        resp = {MKeys.RESPONSE.value: RespCodes.OK.value}
        return resp
    else:
        # Шлем код ошибки

        resp = {MKeys.RESPONSE.value: RespCodes.WRONG_REQUEST.value}
    return resp


class PortProperty:
    """
    Класс задает тип данных для порт сервера.
    При попытке неккорректного присваивания вызвывает исключение.
    """
    def __set__(self, instance, value):
        if isinstance(value, int):
            if value >= 0:
                instance.__dict__[self.my_attr] = value
            else:
                raise ValueError('Порт не может быть отрицательным')
        else:
            raise TypeError('Порт должен быть числом')

        instance.__dict__[self.my_attr] = value

    def __set_name__(self, owner, my_attr):
        self.my_attr = my_attr


# Class Server инициализируем и запускаем сервер

class Server(Thread, metaclass=ServerVerifier):
    """
    Основной класс реализаующий подключение клиентов, обмен сообщениями и
    запись в БД
    """

    port = PortProperty()

    def __init__(self, addr='', port=7777, dbname=r'db\jim.db3'):
        """
        В конструкторе происходит подключение к БД
        и задаются параметры сервера.
        """
        self.db_storage = Storage(dbname)
        self.addr = addr
        self.port = port
        self.clients = {}
        self.quit_event = Event()
        super().__init__()
        self.daemon = True

    def s_start(self):
        """ Метод запускающий прослушивание порта """
        try:
            self.server = socket(AF_INET, SOCK_STREAM)
            self.server.bind((self.addr, self.port))
            self.server.settimeout(1)
            self.server.listen(5)
        except ConnectionAbortedError:
            log.error('Ошибка запуска сервера!')
            return False

        else:
            log.info('Сервер запущен')
            return True

    def s_stop(self):
        """ Метод останавливающий прослушивание порта """

        self.server.close()

    # функция подключения клиента
    def accept_client(self):
        """ Метод обрабатывающий подключение нового клиента. """

        try:
            client, addr = self.server.accept()
            presence = get_message(client)

            print(
                f'Подключился: {presence[MKeys.USER.value][MKeys.ACCOUNT_NAME.value]}')
            # Проверка имя пользователя пароля
            if self.db_storage.check_password(presence[MKeys.USER.value][MKeys.ACCOUNT_NAME.value],
                                              presence[MKeys.USER.value][MKeys.PASSWORD.value]):
                print(
                    f'Снова  с нами: {presence[MKeys.USER.value][MKeys.ACCOUNT_NAME.value]}')
            # Если такого пользователя нет создается новый пользователь.
            elif self.db_storage.add_client(presence[MKeys.USER.value][MKeys.ACCOUNT_NAME.value], os.urandom(16),
                                            presence[MKeys.USER.value][MKeys.PASSWORD.value]):
                print(
                    f'Впервые подключился: {presence[MKeys.USER.value][MKeys.ACCOUNT_NAME.value]}')
            else:
                #  отсылаем ошибку и закрываем соединение
                send_response(
                    client, {
                        MKeys.RESPONSE.value: RespCodes.AUTH_FAILED.value})
                client.close()
                return False

            self.db_storage.add_session(presence[MKeys.USER.value][MKeys.ACCOUNT_NAME.value], addr[0],
                                        datetime.datetime.fromtimestamp(presence[MKeys.TIME.value]))
            self.clients[client] = [
                presence[MKeys.USER.value][MKeys.ACCOUNT_NAME.value]]

            response = presence_response(presence)
            send_response(client, response)

        except OSError:
            pass
        return True

    def run(self):
        """
        Метод с основным потоком сервера,
        отвечающим за сетевое взаимодейстие.
        """

        while not self.quit_event.is_set():
            self.accept_client()
            r = []
            w = []
            requests = {}
            try:
                r, w, e = select.select(
                    self.clients.keys(), self.clients.keys(), [], 1)
            except BaseException:
                pass
            if r:
                requests = get_messages(r, self.clients)
                req = []
                # обработка сообщений
                # обработанные сообщения добавляются в req и потом удаляются из основного словаря
                # оставшиеся уходят на отправку
                for sock in requests:
                    # Присоединение к чату
                    if requests[sock][MKeys.ACTION.value] == MTypes.JOIN.value:
                        self.clients[sock].append(
                            requests[sock][MKeys.TO.value])
                        req.append(sock)
                    # Получение списка контактов
                    elif requests[sock][MKeys.ACTION.value] == MTypes.GET_CONTACTS.value:
                        print(requests[sock])
                        req.append(sock)
                        #response = presence_response(req)
                        #send_message(client, response)
                        contactlist = self.db_storage.get_contacts(
                            requests[sock][MKeys.USER.value][MKeys.ACCOUNT_NAME.value])

                        send_response(sock, {
                            MKeys.RESPONSE.value: RespCodes.ACCEPTED.value,
                            MKeys.MSG.value: contactlist})

                        # print('get_contacts')
                    elif requests[sock][MKeys.ACTION.value] == MTypes.ADD_CONTACT.value:
                        print(requests[sock])
                        req.append(sock)
                        self.db_storage.add_contact(requests[sock][MKeys.USER.value][MKeys.ACCOUNT_NAME.value],
                                                    requests[sock][MKeys.TO.value])
                        # ToDo доделать респонс добавить ACTION в клиенте обработка в get_thread
                        #send_response(sock, {MKeys.RESPONSE.value: RespCodes.ACCEPTED.value})
                        # print('get_contacts')
                    elif requests[sock][MKeys.ACTION.value] == MTypes.DEL_CONTACT.value:
                        print(requests[sock])
                        req.append(sock)
                        self.db_storage.del_contact(requests[sock][MKeys.USER.value][MKeys.ACCOUNT_NAME.value],
                                                    requests[sock][MKeys.TO.value])
                        # ToDo доделать респонс добавить ACTION
                        #send_response(sock, {MKeys.RESPONSE.value: RespCodes.ACCEPTED.value})

                for ireq in req:
                    requests.pop(ireq)
            if requests:
                send_messages(w, self.clients, requests)
        print('Сервер остановлен')


class GuiServer:
    """Класс реализующий запуск сервера в графическом режиме"""

    def __init__(self):
        """
        Конструктор класса создает обьект serv для сетевого взаимодействия
        и обьект app реализующий графический интерфейс программы
        связывает обьекты графического интерфейса со слотами класса
        """

        self.serv = 0
        self.app = QtWidgets.QApplication(sys.argv)
        window = QtWidgets.QMainWindow()
        self.ui = serv_form.Ui_MainWindow()
        self.ui.setupUi(window)
        self.ui.startBtn.clicked.connect(self.start_server)
        self.ui.stopBtn.clicked.connect(self.stop_server)
        window.show()
        sys.exit(self.app.exec_())

# коннектор для кнопки старт

    def start_server(self):
        """
        Слот обрабатывающий нажатие кнопки старт.
        Берет из  графического интерфейса настройки соединения
        и пытается создать соединение.
        """

        # получаем информацию из GUI
        # ToDO добавить проверку на валидность
        dbname = self.ui.dbnameEdit.text()
        ip_address = self.ui.ipEdit.text()
        port = int(self.ui.portEdit.text())

        self.serv = Server(ip_address, port, dbname)
        if self.serv.s_start():
            self.serv.quit_event.clear()
            self.serv.daemon = True
            self.serv.start()
            self.ui.connect_db(dbname)
            self.ui.statusbar.showMessage('Сервер запущен!')
            self.ui.startBtn.setEnabled(False)
            self.ui.stopBtn.setEnabled(True)

# коннектор для кнопки стоп

    def stop_server(self):
        """
        Слот обрабатывающий нажатие кнопки стоп.
        закрывет все соединения.
        """

        self.serv.quit_event.set()
        self.serv.join()
        self.serv.s_stop()
        self.ui.statusbar.showMessage('Сервер остановлен!')
        self.ui.startBtn.setEnabled(True)
        self.ui.stopBtn.setEnabled(False)


if __name__ == '__main__':

    guiserv = GuiServer()
    # создаем обьект класса сервер
