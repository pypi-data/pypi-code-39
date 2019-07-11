# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy

# from sqlalchemy import create_engine


db = SQLAlchemy(use_native_unicode='utf8')
# engine = create_engine('sqlalchemy-uri', encoding='utf-8', echo=True)


"""
use __bind_key__ binds other db

from sqlalchemy import func

class Company(db.Model):
    __bind_key__ = 'shouwei'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), nullable=False, unique=True)
    name = db.Column(db.String(32, u'utf8_bin'), nullable=False)
    encryption_type = db.Column(db.Integer, nullable=False)
"""