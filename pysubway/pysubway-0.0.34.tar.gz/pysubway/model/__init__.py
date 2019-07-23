# -*- coding: utf-8 -*-
from typing import Any

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

db = SQLAlchemy(use_native_unicode='utf8')


def generate_engine(url: str) -> Engine:
    return create_engine(url, encoding='utf-8', echo=True)


def call_procedure(url: str, procedure_name: str, *args: Any) -> None:
    """

    :param url:
    :param procedure_name: just procedure name not call procedure_name
    :param args:
    :return:
    """
    connection = generate_engine(url).raw_connection()
    cursor = connection.cursor()
    try:
        s = cursor.callproc(procedure_name, args=args)
        print(s)
        connection.commit()
    except Exception as e:
        connection.rollback()
    finally:
        cursor.close()
        connection.close()
