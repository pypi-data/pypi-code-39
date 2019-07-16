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


__all__ = ["IpInterfaceSvm", "IpInterfaceSvmSchema"]
__pdoc__ = {
    "IpInterfaceSvmSchema.resource": False,
    "IpInterfaceSvm": False,
}


class IpInterfaceSvmSchema(ResourceSchema):
    """The fields of the IpInterfaceSvm object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the ip_interface_svm.
 """
    ip = fields.Nested("IpInterfaceSvmIpSchema", unknown=EXCLUDE)
    r""" The ip field of the ip_interface_svm.
 """
    location = fields.Nested("IpInterfaceSvmLocationSchema", unknown=EXCLUDE)
    r""" The location field of the ip_interface_svm.
 """
    name = fields.Str()
    r""" The name of the interface (optional).

Example: lif1 """
    service_policy = fields.Str()
    r""" The service_policy field of the ip_interface_svm.
 """
    uuid = fields.Str()
    r""" The UUID that uniquely identifies the interface.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return IpInterfaceSvm

    @property
    def patchable_fields(self):
        return [
            "service_policy",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "ip",
            "location",
            "name",
            "service_policy",
        ]


class IpInterfaceSvm(Resource):  # pylint: disable=missing-docstring

    _schema = IpInterfaceSvmSchema
