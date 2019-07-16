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


__all__ = ["IscsiConnectionInterface", "IscsiConnectionInterfaceSchema"]
__pdoc__ = {
    "IscsiConnectionInterfaceSchema.resource": False,
    "IscsiConnectionInterface": False,
}


class IscsiConnectionInterfaceSchema(ResourceSchema):
    """The fields of the IscsiConnectionInterface object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the iscsi_connection_interface.
 """
    ip = fields.Nested("IscsiConnectionInterfaceIpSchema", unknown=EXCLUDE)
    r""" The ip field of the iscsi_connection_interface.
 """
    name = fields.Str()
    r""" The name of the interface.

Example: lif1 """
    uuid = fields.Str()
    r""" The UUID that uniquely identifies the interface.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return IscsiConnectionInterface

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "ip",
        ]


class IscsiConnectionInterface(Resource):  # pylint: disable=missing-docstring

    _schema = IscsiConnectionInterfaceSchema
