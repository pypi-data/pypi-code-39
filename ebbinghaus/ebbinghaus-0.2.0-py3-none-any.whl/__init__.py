from .database import atomic
from .database import set_database
from .database import EbbinghausModel as _EbbinghausModel
from .exceptions import ExternalKeyExistsError, ExternalKeyNotExistsError


def _assume_exists(id):
    if not exists(id):
        raise ExternalKeyNotExistsError('External key {} not exists.'.format(id))


def exists(id: int):
    obj_list = _EbbinghausModel.select().where(_EbbinghausModel.external_id == id)
    return bool(obj_list)


def register(id: int):
    if exists(id):
        raise ExternalKeyExistsError('External key {} already exists.'.format(id))
    _EbbinghausModel.create(external_id=id)


def get_stage(id: int):
    _assume_exists(id)
    return _EbbinghausModel.get(_EbbinghausModel.external_id == id).stage


def remember(id: int):
    _assume_exists(id)
    _EbbinghausModel.get(_EbbinghausModel.external_id == id).remember()


def forget(id: int):
    _assume_exists(id)
    _EbbinghausModel.get(_EbbinghausModel.external_id == id).forget()


def random(n: int):
    return _EbbinghausModel.random(n)
