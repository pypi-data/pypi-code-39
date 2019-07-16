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


__all__ = ["AuditEvents", "AuditEventsSchema"]
__pdoc__ = {
    "AuditEventsSchema.resource": False,
    "AuditEvents": False,
}


class AuditEventsSchema(ResourceSchema):
    """The fields of the AuditEvents object"""

    authorization_policy = fields.Boolean()
    r""" Authorization policy change events
 """
    cap_staging = fields.Boolean()
    r""" Central access policy staging events
 """
    cifs_logon_logoff = fields.Boolean()
    r""" CIFS logon and logoff events
 """
    file_operations = fields.Boolean()
    r""" File operation events
 """
    file_share = fields.Boolean()
    r""" File share category events
 """
    security_group = fields.Boolean()
    r""" Local security group management events
 """
    user_account = fields.Boolean()
    r""" Local user account management events
 """

    @property
    def resource(self):
        return AuditEvents

    @property
    def patchable_fields(self):
        return [
            "authorization_policy",
            "cap_staging",
            "cifs_logon_logoff",
            "file_operations",
            "file_share",
            "security_group",
            "user_account",
        ]

    @property
    def postable_fields(self):
        return [
            "authorization_policy",
            "cap_staging",
            "cifs_logon_logoff",
            "file_operations",
            "file_share",
            "security_group",
            "user_account",
        ]


class AuditEvents(Resource):  # pylint: disable=missing-docstring

    _schema = AuditEventsSchema
