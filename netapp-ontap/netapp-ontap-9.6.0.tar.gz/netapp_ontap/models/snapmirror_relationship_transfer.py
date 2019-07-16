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


__all__ = ["SnapmirrorRelationshipTransfer", "SnapmirrorRelationshipTransferSchema"]
__pdoc__ = {
    "SnapmirrorRelationshipTransferSchema.resource": False,
    "SnapmirrorRelationshipTransfer": False,
}


class SnapmirrorRelationshipTransferSchema(ResourceSchema):
    """The fields of the SnapmirrorRelationshipTransfer object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the snapmirror_relationship_transfer.
 """
    bytes_transferred = fields.Integer()
    r""" Bytes transferred.
 """
    state = fields.Str()
    r""" The state field of the snapmirror_relationship_transfer.

Valid choices:

* aborted
* failed
* hard_aborted
* queued
* success
* transferring """
    uuid = fields.Str()
    r""" The uuid field of the snapmirror_relationship_transfer.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return SnapmirrorRelationshipTransfer

    @property
    def patchable_fields(self):
        return [
            "bytes_transferred",
            "state",
            "uuid",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "bytes_transferred",
            "state",
            "uuid",
        ]


class SnapmirrorRelationshipTransfer(Resource):  # pylint: disable=missing-docstring

    _schema = SnapmirrorRelationshipTransferSchema
