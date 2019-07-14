"""Модуль реализующий работу с БД клиента"""

from sqlalchemy.orm import mapper
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy.exc
import hashlib
Base = declarative_base()


class Clients(Base):
    """
    Класс описывающий таблицу clients,
    где хранится список клиентов зарегистрированных на сервере
    """
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    salt = Column(String)
    hash = Column(String)

    def __init__(self, username, salt, hash):
        self.username = username
        self.salt = salt
        self.hash = hash

    def __repr__(self):
        return f'<User( {self.username} , {self.info} )>'


class Sessions(Base):
    """
    Класс описывающий таблицу sessions,
    где хранится информация о подключениях клиентов
    """

    __tablename__ = 'sessions'
    session_id = Column(Integer, primary_key=True)
    id = Column(Integer(), ForeignKey('clients.id'))
    ip = Column(String)
    datetime = Column(DateTime())

    def __init__(self, id, ip, datetime):
        self.id = id
        self.ip = ip
        self.datetime = datetime


class Contacts(Base):
    """
    Класс описывающий таблицу contacts,
    где храниться информация о контактах клиентов
    """

    __tablename__ = 'contacts'
    c_id = Column(Integer, primary_key=True)
    id = Column(Integer(), ForeignKey('clients.id'))
    contact_id = Column(Integer(), ForeignKey('clients.id'))

    def __init__(self, id, contact_id):
        self.id = id
        self.contact_id = contact_id


class Storage:
    """ Класс реализующий работу с БД клиента """

    def __init__(self, dbname):
        """ В конструкторе осуществляется подключение к БД """
        self.engine = create_engine(f'sqlite:///{dbname}')
        self.metadata = Base.metadata
        self.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    # добавляем нового клиента
    def add_client(self, username, salt, pwd):
        """ Метод добавление нового клиента """

        pwdhash = hashlib.sha3_256(
            f'{salt}{pwd}'.encode(
                encoding='UTF-8')).hexdigest()

        client = Clients(username, salt, pwdhash)
        self.session.add(client)
        try:
            self.session.commit()
            return True
        except sqlalchemy.exc.IntegrityError:
            self.session.rollback()
            return False
    # проверка пароля

    def check_password(self, username, password):
        """ Метод проверки паспорта клиента """

        client = self.session.query(Clients).filter_by(
            username=username).first()
        if client:
            pwdhash = hashlib.sha3_256(
                f'{client.salt}{password}'.encode(
                    encoding='UTF-8')).hexdigest()
            if pwdhash == client.hash:
                return True
            else:
                return False
        else:
            return False

    # пишем статистку
    def add_session(self, username, ip, datetime):
        """ Метод записи информации о подключениях клиентов """

        client = self.session.query(Clients).filter_by(
            username=username).first()
        ses = Sessions(client.id, ip, datetime)
        self.session.add(ses)
        self.session.commit()

    # возвращаем список контактов
    def get_contacts(self, username):
        """ Метод получения списка контактов клиента """

        # получаем пользователя
        client = self.session.query(Clients).filter_by(
            username=username).first()
        # print(client)
        # Получаем список контактов
        query = self.session.query(
            Contacts,
            Clients.username).filter_by(
            id=client.id). join(
            Clients,
            Contacts.contact_id == Clients.id)

        # выбираем только имена пользователей и возвращаем их.
        return [contact[1] for contact in query.all()]

    # Добавление контакта
    def add_contact(self, user, contact):
        """Метод добавление контакта в список контактов"""

        # получаем пользователей
        client = self.session.query(Clients).filter_by(username=user).first()
        contact = self.session.query(
            Clients).filter_by(username=contact).first()
        #print(client, contact)
        # Проверяем на корректность и дубль
        if contact and client:
            if not self.session.query(Contacts).filter_by(
                    id=client.id, contact_id=contact.id).count():
                new_contact = Contacts(client.id, contact.id)
                self.session.add(new_contact)
                self.session.commit()

    # Удаление контакта
    def del_contact(self, user, contact):
        """Метод удаления контакта из списка контактов"""

        # получаем пользователей
        client = self.session.query(Clients).filter_by(username=user).first()
        contact = self.session.query(
            Clients).filter_by(username=contact).first()
        # Проверяем на корректность и удаляем
        if contact and client:
            self.session.query(Contacts).filter_by(
                id=client.id, contact_id=contact.id).delete()
            self.session.commit()


if __name__ == '__main__':
    # проверка
    db_storage = Storage(r'db\jim.db3')
    pwd = 'P@ssw0rd'
    salt = 'salt'
    pwdhash = hashlib.sha3_256(
        f'{salt}{pwd}'.encode(
            encoding='UTF-8')).hexdigest()
    db_storage.add_client('Login1', salt, pwd)
    print(db_storage.check_password('Login1', pwd))
    '''
    db_storage.add_contact('Anonym', 'Yephim')
    db_storage.add_contact('Anonym', 'Yephim3')
    db_storage.add_contact('Anonym', 'Guest')

    print(db_storage.get_contacts('Anonym'))
    db_storage.del_contact('Anonym', 'Yephim3')
    print(db_storage.get_contacts('Anonym'))
    '''
