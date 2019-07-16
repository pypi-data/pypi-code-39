# pylint: disable=trailing-newlines
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=unused-import
# pylint: disable=invalid-name

r"""
Copyright &copy; 2019 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema


__all__ = ["OracleOnNfsRedoLog", "OracleOnNfsRedoLogSchema"]
__pdoc__ = {
    "OracleOnNfsRedoLogSchema.resource": False,
    "OracleOnNfsRedoLog": False,
}


class OracleOnNfsRedoLogSchema(ResourceSchema):
    """The fields of the OracleOnNfsRedoLog object"""

    mirrored = fields.Boolean()
    r""" Should the redo log group be mirrored? Optional in the POST body
 """
    size = fields.Integer()
    r""" The size of the redo log group. Usage: {&lt;integer&gt;[KB|MB|GB|TB|PB]} Required in the POST body and optional in the PATCH body
 """
    storage_service = fields.Nested("OracleOnNfsRedoLogStorageServiceSchema", unknown=EXCLUDE)
    r""" The storage_service field of the oracle_on_nfs_redo_log.
 """

    @property
    def resource(self):
        return OracleOnNfsRedoLog

    @property
    def patchable_fields(self):
        return [
            "size",
        ]

    @property
    def postable_fields(self):
        return [
            "mirrored",
            "size",
            "storage_service",
        ]


class OracleOnNfsRedoLog(Resource):  # pylint: disable=missing-docstring

    _schema = OracleOnNfsRedoLogSchema
