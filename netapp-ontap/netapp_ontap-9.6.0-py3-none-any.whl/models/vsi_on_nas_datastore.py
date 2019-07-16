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


__all__ = ["VsiOnNasDatastore", "VsiOnNasDatastoreSchema"]
__pdoc__ = {
    "VsiOnNasDatastoreSchema.resource": False,
    "VsiOnNasDatastore": False,
}


class VsiOnNasDatastoreSchema(ResourceSchema):
    """The fields of the VsiOnNasDatastore object"""

    count = fields.Integer()
    r""" The number of datastores to support. Optional in the POST or PATCH body
 """
    size = fields.Integer()
    r""" The size of the datastore. Usage: {&lt;integer&gt;[KB|MB|GB|TB|PB]} Required in the POST body
 """
    storage_service = fields.Nested("VsiOnNasDatastoreStorageServiceSchema", unknown=EXCLUDE)
    r""" The storage_service field of the vsi_on_nas_datastore.
 """

    @property
    def resource(self):
        return VsiOnNasDatastore

    @property
    def patchable_fields(self):
        return [
            "count",
        ]

    @property
    def postable_fields(self):
        return [
            "count",
            "size",
            "storage_service",
        ]


class VsiOnNasDatastore(Resource):  # pylint: disable=missing-docstring

    _schema = VsiOnNasDatastoreSchema
