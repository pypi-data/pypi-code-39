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


__all__ = ["IscsiConnection", "IscsiConnectionSchema"]
__pdoc__ = {
    "IscsiConnectionSchema.resource": False,
    "IscsiConnection": False,
}


class IscsiConnectionSchema(ResourceSchema):
    """The fields of the IscsiConnection object"""

    links = fields.Nested("CollectionLinksSchema", unknown=EXCLUDE)
    r""" The links field of the iscsi_connection.
 """
    authentication_type = fields.Str()
    r""" The iSCSI authentication type used to establish the connection.


Valid choices:

* chap
* none """
    cid = fields.Integer()
    r""" The identifier of the connection within the session.
 """
    initiator_address = fields.Nested("IscsiConnectionInitiatorAddressSchema", unknown=EXCLUDE)
    r""" The initiator_address field of the iscsi_connection.
 """
    interface = fields.Nested("IscsiConnectionInterfaceSchema", unknown=EXCLUDE)
    r""" The interface field of the iscsi_connection.
 """

    @property
    def resource(self):
        return IscsiConnection

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "initiator_address",
            "interface",
        ]


class IscsiConnection(Resource):  # pylint: disable=missing-docstring

    _schema = IscsiConnectionSchema
