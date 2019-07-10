from .database import atomic
from .database import set_database
from .database import EbbinghausModel as _EbbinghausModel


def register(id: int):
    _EbbinghausModel.create(external_id=id)


def get_stage(id: int):
    return _EbbinghausModel.get(_EbbinghausModel.external_id == id).stage


def remember(id: int):
    _EbbinghausModel.get(_EbbinghausModel.external_id == id).remember()


def forget(id: int):
    _EbbinghausModel.get(_EbbinghausModel.external_id == id).forget()


def random(n: int):
    return _EbbinghausModel.random(n)
