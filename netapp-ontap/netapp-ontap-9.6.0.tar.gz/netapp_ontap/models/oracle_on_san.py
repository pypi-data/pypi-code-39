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


__all__ = ["OracleOnSan", "OracleOnSanSchema"]
__pdoc__ = {
    "OracleOnSanSchema.resource": False,
    "OracleOnSan": False,
}


class OracleOnSanSchema(ResourceSchema):
    """The fields of the OracleOnSan object"""

    archive_log = fields.Nested("OracleOnNfsArchiveLogSchema", unknown=EXCLUDE)
    r""" The archive_log field of the oracle_on_san.
 """
    db = fields.Nested("OracleOnNfsDbSchema", unknown=EXCLUDE)
    r""" The db field of the oracle_on_san.
 """
    igroup_name = fields.Str()
    r""" The name of the initiator group through which the contents of this application will be accessed. Modification of this parameter is a disruptive operation. All LUNs in the application component will be unmapped from the current igroup and re-mapped to the new igroup. Required in the POST body and optional in the PATCH body
 """
    new_igroups = fields.Nested("OracleOnSanNewIgroupsSchema", unknown=EXCLUDE, many=True)
    r""" The list of initiator groups to create. Optional in the POST or PATCH body
 """
    ora_home = fields.Nested("OracleOnNfsOraHomeSchema", unknown=EXCLUDE)
    r""" The ora_home field of the oracle_on_san.
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
    r""" The protection_type field of the oracle_on_san.
 """
    redo_log = fields.Nested("OracleOnNfsRedoLogSchema", unknown=EXCLUDE)
    r""" The redo_log field of the oracle_on_san.
 """

    @property
    def resource(self):
        return OracleOnSan

    @property
    def patchable_fields(self):
        return [
            "igroup_name",
        ]

    @property
    def postable_fields(self):
        return [
            "archive_log",
            "db",
            "igroup_name",
            "new_igroups",
            "ora_home",
            "os_type",
            "protection_type",
            "redo_log",
        ]


class OracleOnSan(Resource):  # pylint: disable=missing-docstring

    _schema = OracleOnSanSchema
