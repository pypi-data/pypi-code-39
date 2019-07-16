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


__all__ = ["VolumeGuarantee", "VolumeGuaranteeSchema"]
__pdoc__ = {
    "VolumeGuaranteeSchema.resource": False,
    "VolumeGuarantee": False,
}


class VolumeGuaranteeSchema(ResourceSchema):
    """The fields of the VolumeGuarantee object"""

    honored = fields.Boolean()
    r""" Is the space guarantee of this volume honored in the aggregate?
 """
    type = fields.Str()
    r""" The type of space guarantee of this volume in the aggregate.

Valid choices:

* volume
* none """

    @property
    def resource(self):
        return VolumeGuarantee

    @property
    def patchable_fields(self):
        return [
            "type",
        ]

    @property
    def postable_fields(self):
        return [
            "type",
        ]


class VolumeGuarantee(Resource):  # pylint: disable=missing-docstring

    _schema = VolumeGuaranteeSchema
