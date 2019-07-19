# encoding: utf-8

from openbayestool.updater import Updater
from openbayestool.jwt_client import JwtClient
from openbayestool.uaa_client import UAAClient
from openbayestool.http_client import HttpClient
from openbayestool import config


_updater = None


def updater():
    global _updater
    if _updater is None:
        if config.job_access_token is None:
            uaaclient = UAAClient(HttpClient(), config.uaa_username, config.uaa_password, config.uaa_token_url)
        else:
            uaaclient = UAAClient(HttpClient(), job_access_token=config.job_access_token)
        jwtclient = JwtClient(uaaclient)
        _updater = Updater(jwtclient, config.callback_url)
    return _updater


def log_param(key, value):
    return updater().log_param(key, value)


def log_metric(key, value):
    return updater().log_metric(key, value)


def set_callback_url(url):
    return updater().set_callback_url(url)


def get_callback_url():
    return updater().get_callback_url()


def set_job_access_token(token):
    updater().set_access_token(token)


def get_job_access_token():
    return updater().get_access_token()