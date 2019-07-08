import os

from flask import Flask, g
from flask_pymongo import PyMongo
from api import GisceStg
from backend.pool import Pool
from osconf import config_from_environment


class MongoRequestCounter(object):

    def __init__(self, mongo):
        self.mongo = mongo

    def next(self):
        return self.mongo.db.tg_request_counter.find_and_modify(
            {}, {"$inc": {"counter": 1}}, upsert=True, new=True
        )['counter']


class AppSetup(object):

    def __init__(self):
        self.api = GisceStg(prefix='/api')
        self.mongo = PyMongo()
        self.pool = Pool()

    def create_app(self, **config):
        """
        Create a gisce_stg app
        :param config:
        :return: gisce_stg app
        """
        app = Flask(__name__, static_folder=None)

        if 'MONGO_URI' in os.environ:
            app.config['MONGO_URI'] = os.environ['MONGO_URI']
        elif 'MONGO_HOST' and 'MONGO_DBNAME' in os.environ:
            app.config['MONGO_HOST'] = os.environ['MONGO_HOST']
            app.config['MONGO_DBNAME'] = os.environ['MONGO_DBNAME']

        app.config.update(config)

        self.configure_api(app)
        self.configure_mongodb(app)
        self.configure_counter(app)
        self.configure_backend(app)

        return app

    def configure_api(self, app):
        """
        Configure different API endpoints
        :param app: Flask application
        :return:
        """
        from api import resources
        for resource in resources:
            self.api.add_resource(*resource)

        self.api.init_app(app)

    def configure_mongodb(self, app):
        """
        Configure MongoDB connection
        :param app:
        :return:
        """
        self.mongo.init_app(app)

    def configure_counter(self, app):
        """
        Configure MongoDB counter
        :param app:
        :return:
        """
        app.counter = MongoRequestCounter(self.mongo)
        return app

    def setup_backend_conn(self):
        try:
            client = self.pool.connect(**config_from_environment('PEEK'))
            g.backend_cnx = client
        except Exception:
            pass

    def configure_backend(self, app):
        app.before_request(self.setup_backend_conn)

