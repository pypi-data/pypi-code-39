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


__all__ = ["OracleRacOnSan", "OracleRacOnSanSchema"]
__pdoc__ = {
    "OracleRacOnSanSchema.resource": False,
    "OracleRacOnSan": False,
}


class OracleRacOnSanSchema(ResourceSchema):
    """The fields of the OracleRacOnSan object"""

    archive_log = fields.Nested("OracleOnNfsArchiveLogSchema", unknown=EXCLUDE)
    r""" The archive_log field of the oracle_rac_on_san.
 """
    db = fields.Nested("OracleOnNfsDbSchema", unknown=EXCLUDE)
    r""" The db field of the oracle_rac_on_san.
 """
    db_sids = fields.Nested("OracleRacOnSanDbSidsSchema", unknown=EXCLUDE, many=True)
    r""" The db_sids field of the oracle_rac_on_san.
 """
    grid_binary = fields.Nested("OracleRacOnNfsGridBinarySchema", unknown=EXCLUDE)
    r""" The grid_binary field of the oracle_rac_on_san.
 """
    new_igroups = fields.Nested("OracleRacOnSanNewIgroupsSchema", unknown=EXCLUDE, many=True)
    r""" The list of initiator groups to create. Optional in the POST or PATCH body
 """
    ora_home = fields.Nested("OracleOnNfsOraHomeSchema", unknown=EXCLUDE)
    r""" The ora_home field of the oracle_rac_on_san.
 """
    oracle_crs = fields.Nested("OracleRacOnNfsOracleCrsSchema", unknown=EXCLUDE)
    r""" The oracle_crs field of the oracle_rac_on_san.
 """
    os_type = fields.Str()
    r""" The name of the host OS running the application. Required in the POST body

Valid choices:

* aix
* hpux
* hyper_v
* linux
* solaris
* solaris_efi
* vmware
* windows
* windows_2008
* windows_gpt
* xen """
    protection_type = fields.Nested("MongoDbOnSanProtectionTypeSchema", unknown=EXCLUDE)
    r""" The protection_type field of the oracle_rac_on_san.
 """
    redo_log = fields.Nested("OracleOnNfsRedoLogSchema", unknown=EXCLUDE)
    r""" The redo_log field of the oracle_rac_on_san.
 """

    @property
    def resource(self):
        return OracleRacOnSan

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "archive_log",
            "db",
            "db_sids",
            "grid_binary",
            "new_igroups",
            "ora_home",
            "oracle_crs",
            "os_type",
            "protection_type",
            "redo_log",
        ]


class OracleRacOnSan(Resource):  # pylint: disable=missing-docstring

    _schema = OracleRacOnSanSchema
