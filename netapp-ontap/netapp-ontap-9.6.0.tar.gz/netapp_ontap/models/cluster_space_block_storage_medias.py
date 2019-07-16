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


__all__ = ["ClusterSpaceBlockStorageMedias", "ClusterSpaceBlockStorageMediasSchema"]
__pdoc__ = {
    "ClusterSpaceBlockStorageMediasSchema.resource": False,
    "ClusterSpaceBlockStorageMedias": False,
}


class ClusterSpaceBlockStorageMediasSchema(ResourceSchema):
    """The fields of the ClusterSpaceBlockStorageMedias object"""

    available = fields.Integer()
    r""" Available space
 """
    size = fields.Integer()
    r""" Total space
 """
    type = fields.Str()
    r""" The type of media being used

Valid choices:

* hdd
* hybrid
* lun
* ssd
* vmdisk """
    used = fields.Integer()
    r""" Used space
 """

    @property
    def resource(self):
        return ClusterSpaceBlockStorageMedias

    @property
    def patchable_fields(self):
        return [
            "available",
            "size",
            "type",
            "used",
        ]

    @property
    def postable_fields(self):
        return [
            "available",
            "size",
            "type",
            "used",
        ]


class ClusterSpaceBlockStorageMedias(Resource):  # pylint: disable=missing-docstring

    _schema = ClusterSpaceBlockStorageMediasSchema
