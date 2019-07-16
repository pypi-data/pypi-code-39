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


__all__ = ["IpInterfaceLocation", "IpInterfaceLocationSchema"]
__pdoc__ = {
    "IpInterfaceLocationSchema.resource": False,
    "IpInterfaceLocation": False,
}


class IpInterfaceLocationSchema(ResourceSchema):
    """The fields of the IpInterfaceLocation object"""

    auto_revert = fields.Boolean()
    r""" The auto_revert field of the ip_interface_location.
 """
    broadcast_domain = fields.Nested("BroadcastDomainSvmSchema", unknown=EXCLUDE)
    r""" The broadcast_domain field of the ip_interface_location.
 """
    failover = fields.Str()
    r""" The failover field of the ip_interface_location.
 """
    home_node = fields.Nested("NodeSchema", unknown=EXCLUDE)
    r""" The home_node field of the ip_interface_location.
 """
    home_port = fields.Nested("PortSchema", unknown=EXCLUDE)
    r""" The home_port field of the ip_interface_location.
 """
    is_home = fields.Boolean()
    r""" The is_home field of the ip_interface_location.
 """
    node = fields.Nested("NodeSchema", unknown=EXCLUDE)
    r""" The node field of the ip_interface_location.
 """
    port = fields.Nested("PortSchema", unknown=EXCLUDE)
    r""" The port field of the ip_interface_location.
 """

    @property
    def resource(self):
        return IpInterfaceLocation

    @property
    def patchable_fields(self):
        return [
            "auto_revert",
            "failover",
        ]

    @property
    def postable_fields(self):
        return [
            "auto_revert",
            "broadcast_domain",
            "failover",
            "home_node",
            "home_port",
        ]


class IpInterfaceLocation(Resource):  # pylint: disable=missing-docstring

    _schema = IpInterfaceLocationSchema
