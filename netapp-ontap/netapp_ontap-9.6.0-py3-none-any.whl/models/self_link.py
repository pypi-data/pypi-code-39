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


__all__ = ["SelfLink", "SelfLinkSchema"]
__pdoc__ = {
    "SelfLinkSchema.resource": False,
    "SelfLink": False,
}


class SelfLinkSchema(ResourceSchema):
    """The fields of the SelfLink object"""

    self_ = fields.Nested("HrefSchema", unknown=EXCLUDE)
    r""" The self_ field of the self_link.
 """

    @property
    def resource(self):
        return SelfLink

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "self_",
        ]


class SelfLink(Resource):  # pylint: disable=missing-docstring

    _schema = SelfLinkSchema
