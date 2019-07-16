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


__all__ = ["NetworkRouteForSvm", "NetworkRouteForSvmSchema"]
__pdoc__ = {
    "NetworkRouteForSvmSchema.resource": False,
    "NetworkRouteForSvm": False,
}


class NetworkRouteForSvmSchema(ResourceSchema):
    """The fields of the NetworkRouteForSvm object"""

    destination = fields.Nested("IpInfoSchema", unknown=EXCLUDE)
    r""" The destination field of the network_route_for_svm.
 """
    gateway = fields.Str()
    r""" The IP address of the gateway router leading to the destination.

Example: 10.1.1.1 """

    @property
    def resource(self):
        return NetworkRouteForSvm

    @property
    def patchable_fields(self):
        return [
            "gateway",
        ]

    @property
    def postable_fields(self):
        return [
            "destination",
            "gateway",
        ]


class NetworkRouteForSvm(Resource):  # pylint: disable=missing-docstring

    _schema = NetworkRouteForSvmSchema
