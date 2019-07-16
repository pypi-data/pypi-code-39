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


__all__ = ["NvmeNamespaceClone", "NvmeNamespaceCloneSchema"]
__pdoc__ = {
    "NvmeNamespaceCloneSchema.resource": False,
    "NvmeNamespaceClone": False,
}


class NvmeNamespaceCloneSchema(ResourceSchema):
    """The fields of the NvmeNamespaceClone object"""

    source = fields.Nested("NvmeNamespaceCloneSourceSchema", unknown=EXCLUDE)
    r""" The source field of the nvme_namespace_clone.
 """

    @property
    def resource(self):
        return NvmeNamespaceClone

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "source",
        ]


class NvmeNamespaceClone(Resource):  # pylint: disable=missing-docstring

    _schema = NvmeNamespaceCloneSchema
