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


__all__ = ["IpInterfaceSvmLocation", "IpInterfaceSvmLocationSchema"]
__pdoc__ = {
    "IpInterfaceSvmLocationSchema.resource": False,
    "IpInterfaceSvmLocation": False,
}


class IpInterfaceSvmLocationSchema(ResourceSchema):
    """The fields of the IpInterfaceSvmLocation object"""

    broadcast_domain = fields.Nested("BroadcastDomainSvmSchema", unknown=EXCLUDE)
    r""" The broadcast_domain field of the ip_interface_svm_location.
 """
    home_node = fields.Nested("NodeSchema", unknown=EXCLUDE)
    r""" The home_node field of the ip_interface_svm_location.
 """

    @property
    def resource(self):
        return IpInterfaceSvmLocation

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "broadcast_domain",
            "home_node",
        ]


class IpInterfaceSvmLocation(Resource):  # pylint: disable=missing-docstring

    _schema = IpInterfaceSvmLocationSchema
