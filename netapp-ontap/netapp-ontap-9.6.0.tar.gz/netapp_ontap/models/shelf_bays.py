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


__all__ = ["ShelfBays", "ShelfBaysSchema"]
__pdoc__ = {
    "ShelfBaysSchema.resource": False,
    "ShelfBays": False,
}


class ShelfBaysSchema(ResourceSchema):
    """The fields of the ShelfBays object"""

    has_disk = fields.Boolean()
    r""" The has_disk field of the shelf_bays.
 """
    id = fields.Integer()
    r""" The id field of the shelf_bays.

Example: 0 """
    state = fields.Str()
    r""" The state field of the shelf_bays.

Valid choices:

* unknown
* ok
* error """
    type = fields.Str()
    r""" The type field of the shelf_bays.

Valid choices:

* unknown
* single_disk
* multi_lun """

    @property
    def resource(self):
        return ShelfBays

    @property
    def patchable_fields(self):
        return [
            "has_disk",
            "id",
            "state",
            "type",
        ]

    @property
    def postable_fields(self):
        return [
            "has_disk",
            "id",
            "state",
            "type",
        ]


class ShelfBays(Resource):  # pylint: disable=missing-docstring

    _schema = ShelfBaysSchema
