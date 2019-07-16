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


__all__ = ["SecurityKeyManagerExternal", "SecurityKeyManagerExternalSchema"]
__pdoc__ = {
    "SecurityKeyManagerExternalSchema.resource": False,
    "SecurityKeyManagerExternal": False,
}


class SecurityKeyManagerExternalSchema(ResourceSchema):
    """The fields of the SecurityKeyManagerExternal object"""

    client_certificate = fields.Nested("SecurityCertificateSchema", unknown=EXCLUDE)
    r""" The client_certificate field of the security_key_manager_external.
 """
    server_ca_certificates = fields.Nested("SecurityCertificateSchema", unknown=EXCLUDE, many=True)
    r""" The UUIDs of the server CA certificates already installed in the cluster or SVM. The array of certificates are common for all the keyservers per SVM.
 """
    servers = fields.Nested("KeyServerReadcreateSchema", unknown=EXCLUDE, many=True)
    r""" The set of external key servers.
 """

    @property
    def resource(self):
        return SecurityKeyManagerExternal

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "client_certificate",
            "server_ca_certificates",
            "servers",
        ]


class SecurityKeyManagerExternal(Resource):  # pylint: disable=missing-docstring

    _schema = SecurityKeyManagerExternalSchema
