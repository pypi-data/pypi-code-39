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


__all__ = ["LunClone", "LunCloneSchema"]
__pdoc__ = {
    "LunCloneSchema.resource": False,
    "LunClone": False,
}


class LunCloneSchema(ResourceSchema):
    """The fields of the LunClone object"""

    source = fields.Nested("LunCloneSourceSchema", unknown=EXCLUDE)
    r""" The source field of the lun_clone.
 """

    @property
    def resource(self):
        return LunClone

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "source",
        ]


class LunClone(Resource):  # pylint: disable=missing-docstring

    _schema = LunCloneSchema
