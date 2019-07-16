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


__all__ = ["BroadcastDomainSvm", "BroadcastDomainSvmSchema"]
__pdoc__ = {
    "BroadcastDomainSvmSchema.resource": False,
    "BroadcastDomainSvm": False,
}


class BroadcastDomainSvmSchema(ResourceSchema):
    """The fields of the BroadcastDomainSvm object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the broadcast_domain_svm.
 """
    name = fields.Str()
    r""" Name of the broadcast domain, scoped to its IPspace

Example: bd1 """
    uuid = fields.Str()
    r""" Broadcast domain UUID

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return BroadcastDomainSvm

    @property
    def patchable_fields(self):
        return [
            "name",
            "uuid",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "name",
            "uuid",
        ]


class BroadcastDomainSvm(Resource):  # pylint: disable=missing-docstring

    _schema = BroadcastDomainSvmSchema
