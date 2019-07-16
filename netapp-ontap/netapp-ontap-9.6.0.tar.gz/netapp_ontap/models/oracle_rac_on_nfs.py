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


__all__ = ["OracleRacOnNfs", "OracleRacOnNfsSchema"]
__pdoc__ = {
    "OracleRacOnNfsSchema.resource": False,
    "OracleRacOnNfs": False,
}


class OracleRacOnNfsSchema(ResourceSchema):
    """The fields of the OracleRacOnNfs object"""

    archive_log = fields.Nested("OracleOnNfsArchiveLogSchema", unknown=EXCLUDE)
    r""" The archive_log field of the oracle_rac_on_nfs.
 """
    db = fields.Nested("OracleOnNfsDbSchema", unknown=EXCLUDE)
    r""" The db field of the oracle_rac_on_nfs.
 """
    grid_binary = fields.Nested("OracleRacOnNfsGridBinarySchema", unknown=EXCLUDE)
    r""" The grid_binary field of the oracle_rac_on_nfs.
 """
    nfs_access = fields.Nested("AppNfsAccessSchema", unknown=EXCLUDE, many=True)
    r""" The list of NFS access controls. Optional in the POST body
 """
    ora_home = fields.Nested("OracleOnNfsOraHomeSchema", unknown=EXCLUDE)
    r""" The ora_home field of the oracle_rac_on_nfs.
 """
    oracle_crs = fields.Nested("OracleRacOnNfsOracleCrsSchema", unknown=EXCLUDE)
    r""" The oracle_crs field of the oracle_rac_on_nfs.
 """
    protection_type = fields.Nested("MongoDbOnSanProtectionTypeSchema", unknown=EXCLUDE)
    r""" The protection_type field of the oracle_rac_on_nfs.
 """
    redo_log = fields.Nested("OracleOnNfsRedoLogSchema", unknown=EXCLUDE)
    r""" The redo_log field of the oracle_rac_on_nfs.
 """

    @property
    def resource(self):
        return OracleRacOnNfs

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "archive_log",
            "db",
            "grid_binary",
            "nfs_access",
            "ora_home",
            "oracle_crs",
            "protection_type",
            "redo_log",
        ]


class OracleRacOnNfs(Resource):  # pylint: disable=missing-docstring

    _schema = OracleRacOnNfsSchema
