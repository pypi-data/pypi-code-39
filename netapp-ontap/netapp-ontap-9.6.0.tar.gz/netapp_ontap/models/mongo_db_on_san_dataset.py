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


__all__ = ["MongoDbOnSanDataset", "MongoDbOnSanDatasetSchema"]
__pdoc__ = {
    "MongoDbOnSanDatasetSchema.resource": False,
    "MongoDbOnSanDataset": False,
}


class MongoDbOnSanDatasetSchema(ResourceSchema):
    """The fields of the MongoDbOnSanDataset object"""

    element_count = fields.Integer()
    r""" The number of storage elements (LUNs for SAN) of the database to maintain.  Must be an even number between 2 and 16.  Odd numbers will be rounded up to the next even number within range. Optional in the POST body
 """
    replication_factor = fields.Integer()
    r""" The number of data bearing members of the replicaset, including 1 primary and at least 1 secondary. Optional in the POST body
 """
    size = fields.Integer()
    r""" The size of the database. Usage: {&lt;integer&gt;[KB|MB|GB|TB|PB]} Required in the POST body and optional in the PATCH body
 """
    storage_service = fields.Nested("MongoDbOnSanDatasetStorageServiceSchema", unknown=EXCLUDE)
    r""" The storage_service field of the mongo_db_on_san_dataset.
 """

    @property
    def resource(self):
        return MongoDbOnSanDataset

    @property
    def patchable_fields(self):
        return [
            "size",
        ]

    @property
    def postable_fields(self):
        return [
            "element_count",
            "replication_factor",
            "size",
            "storage_service",
        ]


class MongoDbOnSanDataset(Resource):  # pylint: disable=missing-docstring

    _schema = MongoDbOnSanDatasetSchema
