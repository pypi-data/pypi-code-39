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


__all__ = ["SvmDns", "SvmDnsSchema"]
__pdoc__ = {
    "SvmDnsSchema.resource": False,
    "SvmDns": False,
}


class SvmDnsSchema(ResourceSchema):
    """The fields of the SvmDns object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the svm_dns.
 """
    domains = fields.List(fields.Str)
    r""" The domains field of the svm_dns.
 """
    servers = fields.List(fields.Str)
    r""" The servers field of the svm_dns.
 """

    @property
    def resource(self):
        return SvmDns

    @property
    def patchable_fields(self):
        return [
            "domains",
            "servers",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "domains",
            "servers",
        ]


class SvmDns(Resource):  # pylint: disable=missing-docstring

    _schema = SvmDnsSchema
