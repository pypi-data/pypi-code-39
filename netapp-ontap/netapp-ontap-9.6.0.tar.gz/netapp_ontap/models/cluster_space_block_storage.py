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


__all__ = ["ClusterSpaceBlockStorage", "ClusterSpaceBlockStorageSchema"]
__pdoc__ = {
    "ClusterSpaceBlockStorageSchema.resource": False,
    "ClusterSpaceBlockStorage": False,
}


class ClusterSpaceBlockStorageSchema(ResourceSchema):
    """The fields of the ClusterSpaceBlockStorage object"""

    medias = fields.Nested("ClusterSpaceBlockStorageMediasSchema", unknown=EXCLUDE, many=True)
    r""" The medias field of the cluster_space_block_storage.
 """
    size = fields.Integer()
    r""" Total space across the cluster
 """
    used = fields.Integer()
    r""" Space used (includes volume reserves)
 """

    @property
    def resource(self):
        return ClusterSpaceBlockStorage

    @property
    def patchable_fields(self):
        return [
            "size",
            "used",
        ]

    @property
    def postable_fields(self):
        return [
            "medias",
            "size",
            "used",
        ]


class ClusterSpaceBlockStorage(Resource):  # pylint: disable=missing-docstring

    _schema = ClusterSpaceBlockStorageSchema
