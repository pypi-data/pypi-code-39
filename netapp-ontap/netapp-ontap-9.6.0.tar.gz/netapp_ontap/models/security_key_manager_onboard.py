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


__all__ = ["SecurityKeyManagerOnboard", "SecurityKeyManagerOnboardSchema"]
__pdoc__ = {
    "SecurityKeyManagerOnboardSchema.resource": False,
    "SecurityKeyManagerOnboard": False,
}


class SecurityKeyManagerOnboardSchema(ResourceSchema):
    """The fields of the SecurityKeyManagerOnboard object"""

    enabled = fields.Boolean()
    r""" Is the onboard key manager enabled?
 """
    existing_passphrase = fields.Str()
    r""" The cluster-wide passphrase. This is not audited.

Example: The cluster password of length 32-256 ASCII characters. """
    passphrase = fields.Str()
    r""" The cluster-wide passphrase. This is not audited.

Example: The cluster password of length 32-256 ASCII characters. """

    @property
    def resource(self):
        return SecurityKeyManagerOnboard

    @property
    def patchable_fields(self):
        return [
            "existing_passphrase",
            "passphrase",
        ]

    @property
    def postable_fields(self):
        return [
            "existing_passphrase",
            "passphrase",
        ]


class SecurityKeyManagerOnboard(Resource):  # pylint: disable=missing-docstring

    _schema = SecurityKeyManagerOnboardSchema
