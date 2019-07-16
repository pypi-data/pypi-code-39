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


__all__ = ["ScopeIpspace", "ScopeIpspaceSchema"]
__pdoc__ = {
    "ScopeIpspaceSchema.resource": False,
    "ScopeIpspace": False,
}


class ScopeIpspaceSchema(ResourceSchema):
    """The fields of the ScopeIpspace object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the scope_ipspace.
 """
    name = fields.Str()
    r""" IPspace name

Example: exchange """
    uuid = fields.Str()
    r""" IPspace UUID

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return ScopeIpspace

    @property
    def patchable_fields(self):
        return [
            "name",
            "uuid",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "name",
            "uuid",
        ]


class ScopeIpspace(Resource):  # pylint: disable=missing-docstring

    _schema = ScopeIpspaceSchema
