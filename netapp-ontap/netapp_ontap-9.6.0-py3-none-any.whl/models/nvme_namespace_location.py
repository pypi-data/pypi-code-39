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


__all__ = ["NvmeNamespaceLocation", "NvmeNamespaceLocationSchema"]
__pdoc__ = {
    "NvmeNamespaceLocationSchema.resource": False,
    "NvmeNamespaceLocation": False,
}


class NvmeNamespaceLocationSchema(ResourceSchema):
    """The fields of the NvmeNamespaceLocation object"""

    namespace = fields.Str()
    r""" The base name component of the NVMe namespace. Valid in POST.<br/>
If properties `name` and `location.namespace` are specified in the same request, they must refer to the base name.<br/>
NVMe namespaces do not support rename.


Example: namespace1 """
    qtree = fields.Nested("QtreeSchema", unknown=EXCLUDE)
    r""" The qtree field of the nvme_namespace_location.
 """
    volume = fields.Nested("VolumeSchema", unknown=EXCLUDE)
    r""" The volume field of the nvme_namespace_location.
 """

    @property
    def resource(self):
        return NvmeNamespaceLocation

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "namespace",
            "qtree",
            "volume",
        ]


class NvmeNamespaceLocation(Resource):  # pylint: disable=missing-docstring

    _schema = NvmeNamespaceLocationSchema
