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


__all__ = ["LunLocation", "LunLocationSchema"]
__pdoc__ = {
    "LunLocationSchema.resource": False,
    "LunLocation": False,
}


class LunLocationSchema(ResourceSchema):
    """The fields of the LunLocation object"""

    logical_unit = fields.Str()
    r""" The base name component of the LUN. Valid in POST and PATCH.<br/>
If properties `name` and `location.logical_unit` are specified in the same request, they must refer to the base name.<br/>
A PATCH that modifies the base name of the LUN is considered a rename operation.


Example: lun1 """
    qtree = fields.Nested("QtreeSchema", unknown=EXCLUDE)
    r""" The qtree field of the lun_location.
 """
    volume = fields.Nested("VolumeSchema", unknown=EXCLUDE)
    r""" The volume field of the lun_location.
 """

    @property
    def resource(self):
        return LunLocation

    @property
    def patchable_fields(self):
        return [
            "logical_unit",
        ]

    @property
    def postable_fields(self):
        return [
            "logical_unit",
            "qtree",
            "volume",
        ]


class LunLocation(Resource):  # pylint: disable=missing-docstring

    _schema = LunLocationSchema
