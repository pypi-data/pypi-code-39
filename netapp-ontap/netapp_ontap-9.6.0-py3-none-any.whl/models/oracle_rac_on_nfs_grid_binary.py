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


__all__ = ["OracleRacOnNfsGridBinary", "OracleRacOnNfsGridBinarySchema"]
__pdoc__ = {
    "OracleRacOnNfsGridBinarySchema.resource": False,
    "OracleRacOnNfsGridBinary": False,
}


class OracleRacOnNfsGridBinarySchema(ResourceSchema):
    """The fields of the OracleRacOnNfsGridBinary object"""

    size = fields.Integer()
    r""" The size of the Oracle grid binary storage volume. Usage: {&lt;integer&gt;[KB|MB|GB|TB|PB]} Optional in the POST or PATCH body
 """
    storage_service = fields.Nested("OracleRacOnNfsGridBinaryStorageServiceSchema", unknown=EXCLUDE)
    r""" The storage_service field of the oracle_rac_on_nfs_grid_binary.
 """

    @property
    def resource(self):
        return OracleRacOnNfsGridBinary

    @property
    def patchable_fields(self):
        return [
            "size",
        ]

    @property
    def postable_fields(self):
        return [
            "size",
            "storage_service",
        ]


class OracleRacOnNfsGridBinary(Resource):  # pylint: disable=missing-docstring

    _schema = OracleRacOnNfsGridBinarySchema
