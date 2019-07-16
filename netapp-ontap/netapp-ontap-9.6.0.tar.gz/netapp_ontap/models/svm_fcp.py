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


__all__ = ["SvmFcp", "SvmFcpSchema"]
__pdoc__ = {
    "SvmFcpSchema.resource": False,
    "SvmFcp": False,
}


class SvmFcpSchema(ResourceSchema):
    """The fields of the SvmFcp object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the svm_fcp.
 """
    enabled = fields.Boolean()
    r""" Enable Fiber Channel Protocol (FCP)? Setting to true creates a service if not already created.
 """

    @property
    def resource(self):
        return SvmFcp

    @property
    def patchable_fields(self):
        return [
            "enabled",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "enabled",
        ]


class SvmFcp(Resource):  # pylint: disable=missing-docstring

    _schema = SvmFcpSchema
