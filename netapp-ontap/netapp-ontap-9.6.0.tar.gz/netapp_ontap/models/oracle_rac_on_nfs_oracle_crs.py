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


__all__ = ["OracleRacOnNfsOracleCrs", "OracleRacOnNfsOracleCrsSchema"]
__pdoc__ = {
    "OracleRacOnNfsOracleCrsSchema.resource": False,
    "OracleRacOnNfsOracleCrs": False,
}


class OracleRacOnNfsOracleCrsSchema(ResourceSchema):
    """The fields of the OracleRacOnNfsOracleCrs object"""

    copies = fields.Integer()
    r""" The number of CRS volumes. Optional in the POST body
 """
    size = fields.Integer()
    r""" The size of the Oracle CRS/voting storage volume. Usage: {&lt;integer&gt;[KB|MB|GB|TB|PB]} Optional in the POST body
 """
    storage_service = fields.Nested("OracleRacOnNfsOracleCrsStorageServiceSchema", unknown=EXCLUDE)
    r""" The storage_service field of the oracle_rac_on_nfs_oracle_crs.
 """

    @property
    def resource(self):
        return OracleRacOnNfsOracleCrs

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "copies",
            "size",
            "storage_service",
        ]


class OracleRacOnNfsOracleCrs(Resource):  # pylint: disable=missing-docstring

    _schema = OracleRacOnNfsOracleCrsSchema
