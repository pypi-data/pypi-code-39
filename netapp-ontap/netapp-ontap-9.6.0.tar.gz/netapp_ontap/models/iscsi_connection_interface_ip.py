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


__all__ = ["IscsiConnectionInterfaceIp", "IscsiConnectionInterfaceIpSchema"]
__pdoc__ = {
    "IscsiConnectionInterfaceIpSchema.resource": False,
    "IscsiConnectionInterfaceIp": False,
}


class IscsiConnectionInterfaceIpSchema(ResourceSchema):
    """The fields of the IscsiConnectionInterfaceIp object"""

    address = fields.Str()
    r""" The address field of the iscsi_connection_interface_ip.
 """
    port = fields.Integer()
    r""" The TCP port number of the iSCSI access endpoint.

Example: 3260 """

    @property
    def resource(self):
        return IscsiConnectionInterfaceIp

    @property
    def patchable_fields(self):
        return [
            "address",
        ]

    @property
    def postable_fields(self):
        return [
            "address",
        ]


class IscsiConnectionInterfaceIp(Resource):  # pylint: disable=missing-docstring

    _schema = IscsiConnectionInterfaceIpSchema
