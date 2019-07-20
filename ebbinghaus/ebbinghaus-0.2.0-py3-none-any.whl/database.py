import os
import datetime
import peewee
import random

INITIAL_DATE = datetime.date(1970, 1, 1)
database_proxy = peewee.DatabaseProxy()


class EbbinghausModel(peewee.Model):
    class Meta:
        database = database_proxy

    external_id = peewee.IntegerField(unique=True)
    created_datetime = peewee.DateField(default=datetime.date.today)
    date_1 = peewee.DateField(default=INITIAL_DATE)
    date_2 = peewee.DateField(default=INITIAL_DATE)
    date_3 = peewee.DateField(default=INITIAL_DATE)
    date_4 = peewee.DateField(default=INITIAL_DATE)
    date_5 = peewee.DateField(default=INITIAL_DATE)
    date_6 = peewee.DateField(default=INITIAL_DATE)
    date_7 = peewee.DateField(default=INITIAL_DATE)
    date_8 = peewee.DateField(default=INITIAL_DATE)

    @property
    def stage(self):
        return len([date for date in [
            self.date_1, self.date_2, self.date_3, self.date_4,
            self.date_5, self.date_6, self.date_7, self.date_8,
        ] if date != INITIAL_DATE])

    @property
    def available(self):
        return [
                   self.created_datetime,
                   self.date_1 + datetime.timedelta(1),
                   self.date_2 + datetime.timedelta(2),
                   self.date_3 + datetime.timedelta(4),
                   self.date_4 + datetime.timedelta(8),
                   self.date_5 + datetime.timedelta(16),
                   self.date_6 + datetime.timedelta(32),
                   self.date_7 + datetime.timedelta(64),
                   self.date_8 + datetime.timedelta(128),
               ][self.stage] <= datetime.date.today()

    def remember(self):
        if self.stage == 8:
            raise ValueError("An already remembered item could not be remembered again.")
        today = datetime.date.today()
        setattr(self, 'date_{}'.format(self.stage + 1), today)
        self.save()

    def forget(self):
        if self.stage == 0:
            raise ValueError("An not remembered item could not be forget.")
        setattr(self, 'date_{}'.format(self.stage), INITIAL_DATE)
        self.save()

    @classmethod
    def random(cls, length=1):
        available_list = [obj.external_id for obj in cls.select() if obj.available]
        length = min(length, len(available_list))
        return random.sample(available_list, k=length)


def set_database(path=':memory:'):
    if not path == ':memory:':
        dir_name = os.path.dirname(path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
    database = peewee.SqliteDatabase(path)
    database_proxy.initialize(database)
    EbbinghausModel.create_table()
    return database


atomic = database_proxy.atomic
