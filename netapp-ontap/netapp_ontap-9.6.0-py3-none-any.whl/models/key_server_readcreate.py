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


__all__ = ["KeyServerReadcreate", "KeyServerReadcreateSchema"]
__pdoc__ = {
    "KeyServerReadcreateSchema.resource": False,
    "KeyServerReadcreate": False,
}


class KeyServerReadcreateSchema(ResourceSchema):
    """The fields of the KeyServerReadcreate object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the key_server_readcreate.
 """
    server = fields.Str()
    r""" External key server for key management. If no port is provided, a default port of 5696 is used.

Example: keyserver1.com:5698 """
    timeout = fields.Integer()
    r""" I/O timeout in seconds for communicating with the key server.

Example: 60 """
    username = fields.Str()
    r""" Username credentials for connecting with the key server.

Example: username """

    @property
    def resource(self):
        return KeyServerReadcreate

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "server",
        ]


class KeyServerReadcreate(Resource):  # pylint: disable=missing-docstring

    _schema = KeyServerReadcreateSchema
