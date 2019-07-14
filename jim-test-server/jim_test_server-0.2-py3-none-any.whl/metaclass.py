""" Модуль реализующий метаклассы проверки кода """

from socket import socket
import types
import dis


class ServerVerifier(type):
    """
    Метакласс реализующий проверку  класса сервера
    на использование  протокола TCP и сетевой
    функции connect характерной для клиента.
    """
    def __init__(self, clsname, bases, clsdict):

        # прооверка по словарю аттрибутов и методов класса
        for key in clsdict.keys():
            # для функции  ищем методы сокета в коде.
            if isinstance(clsdict[key], types.FunctionType):
                # print(key)
                bytecode = dis.Bytecode(clsdict[key])
                for instr in bytecode:
                    if instr.argval == 'SOCK_STREAM':
                        print(f'Используется протокол TCP в  методе {key}')
                    if instr.argval == 'connect':
                        print(f'Используется  connect в  методе {key}')
        # Обязательно вызываем конструткор предка:
        super().__init__(clsname, bases, clsdict)


class ClientVerifier(type):
    """
    МетаКласс реализующий проверку класса клиента
    на использование  протокола TCP, сетевых
    функций accept и listen характерной для клиента
    и создания сокетов на уровне классов.
    """
    def __init__(self, clsname, bases, clsdict):

        # прооверка по словарю аттрибутов и методов класса
        for key in clsdict.keys():
            # для функции  ищем методы сокета в коде.
            if isinstance(clsdict[key], types.FunctionType):
                bytecode = dis.Bytecode(clsdict[key])
                for instr in bytecode:
                    if instr.argval == 'SOCK_STREAM':
                        print(f'Используется протокол TCP в  методе {key}')
                    if instr.argval == 'accept':
                        print(f'Используется  accept в  методе {key}')
                    if instr.argval == 'listen':
                        print(f'Используется  listen в  методе {key}')
            elif isinstance(clsdict[key], type(socket())):
                print(f'Атрибут {key} это сокет')

        # Обязательно вызываем конструткор предка:
        super().__init__(clsname, bases, clsdict)
