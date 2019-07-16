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


__all__ = ["VolumeQos", "VolumeQosSchema"]
__pdoc__ = {
    "VolumeQosSchema.resource": False,
    "VolumeQos": False,
}


class VolumeQosSchema(ResourceSchema):
    """The fields of the VolumeQos object"""

    policy = fields.Nested("QosPolicySchema", unknown=EXCLUDE)
    r""" The policy field of the volume_qos.
 """

    @property
    def resource(self):
        return VolumeQos

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "policy",
        ]


class VolumeQos(Resource):  # pylint: disable=missing-docstring

    _schema = VolumeQosSchema
