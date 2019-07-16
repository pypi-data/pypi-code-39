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


__all__ = ["IscsiCredentialsChap", "IscsiCredentialsChapSchema"]
__pdoc__ = {
    "IscsiCredentialsChapSchema.resource": False,
    "IscsiCredentialsChap": False,
}


class IscsiCredentialsChapSchema(ResourceSchema):
    """The fields of the IscsiCredentialsChap object"""

    inbound = fields.Nested("IscsiCredentialsChapInboundSchema", unknown=EXCLUDE)
    r""" The inbound field of the iscsi_credentials_chap.
 """
    outbound = fields.Nested("IscsiCredentialsChapOutboundSchema", unknown=EXCLUDE)
    r""" The outbound field of the iscsi_credentials_chap.
 """

    @property
    def resource(self):
        return IscsiCredentialsChap

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "inbound",
            "outbound",
        ]


class IscsiCredentialsChap(Resource):  # pylint: disable=missing-docstring

    _schema = IscsiCredentialsChapSchema
