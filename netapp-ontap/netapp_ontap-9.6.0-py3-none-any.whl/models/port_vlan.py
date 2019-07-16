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


__all__ = ["PortVlan", "PortVlanSchema"]
__pdoc__ = {
    "PortVlanSchema.resource": False,
    "PortVlan": False,
}


class PortVlanSchema(ResourceSchema):
    """The fields of the PortVlan object"""

    base_port = fields.Nested("PortSchema", unknown=EXCLUDE)
    r""" The base_port field of the port_vlan.
 """
    tag = fields.Integer()
    r""" VLAN ID

Example: 100 """

    @property
    def resource(self):
        return PortVlan

    @property
    def patchable_fields(self):
        return [
            "tag",
        ]

    @property
    def postable_fields(self):
        return [
            "base_port",
            "tag",
        ]


class PortVlan(Resource):  # pylint: disable=missing-docstring

    _schema = PortVlanSchema
